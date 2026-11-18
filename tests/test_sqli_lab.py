import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lab"))
import app as lab_app

class SQLInjectionLabTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "test.sqlite3"
        lab_app.initialize_database(self.db)

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_demo_credentials(self):
        self.assertTrue(lab_app.authenticate_vulnerable("aluno", "dio123", self.db))
        self.assertTrue(lab_app.authenticate_secure("aluno", "dio123", self.db))

    def test_wrong_password_is_rejected(self):
        self.assertFalse(lab_app.authenticate_vulnerable("aluno", "errada", self.db))
        self.assertFalse(lab_app.authenticate_secure("aluno", "errada", self.db))

    def test_demo_sqli_input_bypasses_only_vulnerable_query(self):
        payload = "' OR '1'='1' -- "
        self.assertTrue(lab_app.authenticate_vulnerable(payload, "", self.db))
        self.assertFalse(lab_app.authenticate_secure(payload, "", self.db))

if __name__ == "__main__":
    unittest.main()
