import unittest
from patchparser import github_parser_local as gpl
import pandas as pd


class TestGitHubPatchParserLocal(unittest.TestCase):

    def test_locally_cloned_repo(self):
        """
        Testing GitHub Parser for a locally cloned repository
        Example commit: https://github.com/tdunlap607/patchparser/commit/0dfe5bacc3833160dbe3ea9edf49cd7d599ad290
        """
        parsed = gpl.commit_local(repo_owner="tdunlap607",
                                  repo_name="patchparser",
                                  sha="0dfe5bacc3833160dbe3ea9edf49cd7d599ad290",
                                  base_repo_path="./")

        # Sample test
        original = gpl.commit_local(repo_owner="gofiber",
                                    repo_name="fiber",
                                    sha="b50d91d58ecdff2a330bf07950244b6c4caf65b1",
                                    base_repo_path="./../../test_clone_repo/gofiber/fiber/")

        original = pd.DataFrame(original)

        new = gpl.commit_local_updated(repo_owner="gofiber",
                                       repo_name="fiber",
                                       sha="b50d91d58ecdff2a330bf07950244b6c4caf65b1",
                                       base_repo_path="./../../test_clone_repo/gofiber/fiber/")

        new = pd.DataFrame(new)
        """Expecting 5 changes from the above commit"""
        self.assertEqual(len(parsed), 5)


if __name__ == '__main__':
    unittest.main()
