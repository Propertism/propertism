# 📡 Propertism Backend API Specification

**Version**: 1.0.0  
**Base URL**: `https://api.propertism.com/api/v1`  
**Authentication**: Bearer Token (JWT)

---

## 📚 Table of Contents

- [Authentication](#authentication)
- [Properties](#properties)
- [Inquiries](#inquiries)
- [Maintenance Requests](#maintenance-requests)
- [Construction Updates](#construction-updates)
- [Contact Messages](#contact-messages)
- [Subscriptions](#subscriptions)
- [Support Tickets](#support-tickets)
- [Error Handling](#error-handling)

---

## 🔐 Authentication

### Register User

```
POST /api/v1/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "strongpassword123",
  "name": "John Doe",
  "phone": "+91 9876543210"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+91 9876543210",
  "role": "user",
  "created_at": "2026-02-22T10:00:00Z"
}
```

### Login

```
POST /api/v1/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "strongpassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user"
  }
}
```

### Get Current User

```
GET /api/v1/auth/me
Headers: Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+91 9876543210",
  "role": "user",
  "created_at": "2026-02-22T10:00:00Z"
}
```

---

## 🏠 Properties

### List Properties

```
GET /api/v1/properties
```

**Query Parameters:**
- `page` (default: 1)
- `limit` (default: 20)
- `property_type` (optional)
- `min_price` (optional)
- `max_price` (optional)
- `location` (optional)
- `bedrooms` (optional)

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Luxury Villa in Chennai",
      "description": "Beautiful luxury villa...",
      "price": 5000000,
      "area": 2500,
      "bedrooms": 4,
      "bathrooms": 3,
      "location": "Chennai, Tamil Nadu",
      "property_type": "villa",
      "status": "available",
      "images": [
        {
          "id": 1,
          "url": "/images/villa1.jpg",
          "is_primary": true
        }
      ],
      "created_at": "2026-02-20T10:00:00Z"
    }
  ],
  "total": 15,
  "page": 1,
  "limit": 20
}
```

### Get Property Details

```
GET /api/v1/properties/{id}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Luxury Villa in Chennai",
  "description": "Beautiful luxury villa...",
  "price": 5000000,
  "area": 2500,
  "bedrooms": 4,
  "bathrooms": 3,
  "location": "Chennai, Tamil Nadu",
  "property_type": "villa",
  "status": "available",
  "features": ["swimming_pool", "garden", "security"],
  "images": [
    {
      "id": 1,
      "url": "/images/villa1.jpg",
      "caption": "Front View",
      "is_primary": true
    }
  ],
  "created_at": "2026-02-20T10:00:00Z"
}
```

### Create Property (Admin)

```
POST /api/v1/properties
Headers: Authorization: Bearer <admin_token>
```

**Request Body:**
```json
{
  "title": "New Property",
  "description": "Property description",
  "price": 3000000,
  "area": 1500,
  "bedrooms": 3,
  "bathrooms": 2,
  "location": "Coimbatore, Tamil Nadu",
  "property_type": "house",
  "status": "available",
  "features": ["parking", "garden"]
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "title": "New Property",
  "description": "Property description",
  "price": 3000000,
  "created_at": "2026-02-22T12:00:00Z"
}
```

---

## 📩 Inquiries

### Create Inquiry

```
POST /api/v1/inquiries
```

**Request Body:**
```json
{
  "property_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91 9876543210",
  "message": "I'm interested in this property",
  "inquiry_type": "purchase"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "property_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91 9876543210",
  "message": "I'm interested in this property",
  "inquiry_type": "purchase",
  "status": "pending",
  "created_at": "2026-02-22T14:00:00Z"
}
```

### List User Inquiries

```
GET /api/v1/inquiries
Headers: Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "property_id": 1,
      "property_title": "Luxury Villa in Chennai",
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+91 9876543210",
      "message": "I'm interested in this property",
      "inquiry_type": "purchase",
      "status": "pending",
      "created_at": "2026-02-22T14:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 20
}
```

---

## 🔧 Maintenance Requests

### Create Maintenance Request

```
POST /api/v1/maintenance
```

**Request Body:**
```json
{
  "property_id": 1,
  "title": "Leaking Faucet",
  "description": "Kitchen faucet is leaking",
  "priority": "medium"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "property_id": 1,
  "title": "Leaking Faucet",
  "description": "Kitchen faucet is leaking",
  "priority": "medium",
  "status": "pending",
  "created_at": "2026-02-22T15:00:00Z"
}
```

### List User Maintenance Requests

```
GET /api/v1/maintenance
Headers: Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "property_id": 1,
      "property_title": "Luxury Villa in Chennai",
      "title": "Leaking Faucet",
      "description": "Kitchen faucet is leaking",
      "priority": "medium",
      "status": "pending",
      "created_at": "2026-02-22T15:00:00Z"
    }
  ],
  "total": 1
}
```

---

## 🏗️ Construction Updates

### List Construction Updates

```
GET /api/v1/construction-updates
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "property_id": 1,
      "property_title": "Luxury Villa in Chennai",
      "title": "Foundation Complete",
      "description": "Foundation work completed successfully",
      "images": ["/images/foundation.jpg"],
      "date": "2026-02-15",
      "created_at": "2026-02-15T10:00:00Z"
    }
  ],
  "total": 5
}
```

---

## 📞 Contact Messages

### Send Contact Message

```
POST /api/v1/contact
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91 9876543210",
  "subject": "Inquiry about property",
  "message": "I have a question about your properties"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91 9876543210",
  "subject": "Inquiry about property",
  "message": "I have a question about your properties",
  "status": "pending",
  "created_at": "2026-02-22T16:00:00Z"
}
```

---

## 📧 Subscriptions

### Subscribe

```
POST /api/v1/subscriptions
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "john@example.com",
  "name": "John Doe",
  "status": "active",
  "created_at": "2026-02-22T17:00:00Z"
}
```

### List Subscribers (Admin)

```
GET /api/v1/subscriptions
Headers: Authorization: Bearer <admin_token>
```

---

## 🎫 Support Tickets

### Create Ticket

```
POST /api/v1/tickets
```

**Request Body:**
```json
{
  "subject": "Payment issue",
  "description": "I'm having trouble with payment",
  "priority": "high",
  "category": "billing"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "subject": "Payment issue",
  "description": "I'm having trouble with payment",
  "priority": "high",
  "category": "billing",
  "status": "open",
  "created_at": "2026-02-22T18:00:00Z"
}
```

### List User Tickets

```
GET /api/v1/tickets
Headers: Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": 1,
      "subject": "Payment issue",
      "description": "I'm having trouble with payment",
      "priority": "high",
      "category": "billing",
      "status": "open",
      "created_at": "2026-02-22T18:00:00Z"
    }
  ],
  "total": 1
}
```

### Add Ticket Comment

```
POST /api/v1/tickets/{id}/comments
```

**Request Body:**
```json
{
  "message": "Please check my payment status"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "ticket_id": 1,
  "message": "Please check my payment status",
  "is_internal": false,
  "created_at": "2026-02-22T19:00:00Z"
}
```

---

## ⚠️ Error Handling

### 400 Bad Request
```json
{
  "error": "validation_error",
  "message": "Invalid input data",
  "details": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

### 401 Unauthorized
```json
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "error": "forbidden",
  "message": "You don't have permission to access this resource"
}
```

### 404 Not Found
```json
{
  "error": "not_found",
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "internal_error",
  "message": "An unexpected error occurred"
}
```

---

## 📝 Notes

- All timestamps are in ISO 8601 format (UTC)
- Pagination uses `page` and `limit` query parameters
- Authentication is required for protected endpoints
- Admin endpoints require admin role
- File uploads use multipart/form-data

---

**API Version**: v1  
**Last Updated**: February 22, 2026
