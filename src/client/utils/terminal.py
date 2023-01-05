import sys


def rename_terminal(title: str) -> None:
    # Renames the terminal
    # Note: This renames the whole terminal window, not just the tab!
    sys.stdout.write(f'\x1b]2;{title}\x07')
