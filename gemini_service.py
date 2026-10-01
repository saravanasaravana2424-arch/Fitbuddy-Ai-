import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None

GEMINI_MODEL = "gemini-3.8-flash"


# Fallback Fitness Plan
def fallback_fitness_plan(name, age, fitness_level, goal):

    return f"""
FitBuddy – 7-Day Fitness Plan

Name: {name}
Age: {age}
Fitness Level: {fitness_level}
Fitness Goal: {goal}

Day 1 – Full Body
- Warm-up: 5 minutes
- Comfortable squats
- Wall push-ups
- Gentle cool-down

Day 2 – Light Cardio
- Comfortable walking
- Gentle stretching
- Rest when needed

Day 3 – Upper Body
- Wall push-ups
- Gentle arm movements
- Cool-down

Day 4 – Recovery
- Rest
- Gentle movement if comfortable

Day 5 – Lower Body
- Warm-up
- Chair squats
- Gentle stretching

Day 6 – Light Activity
- Choose an enjoyable activity
- Move at a comfortable pace

Day 7 – Rest
- Recovery
- Relaxation

Safety Tips:
- Start gradually.
- Take breaks when needed.
- Stop if you feel pain or unwell.

This is a general wellness plan, not medical advice.

Note: Gemini was unavailable, so this sample plan is displayed.
"""


# Generate Fitness Plan using Gemini
def generate_fitness_plan(name, age, fitness_level, goal):

    if client is None:
        return fallback_fitness_plan(name, age, fitness_level, goal)

    prompt = f"""
Create a general beginner-friendly 7-day fitness plan.

Name: {name}
Age: {age}
Fitness Level: {fitness_level}
Fitness Goal: {goal}

Include:
- Warm-up
- Gentle activities
- Recovery
- Safety tips

Keep it simple and easy to understand.
Avoid extreme exercise recommendations.
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if response.text:
            return response.text

        return fallback_fitness_plan(name, age, fitness_level, goal)

    except Exception as e:
        print("Gemini Error:", e)

        return fallback_fitness_plan(name, age, fitness_level, goal)


# Nutrition Tip using Gemini
def generate_nutrition_tip_with_flash(goal):

    if client is None:
        return "Focus on balanced meals, hydration, and adequate rest."

    prompt = f"""
Give a short general nutrition and recovery tip
for a person whose fitness goal is {goal}.

Focus on:
- Balanced meals
- Drinking enough water
- Adequate sleep
- Recovery

Avoid restrictive diets or medical claims.
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if response.text:
            return response.text

        return "Focus on balanced meals, hydration, and adequate rest."

    except Exception as e:
        print("Gemini Nutrition Error:", e)

        return "Focus on balanced meals, hydration, and adequate rest."