import sys

def rename_terminal(title):
    # Renames the terminal
    # Note: This renames the whole terminal window, not just the tab!
    sys.stdout.write("\x1b]2;%s\x07" % title)