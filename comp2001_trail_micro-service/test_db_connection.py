from config import app, db
from sqlalchemy.sql import text  # Import text function for raw SQL queries

# Wrap the test code in an application context
with app.app_context():
    try:
        # Test the database connection using text()
        db.session.execute(text("SELECT 1"))
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")

