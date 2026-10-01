
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

from database import engine, Base, SessionLocal
from models import User

from gemini_service import (
    generate_fitness_plan,
    generate_nutrition_tip_with_flash
)

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")

templates = Jinja2Templates(directory="templates")

# Create database tables
Base.metadata.create_all(bind=engine)


# ---------------- HOME PAGE ----------------

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# ---------------- GENERATE FITNESS PLAN ----------------

@app.post("/generate")
def generate_plan(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    fitness_level: str = Form(...),
    goal: str = Form(...)
):
    plan = generate_fitness_plan(
        name, age, fitness_level, goal
    )

    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    db = SessionLocal()

    try:
        user = User(
            name=name,
            age=age,
            fitness_level=fitness_level,
            goal=goal,
            fitness_plan=plan
        )

        db.add(user)
        db.commit()

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "name": name,
                "age": age,
                "fitness_level": fitness_level,
                "goal": goal,
                "plan": plan,
                "nutrition_tip": nutrition_tip
            }
        )

    finally:
        db.close()


# ---------------- ADMIN PANEL ----------------

@app.get("/all-users")
def all_users(request: Request):
    db = SessionLocal()

    try:
        users = db.query(User).all()

        return templates.TemplateResponse(
            request=request,
            name="all_users.html",
            context={"users": users}
        )

    finally:
        db.close()


# ---------------- DELETE USER ----------------

@app.post("/delete-user/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if user:
            db.delete(user)
            db.commit()

    finally:
        db.close()

    return RedirectResponse(
        url="/all-users",
        status_code=303
    )


# ---------------- SUBMIT FEEDBACK ----------------

@app.post("/feedback")
def submit_feedback(
    name: str = Form(...),
    feedback: str = Form(...)
):
    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.name == name)
            .order_by(User.id.desc())
            .first()
        )

        if user:
            user.feedback = feedback
            db.commit()

    finally:
        db.close()

    return RedirectResponse(
        url="/all-users",
        status_code=303
    )


# ---------------- DOWNLOAD FITNESS PLAN ----------------

@app.get("/download-plan")
def download_plan(
    name: str,
    age: int,
    fitness_level: str,
    goal: str,
    plan: str
):
    content = f"""
FitBuddy - Fitness Plan

Name: {name}
Age: {age}
Fitness Level: {fitness_level}
Fitness Goal: {goal}

{plan}

Thank you for using FitBuddy!
"""

    return PlainTextResponse(
        content=content,
        headers={
            "Content-Disposition":
            "attachment; filename=FitBuddy_Plan.txt"
        }
    )


# ---------------- DASHBOARD ----------------

@app.get("/dashboard")
def dashboard(request: Request):
    db = SessionLocal()

    try:
        total_users = db.query(User).count()

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "total_users": total_users
            }
        )

    finally:
        db.close()


# ---------------- USER PROFILE ----------------

@app.get("/profile/{user_id}")
def user_profile(request: Request, user_id: int):
    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:
            return {"message": "User not found"}

        return templates.TemplateResponse(
            request=request,
            name="profile.html",
            context={"user": user}
        )

    finally:
        db.close()