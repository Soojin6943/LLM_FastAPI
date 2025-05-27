from openai import OpenAI
import os
import json
from datetime import datetime
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

class ChatRequest(BaseModel):
    userId: int
    message: str

class ExpenseData(BaseModel):
    category: str
    amount: int
    date: str

class ChatResponse(BaseModel):
    type: str
    reply: str
    data: Union[ExpenseData, None] = None

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

def handle_message(message: str):

    today = datetime.today().strftime("%Y-%m-%d")

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": f"""너는 사용자 소비 내역을 정리해주는 가계부 어시스턴트야. 
            오늘 날짜는 {today}야.
            만약 사용자가 '오늘', '어제', '그제' 같은 말을 하면 이를 기준으로 정확한 날짜(YYY-MM-DD)로 바꿔줘.
            소비 내역을 말하면 카테고리와 금액, 날짜를 파싱해서 JSON 형태로 반환해주고, 
            일반적인 질문이나 조언 요청이면 텍스트로 피드백을 반환해줘."""},
            {"role": "user", "content": message}
        ],
        tools=tools,
        tool_choice="auto"
    )

# 함수 코드 실행 - 모델의 응답을 구문 분석하고 함수 호출을 처리

    msg = response.choices[0].message

    # 함수 호출이 있는 경우
    if msg.tool_calls:
        args = json.loads(msg.tool_calls[0].function.arguments)
        return {
            "type":"expense",
            "reply": f"{args['category']} 카테고리로 {args['amount']}원을 기록했어요.",
            "data": {
                "category": args["category"],
                "amount": args["amount"],
                "date": args["date"]
            }
        }
    else:
        return {
            "type":"feedback",
            "reply": msg.content
        }
    
