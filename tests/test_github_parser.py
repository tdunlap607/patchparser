import unittest
from patchparser import github_parser as gp


class TestGitHubPatchParser(unittest.TestCase):

    def test_commit(self):
        """
        Testing GitHub Parser for a given commit
        Associated CVE: https://nvd.nist.gov/vuln/detail/CVE-2021-4118
        Example commit: https://github.com/Lightning-AI/lightning/commit/62f1e82e032eb16565e676d39e0db0cac7e34ace
        """
        parsed = gp.commit(repo_owner="Lightning-AI",
                           repo_name="lightning",
                           sha="62f1e82e032eb16565e676d39e0db0cac7e34ace")
                
        """Expecting 5 changes from the above commit"""
        self.assertEqual(len(parsed), 5)


if __name__ == '__main__':
    unittest.main()
