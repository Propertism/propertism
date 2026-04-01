# 🗄️ Phase 2: Database Design Guide

**Project**: New Propertism Website  
**Duration**: 1 week  
**Status**: Ready to Execute

---

## 📋 Overview

This guide walks you through designing and implementing the database schema for the new Propertism website.

---

## 🎯 Database Requirements

### Core Entities
1. **Users** - User accounts and authentication
2. **Properties** - Property listings
3. **Inquiries** - Property inquiries
4. **Maintenance** - Maintenance requests
5. **Tickets** - Support tickets
6. **Construction Updates** - Construction progress
7. **Contact Messages** - Contact form submissions
8. **Subscriptions** - Email subscriptions

---

## 📊 Database Schema

### Entity Relationship Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   users     │     │ properties  │     │ inquiries   │
├─────────────┤     ├─────────────┤     ├─────────────┤
│ id          │     │ id          │     │ id          │
│ email       │     │ title       │     │ property_id │
│ password    │     │ description │     │ user_id     │
│ name        │     │ price       │     │ name        │
│ phone       │     │ area        │     │ email       │
│ role        │     │ bedrooms    │     │ phone       │
│ created_at  │     │ bathrooms   │     │ message     │
│ updated_at  │     │ location    │     │ type        │
└─────────────┘     │ status      │     │ status      │
                    │ type_id     │     │ created_at  │
                    │ images      │     └─────────────┘
                    │ features    │
                    │ created_at  │     ┌─────────────┐     ┌─────────────┐
                    └─────────────┘     │ maintenance │     │  tickets    │
                                        ├─────────────┤     ├─────────────┤
┌───────────────┐     ┌───────────────┤ id          │     │ id          │
│ property_types│     │ property_images ├─────────────┤     │ user_id     │
├───────────────┤     ├───────────────┤ user_id     │     │ subject     │
│ id            │     │ id          │     │ property_id │     │ description │
│ name          │     │ property_id │     │ title       │     │ priority    │
│ slug          │     │ image_url   │     │ description │     │ category    │
│ description   │     │ caption     │     │ priority    │     │ status      │
│ icon          │     │ is_primary  │     │ status      │     │ created_at  │
└───────────────┘     │ sort_order  │     │ created_at  │     └─────────────┘
                      └───────────────┘     │ updated_at  │
                                            └─────────────┘
┌─────────────────────┐
│ construction_updates│     ┌───────────────┐     ┌───────────────┐
├─────────────────────┤     │ contact_msgs  │     │ subscriptions │
│ id                  │     ├───────────────┤     ├───────────────┤
│ property_id         │     │ id          │     │ id          │
│ title               │     │ name        │     │ email       │
│ description         │     │ email       │     │ name        │
│ images              │     │ phone       │     │ status      │
│ date                │     │ subject     │     │ created_at  │
│ created_at          │     │ message     │     └───────────────┘
└─────────────────────┘     │ status      │
                            │ created_at  │     ┌───────────────┐
                            └───────────────┘     │ ticket_comms  │
                                                  ├───────────────┤
                                                  │ id          │
                                                  │ ticket_id   │
                                                  │ user_id     │
                                                  │ message     │
                                                  │ is_internal │
                                                  │ created_at  │
                                                  └───────────────┘
```

---

## 📝 SQL Schema

### Users Table

```sql
-- users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

### Property Types Table

```sql
-- property_types table
CREATE TABLE property_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO property_types (name, slug, description, icon) VALUES
('House', 'house', 'Single-family home', 'home'),
('Villa', 'villa', 'Luxury villa', 'villa'),
('Apartment', 'apartment', 'Apartment unit', 'building'),
('Plot', 'plot', 'Land plot', 'land'),
('Commercial', 'commercial', 'Commercial property', 'building'),
('Industrial', 'industrial', 'Industrial property', 'factory');
```

### Properties Table

```sql
-- properties table
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(15, 2) NOT NULL,
    area DECIMAL(10, 2),
    bedrooms INTEGER DEFAULT 0,
    bathrooms INTEGER DEFAULT 0,
    location VARCHAR(255) NOT NULL,
    property_type_id INTEGER REFERENCES property_types(id),
    status VARCHAR(50) DEFAULT 'available',
    images JSONB,
    features JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_properties_title ON properties(title);
CREATE INDEX idx_properties_price ON properties(price);
CREATE INDEX idx_properties_type ON properties(property_type_id);
CREATE INDEX idx_properties_status ON properties(status);
CREATE INDEX idx_properties_location ON properties(location);
```

### Property Images Table

```sql
-- property_images table
CREATE TABLE property_images (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
    image_url VARCHAR(500) NOT NULL,
    caption VARCHAR(255),
    is_primary BOOLEAN DEFAULT false,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_property_images_property ON property_images(property_id);
```

### Inquiries Table

```sql
-- inquiries table
CREATE TABLE inquiries (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id) ON DELETE SET NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    message TEXT,
    inquiry_type VARCHAR(50) DEFAULT 'general',
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_inquiries_property ON inquiries(property_id);
CREATE INDEX idx_inquiries_user ON inquiries(user_id);
CREATE INDEX idx_inquiries_status ON inquiries(status);
```

### Maintenance Requests Table

```sql
-- maintenance_requests table
CREATE TABLE maintenance_requests (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id) ON DELETE SET NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    priority VARCHAR(50) DEFAULT 'medium',
    status VARCHAR(50) DEFAULT 'pending',
    assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_maintenance_property ON maintenance_requests(property_id);
CREATE INDEX idx_maintenance_user ON maintenance_requests(user_id);
CREATE INDEX idx_maintenance_status ON maintenance_requests(status);
CREATE INDEX idx_maintenance_priority ON maintenance_requests(priority);
```

### Construction Updates Table

```sql
-- construction_updates table
CREATE TABLE construction_updates (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    images JSONB,
    update_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_construction_property ON construction_updates(property_id);
CREATE INDEX idx_construction_date ON construction_updates(update_date);
```

### Contact Messages Table

```sql
-- contact_messages table
CREATE TABLE contact_messages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    subject VARCHAR(255),
    message TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_contact_status ON contact_messages(status);
```

### Subscriptions Table

```sql
-- subscriptions table
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_subscriptions_status ON subscriptions(status);
```

### Support Tickets Table

```sql
-- support_tickets table
CREATE TABLE support_tickets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    subject VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    priority VARCHAR(50) DEFAULT 'medium',
    category VARCHAR(100),
    status VARCHAR(50) DEFAULT 'open',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tickets_user ON support_tickets(user_id);
CREATE INDEX idx_tickets_status ON support_tickets(status);
CREATE INDEX idx_tickets_priority ON support_tickets(priority);
```

### Ticket Comments Table

```sql
-- ticket_comments table
CREATE TABLE ticket_comments (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER REFERENCES support_tickets(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    message TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ticket_comments_ticket ON ticket_comments(ticket_id);
```

---

## 🗄️ Migration Files

### Initial Migration

Create `database/migrations/versions/001_initial_schema.py`:

```python
"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2026-02-22

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create property_types table
    op.create_table('property_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    
    # Insert default property types
    op.execute("""
        INSERT INTO property_types (name, slug, description, icon) VALUES
        ('House', 'house', 'Single-family home', 'home'),
        ('Villa', 'villa', 'Luxury villa', 'villa'),
        ('Apartment', 'apartment', 'Apartment unit', 'building'),
        ('Plot', 'plot', 'Land plot', 'land'),
        ('Commercial', 'commercial', 'Commercial property', 'building'),
        ('Industrial', 'industrial', 'Industrial property', 'factory')
    """)
    
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Create properties table
    op.create_table('properties',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('price', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('area', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('bedrooms', sa.Integer(), nullable=True),
        sa.Column('bathrooms', sa.Integer(), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=False),
        sa.Column('property_type_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('images', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('features', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create property_images table
    op.create_table('property_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('property_id', sa.Integer(), nullable=True),
        sa.Column('image_url', sa.String(length=500), nullable=False),
        sa.Column('caption', sa.String(length=255), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create inquiries table
    op.create_table('inquiries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('property_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('inquiry_type', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create maintenance_requests table
    op.create_table('maintenance_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('property_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('priority', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('assigned_to', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create construction_updates table
    op.create_table('construction_updates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('property_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('images', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('update_date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create contact_messages table
    op.create_table('contact_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('subject', sa.String(length=255), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create subscriptions table
    op.create_table('subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Create support_tickets table
    op.create_table('support_tickets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('subject', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('priority', sa.String(length=50), nullable=True),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create ticket_comments table
    op.create_table('ticket_comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticket_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_internal', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['ticket_id'], ['support_tickets.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_role', 'users', ['role'])
    op.create_index('idx_properties_title', 'properties', ['title'])
    op.create_index('idx_properties_price', 'properties', ['price'])
    op.create_index('idx_properties_type', 'properties', ['property_type_id'])
    op.create_index('idx_properties_status', 'properties', ['status'])
    op.create_index('idx_properties_location', 'properties', ['location'])
    op.create_index('idx_property_images_property', 'property_images', ['property_id'])
    op.create_index('idx_inquiries_property', 'inquiries', ['property_id'])
    op.create_index('idx_inquiries_user', 'inquiries', ['user_id'])
    op.create_index('idx_inquiries_status', 'inquiries', ['status'])
    op.create_index('idx_maintenance_property', 'maintenance_requests', ['property_id'])
    op.create_index('idx_maintenance_user', 'maintenance_requests', ['user_id'])
    op.create_index('idx_maintenance_status', 'maintenance_requests', ['status'])
    op.create_index('idx_maintenance_priority', 'maintenance_requests', ['priority'])
    op.create_index('idx_construction_property', 'construction_updates', ['property_id'])
    op.create_index('idx_construction_date', 'construction_updates', ['update_date'])
    op.create_index('idx_contact_status', 'contact_messages', ['status'])
    op.create_index('idx_subscriptions_status', 'subscriptions', ['status'])
    op.create_index('idx_tickets_user', 'support_tickets', ['user_id'])
    op.create_index('idx_tickets_status', 'support_tickets', ['status'])
    op.create_index('idx_tickets_priority', 'support_tickets', ['priority'])
    op.create_index('idx_ticket_comments_ticket', 'ticket_comments', ['ticket_id'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_ticket_comments_ticket', table_name='ticket_comments')
    op.drop_index('idx_tickets_priority', table_name='support_tickets')
    op.drop_index('idx_tickets_status', table_name='support_tickets')
    op.drop_index('idx_tickets_user', table_name='support_tickets')
    op.drop_index('idx_subscriptions_status', table_name='subscriptions')
    op.drop_index('idx_contact_status', table_name='contact_messages')
    op.drop_index('idx_construction_date', table_name='construction_updates')
    op.drop_index('idx_construction_property', table_name='construction_updates')
    op.drop_index('idx_maintenance_priority', table_name='maintenance_requests')
    op.drop_index('idx_maintenance_status', table_name='maintenance_requests')
    op.drop_index('idx_maintenance_user', table_name='maintenance_requests')
    op.drop_index('idx_maintenance_property', table_name='maintenance_requests')
    op.drop_index('idx_inquiries_status', table_name='inquiries')
    op.drop_index('idx_inquiries_user', table_name='inquiries')
    op.drop_index('idx_inquiries_property', table_name='inquiries')
    op.drop_index('idx_property_images_property', table_name='property_images')
    op.drop_index('idx_properties_location', table_name='properties')
    op.drop_index('idx_properties_status', table_name='properties')
    op.drop_index('idx_properties_type', table_name='properties')
    op.drop_index('idx_properties_price', table_name='properties')
    op.drop_index('idx_properties_title', table_name='properties')
    op.drop_index('idx_users_role', table_name='users')
    op.drop_index('idx_users_email', table_name='users')
    
    # Drop tables
    op.drop_table('ticket_comments')
    op.drop_table('support_tickets')
    op.drop_table('subscriptions')
    op.drop_table('contact_messages')
    op.drop_table('construction_updates')
    op.drop_table('maintenance_requests')
    op.drop_table('inquiries')
    op.drop_table('property_images')
    op.drop_table('properties')
    op.drop_table('users')
    op.drop_table('property_types')
```

---

## 📊 Seed Data

### Create Seed Script

Create `database/seed_data/seed_initial.py`:

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import PropertyType, User, Property, Inquiry, MaintenanceRequest, Ticket

DATABASE_URL = "postgresql://propertism_user:your_password@localhost:5432/propertism_dev"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_database():
    db = SessionLocal()
    
    # Seed property types
    property_types = [
        {"name": "House", "slug": "house", "description": "Single-family home", "icon": "home"},
        {"name": "Villa", "slug": "villa", "description": "Luxury villa", "icon": "villa"},
        {"name": "Apartment", "slug": "apartment", "description": "Apartment unit", "icon": "building"},
        {"name": "Plot", "slug": "plot", "description": "Land plot", "icon": "land"},
        {"name": "Commercial", "slug": "commercial", "description": "Commercial property", "icon": "building"},
        {"name": "Industrial", "slug": "industrial", "description": "Industrial property", "icon": "factory"},
    ]
    
    for pt in property_types:
        db.add(PropertyType(**pt))
    
    db.commit()
    print("✅ Property types seeded")
    
    # Seed admin user
    admin = User(
        email="admin@propertism.com",
        name="Admin User",
        phone="+91 9876543210",
        role="admin",
        is_active=True
    )
    admin.password_hash = "hashed_password_here"  # Use get_password_hash()
    db.add(admin)
    
    db.commit()
    print("✅ Admin user seeded")
    
    db.close()
    print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
```

---

## ✅ Verification Checklist

After completing all steps, verify:

- [ ] All tables created successfully
- [ ] All indexes created
- [ ] Foreign key relationships working
- [ ] Seed data inserted
- [ ] Database connection working
- [ ] Alembic migrations working

---

## 🎯 Next Steps

Once database is ready:

1. **Create SQLAlchemy models** - Map tables to Python classes
2. **Create Pydantic schemas** - Define API request/response models
3. **Begin backend development** - Implement API endpoints

---

**Database Design Complete! Ready to start backend development. 🚀**
