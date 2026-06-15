import os
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/resources", tags=["resources"])

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


# --- CREATE ---
@router.post("/", response_model=schemas.ResourceResponse, status_code=status.HTTP_201_CREATED)
async def upload_resource(
        title: str = Form(...),
        description: str = Form(...),  # Reads the combined string from the frontend
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    safe_filename = os.path.basename(file.filename)
    file_path = os.path.join("uploads", safe_filename).replace("\\", "/")

    # Create the uploads folder directory if it doesn't exist yet
    os.makedirs("uploads", exist_ok=True)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return crud.create_resource(db=db, title=title, description=description, file_path=file_path)

# --- READ ALL ---
@router.get("/", response_model=list[schemas.ResourceResponse])
def read_all_resources(db: Session = Depends(get_db)):
    return crud.get_resources(db)


# --- READ ONE ---
@router.get("/{resource_id}", response_model=schemas.ResourceResponse)
def read_single_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = crud.get_resource(db, resource_id=resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


# --- UPDATE ---
@router.put("/{resource_id}", response_model=schemas.ResourceResponse)
def update_resource_details(
        resource_id: int,
        title: str = Form(...),
        description: str = Form(None),
        db: Session = Depends(get_db)
):
    updated_resource = crud.update_resource(db, resource_id=resource_id, title=title, description=description)
    if not updated_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return updated_resource


# --- DELETE ---
@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource_item(resource_id: int, db: Session = Depends(get_db)):
    # Find the resource first to get the file path
    resource = crud.get_resource(db, resource_id=resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Delete the physical file from the uploads folder
    if os.path.exists(resource.file_path):
        os.remove(resource.file_path)

    # Delete from database
    crud.delete_resource(db, resource_id=resource_id)
    return None