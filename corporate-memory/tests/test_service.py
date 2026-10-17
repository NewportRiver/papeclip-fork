import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

from corporate_memory import AuthorizationError, CorporateMemoryService, ValidationError


class CorporateMemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "memory.sqlite3"

    def tearDown(self):
        self.tmp.cleanup()

    def make_service(self, role="employee", actor="hermes-01", path=None):
        return CorporateMemoryService(path or self.path, actor, role)

    def propose(self, service, **overrides):
        values = dict(title="Engineering SOP", body="Use evidence-backed tests and rollback.", domain="Engineering", scope="Corporate", classification="Internal", owner="Technology Department", source="HERMES_ENGINEERING_GUIDE.md", rationale="Approved SOP foundation")
        values.update(overrides)
        return service.propose(**values)

    def test_migration_health_and_approval_visibility(self):
        service = self.make_service()
        self.assertTrue(service.health()["ok"])
        proposal = self.propose(service)
        self.assertEqual(service.search("Engineering"), [])
        reviewer = self.make_service("reviewer", "cto")
        self.assertEqual(reviewer.review(proposal, "approve")["status"], "Approved")
        self.assertEqual(service.search("Engineering")[0]["status"], "Approved")
        service.close(); reviewer.close()

    def test_employee_cannot_review_and_private_content_is_rejected(self):
        service = self.make_service()
        proposal = self.propose(service)
        with self.assertRaises(AuthorizationError):
            service.review(proposal, "approve")
        with self.assertRaises(ValidationError):
            self.propose(service, body="Store the API key in shared memory.")
        service.close()

    def test_only_approved_proposals_can_publish(self):
        service = self.make_service("publisher", "cto")
        proposal = self.propose(service)
        with self.assertRaises(AuthorizationError):
            service.publish(proposal)
        service.review(proposal, "approve")
        self.assertEqual(service.publish(proposal)["status"], "Published")
        service.close()

    def test_backup_and_clean_restore(self):
        service = self.make_service("admin", "memory-admin")
        proposal = self.propose(service)
        service.review(proposal, "approve")
        backup = Path(self.tmp.name) / "backup.sqlite3"
        service.backup(backup)
        restored = self.make_service("employee", "reader", backup)
        self.assertEqual(restored.search("Engineering")[0]["title"], "Engineering SOP")
        self.assertTrue(restored.health()["ok"])
        service.close(); restored.close()

    def test_mcp_stdio_exposes_tools(self):
        env = os.environ.copy()
        env.update({"PYTHONPATH": str(Path(__file__).parents[1] / "src"), "CORPORATE_MEMORY_DB": str(Path(self.tmp.name) / "mcp.sqlite3"), "CORPORATE_MEMORY_TOKENS_JSON": json.dumps({"t": {"actor": "hermes-01", "role": "employee"}}), "CORPORATE_MEMORY_ACCESS_TOKEN": "t"})
        proc = subprocess.Popen([sys.executable, "-m", "corporate_memory.mcp_stdio"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, env=env)
        assert proc.stdin is not None and proc.stdout is not None
        proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}) + "\n")
        proc.stdin.flush()
        response = json.loads(proc.stdout.readline())
        self.assertGreaterEqual({tool["name"] for tool in response["result"]["tools"]}, {"search_knowledge", "propose_knowledge", "review_knowledge"})
        proc.terminate(); proc.wait(timeout=5)
        proc.stdin.close(); proc.stdout.close()

    def test_concurrent_proposals_do_not_corrupt_database(self):
        errors = []

        def worker(index):
            try:
                service = self.make_service("employee", f"agent-{index}")
                self.propose(service, title=f"Concurrent SOP {index}")
                service.close()
            except Exception as exc:  # pragma: no cover - assertion below reports it
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(index,)) for index in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(errors, [])
        verifier = self.make_service()
        self.assertEqual(verifier.db.execute("SELECT COUNT(*) FROM knowledge_records").fetchone()[0], 8)
        self.assertTrue(verifier.health()["ok"])
        verifier.close()


if __name__ == "__main__":
    unittest.main()
