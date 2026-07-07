"""
Migration 0018 — M2.14 Security, Authorization & Platform Governance.
Creates SecurityEvent and SecurityPolicy models.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0017_orchestrationworkflow_workflowexecutionstep'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityEvent',
            fields=[
                ('event_id', models.CharField(editable=False, max_length=20, primary_key=True, serialize=False, unique=True)),
                ('event_type', models.CharField(choices=[
                    ('session_started', 'Session Started'),
                    ('session_terminated', 'Session Terminated'),
                    ('invalid_request', 'Invalid Request'),
                    ('authorization_failure', 'Authorization Failure'),
                    ('policy_violation', 'Policy Violation'),
                    ('rate_limit_triggered', 'Rate Limit Triggered'),
                    ('abuse_detected', 'Abuse Detected'),
                    ('configuration_access', 'Configuration Access'),
                    ('administrative_change', 'Administrative Change'),
                    ('security_exception', 'Security Exception'),
                ], max_length=30)),
                ('severity', models.CharField(choices=[('info', 'Info'), ('warning', 'Warning'), ('critical', 'Critical')], default='info', max_length=10)),
                ('source_ip', models.CharField(blank=True, default='', max_length=50)),
                ('session_id', models.CharField(blank=True, default='', max_length=50)),
                ('request_path', models.CharField(blank=True, default='', max_length=500)),
                ('details', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SecurityPolicy',
            fields=[
                ('policy_id', models.CharField(editable=False, max_length=20, primary_key=True, serialize=False, unique=True)),
                ('policy_key', models.CharField(max_length=100, unique=True)),
                ('domain', models.CharField(choices=[
                    ('session', 'Session Security'),
                    ('request', 'Request Validation'),
                    ('input', 'Input Validation'),
                    ('output', 'Output Validation'),
                    ('configuration', 'Configuration Security'),
                    ('workflow', 'Workflow Security'),
                    ('action', 'Action Authorization'),
                    ('navigation', 'Navigation Security'),
                    ('inquiry', 'Inquiry Protection'),
                    ('analytics', 'Analytics Protection'),
                    ('admin', 'Administrative Security'),
                    ('api', 'API Security'),
                ], max_length=20)),
                ('policy_type', models.CharField(choices=[
                    ('limit', 'Limit'),
                    ('threshold', 'Threshold'),
                    ('rule', 'Rule'),
                    ('validation', 'Validation'),
                ], max_length=20)),
                ('value', models.TextField()),
                ('default_value', models.TextField(blank=True, default='')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
