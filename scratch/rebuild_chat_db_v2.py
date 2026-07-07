from django.db import connection

with connection.cursor() as cursor:
    # Disable foreign key checks
    cursor.execute("PRAGMA foreign_keys = OFF")
    
    # Query all tables starting with chat_
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'chat_%'")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        print(f"Dropping table {table}...")
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
        
    cursor.execute("PRAGMA foreign_keys = ON")
    
    print("Deleting migration history for chat app (beyond 0003_initial)...")
    cursor.execute(
        "DELETE FROM django_migrations WHERE app = 'chat' AND name NOT IN ('0001_initial', '0002_delete_chatmessage', '0003_initial')"
    )
print("Database chat app tables dropped and migrations cleared completely.")
