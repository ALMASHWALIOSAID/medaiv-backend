# seed_user.py
from sqlmodel import Session, select
from app.core.config import engine
from app.models.user import User
from app.core.security import hash_password

def main():
    username = "testuser"
    password = "testpass"
    with Session(engine) as session:
        # check for existing user
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing:
            print(f"User {username!r} already exists, skipping.")
            return

        user = User(
            username=username,
            hashed_password=hash_password(password),
            disabled=False,
        )
        session.add(user)
        session.commit()
        print(f"Created user {username!r}")

if __name__ == "__main__":
    main()
