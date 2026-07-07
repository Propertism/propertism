from django.db import connection

with connection.cursor() as cursor:
    print("Deleting all migration history for chat app...")
    cursor.execute("DELETE FROM django_migrations WHERE app = 'chat'")
print("All chat app migration history cleared.")
