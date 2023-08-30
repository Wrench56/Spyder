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
    try:
        with open(_evaluate_path(path, private), mode, encoding=encoding) as file:
            file.write(content)
            file.close()
        return True
    except IOError:
        logging.error(f'Can\'t create {"private" if private else "shared"} file "{path}"')

    return False


def create_directory(path: str, private: bool = True) -> bool:
    try:
        os.mkdir(_evaluate_path(path, private))
        return True
    except FileExistsError:
        logging.error(f'Can\'t create directory "{path}" because it already exits')
    except FileNotFoundError:
        logging.error(f'Can\'t create directory "{path}" because one of the parent directories do not exist')

    return False


def read_file(path: str, mode: str = 'r', encoding: str = 'utf-8', private: bool = True) -> Optional[List[str]]:
    try:
        with open(_evaluate_path(path, private), mode, encoding=encoding) as file:
            data = file.readlines()
            file.close()
        return data
    except IOError:
        logging.error(f'Can\'t read {"private" if private else "shared"} file {path}')

    return None


def delete_file(path: str, private: bool = True) -> bool:
    try:
        os.remove(_evaluate_path(path, private))
        return True
    except FileNotFoundError:
        logging.error(f'The file {path} you tried to delete does not exist')
    except OSError:
        logging.error('Can\'t delete a directory with delete_file()')

    return False


def delete_directory(path: str, private: bool = True) -> bool:
    try:
        shutil.rmtree(_evaluate_path(path, private), onerror=lambda _, epath, __: _raise(PermissionError(epath)))
        return True
    except PermissionError as error:
        logging.error(f'Couldn\'t delete directory \"{error}\"')

    return False


def symlink(src: str, dst: str, src_private: bool = True, dst_private: bool = True) -> bool:
    try:
        os.symlink(_evaluate_path(src, src_private), _evaluate_path(dst, dst_private))
        return True
    except OSError:
        logging.error(f'Creating symlink from {src} to {dst} failed: unprivileged user')

    return False


def copy_directory(src: str, dst: str, src_private: bool = True, dst_private: bool = True, overwrite: bool = False) -> bool:
    try:
        shutil.copytree(_evaluate_path(src, src_private), _evaluate_path(dst, dst_private), dirs_exist_ok=overwrite)
        return True
    except FileExistsError:
        logging.error(f'Can\'t copy directory "{src}": destination directory "{dst}" already exists')
    except shutil.Error:
        logging.error(f'Miscellaneus errors occured when copying directory "{src}"')

    return False


def copy_file(src: str, dst: str, src_private: bool = True, dst_private: bool = True) -> bool:
    try:
        shutil.copyfile(_evaluate_path(src, src_private), _evaluate_path(dst, dst_private))
        return True
    except shutil.SameFileError:
        logging.error('Source and destination file are the same file')
    except OSError:
        logging.error('Destination file is not writable')

    return False


def walk(path: str, private: bool = True) -> Optional[Iterator[Tuple[str, List[str], List[str]]]]:
    try:
        return os.walk(_evaluate_path(path, private), onerror=_raise)
    except OSError:
        logging.error('Can\'t continue directory walk')

    return None


def exists(path: str, private: bool = True) -> bool:
    return os.path.exists(_evaluate_path(path, private))
