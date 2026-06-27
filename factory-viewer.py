import sqlite3
import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI(title="Ontology Viewer")
templates = Jinja2Templates(directory="factory-templates")

DB_PATH = ".commonai/ontology.db"

def get_db_connection():
    # Provide a fallback if running from a different directory
    path = DB_PATH if os.path.exists(DB_PATH) else "ontology.db"
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def get_dashboard_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM features")
        features = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM user_stories")
        user_stories = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM acceptance_criteria")
        acceptance_criteria = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
    except Exception as e:
        features = []
        user_stories = []
        acceptance_criteria = []
        print(f"Error reading db: {e}")
    
    # Organize data hierarchically
    features_dict = {f["id"]: f for f in features}
    for f in features_dict.values():
        f["user_stories"] = []
        
    stories_dict = {us["id"]: us for us in user_stories}
    for us in stories_dict.values():
        us["acceptance_criteria"] = []
        
    for ac in acceptance_criteria:
        us_id = ac["user_story_id"]
        if us_id in stories_dict:
            stories_dict[us_id]["acceptance_criteria"].append(ac)
            
    for us in stories_dict.values():
        f_id = us["feature_id"]
        if f_id in features_dict:
            features_dict[f_id]["user_stories"].append(us)
            
    return list(features_dict.values()), list(stories_dict.values())

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    features, _ = get_dashboard_data()
    return templates.TemplateResponse(request=request, name="index.html", context={
        "features": features,
        "active_page": "index"
    })

@app.get("/board", response_class=HTMLResponse)
async def board(request: Request):
    _, stories = get_dashboard_data()
    # Group stories by status
    board_data = {
        "pending": [s for s in stories if s.get("status") == "pending"],
        "in_progress": [s for s in stories if s.get("status") == "in_progress"],
        "completed": [s for s in stories if s.get("status") == "completed"]
    }
    return templates.TemplateResponse(request=request, name="board.html", context={
        "board": board_data,
        "active_page": "board"
    })

@app.get("/features", response_class=HTMLResponse)
async def features_view(request: Request):
    features, _ = get_dashboard_data()
    return templates.TemplateResponse(request=request, name="features.html", context={
        "features": features,
        "active_page": "features"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("factory-viewer:app", host="0.0.0.0", port=8000, reload=True)
