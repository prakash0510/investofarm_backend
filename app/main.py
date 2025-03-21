from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import users, notification, project, feedback, sent_email

app = FastAPI()
origins = [
    "http://localhost:3000",  
    "http://127.0.0.1:5500",
    "*",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
app.include_router(users.router, prefix="/api/users", tags=["Users"])

@app.get("/")
def home():
    return {"message": "FastAPI with JWT Authentication"}

app.include_router(notification.router)
app.include_router(project.router)
app.include_router(feedback.router)
app.include_router(sent_email.router)