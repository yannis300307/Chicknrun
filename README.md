# Chicknrun V3

Chicknrun is a command line tool written in Python that can help you to be much more efficient during 42' piscine.

Type `cr3 help` to get a list of all the commands.

## Features:
- Compilation with the needed flags (`cr3 compile`)
- Compile and run program with arguments (`cr3 run [args]`)
- Check the Norminette with needed flags (`cr3 norminette`)
- Check Norminette, compilation errors, unstaged commits and non pushed commits (`cr3 check`)
- Fast temporary main writing (`cr3 run_main "[Escaped main content]"`)
- One command update (`cr3 update`)
- Automatic exercises directories and .gitignore creation (`cr3 create_dirs [amount]`)

When generating the main function, all C files in the current directory and subdirectories will be included as well as stdio.h, stdlib.h and unistd.h.

## Installation

Run the command : 
```bash
git clone https://github.com/yannis300307/Chicknrun.git ~/.chicknrun && echo "alias cr3=\"python3 ~/.chicknrun/cr3.py\"" >> ~/.zshrc && source ~/.zshrc
```

This command will create the `~/.chicknrun` folder and add the alias at the end of `~/.zshrc`.
