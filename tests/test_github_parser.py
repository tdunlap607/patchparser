import unittest
from patchparser import github_parser as gp


class TestGitHubPatchParser(unittest.TestCase):

    def test_github_api(self):
        """
        Testing GitHub Parser for a given commit by using the GitHub API
        Example commit: https://github.com/tdunlap607/patchparser/commit/0dfe5bacc3833160dbe3ea9edf49cd7d599ad290
        """
        parsed = gp.commit(repo_owner="tdunlap607",
                           repo_name="patchparser",
                           sha="0dfe5bacc3833160dbe3ea9edf49cd7d599ad290")
                
        """Expecting 5 changes from the above commit"""
        self.assertEqual(len(parsed), 5)


if __name__ == '__main__':
    unittest.main()
