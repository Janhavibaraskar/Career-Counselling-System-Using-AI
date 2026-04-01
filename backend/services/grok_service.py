import os
import pdfplumber
import pytesseract
from PIL import Image
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


# ---------------- TEXT EXTRACTION ----------------
def extract_text_from_file(filepath):
    text = ""

    if filepath.endswith(".pdf"):
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    elif filepath.endswith((".png", ".jpg", ".jpeg")):
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)

    return text


# ---------------- AI CAREER RECOMMENDATION ----------------
def get_career_recommendation(level, interests, scores, document_text):

    interest_domains = scores.get("interestDomains", {})

    prompt = f"""
You are an intelligent AI Career Counselor.

Analyze the student's assessment data and provide a clear, personalized career recommendation.

-------------------------------
Student Profile:
- Academic Level: {level}
- Selected Interest: {interests}

Assessment Scores (0-100):
- Interest Score: {scores.get("interest", 0)}
- Analytical Ability: {scores.get("Analytical", 0)}
- Personality Traits: {scores.get("personality", 0)}
- Domain Knowledge: {scores.get("domain", 0)}

Domain-wise Interest:
{interest_domains}

Student Resume / Marks:
{document_text}
-------------------------------

Instructions:

- Identify the TOP suitable career domain based on domain-wise interest and scores.
- Give recommendation based on student's academic level:
    • Class 10 → suggest stream (Science / Commerce / Arts / Diploma)
    • Class 12 → suggest degree + entrance exams
    • Graduate → suggest job roles + upskilling + higher studies

- Keep response SHORT (max 120 words)
- Use clear bullet points
- Be practical and specific (no generic advice)

Output Format:

Career Recommendation:
(1–2 best career options)

Why This Career Fits You:
- (2 points based on scores & interest)

Skill Gap to Improve:
- (2–3 skills)

Suggested Courses / Exams:
- (2–3 relevant suggestions)

IMPORTANT:
Start response with:
"Based on your domain interest, analytical ability, and personality..."
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an AI career counselor specializing in student guidance"},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception:
        return "AI recommendation currently unavailable."