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

# Create Receiver
def create_receiver(db: Session, receiver: schemas.ReceiverCreate):
    db_receiver = models.Receiver(
        Receiver_ID=receiver.Receiver_ID,
        Name=receiver.Name,
        Type=receiver.Type,
        Address=receiver.Address,
        City=receiver.City,
        Contact=receiver.Contact,
    )
    db.add(db_receiver)
    db.commit()
    db.refresh(db_receiver)
    return db_receiver

# Read Receivers
def get_receivers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Receiver).offset(skip).limit(limit).all()

# Update Receiver
def update_receiver(db: Session, receiver_id: int, updated_data: schemas.ReceiverUpdate):
    db_receiver = db.query(models.Receiver).filter(models.Receiver.Receiver_ID == receiver_id).first()
    if db_receiver:
        for key, value in updated_data.dict(exclude_unset=True).items():
            setattr(db_receiver, key, value)
        db.commit()
        db.refresh(db_receiver)
    return db_receiver

# Delete Receiver
def delete_receiver(db: Session, receiver_id: int):
    db_receiver = db.query(models.Receiver).filter(models.Receiver.Receiver_ID == receiver_id).first()
    if db_receiver:
        db.delete(db_receiver)
        db.commit()
    return db_receiver

# Create Food Listing
def create_food_listing(db: Session, listing: schemas.FoodListingCreate):
    db_listing = models.FoodListing(
        Listing_ID=listing.Listing_ID,
        Provider_ID=listing.Provider_ID,
        Food_Name=listing.Food_Name,
        Quantity=listing.Quantity,
        Expiry_Date=listing.Expiry_Date,
    )
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing

# Read Food Listings
def get_food_listings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.FoodListing).offset(skip).limit(limit).all()

# Update Food Listing
def update_food_listing(db: Session, listing_id: int, updated_data: schemas.FoodListingUpdate):
    db_listing = db.query(models.FoodListing).filter(models.FoodListing.Listing_ID == listing_id).first()
    if db_listing:
        for key, value in updated_data.dict(exclude_unset=True).items():
            setattr(db_listing, key, value)
        db.commit()
        db.refresh(db_listing)
    return db_listing

# Delete Food Listing
def delete_food_listing(db: Session, listing_id: int):
    db_listing = db.query(models.FoodListing).filter(models.FoodListing.Listing_ID == listing_id).first()
    if db_listing:
        db.delete(db_listing)
        db.commit()
    return db_listing

# Create Claim
def create_claim(db: Session, claim: schemas.ClaimCreate):
    db_claim = models.Claim(
        Claim_ID=claim.Claim_ID,
        Listing_ID=claim.Listing_ID,
        Receiver_ID=claim.Receiver_ID,
        Claim_Date=claim.Claim_Date,
        Quantity=claim.Quantity,
    )
    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim

# Read Claims
def get_claims(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Claim).offset(skip).limit(limit).all()

# Update Claim
def update_claim(db: Session, claim_id: int, updated_data: schemas.ClaimUpdate):
    db_claim = db.query(models.Claim).filter(models.Claim.Claim_ID == claim_id).first()
    if db_claim:
        for key, value in updated_data.dict(exclude_unset=True).items():
            setattr(db_claim, key, value)
        db.commit()
        db.refresh(db_claim)
    return db_claim

# Delete Claim
def delete_claim(db: Session, claim_id: int):
    db_claim = db.query(models.Claim).filter(models.Claim.Claim_ID == claim_id).first()
    if db_claim:
        db.delete(db_claim)
        db.commit()
    return db_claim
