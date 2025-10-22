# main.py
import requests
from fastapi import FastAPI
from pydantic import BaseModel

# FastAPI 앱(서버) 생성
app = FastAPI()

# Postman으로부터 받을 데이터 형식을 미리 정의합니다.
# {"tag": "문자열"} 형태의 JSON만 받겠다는 의미입니다.
class TagRequest(BaseModel):
    tag: str

# '/search-problems' 라는 주소로 POST 방식의 요청이 오면 아래 함수를 실행합니다.
@app.post("/search-problems")
def search_baekjoon_problems(request: TagRequest):
    """
    Postman에서 요청한 'tag'를 받아서 Solved.ac API로 문제 목록을 검색합니다.
    """
    tag_to_search = request.tag
    api_url = f"https://solved.ac/api/v3/search/problem?query=tag:{tag_to_search}"
    
    try:
        # Solved.ac API 서버에 데이터를 요청합니다.
        response = requests.get(api_url)
        response.raise_for_status()  # 요청이 실패하면 에러를 발생시킵니다.

        # 받아온 JSON 데이터를 파이썬 객체로 변환합니다.
        data = response.json()
        
        # 받은 데이터 중에서 필요한 정보만 골라서 깔끔하게 정리합니다.
        problems = [
            {
                "id": item.get("problemId"),
                "title": item.get("titleKo"),
                "level": item.get("level")
            }
            # 'items' 라는 키에 실제 문제 목록이 들어있습니다.
            for item in data.get("items", [])
        ]
        
        # 정리된 데이터를 Postman에게 응답으로 보내줍니다.
        return {"status": "success", "tag": tag_to_search, "count": len(problems), "problems": problems}

    except requests.exceptions.RequestException as e:
        # API 통신 중 문제가 생기면 에러 메시지를 응답으로 보냅니다.
        return {"status": "error", "message": f"API 요청에 실패했습니다: {e}"}

# 서버의 기본 주소('/')로 접속했을 때 보여줄 간단한 메시지
@app.get("/")
def root():
    return {"message": "백준 문제 검색 서버가 작동 중입니다."}