# 🔧 Phase 3: Backend Development Guide

**Project**: New Propertism Website  
**Duration**: 3-4 weeks  
**Status**: Ready to Execute

---

## 📋 Overview

This guide walks you through implementing the FastAPI backend for the new Propertism website.

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py
│   │           ├── properties.py
│   │           ├── inquiries.py
│   │           ├── maintenance.py
│   │           ├── construction.py
│   │           ├── contact.py
│   │           ├── subscriptions.py
│   │           └── tickets.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── property.py
│   │   ├── inquiry.py
│   │   ├── maintenance.py
│   │   ├── ticket.py
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── property.py
│   │   ├── inquiry.py
│   │   ├── maintenance.py
│   │   ├── ticket.py
│   │   └── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── session.py
│   └── main.py
├── requirements.txt
└── .env
```

---

## 🗄️ Step 1: Create Database Models

### `app/models/__init__.py`

```python
from .user import User, UserCreate, UserUpdate, UserInDB
from .property import Property, PropertyCreate, PropertyUpdate, PropertyType
from .inquiry import Inquiry, InquiryCreate, InquiryUpdate
from .maintenance import MaintenanceRequest, MaintenanceCreate, MaintenanceUpdate
from .ticket import Ticket, TicketCreate, TicketUpdate, TicketComment
from .subscription import Subscription, SubscriptionCreate

__all__ = [
    "User",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "Property",
    "PropertyCreate",
    "PropertyUpdate",
    "PropertyType",
    "Inquiry",
    "InquiryCreate",
    "InquiryUpdate",
    "MaintenanceRequest",
    "MaintenanceCreate",
    "MaintenanceUpdate",
    "Ticket",
    "TicketCreate",
    "TicketUpdate",
    "TicketComment",
    "Subscription",
    "SubscriptionCreate",
]
```

### `app/models/user.py`

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(20))
    role = Column(String(50), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    inquiries = relationship("Inquiry", back_populates="user")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="user")
    tickets = relationship("Ticket", back_populates="user")
    ticket_comments = relationship("TicketComment", back_populates="user")
```

### `app/models/property.py`

```python
from sqlalchemy import Column, Integer, String, Numeric, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

Base = declarative_base()

class PropertyType(Base):
    __tablename__ = "property_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(500))
    icon = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=func.now())

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric(15, 2), nullable=False)
    area = Column(Numeric(10, 2))
    bedrooms = Column(Integer, default=0)
    bathrooms = Column(Integer, default=0)
    location = Column(String(255), nullable=False)
    property_type_id = Column(Integer, ForeignKey("property_types.id"))
    status = Column(String(50), default="available")
    images = Column(JSONB)
    features = Column(JSONB)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    property_type = relationship("PropertyType")
    images_list = relationship("PropertyImage", back_populates="property")
    inquiries = relationship("Inquiry", back_populates="property")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="property")
    construction_updates = relationship("ConstructionUpdate", back_populates="property")

class PropertyImage(Base):
    __tablename__ = "property_images"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"))
    image_url = Column(String(500), nullable=False)
    caption = Column(String(255))
    is_primary = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now())

    # Relationships
    property = relationship("Property", back_populates="images_list")
```

### `app/models/inquiry.py`

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Inquiry(Base):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="SET NULL"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    message = Column(Text)
    inquiry_type = Column(String(50), default="general")
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    property = relationship("Property", back_populates="inquiries")
    user = relationship("User", back_populates="inquiries")
```

### `app/models/maintenance.py`

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="SET NULL"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(50), default="medium")
    status = Column(String(50), default="pending")
    assigned_to = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    property = relationship("Property", back_populates="maintenance_requests")
    user = relationship("User", back_populates="maintenance_requests")
    assigned_user = relationship("User", foreign_keys=[assigned_to])
```

### `app/models/ticket.py`

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Ticket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(50), default="medium")
    category = Column(String(100))
    status = Column(String(50), default="open")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="tickets")
    comments = relationship("TicketComment", back_populates="ticket")

class TicketComment(Base):
    __tablename__ = "ticket_comments"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("support_tickets.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    message = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

    # Relationships
    ticket = relationship("Ticket", back_populates="comments")
    user = relationship("User", back_populates="ticket_comments")
```

### `app/models/subscription.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255))
    status = Column(String(50), default="active")
    created_at = Column(DateTime(timezone=True), default=func.now())
```

---

## 📝 Step 2: Create Pydantic Schemas

### `app/schemas/__init__.py`

```python
from .user import User, UserCreate, UserUpdate, UserInDB, Token, TokenData
from .property import Property, PropertyCreate, PropertyUpdate, PropertyType
from .inquiry import Inquiry, InquiryCreate, InquiryUpdate
from .maintenance import MaintenanceRequest, MaintenanceCreate, MaintenanceUpdate
from .ticket import Ticket, TicketCreate, TicketUpdate, TicketComment
from .subscription import Subscription, SubscriptionCreate

__all__ = [
    "User",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "Token",
    "TokenData",
    "Property",
    "PropertyCreate",
    "PropertyUpdate",
    "PropertyType",
    "Inquiry",
    "InquiryCreate",
    "InquiryUpdate",
    "MaintenanceRequest",
    "MaintenanceCreate",
    "MaintenanceUpdate",
    "Ticket",
    "TicketCreate",
    "TicketUpdate",
    "TicketComment",
    "Subscription",
    "SubscriptionCreate",
]
```

### `app/schemas/user.py`

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class User(UserInDB):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
```

### `app/schemas/property.py`

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any

class PropertyTypeBase(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None

class PropertyImageBase(BaseModel):
    id: int
    image_url: str
    caption: Optional[str] = None
    is_primary: bool = False

class PropertyBase(BaseModel):
    title: str
    description: str
    price: float
    area: Optional[float] = None
    bedrooms: int = 0
    bathrooms: int = 0
    location: str
    property_type_id: Optional[int] = None
    status: str = "available"
    images: Optional[List[Any]] = None
    features: Optional[List[str]] = None

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    area: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    location: Optional[str] = None
    property_type_id: Optional[int] = None
    status: Optional[str] = None
    images: Optional[List[Any]] = None
    features: Optional[List[str]] = None

class Property(PropertyBase):
    id: int
    property_type: Optional[PropertyTypeBase] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PropertyList(BaseModel):
    items: List[Property]
    total: int
    page: int
    limit: int
```

### `app/schemas/inquiry.py`

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InquiryBase(BaseModel):
    property_id: int
    name: str
    email: str
    phone: str
    message: Optional[str] = None
    inquiry_type: str = "general"

class InquiryCreate(InquiryBase):
    pass

class InquiryUpdate(BaseModel):
    status: Optional[str] = None

class Inquiry(InquiryBase):
    id: int
    user_id: Optional[int] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InquiryList(BaseModel):
    items: List[Inquiry]
    total: int
    page: int
    limit: int
```

### `app/schemas/maintenance.py`

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MaintenanceBase(BaseModel):
    property_id: int
    title: str
    description: str
    priority: str = "medium"

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None

class MaintenanceRequest(MaintenanceBase):
    id: int
    user_id: Optional[int] = None
    status: str
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MaintenanceList(BaseModel):
    items: List[MaintenanceRequest]
    total: int
```

### `app/schemas/ticket.py`

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TicketBase(BaseModel):
    subject: str
    description: str
    priority: str = "medium"
    category: Optional[str] = None

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None

class TicketCommentBase(BaseModel):
    message: str
    is_internal: bool = False

class TicketCommentCreate(TicketCommentBase):
    pass

class TicketComment(TicketCommentBase):
    id: int
    ticket_id: int
    user_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Ticket(TicketBase):
    id: int
    user_id: Optional[int] = None
    status: str
    created_at: datetime
    updated_at: datetime
    comments: List[TicketComment] = []

    class Config:
        from_attributes = True

class TicketList(BaseModel):
    items: List[Ticket]
    total: int
```

### `app/schemas/subscription.py`

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class SubscriptionBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class SubscriptionList(BaseModel):
    items: List[Subscription]
    total: int
```

---

## 🔌 Step 3: Create API Endpoints

### `app/api/v1/endpoints/auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core import security
from app.core.config import settings
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserInDB, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    hashed_password = security.get_password_hash(user.password)
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
        name=user.name,
        phone=user.phone,
        role="user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(hours=settings.JWT_EXPIRY_HOURS)
    access_token = security.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserInDB)
def read_users_me(
    current_user: User = Depends(security.get_current_active_user)
):
    return current_user
```

### `app/api/v1/endpoints/properties.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.property import Property, PropertyType
from app.models.user import User
from app.schemas.property import PropertyCreate, PropertyUpdate, PropertyList
from app.core.security import get_current_active_user

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.get("/", response_model=PropertyList)
def read_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Property)
    
    if property_type:
        query = query.join(PropertyType).filter(PropertyType.slug == property_type)
    if min_price:
        query = query.filter(Property.price >= min_price)
    if max_price:
        query = query.filter(Property.price <= max_price)
    if location:
        query = query.filter(Property.location.ilike(f"%{location}%"))
    
    total = query.count()
    properties = query.offset(skip).limit(limit).all()
    
    return {
        "items": properties,
        "total": total,
        "page": skip // limit + 1,
        "limit": limit
    }

@router.get("/{property_id}", response_model=Property)
def read_property(property_id: int, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

@router.post("/", response_model=Property, status_code=status.HTTP_201_CREATED)
def create_property(
    property: PropertyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_property = Property(**property.model_dump())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@router.put("/{property_id}", response_model=Property)
def update_property(
    property_id: int,
    property: PropertyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    for key, value in property.model_dump(exclude_unset=True).items():
        setattr(db_property, key, value)
    
    db.commit()
    db.refresh(db_property)
    return db_property

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    db.delete(db_property)
    db.commit()
    return None
```

### `app/api/v1/endpoints/inquiries.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.inquiry import Inquiry
from app.models.user import User
from app.schemas.inquiry import InquiryCreate, InquiryList
from app.core.security import get_current_active_user, get_current_admin

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])

@router.post("/", response_model=Inquiry, status_code=status.HTTP_201_CREATED)
def create_inquiry(
    inquiry: InquiryCreate,
    db: Session = Depends(get_db)
):
    db_inquiry = Inquiry(**inquiry.model_dump())
    db.add(db_inquiry)
    db.commit()
    db.refresh(db_inquiry)
    return db_inquiry

@router.get("/", response_model=InquiryList)
def read_user_inquiries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    inquiries = db.query(Inquiry).filter(Inquiry.user_id == current_user.id).all()
    return {"items": inquiries, "total": len(inquiries), "page": 1, "limit": 100}

@router.get("/{inquiry_id}", response_model=Inquiry)
def read_inquiry(inquiry_id: int, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return inquiry

@router.put("/{inquiry_id}/status", response_model=Inquiry)
def update_inquiry_status(
    inquiry_id: int,
    status_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    
    inquiry.status = status_update.get("status", inquiry.status)
    db.commit()
    db.refresh(inquiry)
    return inquiry
```

### `app/api/v1/endpoints/maintenance.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.maintenance import MaintenanceRequest
from app.models.user import User
from app.schemas.maintenance import MaintenanceCreate, MaintenanceList
from app.core.security import get_current_active_user, get_current_admin

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

@router.post("/", response_model=MaintenanceRequest, status_code=201)
def create_maintenance_request(
    request: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_request = MaintenanceRequest(**request.model_dump(), user_id=current_user.id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.get("/", response_model=MaintenanceList)
def read_user_maintenance_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    requests = db.query(MaintenanceRequest).filter(MaintenanceRequest.user_id == current_user.id).all()
    return {"items": requests, "total": len(requests)}

@router.put("/{request_id}/status", response_model=MaintenanceRequest)
def update_maintenance_status(
    request_id: int,
    status_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    db_request = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    db_request.status = status_update.get("status", db_request.status)
    db.commit()
    db.refresh(db_request)
    return db_request
```

### `app/api/v1/endpoints/tickets.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.ticket import Ticket, TicketComment
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketCommentCreate, TicketList
from app.core.security import get_current_active_user, get_current_admin

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=Ticket, status_code=201)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_ticket = Ticket(**ticket.model_dump(), user_id=current_user.id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.get("/", response_model=TicketList)
def read_user_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    tickets = db.query(Ticket).filter(Ticket.user_id == current_user.id).all()
    return {"items": tickets, "total": len(tickets)}

@router.post("/{ticket_id}/comments", response_model=TicketComment, status_code=201)
def add_ticket_comment(
    ticket_id: int,
    comment: TicketCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_comment = TicketComment(
        **comment.model_dump(),
        ticket_id=ticket_id,
        user_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.put("/{ticket_id}/status", response_model=Ticket)
def update_ticket_status(
    ticket_id: int,
    status_update: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    db_ticket.status = status_update.get("status", db_ticket.status)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
```

### `app/api/v1/endpoints/contact.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionList
from app.core.security import get_current_admin

router = APIRouter(prefix="/contact", tags=["Contact"])

@router.post("/", response_model=Subscription, status_code=201)
def create_subscription(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db)
):
    db_subscription = Subscription(**subscription.model_dump())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@router.get("/", response_model=SubscriptionList)
def read_subscriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    subscriptions = db.query(Subscription).all()
    return {"items": subscriptions, "total": len(subscriptions)}
```

### `app/api/v1/endpoints/construction.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.property import Property
from app.schemas.property import PropertyList
from app.core.security import get_current_active_user

router = APIRouter(prefix="/construction-updates", tags=["Construction Updates"])

@router.get("/", response_model=PropertyList)
def read_construction_updates(
    db: Session = Depends(get_db)
):
    properties = db.query(Property).filter(Property.status == "construction").all()
    return {"items": properties, "total": len(properties), "page": 1, "limit": 100}
```

---

## 📋 Step 4: Create Main Application

### `app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1.endpoints import auth, properties, inquiries, maintenance, tickets, contact, construction, subscriptions

app = FastAPI(
    title="Propertism API",
    description="Real Estate Property Management API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(properties.router, prefix="/api/v1")
app.include_router(inquiries.router, prefix="/api/v1")
app.include_router(maintenance.router, prefix="/api/v1")
app.include_router(tickets.router, prefix="/api/v1")
app.include_router(contact.router, prefix="/api/v1")
app.include_router(construction.router, prefix="/api/v1")
app.include_router(subscriptions.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Propertism API v1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

## 📦 Step 5: Create Requirements

### `requirements.txt`

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.2
pydantic-settings==2.1.0
alembic==1.13.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
```

---

## 📝 Step 6: Create Environment File

### `.env`

```env
DATABASE_URL=postgresql://propertism_user:your_password@localhost:5432/propertism_dev
SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=smtp@example.com
SMTP_PASSWORD=smtp-password
```

---

## ✅ Verification Checklist

After completing all steps, verify:

- [ ] All API endpoints working
- [ ] Authentication working
- [ ] Database models created
- [ ] Pydantic schemas working
- [ ] CORS configured
- [ ] Documentation available at `/docs`

---

## 🎯 Next Steps

Once backend is ready:

1. **Test all endpoints** - Use Swagger UI at `/docs`
2. **Create frontend services** - Connect to API
3. **Begin frontend development** - Implement pages

---

**Backend Development Complete! Ready to start frontend development. 🚀**
