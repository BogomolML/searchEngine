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

    def interface_output(self):
        while True:
            self._searcher.__init__()
            self._menu()
            self._get_request()

    def _get_request(self):
        while True:
            if is_pressed('1'):
                print('pressed 1')
                self._update_idx.rebuild_index()
                break
            elif is_pressed('2'):
                request = input('Введите запрос: ')
                print(request)
                result = self._searcher.search(request)
                print(result)
                break
            elif is_pressed('esc'):
                exit()
            elif is_pressed('5'):
                r = input()
                print(len(self._update_idx.inverted_index[r]))
                print(self._update_idx.inverted_index[r])
                break

    @staticmethod
    def _menu():
        print('\nНажмите клавишу на клавиатуре, чтобы выбрать')
        print('(ВАЖНО) Для корректной работы программы уберите курсор из терминала при выборе действия')
        print(f'{Font.GREEN}[1]{Font.END} Обновить индекс')
        print(f'{Font.GREEN}[2]{Font.END} Поиск')
        print(f'{Font.GREEN}[ESC]{Font.END} Выход')
