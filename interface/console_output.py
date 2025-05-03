# console_output.py

from keyboard import is_pressed

from logic.indexer import Indexer
from logic.searching import Searcher
from logic.singleton import singleton
from interface.font import Font


@singleton
class ConsoleInterface:
    def __init__(self):
        self._update_idx = Indexer()
        self._update_idx.build_index()
        self._searcher = Searcher()

    def menu(self):
        while True:
            self._searcher.__init__()
            print('\nНажмите цифру на клавиатуре, чтобы выбрать')
            print(f'{Font.GREEN}[1]{Font.END} Обновить индекс')
            print(f'{Font.GREEN}[2]{Font.END} Поиск')
            print(f'{Font.GREEN}[3]{Font.END} Выход')
            while True:
                if is_pressed('1'):
                    self._update_idx.build_index()
                    break
                elif is_pressed('2'):
                    request = input('Введите запрос: ')
                    result = self._searcher.search(request)
                    print(result)
                    break
                elif is_pressed('3'):
                    exit()
