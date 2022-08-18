# PatchParser
A python package to extract features from a commit patch.

Please note this repository is still in the initial development phase.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install patchparser
```

## Usage

```python
from patchparser import github_parser

if __name__ == '__main__':
    # Parse a given commit for a GitHub repository
    parsed = github_parser.commit(repo_owner="Lightning-AI",
                                  repo_name="lightning",
                                  sha="62f1e82e032eb16565e676d39e0db0cac7e34ace")
```

### Parsed Features

|Columns             |Type|Description                                                                                |
|--------------------|----|-------------------------------------------------------------------------------------------|
|repo_owner          |str |Repository Owner                                                                           |
|repo_name           |str |Repository Name                                                                           |
|sha                 |str |Target Commit SHA                                                                          |
|message             |str |Associated commit message                                                                  |
|file_name           |str |Name of file altered in patch                                                              |
|file_number         |int |File number in patch                                                                       |
|file_extension      |str |File extension                                                                             |
|total_files_changed |int |Number of files changed at commit                                                          |
|raw_file_patch      |str |The raw patch for the entire file                                                          |
|patch_number        |int |Patch instance                                                                             |
|total_patches       |int |Total number of patches per file                                                           |
|raw_patch_header    |str |Header of the patch (@@ -A,X +B,Y @@)                                                      |
|raw_patch           |str |The raw patch for a single patch                                                           |
|original_code       |str |The left side (parent commit state) of the git diff in GitHub. Raw code. -'s are stripped.  |
|original_line_start |int |Original line start number (@@ -**A**,X +B,Y @@)                                               |
|original_line_length|int |Original line end (@@ -A,**X** +B,Y @@)                                                        |
|original_line_end   |int |Original_line_start + original_line_length                                                 |
|modified_code       |str |The right side (target commit state) of the git diff in GitHub. Raw code. +'s are stripped.|
|modified_line_start |int |Modified line start number (@@ -A,X +**B**,Y @@)                                               |
|modified_line_length|int |Modified line end (@@ -A,X +B,**Y** @@)                                                        |
|modified_line_end   |int |Modified_line_start + modified_line_length                                                 |
|additions           |int |Added lines count in a patch                                                               |
|added_code          |str |Raw code added during patch                                                                |
|deletions           |int |Deleted lines count in a patch                                                             |
|deleted_code        |str |Raw code deleted during patch                                                              |
|changes             |int |additions + deletions                                                                      |
|status              |str |GitHub status tag at file level (e.g., modified)                                           |
|total_additions     |int |Total lines added for a file                                                               |
|total_deletions     |int |Total lines deleted for a file                                                             |
|total_changes       |int |Total lines changed for a file (total_additions + total_deletions) 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Unlicense](https://choosealicense.com/licenses/unlicense/)