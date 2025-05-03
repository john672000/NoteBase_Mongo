from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from database import notes_collection, users_collection
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from passlib.hash import bcrypt
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
port = os.getenv("PORT", 8000)


class Feedback(BaseModel):
    username: str
    feedback: Optional[str] = None

class User(BaseModel):
    username: str
    password: str
    feedback: Optional[str] = None
    
class UserLogin(BaseModel):
    username: str
    password: str


class Note(BaseModel):
    username: str
    title: str
    created_at: str
    updated_at: str
    text: Optional[str] = None
    
class UpdateNote(BaseModel):
    title: Optional[str] = None
    username: Optional[str] = None
    updated_at: Optional[str] = None
    text: Optional[str] = None


class DeleteRequest(BaseModel):
    username: str


def serialize_notes(note):
    return {
        "id": str(note["_id"]),
        "title": note.get("title", ""),
        "created_at": note.get("created_at", ""),
        "updated_at": note.get("updated_at", ""),
        "text": note.get("text", ""),
    }


@app.post("/feedback")
def feedback(comment : Feedback):
    user = users_collection.find_one({"username": comment.username})
    if user:
       result = users_collection.find_one_and_update(
    {"username": comment.username},
    {"$set": {"feedback": comment.feedback}},
    return_document=True
    )
       if result:
           return {"message":"Feedback recieved successfully"}
       
       else:
        raise HTTPException(
            status_code=500, detail="Failed to send feedback"
        )
    else:
        raise HTTPException(
            status_code=420, detail="username doesn't exisit"
        )
    
    

@app.post("/signup")
def signup(user: User):
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username already exists, #Be-Different"
        )

    hashed_password = bcrypt.hash(user.password)

    result = users_collection.insert_one(
        {"username": user.username, "password": hashed_password}
    )

    return {"message": "User Sucessfully Created", "user_id": str(result.inserted_id)}

@app.post("/ERASE")
def erase_account(user: UserLogin):
    existing_user = users_collection.find_one({"username": user.username})
    
    if not existing_user or not bcrypt.verify(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid Password")

    deleted_notes = notes_collection.delete_many({"username": user.username})
    deleted_user = users_collection.delete_one({"username": user.username})

    return {
        "message": "User and associated data deleted successfully",
        "deleted_notes_count": deleted_notes.deleted_count,
        "deleted_user_count": deleted_user.deleted_count,
    }


@app.post("/login")
def login(user: UserLogin):
    exisiting_user = users_collection.find_one({"username": user.username})
    if not exisiting_user or not bcrypt.verify(
        user.password, exisiting_user["password"]
    ):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login Successful", "username": user.username}


# R -> READ
@app.get("/getnotes/{username}")
def get_notes(username: str):
    notes = notes_collection.find({"username": username})
    return [serialize_notes(note) for note in notes]


# C -> CREATE
@app.post("/addnotes")
def add_note(note: Note):
    note_dict = note.model_dump()
    result = notes_collection.insert_one(note_dict)
    new_note = notes_collection.find_one({"_id": result.inserted_id})
    return serialize_notes(new_note)


# U -> UPDATE
@app.put("/updatenote/{note_id}")
def update_note(note_id: str, note: UpdateNote):

    update_data = note.model_dump(exclude_unset=True)

    if not update_data:
        print("No fields to update")
        raise HTTPException(status_code=400, detail="No fields to update.")

    try:
        # Check if note exists
        existing_note = notes_collection.find_one(
            {"_id": ObjectId(note_id), "username": note.username}
        )
        if not existing_note:
            print(f"Note with ID {note_id} not found")
            raise HTTPException(status_code=404, detail="Note not found")

        result = notes_collection.update_one(
            {"_id": ObjectId(note_id)}, {"$set": update_data}
        )

        print(f"Update result: {result.modified_count} document(s) modified")

        if result.modified_count == 0:
            print("No changes made to the document")
            raise HTTPException(
                status_code=404, detail="Note not found or no changes made."
            )

        # Get the updated note
        updated_note = notes_collection.find_one({"_id": ObjectId(note_id)})
        print(f"Updated note: {updated_note}")

        return serialize_notes(updated_note)
    except Exception as e:
        print(f"Error updating note: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating note: {str(e)}")


# D -> DELETE
@app.delete("/deletenote/{note_id}")
def delete_note(note_id: str):
    result = notes_collection.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found or unauthorized.")
    return {"message": "Note deleted successfully"}


@app.get("/")
def read_root():
    return {"message": "API is up and running!", "at port ": port}
