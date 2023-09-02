"""
This module allows plugins to access the private and shared directories.

This module is a wrapper mostly for the os and shutil modules to make a
sandbox-like environment for the plugins. You can use this module if
you want to store or cache something. _evaluate_path()
only allows plugins to write in data/shared or their own
data/private/{plugin} directory.

Exposed functions:
    - create_file
    - create_directory
    - read_file
    - delete_file
    - delete_directory
    - symlink
    - copy_directory
    - copy_file
    - walk
    - exists
"""

from typing import List, Tuple, Iterator, Optional
import logging
import os
import shutil

from utils import stack


def _raise(exception: Exception) -> None:
    raise exception


def _evaluate_path(path: str, private: bool, depth: int = 3) -> str:
    plugin_name = stack.get_caller(depth)[0].split('.')[-1]
    return f'data/{f"private/{plugin_name}" if private else "shared"}/{path}'


def create_file(path: str, content: str = '', mode: str = 'a', encoding: str = 'utf-8', private: bool = True) -> bool:
    """
    Create a file in the shared or private (plugin) directory.

    Args:
        path: The path to the file
        content: Write the content after creation to the file
        mode: The file buffer mode
        encoding: The file buffer encoding
        private: Whether to create the file in the shared or private directory

    Returns:
        bool: Returns True if operation was successful and False if it failed

    Usage:
        >>> create_file('test.txt', private=False)
        True
    """
    try:
        with open(_evaluate_path(path, private), mode, encoding=encoding) as file:
            file.write(content)
            file.close()
        return True
    except IOError:
        logging.error(f'Can\'t create {"private" if private else "shared"} file "{path}"')

    return False


def create_directory(path: str, private: bool = True) -> bool:
    """
    Create a directory in the shared or private (plugin) directory.

    Args:
        path: The path to the directory
        private: Whether to create the directory in the shared or
                 private directory

    Returns:
        bool: Returns True if operation was successful and False if it failed

    Usage:
        >>> create_directory('', private=False)
        True
    """
    try:
        os.mkdir(_evaluate_path(path, private))
        return True
    except FileExistsError:
        logging.error(f'Can\'t create directory "{path}" because it already exits')
    except FileNotFoundError:
        logging.error(f'Can\'t create directory "{path}" because one of the parent directories do not exist')

    return False


def read_file(path: str, mode: str = 'r', encoding: str = 'utf-8', private: bool = True) -> Optional[List[str]]:
    """
    Read a file in the shared or private (plugin) directory.

    Args:
        path: The path to the file
        mode: The file buffer mode (default='r')
        encoding: The file buffer encoding
        private: Whether to read the file in the shared or private directory

    Returns:
        None | list[str]: Returns a list of strings - each string being a line
        of the original file - if the operation was successful, otherwise None

    Usage:
        >>> create_file('test.txt', 'Hello World!', private=False)
        >>> read_file('test.txt', private=False)
        ['Hello World!']
    """
    try:
        with open(_evaluate_path(path, private), mode, encoding=encoding) as file:
            data = file.readlines()
            file.close()
        return data
    except IOError:
        logging.error(f'Can\'t read {"private" if private else "shared"} file {path}')

    return None


def delete_file(path: str, private: bool = True) -> bool:
    """
    Delete a file in the shared or private (plugin) directory.

    Args:
        path: The path to the file
        private: Whether to delete the file in the shared or private directory

    Returns:
        bool: Returns True if operation was successful and False if it failed

    Usage:
        >>> create_file('test.txt', 'Hello World!', private=False)
        >>> delete_file('test.txt', private=False)
        True
    """
    try:
        os.remove(_evaluate_path(path, private))
        return True
    except FileNotFoundError:
        logging.error(f'The file {path} you tried to delete does not exist')
    except OSError:
        logging.error('Can\'t delete a directory with delete_file()')

    return False


def delete_directory(path: str, private: bool = True) -> bool:
    """
    Delete a directory in the shared or private (plugin) directory.

    Args:
        path: The path to the directory
        private: Whether to delete the directory in the shared
                 or private directory

    Returns:
        bool: Returns True if operation was successful and False if it failed

    Usage:
        >>> create_directory('test', private=False)
        >>> delete_directory('test', private=False)
        True
    """
    try:
        shutil.rmtree(_evaluate_path(path, private), onerror=lambda _, epath, __: _raise(PermissionError(epath)))
        return True
    except PermissionError as error:
        logging.error(f'Couldn\'t delete directory \"{error}\"')

    return False


def symlink(src: str, dst: str, src_private: bool = True, dst_private: bool = True) -> bool:
    """
    Create a symlink in the shared or private (plugin) directory.

    Args:
        src: The path to the source file
        dst: The path to the destination file
        src_private: Whether the source is in the private or shared directory
        dst_private: Whether the destination is in the private
                     or shared directory

    Returns:
        bool: Returns True if operation was successful and False if it failed

    Usage:
        >>> create_file('test.txt', 'Hello World!', private=False)
        >>> symlink('test.txt', 'dest.txt', src_private=False, dst_private=False)
        True
        >>> delete_file('dest.txt')
    """
    try:
        os.symlink(_evaluate_path(src, src_private), _evaluate_path(dst, dst_private))
        return True
    except OSError:
        logging.error(f'Creating symlink from {src} to {dst} failed: unprivileged user')

    return False


def copy_directory(src: str, dst: str, src_private: bool = True, dst_private: bool = True, overwrite: bool = False) -> bool:
    """
    Copy a directory in the shared or private (plugin) directory.

    Args:
        src: The path to the source directory
        dst: The path to the destination directory
        src_private: Whether the source is in the private or shared directory
        dst_private: Whether the destination is in the private
                     or shared directory
        overwrite: Whether the copy overwrites directories with the same name
                   in the destination folder. If overwrite is False and there
                   is a directory/file with the same name as ``dst``, False
                   is going to be returned

    Returns:
        bool: Returns True if operation was successful and False if it failed

    Usage:
        >>> create_directory('test', private=False)
        >>> create_file('test/file.txt', private=False)
        >>> copy_directory('test', 'dest', src_private=False, dst_private=False)
        True
    """
    try:
        shutil.copytree(_evaluate_path(src, src_private), _evaluate_path(dst, dst_private), dirs_exist_ok=overwrite)
        return True
    except FileExistsError:
        logging.error(f'Can\'t copy directory "{src}": destination directory "{dst}" already exists')
    except shutil.Error:
        logging.error(f'Miscellaneus errors occured when copying directory "{src}"')

    return False


def copy_file(src: str, dst: str, src_private: bool = True, dst_private: bool = True) -> bool:
    """
    Copy a file in the shared or private (plugin) directory.

    Args:
        src: The path to the source file
        dst: The path to the destination file
        src_private: Whether the source is in the private or shared directory
        dst_private: Whether the destination is in the private
                     or shared directory

    Returns:
        bool: Returns True if operation was successful and False if it failed

    Usage:
        >>> create_file('test.txt', 'Hello World!', private=False)
        >>> copy_file('test.txt', 'dest.txt', src_private=False, dst_private=False)
        True
    """
    try:
        shutil.copyfile(_evaluate_path(src, src_private), _evaluate_path(dst, dst_private))
        return True
    except shutil.SameFileError:
        logging.error('Source and destination file are the same file')
    except OSError:
        logging.error('Destination file is not writable')

    return False


def walk(path: str, private: bool = True) -> Optional[Iterator[Tuple[str, List[str], List[str]]]]:
    """
    Create a symlink in the shared or private (plugin) directory.

    Args:
        path: The path to the directory
        private: Whether the directory is in the private or shared directory

    Returns:
        None | Iterator[tuple[str, list[str], list[str]]]: Returns None
            if there was an error or an Iterator() with a tuple of 3 elements:
            root_name, files, directories

    """
    try:
        return os.walk(_evaluate_path(path, private), onerror=_raise)
    except OSError:
        logging.error('Can\'t continue directory walk')

    return None


def exists(path: str, private: bool = True) -> bool:
    """
    Check if a file exists in the shared or private (plugin) directory.

    Args:
        path: The path to the directory
        private: Whether the directory is in the private or shared directory

    Returns:
        bool: True if file exists, otherwise False
    """
    return os.path.exists(_evaluate_path(path, private))
