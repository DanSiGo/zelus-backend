from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserCreate
import bcrypt


def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_user(db: Session, user_data: UserCreate): # Usa a classe do Schema
    hashed_password = hash_password(user_data.password)    
    db_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    """Busca um usuário pelo ID único"""
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Lista usuários com paginação (pula 'skip' e limita a 'limit')"""
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    """
    Busca um usuário pelo e-mail exato.
    Útil para validação de cadastro e, futuramente, para o Login (JWT).
    """
    return db.query(User).filter(User.email == email).first()

def update_user(db: Session, user_id: int, user_data: dict):
    """
    Atualiza dados do usuário. 
    Recebe um dicionário com os campos que mudaram.
    """
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user_data.items():
            setattr(db_user, key, value) # Atualiza o campo dinamicamente
        
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Remove um usuário do banco de dados"""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False