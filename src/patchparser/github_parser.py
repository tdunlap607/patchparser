"""
Helper functions to load and process commit data from GitHub
"""
import re
import requests


class CommitParse:
    def __init__(self, repo_owner: str, repo_name: bool, sha: str) -> object:
        """Initialize a class to hold the data for parsing the commit data

        Args:
            repo_owner (str): Repo owner
            repo_name (str): Repo name
            sha (str): Target commit SHA

        Returns:
            object: CommitParse
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.sha = sha
        self.message = None
        self.file_name = None
        self.file_number = None
        self.file_extension = None
        self.total_files_changed = None
        self.raw_file_patch = None
        self.patch_number = None
        self.total_patches = None
        self.raw_patch_header = None
        self.raw_patch = None
        self.original_code = None
        self.original_line_start = None
        self.original_line_length = None
        self.original_line_end = None
        self.modified_code = None
        self.modified_line_start = None
        self.modified_line_length = None
        self.modified_line_end = None
        self.additions = None
        self.added_code = None
        self.deletions = None
        self.deleted_code = None
        self.changes = None
        self.status = None
        self.total_file_additions = None
        self.total_file_deletions = None
        self.total_file_changes = None


def parse_commit_info(commit_info: list, parsed_commit: CommitParse) -> list:
    """Parses the commit_info list

    Args:
        commit_info (list): commit_info list from original data
        parsed_commit (CommitParse): Set CommitParse class with basic info

    Returns:
        list: List of dictionaries with desired data for project
    """
    
    """Master list to hold information"""
    data = []
    
    total_files_changed = len(commit_info)
    
    """
    Enumerate through each row withiin commit_info. 
    A row represents changed files in the commit
    """
    for index, row in enumerate(commit_info):
        file_name = row["filename"]
        file_number = index
        file_extension = file_name.split(".")[-1]
        raw_file_patch = row["patch"]
        status = row["status"]
        total_file_additions = row["additions"]
        total_file_deletions = row["deletions"]
        total_file_changes = row["changes"]
        
        """Patches are None in some instances (e.g., XLSX files)"""
        if raw_file_patch is not None:
            """Find patch headers (e.g., @@ @@)"""
            headers_search = re.findall(r"@@(.*?)@@", raw_file_patch) 
            
            """Cleaning the headers, found @@REPLACE_ME@@ in some random code"""
            headers = []
            for head_row in headers_search:
                if '-' in head_row and '+' in head_row:
                    headers.append(f"@@{head_row}@@")
            total_patches = len(headers)
            
            for index, header in enumerate(headers):
                patch_number = index
                """Get line numbers changed for original code"""
                original_lines = re.search(f"@@ -(.*?) \+", header).group(1)
                if "," in original_lines:
                    original_line_start = int(original_lines.split(",")[0])
                    original_line_length = int(original_lines.split(",")[1])
                else:
                    """This occus for added txt files where the total length is 1: appears as @@ -A -B @@"""
                    original_line_start = int(original_lines)
                    original_line_length = int(original_lines)
                original_line_end = original_line_start + original_line_length - 1
                
                """Get line numbers changed for modified code"""
                modified_lines = re.search(f" \+(.*) @@", header).group(1)
                if "," in modified_lines:
                    modified_line_start = int(modified_lines.split(",")[0])
                    modified_line_length = int(modified_lines.split(",")[1])
                else:
                    """This occurs for added binary files the header will appear as @@ -A,X -B @@"""
                    modified_line_start = int(modified_lines)
                    modified_line_length = int(modified_lines)
                    
                modified_line_end = modified_line_start + modified_line_length - 1
                
                """Check if length of index is equal to last patch, if so read to end of raw_patch"""
                if index + 1 == len(headers):
                    raw_patch = raw_file_patch[raw_file_patch.find(headers[index])+len(headers[index]):]
                else:
                    raw_patch = raw_file_patch[raw_file_patch.find(headers[index])+len(headers[index]):raw_file_patch.find(headers[index+1])]

        
                """Call the function to help parse the patch to get data"""
                patch_parse = parse_raw_patch(raw_patch)
                
                """Create a temporary class to hold the parsed patch data"""                
                temp_parsed_commit = CommitParse(parsed_commit.repo_owner,
                                                 parsed_commit.repo_name,
                                                 parsed_commit.sha)
                
                """Set various values"""
                temp_parsed_commit.message = parsed_commit.message
                temp_parsed_commit.file_name = file_name
                temp_parsed_commit.file_number = file_number
                temp_parsed_commit.file_extension = file_extension
                temp_parsed_commit.total_files_changed = total_files_changed
                temp_parsed_commit.raw_file_patch = raw_file_patch
                temp_parsed_commit.patch_number = patch_number
                temp_parsed_commit.total_patches = total_patches
                temp_parsed_commit.raw_patch_header = header
                temp_parsed_commit.raw_patch = raw_patch
                temp_parsed_commit.original_code = patch_parse["original_code"]
                temp_parsed_commit.original_line_start = original_line_start
                temp_parsed_commit.original_line_length = original_line_length
                temp_parsed_commit.original_line_end = original_line_end
                temp_parsed_commit.modified_code = patch_parse["modified_code"]
                temp_parsed_commit.modified_line_start = modified_line_start
                temp_parsed_commit.modified_line_length = modified_line_length
                temp_parsed_commit.modified_line_end = modified_line_end
                temp_parsed_commit.additions = patch_parse["additions"]
                temp_parsed_commit.added_code = patch_parse["added_code"]
                temp_parsed_commit.deletions = patch_parse["deletions"]
                temp_parsed_commit.deleted_code = patch_parse["deleted_code"]
                temp_parsed_commit.changes = patch_parse["changes"]
                temp_parsed_commit.status = status
                temp_parsed_commit.total_file_additions = total_file_additions
                temp_parsed_commit.total_file_deletions = total_file_deletions
                temp_parsed_commit.total_file_changes = total_file_changes
                
                """Append the class as a dictionary to the data list"""
                data.append(temp_parsed_commit.__dict__)
        else:
            """Sometimes patch is None (e.g., XLSX files)"""
            temp_parsed_commit = CommitParse(parsed_commit.repo_owner,
                                             parsed_commit.repo_name,
                                             parsed_commit.sha)
            
            temp_parsed_commit.message = parsed_commit.message
            temp_parsed_commit.file_name = file_name
            temp_parsed_commit.file_number = file_number
            temp_parsed_commit.file_extension = file_extension
            temp_parsed_commit.total_files_changed = total_files_changed
            temp_parsed_commit.raw_file_patch = raw_file_patch
            temp_parsed_commit.status = status
            temp_parsed_commit.total_file_additions = total_file_additions
            temp_parsed_commit.total_file_deletions = total_file_deletions
            temp_parsed_commit.total_file_changes = total_file_changes
            
            """Append the class as a dictionary to the data list"""
            data.append(temp_parsed_commit.__dict__)
            
    return data
    

def parse_raw_patch(temp_raw_patch: str) -> dict:
    """Parses a single raw patch into original code and modified code

    Args:
        temp_raw_patch (str): Raw string of a single patch

    Returns:
        dict: Simple dictionary with various key values for parsing the raw patch
    """
    
    """Split the code so we can parse line by line"""
    split_code = temp_raw_patch.splitlines()
    
    """Create placeholders for desired values"""
    original_code = []
    modified_code = []
    
    additions = 0
    added_code = []
    deletions = 0
    deleted_code = []
    
    """Loop through each line of code to parse it"""
    for line in split_code:
        """[1:] is due to the spaces added from the git diff for +/- indicators in str"""
        if line.startswith("-"):
            """- signs indicate original code"""
            original_code.append(line[1:])
            deleted_code.append(line[1:])
            deletions += 1
        elif line.startswith("+"):
            """+ signs indicate modified code"""
            modified_code.append(line[1:])
            added_code.append(line[1:])
            additions += 1
        else:
            """Add any unchanged lines to original/modified code"""
            original_code.append(line[1:])
            modified_code.append(line[1:])
    
    original_code_str = "\n".join(original_code)
    modified_code_str = "\n".join(modified_code)
    added_code_str = "\n".join(added_code)
    deleted_code_str = "\n".join(deleted_code)
    changes = additions + deletions
    
    """Create a simple patch to return"""
    patch_parse = dict(
        original_code = original_code_str,
        modified_code = modified_code_str,
        additions = additions,
        added_code = added_code_str,
        deletions = deletions,
        deleted_code = deleted_code_str,
        changes = changes
    )
    
    return patch_parse


def commit(repo_owner: str, repo_name: str, sha: str, verbose=False) -> list:
    """Pass the GitHub repo_owner, repo_name, and associated commit to parse.

    Args:
        repo_owner (str): Target repo owner
        repo_name (str): Target repo name
        commit_sha (str): Target commit SHA from GitHub

    Returns:
        list: List of dictionaries strcutred around the class CommitParse
    """
    
    """Commit info API URL"""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{sha}"
    
    """Get the response"""
    response = requests.get(url)
    response.close()
    
    """Convert to json"""
    commit_info = response.json()
    
    """Initialize a CommitParse to hold data"""
    parsed_commit = CommitParse(repo_owner=repo_owner, 
                                repo_name=repo_name,
                                sha=commit_info["sha"])
    
    """Add commit message"""
    parsed_commit.message = commit_info["commit"]["message"]
    
    """Parse the files"""
    parsed_files = parse_commit_info(commit_info["files"], parsed_commit)
            
    return parsed_files