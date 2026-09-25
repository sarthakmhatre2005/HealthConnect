import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from sqlalchemy.orm import DeclarativeBase

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the base class
db = SQLAlchemy(model_class=Base)

# Create the Flask application
app = Flask(__name__)

# Configure the application
app.secret_key = os.environ.get("SESSION_SECRET", "healthconnect-secret-key-sih-prototype")

# Robust database URI configuration with SQLite fallback
db_url = os.environ.get("DATABASE_URL")
if db_url:
    # Handle older postgres URI schemas if needed
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
else:
    # Use SQLite by default for easy, reliable local execution
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///healthconnect.db"

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Session Cookie settings for SPA compatibility
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = False  # Set to False for local HTTP development

import re

# Enable CORS for React frontend (Vite defaults: port 5173, 5174, fallback 3000, or any localhost port)
CORS(
    app,
    resources={r"/api/*": {"origins": [
        re.compile(r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"),
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:5176",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]}},
    supports_credentials=True
)

# Initialize SQLAlchemy with the app
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Initialize the database and tables
with app.app_context():
    # Import models here so they are registered with SQLAlchemy
    import models
    # Create all tables in the database
    db.create_all()

    # Safe SQLite column migration for next-gen symptom checker fields
    try:
        from sqlalchemy import text
        with db.engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(symptom_check);")).fetchall()
            existing_cols = {row[1] for row in result}
            
            new_columns = [
                ("problem_description", "TEXT"),
                ("patient_details", "TEXT"),
                ("symptom_parameters", "TEXT"),
                ("image_filename", "VARCHAR(255)"),
                ("image_metadata", "TEXT")
            ]
            for col_name, col_type in new_columns:
                if col_name not in existing_cols:
                    conn.execute(text(f"ALTER TABLE symptom_check ADD COLUMN {col_name} {col_type};"))
                    conn.commit()
                    logger.info(f"Added column '{col_name}' to 'symptom_check' table.")
    except Exception as e:
        logger.warning(f"Database migration notice: {e}")

    logger.info("Database schema synchronized successfully.")

# Register all REST API routes
import routes