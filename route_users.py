from fastapi import  APIRouter, FastAPI, Depends, HTTPException, status, Response

from  database import engine,SessionLocal, Base
from schema import UsersSchema
from sqlalchemy.orm import Session
from models import Users

#cria a tabela
Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/users")   

def get_db():
    try:
        db = SessionLocal()
        #TODO 
        yield db
    finally:
        db.close()




@router.post("/add")
async def add_users(request:UsersSchema, db: Session = Depends(get_db)):
    users_on_db = Users(id=request.id, username=request.username, password=request.password, cpf=request.cpf)
    db.add(users_on_db)
    db.commit()
    db.refresh(users_on_db)
    return users_on_db

@router.get("/{users_name}", description="Listar o usuário pelo nome")
def get_users(users_name,db: Session = Depends(get_db)):
    users_on_db= db.query(Users).filter(Users.item == users_name).first()
    return users_on_db

@router.get("/users/listar")
async def get_tarefas(db: Session = Depends(get_db)):
    users= db.query(Users).all()
    return users


@router.delete("/{id}", description="Deletar o usuário pelo id")
def delete_users(id: int, db: Session = Depends(get_db)):
    users_on_db = db.query(Users).filter(Users.id == id).first()
    if users_on_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Sem usuário com este id')
    db.delete(users_on_db)
    db.commit()
    return f"Banco with id {id} deletado.", Response(status_code=status.HTTP_200_OK)
