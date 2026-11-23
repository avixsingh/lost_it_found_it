"""Create the first administrator securely. Usage: python create_admin.py
Credentials are typed at the prompt, so nothing is hardcoded."""
import getpass
import sys

from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()
    name = input("Admin full name: ").strip()
    email = input("Admin email: ").strip().lower()
    password = getpass.getpass("Password (min 8 chars): ")
    confirm = getpass.getpass("Confirm password: ")

    if not name or "@" not in email:
        sys.exit("Invalid name or email.")
    if len(password) < 8 or password != confirm:
        sys.exit("Passwords must match and be at least 8 characters.")
    if User.query.filter_by(email=email).first():
        sys.exit("A user with that email already exists.")

    admin = User(name=name, email=email, role="admin")
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print(f"Administrator '{email}' created.")
