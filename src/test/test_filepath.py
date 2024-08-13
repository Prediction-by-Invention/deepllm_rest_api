import unittest
from pathlib import Path

from src.deepllm.util.file_path_util import FilePathUtil

SRC_ROOT = "deep_llm"


class TestFilePath(unittest.TestCase):
    def test_app_root_path(self) -> None:
        path = Path(FilePathUtil.app_root_path())
        self.assertTrue(path.is_dir())

    def test_api_spec_path(self) -> None:
        path = Path(FilePathUtil.api_spec_path())
        print(path)
        self.assertTrue(path.is_file())


if __name__ == "__main__":
    unittest.main()
