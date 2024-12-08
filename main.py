from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No OpenAI API key found in environment variables")

client = OpenAI()

# GPT 모델에 전달할 시스템 프롬프트 정의
SYSTEM_PROMPT = """You are a professional music composer. 
Given a single keyword, create:
1. A short musical description (under 100 words)
2. A simple melody sequence using the notes: C4, D4, E4, F4, G4, A4, B4, C5
Format the response as JSON:
{
    "description": "musical description here",
    "notes": ["C4", "E4", "G4", ...],
    "durations": ["4n", "8n", "4n", ...],
    "tempo": 120
}
Keep the melody between 8-16 notes."""

# 메인 페이지 라우트
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# 작곡 요청 처리 라우트
@app.route("/compose", methods=["POST"])
def compose():
    # 사용자 입력 키워드 가져오기
    keyword = request.form.get("keyword", "").strip()
    if not keyword:
        return render_template("result.html", 
            keyword="",
            composition={
                "description": "키워드를 입력해주세요.",
                "notes": [],
                "durations": [],
                "tempo": 120
            })

    try:
        # OpenAI API 호출하여 작곡 데이터 생성
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Keyword: {keyword}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        # API 응답을 JSON으로 파싱하여 결과 페이지 렌더링
        result = json.loads(response.choices[0].message.content.strip())
        return render_template("result.html", keyword=keyword, composition=result)
    except Exception as e:
        # 오류 발생 시 에러 메시지 표시
        error_response = {
            "description": f"오류가 발생했습니다: {str(e)}",
            "notes": [],
            "durations": [],
            "tempo": 120
        }
        return render_template("result.html", keyword=keyword, composition=error_response)

if __name__ == "__main__":
    app.run(debug=True)
