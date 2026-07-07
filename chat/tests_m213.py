"""
chat/tests_m213.py — M2.13 Conversation Orchestration Test Suite.
Tests: sequential model IDs, orchestrator execution sequence, isolated stage failures,
       metrics timings, and REST API views.

Run with:
    .\\scripts\\django.cmd test chat.tests_m213
"""
import json
import uuid
from unittest.mock import patch
from django.test import TestCase
from chat.models import OrchestrationWorkflow, WorkflowExecutionStep, RealBotSession
from chat.orchestrator import ConversationOrchestrator


# ─────────────────────────────────────────────────────────────────────────────
# 1. Model & Registry Tests
# ─────────────────────────────────────────────────────────────────────────────

class OrchestratorModelTests(TestCase):

    def test_workflow_id_auto_generated_sequentially(self):
        w1 = OrchestrationWorkflow.objects.create(session_id='session1')
        w2 = OrchestrationWorkflow.objects.create(session_id='session2')
        self.assertEqual(w1.workflow_id, 'WF000001')
        self.assertEqual(w2.workflow_id, 'WF000002')

    def test_step_id_auto_generated_sequentially(self):
        wf = OrchestrationWorkflow.objects.create(session_id='session')
        s1 = WorkflowExecutionStep.objects.create(workflow=wf, stage='Stage1', status='success')
        s2 = WorkflowExecutionStep.objects.create(workflow=wf, stage='Stage2', status='success')
        self.assertEqual(s1.step_id, 'WFS000001')
        self.assertEqual(s2.step_id, 'WFS000002')


# ─────────────────────────────────────────────────────────────────────────────
# 2. Pipeline sequence & isolated failure tests
# ─────────────────────────────────────────────────────────────────────────────

class PipelineExecutionTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())
        self.orch = ConversationOrchestrator()

    def test_orchestration_executes_stages_in_order(self):
        res = self.orch.process_message(
            session_id=str(self.session.session_id),
            message_text="hello"
        )
        self.assertEqual(res['state'], 'Completed')
        
        # Verify 15 stages were recorded in order
        steps = WorkflowExecutionStep.objects.filter(workflow__workflow_id=res['workflow_id']).order_by('created_at')
        self.assertEqual(steps.count(), 15)
        self.assertEqual(steps[0].stage, 'Security Validation')
        self.assertEqual(steps[14].stage, 'Workflow Completion')

    def test_isolated_failure_allows_pipeline_to_complete(self):
        # Mock rule engine stage to crash with exception
        with patch('chat.rule_engine.RuleEngine.evaluate', side_effect=Exception("Rule engine failure")):
            res = self.orch.process_message(
                session_id=str(self.session.session_id),
                message_text="hello"
            )
            # The workflow completes successfully instead of returning a server 500 error
            self.assertEqual(res['state'], 'Completed')
            
            # Rule Engine step status must be 'failed'
            step = WorkflowExecutionStep.objects.get(workflow__workflow_id=res['workflow_id'], stage='Rule Engine')
            self.assertEqual(step.status, 'failed')
            self.assertIn("Rule engine failure", step.logs)


# ─────────────────────────────────────────────────────────────────────────────
# 3. REST API Endpoint Tests
# ─────────────────────────────────────────────────────────────────────────────

class OrchestratorAPIEndpointTests(TestCase):

    def setUp(self):
        self.session = RealBotSession.objects.create(session_id=uuid.uuid4())
        self.orch = ConversationOrchestrator()

    def _post_json(self, url, data):
        return self.client.post(url, json.dumps(data), content_type='application/json')

    def test_message_gateway_endpoint(self):
        url = '/api/v1/realbot/inquiry/orchestrator/message/'
        payload = {
            'session_id': str(self.session.session_id),
            'message_text': 'hello',
            'page_path': '/home/',
            'category': 'General'
        }
        resp = self._post_json(url, payload)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertIn('reply_text', data['data'])

    def test_workflow_status_endpoint(self):
        res = self.orch.process_message(str(self.session.session_id), "hello")
        url = f'/api/v1/realbot/inquiry/orchestrator/status/?workflow_id={res["workflow_id"]}'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['state'], 'Completed')

    def test_workflow_trace_endpoint(self):
        res = self.orch.process_message(str(self.session.session_id), "hello")
        url = f'/api/v1/realbot/inquiry/orchestrator/trace/?workflow_id={res["workflow_id"]}'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['data']['trace']), 15)

    def test_workflow_analytics_endpoint(self):
        # Trigger execution
        self.orch.process_message(str(self.session.session_id), "hello")
        url = '/api/v1/realbot/inquiry/orchestrator/analytics/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['total_executions'], 1)
