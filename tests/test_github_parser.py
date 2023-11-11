import unittest
from patchparser import github_parser as gp


class TestGitHubPatchParser(unittest.TestCase):

    def test_github_api(self):
        """
        Testing GitHub Parser for a given commit by using the GitHub API
        Example commit: https://github.com/tdunlap607/patchparser/commit/0dfe5bacc3833160dbe3ea9edf49cd7d599ad290
        """
        parsed = gp.commit(repo_owner="s3c2",
                           repo_name="vfcfinder",
                           sha="f573763decf499349721c48f11dc8299a91255d1",
                           verbose=True)

        """Expecting 5 changes from the above commit"""
        self.assertEqual(len(parsed), 9)


if __name__ == '__main__':
    unittest.main()
