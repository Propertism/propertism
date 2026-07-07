from django.db import connection

tables = [
    'chat_realbotsession',
    'chat_realbotmessage',
    'chat_businessrule',
    'chat_ruleexecutionlog',
    'chat_serviceprofile',
    'chat_inquiryconversationsession',
    'chat_inquiryconversationlog',
    'chat_suggestiondefinition',
    'chat_suggestioninteractionlog',
    'chat_actiondefinition',
    'chat_actionexecutionlog',
    'chat_responsecomponent',
    'chat_responsecompositionlog',
    'chat_conversationcontext',
    'chat_contextupdatelog',
    'chat_metricaggregate',
    'chat_platformevent',
    'chat_configurationitem',
    'chat_configurationauditlog',
    'chat_orchestrationworkflow',
    'chat_workflowexecutionstep',
    'chat_securityevent',
    'chat_securitypolicy',
    'chat_knowledgedocument',
    'chat_knowledgearticle',
    'chat_knowledgelifecycleauditlog',
    'chat_knowledgeversionhistory',
]

with connection.cursor() as cursor:
    # Disable foreign key checks for dropping tables in sqlite
    cursor.execute("PRAGMA foreign_keys = OFF")
    for table in tables:
        print(f"Dropping table {table} if exists...")
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    cursor.execute("PRAGMA foreign_keys = ON")
    
    print("Deleting migration history for chat app (beyond 0003_initial)...")
    cursor.execute(
        "DELETE FROM django_migrations WHERE app = 'chat' AND name NOT IN ('0001_initial', '0002_delete_chatmessage', '0003_initial')"
    )
print("Database chat app tables dropped and migrations cleared.")
