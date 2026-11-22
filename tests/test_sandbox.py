import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import sandbox


class SandboxPathTests(unittest.TestCase):
    def test_rejects_absolute_and_parent_paths(self):
        for path in ("../main.tf", "/workspace/main.tf", "dir/../main.tf"):
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    sandbox._safe_workspace_path(path)

    def test_accepts_relative_workspace_path(self):
        self.assertEqual(
            sandbox._safe_workspace_path("nested/main.tf"),
            "nested/main.tf",
        )

    def test_rejects_empty_command_without_docker_call(self):
        with patch("sandbox.subprocess.run") as run:
            result = sandbox.run_command("")

        self.assertEqual(result["exit_code"], -1)
        run.assert_not_called()

    def test_rejects_escape_before_write(self):
        with patch("sandbox.subprocess.run") as run:
            result = sandbox.write_file("../main.tf", "content")

        self.assertEqual(result["exit_code"], 1)
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
