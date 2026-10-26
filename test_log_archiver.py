import gzip
import os
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main


class TestArchiver(unittest.TestCase):
    def _make(self, d, name, age_days):
        p = os.path.join(d, name)
        open(p, "w").write("log line\n")
        old = time.time() - age_days * 86400
        os.utime(p, (old, old))
        return p

    def test_dry_run_changes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._make(d, "old.log", 40)
            self.assertEqual(main.find_old(d, 30), [p])
            main.archive([p], dry_run=True)
            self.assertFalse(os.path.exists(p + ".gz"))

    def test_apply_creates_gz_and_keeps_original_by_default(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._make(d, "old.log", 40)
            main.archive([p], dry_run=False)
            self.assertTrue(os.path.exists(p + ".gz"))
            self.assertEqual(gzip.open(p + ".gz", "rt").read(), "log line\n")
            self.assertTrue(os.path.exists(p))

    def test_recent_file_not_selected(self):
        with tempfile.TemporaryDirectory() as d:
            self._make(d, "new.log", 1)
            self.assertEqual(main.find_old(d, 30), [])


if __name__ == "__main__":
    unittest.main()
