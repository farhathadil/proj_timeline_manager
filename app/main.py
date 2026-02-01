from fastapi import FastAPI, Request, Form, UploadFile, File, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from .db import engine, create_db_and_tables
from .models import Project, TaskTimelineItem
from .csv_utils import parse_csv_bytes
from typing import List
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def index(request: Request, q: str = "", category: str = ""):
    with Session(engine) as session:
        stmt = select(Project)
        projects = session.exec(stmt).all()
        # simple in-memory filter/search for clarity
        def match(p: Project):
            if category:
                if (p.category or "Uncategorized") != category:
                    return False
            if q:
                s = q.lower()
                hay = " ".join([p.title or '', p.category or '', p.task_name or '']).lower()
                # also check timeline descriptions
                for t in getattr(p, 'timeline', []):
                    hay += ' ' + (t.description or '')
                return s in hay
            return True
        filtered = [p for p in projects if match(p)]
        # compute timeline span for each
        items = []
        for p in filtered:
            dates = [t.date for t in getattr(p, 'timeline', [])]
            span = None
            if dates:
                span = (min(dates).isoformat(), max(dates).isoformat())
            items.append({'project': p, 'span': span})
        categories = set([p.category or 'Uncategorized' for p in projects])
        return templates.TemplateResponse('index.html', {"request": request, "projects": items, "categories": sorted(categories), "q": q, "category": category})

@app.get('/project/{project_id}')
def project_detail(request: Request, project_id: int):
    with Session(engine) as session:
        p = session.get(Project, project_id)
        if not p:
            raise HTTPException(status_code=404)
        # sort timeline by date
        timeline = sorted(p.timeline, key=lambda x: x.date)
        return templates.TemplateResponse('project_detail.html', {"request": request, "project": p, "timeline": timeline})

@app.post('/project/{project_id}/timeline/add')
def add_timeline(project_id: int, date: str = Form(...), description: str = Form(...)):
    from datetime import datetime
    with Session(engine) as session:
        p = session.get(Project, project_id)
        if not p:
            raise HTTPException(status_code=404)
        dt = datetime.fromisoformat(date).date()
        t = TaskTimelineItem(project_id=project_id, date=dt, description=description)
        session.add(t)
        session.commit()
    return RedirectResponse(url=f'/project/{project_id}', status_code=303)

@app.get('/import')
def import_page(request: Request):
    return templates.TemplateResponse('import.html', {"request": request})

@app.post('/import/preview')
def import_preview(request: Request, file: UploadFile = File(...)):
    data = file.file.read()
    rows, errors = parse_csv_bytes(data)
    return templates.TemplateResponse('import_preview.html', {"request": request, "rows": rows, "errors": errors, "rows_json": json.dumps(rows)})

@app.post('/import/commit')
def import_commit(rows_json: str = Form(...)):
    rows = json.loads(rows_json)
    created_projects = {}
    created_items = 0
    with Session(engine) as session:
        for r in rows:
            key = (r['title'], r['task_name'], r.get('category'))
            proj = None
            # find existing
            stmt = select(Project).where(Project.title == r['title']).where(Project.task_name == r['task_name'])
            candidates = session.exec(stmt).all()
            for c in candidates:
                if (c.category or None) == (r.get('category') or None):
                    proj = c
                    break
            if not proj:
                proj = Project(title=r['title'], task_name=r['task_name'], category=r.get('category'))
                session.add(proj)
                session.commit()
                session.refresh(proj)
                created_projects[key] = proj.id
            # add timeline item
            from datetime import date
            dt = date.fromisoformat(r['date'])
            t = TaskTimelineItem(project_id=proj.id, date=dt, description=r.get('description',''))
            session.add(t)
            created_items += 1
        session.commit()
    return templates.TemplateResponse('import_done.html', {"request": Request({'type':'http'}), "projects_created": len(created_projects), "items_created": created_items})
