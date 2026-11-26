from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


from database import engine, Base, get_db
from models import Project
from schemas import ProjectCreate

Base.metadata.create_all(bind=engine)





# App Config

app = FastAPI()


app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory="templates")

# App Routes


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







    
