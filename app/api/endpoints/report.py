from openai import OpenAI
import os
from pydantic import BaseModel
from typing import List
import json

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

class Expense(BaseModel):
    category: str
    amount: int
    date: str

class ReportRequest(BaseModel):
    userId: int
    month: str
    data: List[Expense]

def analyze_consumption(request: ReportRequest):
    prompt = f"""
    아래는 사용자 {request.userId}의 {request.month} 월 소비 내역이야.
    이 데이터를 바탕으로 월간 소비 습관을 요약하고, 피드백을 제공해줘.
    JSON 형식으로, summary, suggestions(최대 3개), riskCategory를 포함해줘.
    """

    user_data = json.dumps([d.dict() for d in request.data], ensure_ascii=False)
    full_prompt = prompt + "\n" + user_data

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "You are a financial advisor."},
            {"role": "user", "content": full_prompt}
        ],
    )

    return json.loads(response.choices[0].message.content)
