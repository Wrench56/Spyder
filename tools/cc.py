# Clear cache (__pycache__)
# Why to use:
#  1. When you migrate e.g. from Python 3.10
#  to Python 3.11, the __pycache__ folder will
#  still hold every Python 3.10 generated
#  byte codes. With running this command,
#  you get rid of these unused byte codes
#  freeing up some space on your hard drive.
#  2. When you delete a source file from
#  your project, the .pyc file is going
#  to be still in __pycache__.
#  3. The same applies when you rename/
#  relocate a source file.


# Ultimately this script/tool occasionally
# frees up some hard drive space.

import os

BLACKLIST = ['.git', '.github']


def remove_files(path):
    with os.scandir(path) as rdir:
        for entry in rdir:
            if entry.name in BLACKLIST:
                continue
            if entry.is_dir():
                if len(os.listdir(entry.path)) == 0:
                    continue
                remove_files(entry.path)
            elif entry.is_file():
                if entry.name.endswith('.pyc'):
                    os.remove(entry.path)


def main():
    path = os.getcwd()

    remove_files(path)

    print('\n > Done!')


if __name__ == '__main__':
    main()
