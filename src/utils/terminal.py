import os

def rename_terminal(title):
    # Renames the terminal
    # Note: This renames the whole terminal window, not just the tab!
    os.system('echo -n -e "\033]0;{}\007"'.format(title))