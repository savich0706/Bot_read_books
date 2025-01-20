import os
import sys


BOOK_PATH = 'book/book.txt'
book: dict[int, str] = {}
PAGE_SIZE = 900

# Функция возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    ch = ',.!:;?'
    real_size = size
    if len(text) <= size+start:
        real_size = len(text)-start
    else:
        for i in range(size+start-1, start, -1):
            if text[i] in ch and text[i+1] not in ch:
                break
            real_size -= 1
    return text[start: start + real_size], real_size

# функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(path, mode='r', encoding='utf-8-sig') as file:
        text = file.read().lstrip()
        start = 0
        i = 1
        while text:
            data, ind = _get_part_text(text, start, PAGE_SIZE)
            book[i] = data.lstrip(' \t\n\r')
            i += 1
            text = text[ind:]

# Вызов функции prepair_book 
# для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))

if __name__ == '__main__':
    prepare_book(BOOK_PATH)
    print(book[2])