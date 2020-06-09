import string
import random

from timer import Timer

# такое количество строк, в сочетании с длиной строки в +/- 100 символов даёт около 500мб итоговые файлы
LINE_CNT = 4000000
MAX_STRING_SIZE = 100

# генерирует рандомную длину строки, от 5 до 100 символов
# PS Лямбды - не хорошо, но иногда очень хочется
RANDOM_SIZE = lambda max_v: random.randint(5, max_v)

# набор символов для рандомной генерации
RANDOMIZE_STRING = string.ascii_uppercase + string.digits + string.ascii_lowercase

with Timer():  # засекаем время
    # открываем 2 файла на запись
    with open('file_one.txt', "w") as file_one, open('file_two.txt', "w") as file_two:
        for i in range(LINE_CNT):
            key_size = RANDOM_SIZE(MAX_STRING_SIZE)
            key = ''.join(random.choice(RANDOMIZE_STRING) for _ in range(key_size))

            value_size = RANDOM_SIZE(MAX_STRING_SIZE)
            value = ''.join(random.choice(RANDOMIZE_STRING) for _ in range(value_size))

            # в первый файл запишем сразу
            file_one.write(f'{key} - {value}\n')

            # а во второй сгенеруем ещё от 0 до 3 значений
            for j in range(random.randint(0, 3)):
                value_size = RANDOM_SIZE(MAX_STRING_SIZE)
                value = ''.join(random.choice(RANDOMIZE_STRING) for _ in range(value_size))
                file_two.write(f'{key} - {value}\n')

            # выполняет довольно таки долго, по этому чтобы видеть что процес не просто завис, вывожу процент выполнения
            if (i / LINE_CNT * 100) % 1 == 0:
                print(f'{i / LINE_CNT * 100}%')
