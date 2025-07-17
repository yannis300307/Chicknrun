import customcommand as cc
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
def norminette():
	"""Run `norminette -R CheckForbiddenSourceHeader`."""
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
		os.mkdir(f"ex{i :02d}")
	with open(".gitignore", "w") as f:
		f.write("a.out\n*.swp")

@cc.command
def check():
	"""Check norminette, compilation, git modified files, unpushed commits."""
	print("Check Norminette")
	norminette()
	print("Check compilation")
	if call("echo \"int main() {}\" | cc */*.c -Wall -Wextra -Werror -o binary -x c -", shell=True) == 0:
		os.remove("./binary")
	print("Check git uncommitted changes")
	out = getoutput("git ls-files -m -o")
	if len(out) > 1:
		cc.print_error("Uncommitted changes detected!\n" + out)
		return
	print("Passed")
	print("Check Non-pushed commits")
	out = getoutput("git log --oneline --branches --not --remotes")
	if len(out) > 1:
		cc.print_error("Commit not pushed!\n" + out)
		return
	print("All checks done. See if errors have been raised.")

cc.handle_commands()
