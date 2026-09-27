from fastapi import FastAPI
from app.backend.routes import auth

app = FastAPI(title="Personal Finance Intelligence", description="A complete personal finance intelligence system which is having budgeting, investment details and expenses tracking system but its special feature is goal based tracking and goal based investment and savings strategies.", version="0.0.1")

app.include_router(auth.router)

