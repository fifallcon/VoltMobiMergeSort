import os
import sys

from smart_line import SmartLine
from utils import create_tmp_directory, clear_tmp_directory


class Merger:
    one_mb = 1024 * 1024
    size_of_split_file = (one_mb * 4) * 50
    tmp_dir = 'tmpdir'

    def __init__(self, file_one_name, file_two_name):
        """
        :string file_one_name имя первого файла:
        :string file_two_name имя второго файла:
        """
        self.file_one = file_one_name
        self.file_two = file_two_name

    @staticmethod
    def split_sort_file(file_name):
        """
        Разбивает файл на более мелкие сортированные файлы
        :string file_name: - имя большого несортированного файла
        :return: list[string] - список имён маленьких сортированных файлов
        """
        with open(file_name, "r") as in_file:
            chunk_num = 0
            current_size = 0
            split_file_names = []

            next_line = in_file.readline()
            chunk_to_write = []
            while next_line:
                current_size += sys.getsizeof(next_line)
                chunk_to_write.append(next_line)

                if current_size > Merger.size_of_split_file:
                    chunk_to_write.sort()
                    output_filename = os.path.join(Merger.tmp_dir, f"merge{chunk_num}.txt")
                    create_tmp_directory(output_filename)
                    with open(output_filename, "w") as output:
                        for line in chunk_to_write:
                            output.write(f"{line}")

                    split_file_names.append(output_filename)
                    current_size = 0
                    chunk_num += 1
                    chunk_to_write = []

                next_line = in_file.readline()

            if current_size > 0:
                chunk_to_write.sort()
                output_filename = os.path.join(Merger.tmp_dir, f"merge{chunk_num}.txt")
                create_tmp_directory(output_filename)
                with open(output_filename, "w") as output:
                    for line in chunk_to_write:
                        output.write(f"{line}")

                split_file_names.append(output_filename)

        return split_file_names

    @staticmethod
    def mergesort(splited_files, sorted_filename):
        """

        :param splited_files: - список имён маленьких сортированных файлов
        :param sorted_filename: - имя итогового сортированного файла
        :return: None
        """
        def one_step(output_filename, splitted_files):
            first = splitted_files[0]
            second = splitted_files[1]

            first_line = SmartLine(first)
            second_line = SmartLine(second)

            with open(output_filename, "w") as output:
                while first_line.data() or second_line.data():
                    if first_line.data() and not second_line.data():
                        output.write("{0}\n".format(first_line.data()))
                        first_line.next()
                    elif not first_line.data() and second_line.data():
                        output.write("{0}\n".format(second_line.data()))
                        second_line.next()
                    elif first_line.data() < second_line.data():
                        output.write("{0}\n".format(first_line.data()))
                        first_line.next()
                    elif second_line.data() < first_line.data():
                        output.write("{0}\n".format(second_line.data()))
                        second_line.next()

            splitted_files.remove(first)
            splitted_files.remove(second)
            # удаляем более не нужные файлы
            first_line.end_read()
            second_line.end_read()
            if os.path.exists(first):
                os.remove(first)
            if os.path.exists(second):
                os.remove(second)

        merge_n = len(splited_files)
        while len(splited_files) > 2:
            output_filename = os.path.join(Merger.tmp_dir, "merge{0}.txt".format(merge_n))
            merge_n += 1
            one_step(output_filename, splited_files)
            splited_files.append(output_filename)

        if len(splited_files) == 2:
            output_filename = os.path.join(sorted_filename)
            one_step(output_filename, splited_files)

    @staticmethod
    def merge(sorted_one, sorted_two):
        """
        Сливает непосредственно 2 отсортированных файла
        :param sorted_one: - имя первого сортированного файла
        :param sorted_two: - имя второго сортированного файла
        :return: None
        """
        with open('merged_file.txt', 'w') as merged_file:
            one_line = SmartLine(sorted_one)
            two_line = SmartLine(sorted_two)

            result = ""
            while one_line.data():
                result = result or one_line.data()
                if one_line.key() != two_line.key():
                    merged_file.write(f'{result}\n')
                    result = ""
                    one_line.next()
                elif one_line.key() == two_line.key():
                    values = result.split(' - ')[1].split(', ')
                    new_value = ", ".join(values + [two_line.value()])
                    result = f'{one_line.key()} - {new_value}'
                    two_line.next()

    def run(self):
        """
        Вызывает все вспомогательные методы и делают итоговую работу
        После выполнения, в папке образуется файл merged_file.txt который содержит результат работы
        :return: None
        """
        splitted_files = Merger.split_sort_file(self.file_one)
        Merger.mergesort(splitted_files, 's_ ' + self.file_one)

        splitted_files = Merger.split_sort_file(self.file_two)
        Merger.mergesort(splitted_files, 's_' + self.file_two)

        Merger.merge('s_ ' + self.file_one, 's_' + self.file_two)

        clear_tmp_directory(Merger.tmp_dir)
