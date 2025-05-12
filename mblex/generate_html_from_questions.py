import json
from pathlib import Path

# 输入输出路径
INPUT_FILE = "questions_translated.json"
OUTPUT_FILE = "questions_preview.html"

# 读取 JSON 文件
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

# HTML 结构头部
html_parts = [
    "<!DOCTYPE html>",
    "<html lang='zh'>",
    "<head>",
    "<meta charset='UTF-8'>",
    "<title>按摩题库预览</title>",
    "<style>",
    "body { font-family: sans-serif; padding: 20px; max-width: 900px; margin: auto; background: #fcfcfc; }",
    ".question { border: 1px solid #ccc; border-radius: 8px; padding: 16px; margin-bottom: 20px; background: white; }",
    ".question h3 { margin-top: 0; }",
    ".answers { margin: 10px 0; }",
    ".answer { margin-left: 20px; }",
    ".correct { margin-left: 20px; font-weight: bold; color: green; }",
    ".explanation { background: #f9f9f9; border-left: 4px solid #ccc; padding: 10px; margin-top: 10px; white-space: pre-wrap; }",
    "</style>",
    "</head>",
    "<body>",
    "<h1>按摩选择题完整预览</h1>"
]

# 添加每道题目
for q in questions:
    html_parts.append("<div class='question'>")
    html_parts.append(f"<h3>{q['id']}. {q.get('question_cn', '')}<br><small style='color:gray'>{q['question']}</small></h3>")
    html_parts.append("<div class='answers'>")
    for a in q["answers"]:
        cls = "correct" if a["option"] == q["correct_option"] else "answer"
        html_parts.append(f"<div class='{cls}'>{a['text']}</div>")
    html_parts.append("</div>")
    html_parts.append(f"<div class='explanation'><strong>解析：</strong>{q.get('explanation_cn', '')}</div>")
    html_parts.append("</div>")

# 结束 HTML
html_parts.append("</body></html>")

# 写入 HTML 文件
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(html_parts))

print(f"✅ HTML 文件已生成: {OUTPUT_FILE}")
