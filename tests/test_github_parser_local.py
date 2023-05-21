import unittest
from patchparser import github_parser_local as gpl

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
        
        
        """Expecting 5 changes from the above commit"""
        self.assertEqual(len(parsed), 5)


if __name__ == '__main__':
    unittest.main()
