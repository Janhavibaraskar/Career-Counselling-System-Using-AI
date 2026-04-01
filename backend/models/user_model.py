from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ---------------- USER MODEL ----------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


# ---------------- ASSESSMENT MODEL ----------------
class Assessment(db.Model):
    __tablename__ = "assessments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    level = db.Column(db.String(50))
    interests = db.Column(db.String(100))
    document = db.Column(db.String(200))