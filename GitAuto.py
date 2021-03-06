"""
Description: Python wrapper for Git. Script Git to your delight...

Aside: The G is predicting.

"""

__author__ = "Veda Sadhak"
__version__ = "2022.04.01"

import os
import pathlib
import subprocess

PIPE = subprocess.PIPE

def get_posix_path(path):
    return str(pathlib.PureWindowsPath(path).as_posix())

class GitAuto:

    def __init__(self, **kwargs):

        self.repos = kwargs["repos"]

    def run_cmd(self, cmd, print_output=False):

        for repo in self.repos:

            repo_name = repo["name"]
            repo_path = repo["path"]

            os.chdir(repo_path)

            cmd_str = ""
            for param in cmd:
                cmd_str += param + " "

            cmd_str_print = cmd_str
            if "commit" in cmd_str:
                cmd_str_print = "git commit -m release_notes.txt"

            process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
            stdoutput, stderroutput = process.communicate()

            out_raw= str(stdoutput).replace("b'", "").replace('b"', '').replace("'", "").replace('"', '').replace("\\t", "")
            out = []
            for line in out_raw.split("\\n"):
                if line != "":
                    out.append(line)

            err_raw = str(stderroutput).replace("b'", "").replace('b"', '').replace("'", "").replace('"', '').replace("\\t", "")
            err = []
            for line in err_raw.split("\\n"):
                if line != "":
                    err.append(line)

            if "fatal" in str(stderroutput) or "warning" in str(stderroutput):
                print("Cmd: {}| Repo: {} >\n".format(cmd_str_print, repo_name), sep='\n')
                for line in err:
                    print(f"    {line}")
                print("")
            elif print_output:
                print("Cmd: {}| Repo: {} >\n".format(cmd_str_print, repo_name), sep='\n')
                for line in out:
                    print(f"    {line}")
                print("")
            else:
                print("Cmd: {}| Repo: {} > Success".format(cmd_str_print, repo_name), sep='\n')

    def status(self):
        self.run_cmd(["git", "status"], print_output=True)

    def branch(self):
        self.run_cmd(["git", "branch", "--show-current"], print_output=True)

    def pull(self):
        self.run_cmd(["git", "pull"])

    def add(self):
        self.run_cmd(["git", "add", "."])

    def commit(self, msg):
        self.run_cmd(["git", "commit", "-m", msg])

    def push(self):
        self.run_cmd(["git", "push"])

    def push_new(self, branch):
        self.run_cmd(["git", "push", "--set-upstream", "origin", branch])

    def checkout_new(self, branch):
        self.run_cmd(["git", "checkout", "-b", branch])

    def checkout(self, branch):
        self.run_cmd(["git", "checkout", branch])

    def tag(self, tag_name):
        self.run_cmd(["git", "tag", tag_name])

    def push_tags(self):
        self.run_cmd(["git", "push", "--tags"])

    def merge(self, branch_src):
        self.run_cmd(["git", "merge", branch_src])

    def num_commits(self, branch, target):
        self.run_cmd(["git", "rev-list", "--count", branch, f"^origin/{target}"], print_output=True)

    def squash(self, num_commits):
        self.run_cmd(["git", "rebase", "-i", f"HEAD~{num_commits}"])