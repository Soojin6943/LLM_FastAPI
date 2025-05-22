from openai import OpenAI
import os
import json
from datetime import datetime


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

tools = [{
    "type": "function",
    "function": {
    "name": "save_expense",
    "description": "사용자의 소비 내역을 파싱하여 금액과 카테고리, 날짜를 저장",
    "parameters": {
        "type": "object",
        "properties": {
            "category": {
            "type": "string",
            "enum": ["카페", "식비", "교통", "의류", "문화", "공과금", "기타"],
            "description": "정해진 소비 카테고리 중 하나"
            },
            "amount": {
                "type": "integer",
                "description": "금액 (숫자만, 원단위)"
            },
            "date": {
                "type": "string",
                "description": "소비한 날짜"
            }
        },
        "required": ["category", "amount", "date"],
        "additionalProperties": False
    }
    },
    "strict": True
}]

today = datetime.today().strftime("%Y-%m-%d")

response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {"role": "system", "content": f"""너는 사용자 소비 내역을 정리해주는 가계부 어시스턴트야. 
         오늘 날짜는 {today}야.
         만약 사용자가 '오늘', '어제', '그제' 같은 말을 하면 이를 기준으로 정확한 날짜(YYY-MM-DD)로 바꿔줘."""},
        {"role": "user", "content": "오늘 89000원짜리 바지를 샀어"}
    ],
    tools=tools,
    tool_choice="auto"
)

# 함수 코드 실행 - 모델의 응답을 구문 분석하고 함수 호출을 처리
tool_call = response.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

print(args)
