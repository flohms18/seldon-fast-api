from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()

from sqlalchemy import Column, Integer, String



class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String)
    tag = Column(String)



# App Config

app = FastAPI()


app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="templates")

# App Routes

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = 'postgresql://f-18@localhost:5432/postgres'
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine,autoflush=False, autocommit=False)



# App Model

Base.metadata.create_all(bind=engine)



def get_db() :
    db = SessionLocal()
    try : 
        yield db
    finally : 
        db.close()


from pydantic import BaseModel

class ProjectCreate(BaseModel):
    title : str
    tag : str

@app.post('/projects')
def create_project(project : ProjectCreate, db : Session = Depends(get_db)):
    db_project = Project(title = project.title, tag=project.tag)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get('/', response_class=HTMLResponse)
async def home(request : Request, db : Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=request, name='index.html', context= {
            'projects' : db.query(Project).all()
        }
        
    )
    




    
