import json
import time
import openai
import os

# 设置 OpenAI API 密钥（推荐从环境变量中读取）
openai.api_key = os.getenv("OPENAI_API_KEY")

# 输入输出文件名
INPUT_FILE = "questions.json"
OUTPUT_FILE = "questions_translated.json"

# 设定最大处理题目数（调试用）
LIMIT = None  # 改成 None 表示处理全部

# 读取题目列表
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

if LIMIT:
    questions = questions[:LIMIT]

translated_questions = []

def call_gpt_and_parse(prompt, qid):
    """调用 GPT 并尝试解析 JSON 响应，失败时返回默认值"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()

        # 清理 Markdown 代码块
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()

        if not content.startswith("{"):
            print(f"⚠️ 第 {qid} 题：GPT 返回内容不是 JSON 格式，原始内容如下：\n{content}")
            raise ValueError("返回内容格式错误")

        parsed = json.loads(content)
        return parsed.get("question_cn", ""), parsed.get("explanation_cn", "")

    except Exception as e:
        print(f"❌ 第 {qid} 题处理失败: {e}")
        return "", "翻译失败"

# 遍历所有题目
for idx, item in enumerate(questions):
    qid = item["id"]
    question = item["question"]
    correct_option = item["correct_option"]
    correct_answer_text = next((a["text"] for a in item["answers"] if a["option"] == correct_option), None)
    answer_texts = "\n".join([a["text"] for a in item["answers"]])

    prompt = f"""
你是一位医学考试辅导老师。请将以下按摩类考试选择题翻译成中文，并解释正确答案的依据（如按摩技术原理、解剖结构、病理知识等）。

题目:
{question}

选项:
{answer_texts}

正确答案:
{correct_answer_text}

请以 JSON 格式返回，如下：
{{
  "question_cn": "中文题目翻译",
  "explanation_cn": "中文解释"
}}
""".strip()

    print(f"⏳ 正在处理第 {qid} 题...")

    # 调用 GPT 并解析
    question_cn, explanation_cn = call_gpt_and_parse(prompt, qid)
    item["question_cn"] = question_cn
    item["explanation_cn"] = explanation_cn

    translated_questions.append(item)
    time.sleep(0.1)  # 控制节奏，避免限流

# 保存最终 JSON 文件
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(translated_questions, f, indent=2, ensure_ascii=False)

print(f"\n✅ 已完成 {len(translated_questions)} 道题处理，结果保存为：{OUTPUT_FILE}")
