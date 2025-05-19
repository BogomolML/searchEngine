# searching.py

from logic.indexer import Indexer
from interface.font import Font


class Searcher:
    OPERATORS = ['AND', 'OR', 'И', 'ИЛИ']

    def __init__(self):
        self._operator = None
        self._presorted_docs: dict = {}
        self._sorted_docs: list = []
        self._indexer = Indexer()
        self._words_dict = self._indexer.inverted_index

    def search(self, request):
        words: list = request.split()
        result = self._processing_request(words)
        return result

    def _processing_request(self, words):
        if len(words) == 3:
            self._operator = words[1].upper()
            if self._operator not in self.OPERATORS:
                return 'Ошибка обработки запроса'
            words.pop(1)
        elif len(words) == 0:
            return 'Вы ввели пустой запрос'
        elif len(words) > 3:
            return 'Ошибка обработки запроса'
        self._preparation_docs(words)
        result = self._create_result()
        return result

    def _preparation_docs(self, words):
        docs = self._check_operator(words)
        self._sorting_by_relevance(words, list(docs))

    def _create_result(self):
        if len(self._sorted_docs) == 0:
            return 'Документов не найдено'
        result = f'Найдено {Font.GREEN}{len(self._sorted_docs)}{Font.END} документов:\n'
        for i in range(len(self._sorted_docs)):
            rel = self._presorted_docs[self._sorted_docs[i]]
            result += f'{Font.GREEN}{i+1}{Font.END}. {self._sorted_docs[i]} (релевантность {rel})\n'
        return result

    def _check_operator(self, words):
        docs = set()
        if self._operator is None:
            for el in list(self._words_dict[words[0]].keys()):
                docs.add(el)
        elif self._operator == 'И' or self._operator == 'AND':
            docs = self._get_docs_for_and(docs, words)
        elif self._operator == 'ИЛИ' or self._operator == 'OR':
            docs = self._get_docs_for_or(docs, words)
        return docs

    def _get_docs_for_and(self, docs, words):
        docs1 = set(list(self._words_dict[words[0]].keys()))
        docs2 = set(list(self._words_dict[words[1]].keys()))
        for doc1 in docs1:
            for doc2 in docs2:
                if doc1 == doc2:
                    docs.add(doc1)
                    continue
        return docs

    def _get_docs_for_or(self, docs, words):
        for word in words:
            doc = self._words_dict[word].keys()
            for el in doc:
                docs.add(el)
        return docs

    def _sorting_by_relevance(self, words, docs):
        for i in range(len(docs)):
            self._get_presorted_docs(docs, i, words)
        sorted_rels: list = sorted(self._presorted_docs.values(), reverse=True)
        keys = list(self._presorted_docs.keys())
        values = list(self._presorted_docs.values())
        for val in sorted_rels:
            self._sorted_docs.append(keys[values.index(val)])

    def _get_presorted_docs(self, docs, i, words):
        final_relevance: float = 0
        for j in range(len(words)):
            try:
                relevance = self._indexer.calc_tf_idf(words[j], docs[i])
            except KeyError:
                continue
            final_relevance = self._get_final_relevance(final_relevance, relevance)
            self._presorted_docs[docs[i]] = final_relevance

    def _get_final_relevance(self, final_relevance, relevance):
        if self._operator == 'И' or self._operator == 'AND':
            final_relevance += relevance
        elif self._operator == 'ИЛИ' or self._operator == 'OR':
            final_relevance = max(final_relevance, relevance)
        else:
            final_relevance = relevance
        final_relevance = round(final_relevance, 4)
        return final_relevance
