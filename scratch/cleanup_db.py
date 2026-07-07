from django.db import connection

tables = [
    'chat_knowledgearticle',
    'chat_knowledgedocument',
    'chat_knowledgelifecycleauditlog',
    'chat_knowledgeversionhistory',
]

with connection.cursor() as cursor:
    for table in tables:
        print(f"Dropping table {table} if exists...")
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    
    migrations = [
        '0005_knowledge_article',
        '0006_add_knowledge_id',
        '0007_m23_knowledge_document',
        '0019_knowledge_admin_framework'
    ]
    
    print("Deleting migration history...")
    cursor.execute(
        "DELETE FROM django_migrations WHERE app = 'chat' AND name IN ('0005_knowledge_article', '0006_add_knowledge_id', '0007_m23_knowledge_document', '0019_knowledge_admin_framework')"
    )
print("Database cleanup complete.")
