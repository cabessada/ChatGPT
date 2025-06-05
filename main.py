from fastapi import FastAPI, Depends, Header
from services.file_service import router as file_router
from services.github_service import commit_and_push
from services.chatgpt_service import ask_chatgpt
from cron_jobs import start_cron
from utils.auth import verify_token

app = FastAPI()

app.include_router(file_router, prefix="/ficheiros", dependencies=[Depends(verify_token)])

@app.get("/github/push")
def push_to_github(token: str = Depends(verify_token)):
    return {"status": commit_and_push()}

@app.get("/chatgpt")
def chat(prompt: str, token: str = Depends(verify_token)):
    return {"resposta": ask_chatgpt(prompt)}

@app.on_event("startup")
def on_startup():
    start_cron()
