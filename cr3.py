import customcommand as cc
from prettyprint import error, warn, info, success, ask
from subprocess import call, getoutput
import os


@cc.command
def compile(name: str = "binary"):
	"""Compile all the c files in the directory with the needed flags."""
	call("cc -Wall -Werror -Wextra *.c -o " + name, shell=True)

@cc.command
def run(args: str = ""):
	"""Compile all the c files in the directory with the needed flags and run the program."""
	if call("cc -Wall -Werror -Wextra *.c -o binary", shell=True) == 0:
		call("./binary " + args, shell=True)
		os.remove("./binary")

@cc.command
def run_main(content: str = ""):
	"""Add a custom main to the program and run it. It doesn't modify the file."""
	files = "".join([f"#include \\\"{f[2:]}\\\"\\n" for f in getoutput("find . -name \"*.c\"").split("\n")])

	if call("printf '%b\\n' \"#include <stdio.h>\\n#include <stdlib.h>\\n#include <unistd.h>\\n" + files + "int main() {" + content + "}\" | cc -Wall -Wextra -Werror -o binary -x c -", shell=True) == 0:
		call("./binary", shell=True)
		os.remove("./binary")

@cc.command
def run_gdb():
	"""Compile and run GDB."""
	if call("cc -Wall -Werror -Wextra *.c -o binary -g", shell=True) == 0:
		call("gdb ./binary -tui", shell=True)
		os.remove("./binary")

@cc.command
def norminette():
	"""Run `norminette -R CheckForbiddenSourceHeader`."""
	info("Check Norminette")
	call("norminette -R CheckForbiddenSourceHeader", shell=True)

@cc.command
def full_workflow(args: str = "", main_content: str = ""):
	"""Norminette, compile and run the program"""
	norminette()
	if main_content:
		run_main(content = main_content)
	else:
		run(args = args)

@cc.command
def create_dirs(maxi: int):
	"""Create directories from ex00 to exXX in the current directory."""
	for i in range(maxi):
		try :
			os.mkdir(f"ex{i :02d}")
		except :
			print(f"ex{i :02d} already exists !")
	with open(".gitignore", "w") as f:
		f.write("a.out\n*.swp")

@cc.command
def check():
	"""Check norminette, compilation, git modified files, unpushed commits."""
	norminette()
	info("Check compilation")
	if call("echo \"int main() {}\" | cc */*.c -Wall -Wextra -Werror -o binary -x c -", shell=True) == 0:
		os.remove("./binary")
		success("Compilation passed")
	else:
		error("Can't compile!")
	info("Check git uncommitted changes")
	out = getoutput("git ls-files -m -o")
	if len(out) > 1:
		error("Uncommitted changes detected!\n" + out)
		return
	else:
		success("No unstaged changes.")
	
	info("Check Non-pushed commits")
	out = getoutput("git log --oneline --branches --not --remotes")
	if len(out) > 1:
		error("Commits not pushed!\n" + out)
		return
	else:
		success("All commits have been pushed!")
	success("All checks done. Nice!")

@cc.command
def evaluate():
	"""Check Norminette and open all files in git"""
	norminette()
	files = getoutput('find . -name \"*.c\"').split('\n')
	if files == [""]:
		warn("No file has been found.")
		return
	if len(files) >= 5 and ask(f"{len(files)} tabs will be opened. Continue? [y/N]:") not in ("y", "yes"):
			warn("Process aborted.")
			return
	info(f"Opening {len(files)} files in Vim")
	for file in reversed(files):
		call(f"gnome-terminal --tab -- vim {file}", shell=True)

@cc.command
def send(files: str, commit_message: str = ""):
	"""Git add, commit and push the given files. Can generate an automatic commit message if none is given."""
	if len(commit_message) == 0:
		commit_message = "Add " + files + "."
	if ask(f"Confirm push of files {files} with commit message \"{commit_message}\"? (Y/n)").lower() in ("", "y", "yes"):
		call(["git", "add", files])
		call(["git", "commit", files, "-m", commit_message])
		if call(["git", "push"]):
			if call(["git", "push", "--set-upstream", "origin", "master"]):
				error("Git push failed!")
			else:
				success("Files pushed!")
		else:
			success("Files pushed!")
	else:
		warn("Aborted.")

@cc.command
def update():
	"""Update Chicknrun to the latest version."""
	info("Fetching latest version...")
	call("cd ~/.chicknrun && git fetch && git pull", shell=True)

cc.handle_commands()
