from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

app = FastAPI()

class Note(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: str

def init_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         content TEXT NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/notes/", response_model=NoteResponse)
async def create_note(note: Note):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("INSERT INTO notes (title, content) VALUES (?, ?)",
              (note.title, note.content))
    note_id = c.lastrowid
    c.execute("SELECT id, title, content, created_at FROM notes WHERE id = ?", (note_id,))
    result = c.fetchone()
    conn.commit()
    conn.close()
    return NoteResponse(id=result[0], title=result[1], content=result[2], created_at=result[3])

@app.get("/notes/", response_model=List[NoteResponse])
async def get_notes():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT id, title, content, created_at FROM notes")
    notes = c.fetchall()
    conn.close()
    
    if not notes:
        raise HTTPException(status_code=404, detail="No notes found")
    
    return [NoteResponse(id=note[0], title=note[1], content=note[2], created_at=note[3]) for note in notes]

@app.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT id, title, content, created_at FROM notes WHERE id = ?", (note_id,))
    note = c.fetchone()
    conn.close()
    
    if note is None:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found")
    
    return NoteResponse(id=note[0], title=note[1], content=note[2], created_at=note[3])

@app.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int, note: Note):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT id FROM notes WHERE id = ?", (note_id,))
    if not c.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found")
    
    c.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?",
              (note.title, note.content, note_id))
    conn.commit()
    
    c.execute("SELECT id, title, content, created_at FROM notes WHERE id = ?", (note_id,))
    updated_note = c.fetchone()
    conn.close()
    
    return NoteResponse(id=updated_note[0], title=updated_note[1], content=updated_note[2], created_at=updated_note[3])

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT id FROM notes WHERE id = ?", (note_id,))
    if not c.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found")
    
    c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return {"message": f"Note with id {note_id} deleted successfully"}