from fastapi import FastAPI, Depends, Query, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
import csv
import io
import json
from datetime import datetime
from typing import Optional, List
from contextlib import asynccontextmanager

from database import init_db, get_db, Opportunity
from scheduler import start_scheduler, run_scrape_task
from scraper import OpportunityScraper

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    scheduler = start_scheduler()
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(title="OpportunityRadar API", lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.get("/api/opportunities")
def get_opportunities(
    keyword: Optional[str] = None,
    type: Optional[str] = None,
    source: Optional[str] = None,
    deadline_before: Optional[str] = None,
    deadline_after: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1),
    db: Session = Depends(get_db)
):
    query = db.query(Opportunity)
    
    if keyword:
        query = query.filter(or_(
            Opportunity.title.ilike(f"%{keyword}%"),
            Opportunity.description.ilike(f"%{keyword}%"),
            Opportunity.tags.ilike(f"%{keyword}%")
        ))
    
    if type and type != "All":
        query = query.filter(Opportunity.type == type)
        
    if source and source != "All":
        query = query.filter(Opportunity.source_name == source)
        
    if deadline_before:
        query = query.filter(Opportunity.deadline <= deadline_before)
    
    if deadline_after:
        query = query.filter(Opportunity.deadline >= deadline_after)

    total = query.count()
    opportunities = query.order_by(Opportunity.date_added.desc()).offset((page - 1) * limit).limit(limit).all()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": opportunities
    }

@app.get("/api/opportunities/{id}")
def get_opportunity(id: int, db: Session = Depends(get_db)):
    opp = db.query(Opportunity).filter(Opportunity.id == id).first()
    if not opp:
        return JSONResponse(status_code=404, content={"message": "Opportunity not found"})
    return opp

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_count = db.query(Opportunity).count()
    type_counts = db.query(Opportunity.type, func.count(Opportunity.id)).group_by(Opportunity.type).all()
    source_counts = db.query(Opportunity.source_name, func.count(Opportunity.id)).group_by(Opportunity.source_name).all()
    
    last_updated = db.query(func.max(Opportunity.date_added)).scalar()
    
    return {
        "total": total_count,
        "by_type": {t: c for t, c in type_counts},
        "by_source": {s: c for s, c in source_counts},
        "last_updated": last_updated.isoformat() if last_updated else None
    }

@app.get("/api/export/csv")
def export_csv(db: Session = Depends(get_db)):
    opps = db.query(Opportunity).all()
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "ID", "Title", "Type", "Organizer", "Location", "Deadline", 
        "Source Link", "Source Name", "Description", "Funding Range", 
        "Stage", "Remote/On-site", "Tags", "Date Added"
    ])
    
    for opp in opps:
        writer.writerow([
            opp.id, opp.title, opp.type, opp.organizer, opp.location, opp.deadline,
            opp.source_link, opp.source_name, opp.description, opp.funding_range,
            opp.startup_stage, opp.remote_or_onsite, opp.tags, opp.date_added
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=opportunities.csv"}
    )

@app.get("/api/export/json")
def export_json(db: Session = Depends(get_db)):
    opps = db.query(Opportunity).all()
    data = []
    for opp in opps:
        data.append({
            "id": opp.id,
            "title": opp.title,
            "type": opp.type,
            "organizer": opp.organizer,
            "location": opp.location,
            "deadline": opp.deadline,
            "source_link": opp.source_link,
            "source_name": opp.source_name,
            "description": opp.description,
            "funding_range": opp.funding_range,
            "startup_stage": opp.startup_stage,
            "remote_or_onsite": opp.remote_or_onsite,
            "tags": opp.tags,
            "date_added": opp.date_added.isoformat() if opp.date_added else None
        })
    
    return JSONResponse(
        content=data,
        headers={"Content-Disposition": "attachment; filename=opportunities.json"}
    )

@app.post("/api/scrape")
async def trigger_scrape(background_tasks: BackgroundTasks, params: Optional[dict] = None):
    keyword = params.get("keyword", "AI startup") if params else "AI startup"
    background_tasks.add_task(run_scrape_task, keyword=keyword)
    return {"status": "started", "message": f"Scrape for '{keyword}' has been triggered in the background."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
