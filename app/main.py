from fastapi import FastAPI
from app.api.routes import users, notification, project, feedback

app = FastAPI()

app.include_router(users.router, prefix="/api/users", tags=["Users"])

@app.get("/")
def home():
    return {"message": "FastAPI with JWT Authentication"}

app.include_router(notification.router)
app.include_router(project.router)
app.include_router(feedback.router)