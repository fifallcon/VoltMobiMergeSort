import errno
import os
import shutil


def create_tmp_directory(filename):
    """
    Вспомогательная функция
    Если дериктории в которую мы собираемся создать файл - не существует, создадим её.
    :string filename:
    :return None:
    """
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def clear_tmp_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
