from sqlalchemy.orm import Session
import models, schemas

# Create Provider
def create_provider(db: Session, provider: schemas.ProviderCreate):
    db_provider = models.Provider(
        Provider_ID=provider.Provider_ID,
        Name=provider.Name,
        Type=provider.Type,
        Address=provider.Address,
        City=provider.City,
        Contact=provider.Contact,
    )
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

# Read Providers
def get_providers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Provider).offset(skip).limit(limit).all()

# Update Provider
def update_provider(db: Session, provider_id: int, updated_data: schemas.ProviderUpdate):
    db_provider = db.query(models.Provider).filter(models.Provider.Provider_ID == provider_id).first()
    if db_provider:
        for key, value in updated_data.dict(exclude_unset=True).items():
            setattr(db_provider, key, value)
        db.commit()
        db.refresh(db_provider)
    return db_provider

# Delete Provider
def delete_provider(db: Session, provider_id: int):
    db_provider = db.query(models.Provider).filter(models.Provider.Provider_ID == provider_id).first()
    if db_provider:
        db.delete(db_provider)
        db.commit()
    return db_provider
