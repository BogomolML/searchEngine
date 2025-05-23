# indexer.py

from re import findall
from pathlib import Path
from collections import defaultdict
from math import log

from logic.singleton import singleton


@singleton
class Indexer:
    _PATTERN = '\\documents\\'

    def __init__(self):
        deletions, marks = self._read_init_files()
        self._inverted_index = defaultdict(dict)
        self._deletions = frozenset(deletions)
        self._punctuation_marks = frozenset(marks)
        self._path_to_docs = self._get_path_to_docs()
        self._doc_lengths: dict = {}

    def build_index(self):
        for file in self._path_to_docs.glob('*.txt'):
            words = self._tokenize(file)
            word_counts = self._count_words(words)

            for word, count in word_counts.items():
                filename = str(file).split(self._PATTERN)[-1]
                self._inverted_index[word][filename] = count
                self._doc_lengths[filename] = len(words)

    def rebuild_index(self):
        self.__init__()
        self.build_index()

    @staticmethod
    def _read_init_files():
        with open('logic/data/deletions.txt', 'r', encoding='utf-8') as file:
            deletions = file.readline().split()
        with open('logic/data/marks.txt', 'r', encoding='utf-8') as file:
            marks = file.readline().split()
        return deletions, marks

    @staticmethod
    def _get_path_to_docs():
        path = Path(__file__).parent.parent
        directors_names = [d.name for d in path.iterdir() if d.is_dir()]
        if 'documents' not in directors_names:
            raise PermissionError('No folder "documents"')
        else:
            return path / 'documents'

    def _get_text_form_files(self, doc):
        with open(doc, 'r', encoding='utf-8') as file:
            text = file.read().lower()
        for mark in self._punctuation_marks:
            text.replace(mark, '')
        return text

    def _tokenize(self, file_path):
        sorted_words: list = []
        text = self._get_text_form_files(file_path)
        words = findall(r'\b\w+\b', text)
        for word in words:
            if word not in self._deletions:
                sorted_words.append(word)
        return sorted_words

    @staticmethod
    def _count_words(words):
        word_counts = defaultdict(int)
        for word in words:
            word_counts[word] += 1
        return word_counts

    def calc_tf_idf(self, word, doc):
        tf = self._inverted_index[word][doc] / self._doc_lengths[doc]
        idf = log(len(self._doc_lengths) / len(self._inverted_index[word]))
        return round(tf * idf, 4)

    @property
    def inverted_index(self):
        return self._inverted_index
