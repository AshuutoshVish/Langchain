from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ai_agent import get_response_from_ai_agent

load_dotenv()

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

allowed_model_names = ["llama3-70b-8192", "llama-3.3-70b-versatile", "gemini-2.0-flash"]

app = FastAPI(title="LangGraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    try:
        if request.model_name not in allowed_model_names:
            return JSONResponse(status_code=400, content={"error": "Invalid model name. Kindly select a valid model."})

        response = get_response_from_ai_agent(
            llm_id=request.model_name,
            provider=request.model_provider,
            query=request.messages,
            allow_search=request.allow_search,
            system_prompt=request.system_prompt
        )

        return {"response": response}

    except Exception as e:
        print("ERROR in /chat:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)
