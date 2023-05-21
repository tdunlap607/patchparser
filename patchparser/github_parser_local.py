"""
Helper functions to load and process commit data from a local GitHub clone
"""
import re
import git


class CommitParseLocal:
    def __init__(self, repo_owner: str, repo_name: bool, sha: str) -> object:
        """Initialize a class to hold the data for parsing the commit data of a local repo

        Args:
            repo_owner (str): Repo owner
            repo_name (str): Repo name
            sha (str): Target commit SHA

        Returns:
            object: CommitParseLocal
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
        self.commit_author_name = None
        self.commit_author_login = None
        self.commit_author_email = None
        self.commit_author_date = None
        self.commit_committer_name = None
        self.commit_committer_login = None
        self.commit_committer_email = None
        self.commit_committer_date = None
        self.commit_tree_sha = None
        self.commit_tree_url = None
        self.commit_verification_verified = None
        self.commit_verification_reason = None
        self.parents = None


def parse_commit_info(commit_info: list, parsed_commit: CommitParseLocal) -> list:
    """Parses the commit_info list

    Args:
        commit_info (list): commit_info list from original data
        parsed_commit (CommitParseLocal): Set CommitParseLocal class with basic info

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
        """Not all will have patches. E.g., PDF files"""
        if "patch" in row:
            raw_file_patch = row["patch"]
        else:
            raw_file_patch = None
        status = row["status"]
        total_file_additions = row["additions"]
        total_file_deletions = row["deletions"]
        total_file_changes = row["changes"]
        
        """Patches are None in some instances (e.g., XLSX files)"""
        if raw_file_patch is not None and "patch" in row:
            """Find patch headers (e.g., @@ @@)"""
            headers_search = re.findall(r"@@(.*?)@@", raw_file_patch) 
            
            """Cleaning the headers, found @@REPLACE_ME@@ in some random code"""
            headers = []
            for head_row in headers_search:
                if '-' in head_row and '+' in head_row:
                    # get the original line headers
                    original_header_lines = re.search(f"@@ -(.*?) \+", f"@@{head_row}@@").group(1)
                    # make sure the header is of type int
                    if original_header_lines.split(',')[-1].isdigit():
                        headers.append(f"@@{head_row}@@")
            total_patches = len(headers)
            
            for index, header in enumerate(headers):
                patch_number = index
                if header == None:
                    pass
                else:
                    """Get line numbers changed for original code"""
                    try:
                        original_lines = re.search(f"@@ -(.*?) \+", header).group(1)
                        if "," in original_lines:
                            original_line_start = int(original_lines.split(",")[0])
                            original_line_length = int(original_lines.split(",")[1])
                        else:
                            """This occus for added txt files where the total length is 1: appears as @@ -A -B @@"""
                            original_line_start = int(original_lines)
                            original_line_length = int(original_lines)
                        original_line_end = original_line_start + original_line_length - 1
                    except Exception as e:
                        print(f"Error on line 133 of github_parser: {str(e)}")
                    
                    try:
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
                    except Exception as e:
                        print(f"Error on line 148 of github_parser: {str(e)}")
                
                """Check if length of index is equal to last patch, if so read to end of raw_patch"""
                if index + 1 == len(headers):
                    raw_patch = raw_file_patch[raw_file_patch.find(headers[index])+len(headers[index]):]
                else:
                    raw_patch = raw_file_patch[raw_file_patch.find(headers[index])+len(headers[index]):raw_file_patch.find(headers[index+1])]

        
                """Call the function to help parse the patch to get data"""
                patch_parse = parse_raw_patch(raw_patch)
                
                """Create a temporary class to hold the parsed patch data"""                
                temp_parsed_commit = CommitParseLocal(parsed_commit.repo_owner,
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
                temp_parsed_commit.commit_author_name = parsed_commit.commit_author_name
                temp_parsed_commit.commit_author_login = parsed_commit.commit_author_login
                temp_parsed_commit.commit_author_email = parsed_commit.commit_author_email
                temp_parsed_commit.commit_author_date = parsed_commit.commit_author_date
                temp_parsed_commit.commit_committer_name = parsed_commit.commit_committer_name
                temp_parsed_commit.commit_committer_login = parsed_commit.commit_committer_login
                temp_parsed_commit.commit_committer_email = parsed_commit.commit_committer_email
                temp_parsed_commit.commit_committer_date = parsed_commit.commit_committer_date
                temp_parsed_commit.commit_tree_sha = parsed_commit.commit_tree_sha
                temp_parsed_commit.commit_tree_url = parsed_commit.commit_tree_url
                temp_parsed_commit.commit_verification_verified = parsed_commit.commit_verification_verified
                temp_parsed_commit.commit_verification_reason = parsed_commit.commit_verification_reason
                temp_parsed_commit.parents = parsed_commit.parents
                
                """Append the class as a dictionary to the data list"""
                data.append(temp_parsed_commit.__dict__)
        else:
            """Sometimes patch is None (e.g., XLSX files)"""
            temp_parsed_commit = CommitParseLocal(parsed_commit.repo_owner,
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
            temp_parsed_commit.commit_author_name = parsed_commit.commit_author_name
            temp_parsed_commit.commit_author_login = parsed_commit.commit_author_login
            temp_parsed_commit.commit_author_email = parsed_commit.commit_author_email
            temp_parsed_commit.commit_author_date = parsed_commit.commit_author_date
            temp_parsed_commit.commit_committer_name = parsed_commit.commit_committer_name
            temp_parsed_commit.commit_committer_login = parsed_commit.commit_committer_login
            temp_parsed_commit.commit_committer_email = parsed_commit.commit_committer_email
            temp_parsed_commit.commit_committer_date = parsed_commit.commit_committer_date
            temp_parsed_commit.commit_tree_sha = parsed_commit.commit_tree_sha
            temp_parsed_commit.commit_tree_url = parsed_commit.commit_tree_url
            temp_parsed_commit.commit_verification_verified = parsed_commit.commit_verification_verified
            temp_parsed_commit.commit_verification_reason = parsed_commit.commit_verification_reason
            temp_parsed_commit.parents = parsed_commit.parents
            
            """Append the class as a dictionary to the data list"""
            data.append(temp_parsed_commit.__dict__)
    
    if len(data) == 0:
        data.append(parsed_commit.__dict__)
        return data
    else:
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


def commit_local(repo_owner: str, repo_name: str, sha: str, base_repo_path: str, verbose=False) -> list:
    """Pass the local cloned GitHub repo_owner, repo_name, and associated commit to parse.

    Args:
        repo_owner (str): Target repo owner
        repo_name (str): Target repo name
        sha (str): Target commit SHA from GitHub
        base_repo_path (str): Directory of localy cloned repository

    Returns:
        list: List of dictionaries strcutred around the class CommitParseLocal
    """
    
    """Create the repo_path"""
    # repo_path = f"{base_repo_path}{repo_owner}/{repo_name}"
    repo_path = f"{base_repo_path}"
    
    """Commit info API URL"""
    repo = git.Repo(repo_path)
    
    # obtains the raw diff for a given SHA
    # SHA~ represents the prior commit
    diff = repo.git.diff(f"{sha}~", f"{sha}")
    
    # obtain commit information
    commit_info = repo.commit(sha)
    
    # obtain a commit diff
    git_repo_diff = commit_info.diff(f"{sha}~")
    
    # split the raw diff, no need to take 0, it's empty on this split
    diff_splits = diff.split("diff --git")[1:]
    
    """Initialize a CommitParse to hold data"""
    parsed_commit = CommitParseLocal(repo_owner=repo_owner,
                                     repo_name=repo_name,
                                     sha=sha)
            
    """Add commit message"""
    parsed_commit.message = commit_info.message
    parsed_commit.commit_author_name = commit_info.author.name
    # if commit_info.author != None and len(commit_info.author) > 0:
    #     # This doesn't appear in the Git repo? 
    #     # temp_parsed_commit.commit_author_login = commit_info["author"]["login"]
    #     temp_parsed_commit.commit_author_login = commit_info.author.email
    parsed_commit.commit_author_email = commit_info.author.email
    parsed_commit.commit_author_date = commit_info.authored_datetime
    parsed_commit.commit_committer_name = commit_info.committer.name
    # if commit_info.committer != None and len(commit_info.committer) > 0:
    #     # This doesn't appear in the Git repo?
    #     # temp_parsed_commit.commit_committer_login = commit_info["committer"]["login"]
    #     temp_parsed_commit.commit_committer_login = commit_info.committer.email
    parsed_commit.commit_committer_email = commit_info.committer.email
    parsed_commit.commit_committer_date = commit_info.committed_datetime
    parsed_commit.commit_tree_sha = commit_info.tree.hexsha
    # # URLs will be intentionally empty since a local repository
    # temp_parsed_commit.commit_tree_url = commit_info["commit"]["tree"]["url"]
    # # Unable to find commit_verifications?
    # temp_parsed_commit.commit_verification_verified = commit_info["commit"]["verification"]["verified"]
    # temp_parsed_commit.commit_verification_reason = commit_info["commit"]["verification"]["reason"]
    parsed_commit.parents = [z.hexsha for z in commit_info.parents]
    
    
    """Create files list of dictionaries"""
    # creates a placeholder for the parsed raw diff
    files = []
    
    # create a commit info list
    commit_info_list = list(commit_info.stats.files)
    
    for index, file_diff in enumerate(diff_splits[:1000]):
        try:       
            # find the a_file = prior file
            if "new file mode 100644" in file_diff:
                # split between a/ b/ then take the a file for newly added
                a_file = re.findall('(?= a\/)(.*?)(?=\\n)', file_diff)[0].split(' ')[1].strip()
                status = 'A'
            else:
                a_file = re.findall('(?= a\/)(.*?)(?=\\n)', file_diff)[1].strip()
            # find the b_file = how file was changed
            # added files will not have the second b/file
            if "deleted file mode 100644" in file_diff:
                b_file = re.findall('(?= b\/)(.*?)(?=\\n)', file_diff)[0].strip()
                # for some reason the git diff repo sets deleted files as 'A'
                status = 'D'
            else:
                b_file = re.findall('(?= b\/)(.*?)(?=\\n)', file_diff)[1].strip()
                status = git_repo_diff[index].change_type
                
            # take the ending part, similar to the response from GitHub API
            if "deleted file mode 100644" in file_diff:
                # deleted files will not have the typical b_file in the diff
                diff_file = "@@" + file_diff.split(f"/dev/null\n@@")[1]
            else:
                diff_file = "@@" + file_diff.split(f"{b_file}\n@@")[1]
                
            # check if filename was renamed
            # raw filename only ([2:] ignores the a/ of the start)
            if a_file[2:] != b_file[2:]:
                status = "R"
                filename = commit_info_list[index]
            else:
                filename = a_file[2:]

            # This should probably be a class eventually
            temp_parse = {
                "filename":filename,
                "a_file":a_file,
                "b_file":b_file,
                "additions":commit_info.stats.files[filename]['insertions'],
                "deletions":commit_info.stats.files[filename]['deletions'],
                "changes":commit_info.stats.files[filename]['lines'],
                "patch":diff_file,
                "status":status
            }
            
            files.append(temp_parse)
        except:
            print("wait")
        
    """Parse the files"""
    parsed_files = parse_commit_info(files, parsed_commit)
            
    return parsed_files
        