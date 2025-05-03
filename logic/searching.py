# searching.py

from logic.indexer import Indexer
# from interface.progress_bar import Progress
from interface.font import Font


class Searcher:
    def __init__(self):
        self._request: str = ''
        self._presorted_docs: dict = {}
        self._indexer = Indexer()
        # self._progress = Progress()
        self._words_dict = self._indexer.inverted_index

    def search(self, request):
        self._request = request
        oper = False
        try:
            words = self._request.split()
            request_length = len(words)
            if request_length == 3:
                oper = words[1].upper()
                words.pop(1)
            elif request_length == 0:
                result = 'Вы ввели пустой запрос'
                return result
            elif request_length > 3:
                result = 'Ошибка обработки запроса'
                return result

            result = self._create_result(words, oper)
            # self._progress.show_progress(total=len(self._presorted_docs))
            for i, doc_path in enumerate(self._presorted_docs.values(), 1):
                pass
                # self._progress.update_progress()
            return result
        except ValueError as err:
            raise err
        finally:
            pass
            # self._progress.close_progress()

    def _create_result(self, words, oper):
        docs = set()
        if not oper:
            for el in list(self._words_dict[words[0]].keys()):
                docs.add(el)
        elif oper == 'И' or oper == 'AND':
            docs1 = set()
            docs2 = set()
            for el in list(self._words_dict[words[0]].keys()):
                docs1.add(el)
            for el in list(self._words_dict[words[0]].keys()):
                docs2.add(el)
            for doc1 in docs1:
                for doc2 in docs2:
                    if doc1 == doc2:
                        docs.add(doc1)
        elif oper == 'ИЛИ' or oper == 'OR':
            for word in words:
                doc = self._words_dict[word].keys()
                for el in doc:
                    docs.add(el)
        docs = self._sorting_by_relevance(words, list(docs), oper)

        result = f'Найдено {Font.GREEN}{len(docs)}{Font.END} документов:\n'
        for i in range(len(docs)):
            for k, v in self._presorted_docs.items():
                if v == docs[i]:
                    rel = k
                    result += f'{Font.GREEN}{i+1}{Font.END}. {docs[i]} (релевантность {rel})\n'
        return result

    def _sorting_by_relevance(self, words, docs, oper):
        sorted_docs: list = []
        final_rel: float = 0
        for i in range(len(docs)):
            for j in range(len(words)):
                relevance = self._indexer.calc_tf_idf(words[j], docs[i])
                if oper == 'И' or oper == 'AND':
                    final_rel += relevance
                elif oper == 'ИЛИ' or oper == 'OR':
                    final_rel = max(final_rel, relevance)
                else:
                    final_rel = relevance
                self._presorted_docs[final_rel] = docs[i]
        sorted_rels: list = sorted(self._presorted_docs.keys(), reverse=True)
        for key in sorted_rels:
            sorted_docs.append(self._presorted_docs[key])
        return sorted_docs
