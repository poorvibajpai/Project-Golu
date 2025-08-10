from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sqlite3, datetime
# Add to imports
import threading
import time

# Add before uvicorn.run()
def reminder_background_task():
    while True:
        time.sleep(60)  # Check every minute
        # Implement your reminder logic here

threading.Thread(target=reminder_background_task, daemon=True).start()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fake auth (replace with real auth later)
VALID_TOKENS = {"hackathon_token": "user123"}

# Database setup
conn = sqlite3.connect('db.sqlite', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY, user_id TEXT, task TEXT, time TEXT, status TEXT)''')
conn.commit()

@app.post("/validate")
def validate(token: str):
    if token in VALID_TOKENS:
        return {"user_id": VALID_TOKENS[token]}
    raise HTTPException(401, "Invalid token!")

@app.post("/add_task")
async def add_task(request: Request):
    try:
        data = await request.json()
        cursor.execute("INSERT INTO tasks (user_id, task, time, status) VALUES (?, ?, ?, ?)",
                      (data["user_id"], data["task"], data["time"], data["status"]))
        conn.commit()
        return {"status": "success", "task_id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(500, f"Error adding task: {str(e)}")

@app.get("/get_tasks")
def get_tasks(user_id: str = Query(...)):
    cursor.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))
    tasks = cursor.fetchall()
    return [{"id": t[0], "user_id": t[1], "task": t[2], "time": t[3], "status": t[4]} 
            for t in tasks]

@app.post("/update_task")
async def update_task(request: Request):
    data = await request.json()
    cursor.execute("UPDATE tasks SET status=? WHERE id=?", 
                  (data["status"], data["task_id"]))
    conn.commit()
    return {"status": "Updated!"}

@app.post("/delete_task")
async def delete_task(request: Request):
    data = await request.json()
    cursor.execute("DELETE FROM tasks WHERE id=?", (data["task_id"],))
    conn.commit()
    return {"status": "Deleted!"}

@app.post("/get_reminder")
def get_reminder(user_id: str):
    now = datetime.datetime.now().strftime("%H:%M")
    cursor.execute("SELECT task FROM tasks WHERE user_id=? AND time=?", (user_id, now))
    task = cursor.fetchone()
    return {"reminder": task[0] if task else "No tasks right now!"}

@app.get("/get_random_content")
def get_random_content():
    cursor.execute("SELECT content, content_type FROM educational_content WHERE is_active=1 ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    return {"content": result[0], "type": result[1]} if result else {"content": "No content available", "type": "fact"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.post("/add_content")
async def add_content(request: Request):
    data = await request.json()
    cursor.execute("INSERT INTO educational_content (content, content_type) VALUES (?, ?)",
                 (data["content"], data["content_type"]))
    conn.commit()
    return {"status": "Content added!"}

@app.get("/check_reminders")
def check_reminders(user_id: str):
    now = datetime.datetime.now().strftime("%H:%M")
    cursor.execute("SELECT * FROM tasks WHERE user_id=? AND time=? AND status='upcoming'", (user_id, now))
    tasks = cursor.fetchall()
    
    if tasks:
        cursor.execute("UPDATE tasks SET status='ongoing' WHERE id=?", (tasks[0][0],))
        conn.commit()
        
        # Get random content to include with reminder
        cursor.execute("SELECT content FROM educational_content WHERE is_active=1 ORDER BY RANDOM() LIMIT 1")
        extra_content = cursor.fetchone()
        
        return {
            "reminder": tasks[0][2],
            "extra_content": extra_content[0] if extra_content else ""
        }
    return {"reminder": None}

