
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from backend.models.user_model import db, Assessment
from backend.routes.auth_routes import auth
from backend.services.grok_service import extract_text_from_file, get_career_recommendation
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@localhost/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# register blueprint
app.register_blueprint(auth)

test_scores = {}

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- HOME ----------------
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


# ---------------- ASSESSMENT ----------------
@app.route("/assessment", methods=["GET", "POST"])
def assessment():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        level = request.form.get("level")
        interests = request.form.get("interests")

        file = request.files.get("document")
        filename = None

        if file:
            filename = file.filename
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

        new_assessment = Assessment(
            user_id=session["user_id"],
            level=level,
            interests=interests,
            document=filename
        )

        db.session.add(new_assessment)
        db.session.commit()

        return redirect(url_for("test"))

    return render_template("assessment.html")


# ---------------- TEST ----------------
@app.route("/test")
def test():
    assessment = Assessment.query.order_by(Assessment.id.desc()).first()
    return render_template("test.html", interest=assessment.interests)


@app.route("/submit_test", methods=["POST"])
def submit_test():
    global test_scores
    test_scores = request.get_json()
    return jsonify({"status": "success"})


# ---------------- RESULT ----------------
@app.route("/result")
def result():

    global test_scores

    assessment = Assessment.query.order_by(Assessment.id.desc()).first()
    interest_domains = test_scores.get("interestDomains", {})

    document_text = ""
    if assessment.document:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], assessment.document)
        if os.path.exists(filepath):
            document_text = extract_text_from_file(filepath)

    ai_result = get_career_recommendation(
        assessment.level,
        assessment.interests,
        test_scores,
        document_text
    )

    return render_template(
        "result.html",
        Analytical=test_scores.get("Analytical", 0),
        personality=test_scores.get("personality", 0),
        interest=test_scores.get("interest", 0),
        domain=test_scores.get("domain", 0),
        interest_domains=interest_domains,
        ai_result=ai_result
    )


# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)