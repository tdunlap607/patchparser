import unittest
# from patchparser import github_parser as gp
from src.patchparser import github_parser_local


class TestGitHubPatchParser(unittest.TestCase):

    def test_commit(self):
        """
        Testing GitHub Parser for a given commit
        Associated CVE: https://nvd.nist.gov/vuln/detail/CVE-2021-4118
        Example commit: https://github.com/Lightning-AI/lightning/commit/62f1e82e032eb16565e676d39e0db0cac7e34ace
        """
        parsed = github_parser_local.commit(repo_owner="tdunlap607",
                                 repo_name="patchparser",
                                 sha="0dfe5bacc3833160dbe3ea9edf49cd7d599ad290",
                                 base_repo_path="./")
        
        # TODO: we need to add an appropriate test for this
        """Expecting 5 changes from the above commit"""
        self.assertEqual(len(parsed), 5)


if __name__ == '__main__':
    unittest.main()
