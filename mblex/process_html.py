from bs4 import BeautifulSoup
import json

def extract_questions(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    results = []
    question_divs = soup.select('div[id^=question_]')

    for qdiv in question_divs:
        qid = qdiv['id'].split('_')[1]

        # Extract question text (excluding answers)
        question_text = ""
        for content in qdiv.contents:
            if getattr(content, 'name', None) == 'div' and 'answers' in content.get('class', []):
                break
            if isinstance(content, str):
                question_text += content.strip() + " "

        question_text = ' '.join(question_text.split())  # normalize whitespace

        # Extract all answers and find the correct one
        answers_div = qdiv.find('div', class_='answers')
        answer_inputs = answers_div.find_all('input', {'type': 'radio'})

        answers = []
        correct_option = None

        for input_tag in answer_inputs:
            value = input_tag['value']
            full_text = input_tag.next_sibling.strip()
            answers.append({'option': value, 'text': full_text})

        # Find correct answer from the special wrapper
        correct_div = answers_div.find('div', id=f'ans_{qid}')
        if correct_div:
            correct_input = correct_div.find('input')
            if correct_input:
                correct_option = correct_input['value']

        results.append({
            'id': qid,
            'question': question_text,
            'answers': answers,
            'correct_option': correct_option
        })

    return results

# Run and save
html_file_path = 'mblex.xml'
questions = extract_questions(html_file_path)

with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)
