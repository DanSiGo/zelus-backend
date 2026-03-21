from sqlalchemy.orm import Session
# Importando as classes específicas:
from src.models.user import User
from src.schemas.user import UserCreate
# Importaremos um schema de Update que criaremos a seguir
# from src.schemas.user import UserUpdate
import bcrypt


def hash_password(password: str) -> str:
    # Convert string to bytes
    pwd_bytes = password.encode('utf-8')
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # Return as a string to store in the DB
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convert both to bytes for comparison
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    # Use bcrypt's built-in check
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_user(db: Session, user_data: UserCreate): # Usa a classe do Schema
    hashed_password = hash_password(user_data.password)    
    # Usa a classe do Model
    db_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- BUSCA (READ) ---

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

# --- ATUALIZAÇÃO (UPDATE) ---

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

# --- DELEÇÃO (DELETE) ---

def delete_user(db: Session, user_id: int):
    """Remove um usuário do banco de dados"""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False