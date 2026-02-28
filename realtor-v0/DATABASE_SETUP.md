# Database Setup Guide

## Prerequisites

Before running migrations, ensure PostgreSQL is installed and running.

## Step 1: Start PostgreSQL

### Option A: Using XAMPP
1. Open XAMPP Control Panel
2. Start MySQL (PostgreSQL is not included in XAMPP)
3. For PostgreSQL, download and install separately

### Option B: Install PostgreSQL
1. Download from: https://www.postgresql.org/download/windows/
2. Install PostgreSQL 15+
3. Start the PostgreSQL service

## Step 2: Create Database

### Using psql command line:
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE realtor_db;

# Create user
CREATE USER realtor_user WITH PASSWORD 'realtor_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE realtor_db TO realtor_user;

# Exit
\q
```

### Using pgAdmin:
1. Open pgAdmin
2. Right-click "Databases" → Create → Database
3. Name: `realtor_db`
4. Right-click "Users/Groups" → Create → Role
5. Name: `realtor_user`, Password: `realtor_password`
6. Grant privileges to `realtor_db`

## Step 3: Verify Connection

Test the database connection:
```bash
psql -U realtor_user -d realtor_db -h localhost
```

## Step 4: Run Migrations

Once database is ready:
```bash
cd C:\tamil\realtor
python manage.py makemigrations
python manage.py migrate
```

## Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

## Troubleshooting

### Error: "could not connect to server"
- PostgreSQL is not running
- Start PostgreSQL service

### Error: "database does not exist"
- Create the database first (Step 2)

### Error: "password authentication failed"
- Verify password in settings.py matches
- Reset password if needed

### Error: "FATAL: Peer authentication failed"
- Edit `pg_hba.conf` and change method to `md5`
- Restart PostgreSQL
