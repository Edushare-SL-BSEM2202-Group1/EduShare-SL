from sqlalchemy.orm import Session
from app import models, schemas

# 1. CREATE: Save a new resource record
def create_resource(db: Session, title: str, description: str, file_path: str):
    # This matches your model perfectly (only title, description, and file_path)
    db_resource = models.Resource(
        title=title,
        description=description,
        file_path=file_path
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

# 2. READ: Get all resources
def get_resources(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resource).offset(skip).limit(limit).all()

def get_resource(db: Session, resource_id: int):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()

# 3. UPDATE: Update an existing resource's details
def update_resource(db: Session, resource_id: int, title: str, description: str):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if db_resource:
        db_resource.title = title
        db_resource.description = description
        db.commit()
        db.refresh(db_resource)
    return db_resource

# 4. DELETE: Remove a resource record
def delete_resource(db: Session, resource_id: int):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if db_resource:
        db.delete(db_resource)
        db.commit()
        return True
    return False