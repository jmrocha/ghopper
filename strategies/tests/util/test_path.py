from ervin.util.path import Path
from unittest import TestCase, skip


class TestPath(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()

    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        pass

    @skip
    def test_glob(self):
        perf_a = f"{self.results_dir}/benchmark1.perf"
        perf_b = f"{self.results_dir}/benchmark2.perf"
        expected_files = set([perf_a, perf_b])
        files = Path(self.results_dir).glob("*.perf")
        actual_files = set(files)
        self.assertEqual(expected_files, actual_files)
