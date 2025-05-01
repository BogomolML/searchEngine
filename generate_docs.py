# generate_docs.py
# Код сделан нейросетью

import wikipedia
import re
from tqdm import tqdm
from pathlib import Path
from transliterate import translit

# Настройки
WIKI_LANG = "ru"
MAX_ARTICLES = 140
MAX_SIZE_MB = 10
MAX_FILENAME_LENGTH = 15

# Устанавливаем язык Википедии
wikipedia.set_lang(WIKI_LANG)

# Пути
SCRIPT_DIR = Path(__file__).parent.absolute()
DOCUMENTS_DIR = SCRIPT_DIR / "documents"
DOCUMENTS_DIR.mkdir(exist_ok=True)


def transliterate_filename(text):
    """Транслитерация и очистка названия"""
    # Транслитерация русского текста
    translit_text = translit(text, 'ru', reversed=True)

    # Удаляем все не-ASCII символы и оставляем только буквы/цифры
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', translit_text)

    # Обрезаем до максимальной длины
    return cleaned[:MAX_FILENAME_LENGTH].lower()


def get_random_articles(count):
    """Получаем список случайных статей"""
    print("Получаем список случайных статей...")
    return wikipedia.random(count)


def save_article(title, content):
    """Сохраняем статью с правильным именем файла"""
    filename = transliterate_filename(title) + ".txt"
    filepath = DOCUMENTS_DIR / filename

    if len(content.encode('utf-8')) > MAX_SIZE_MB * 1024 * 1024:
        print(f"Статья '{title}' слишком большая, пропускаем")
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"{title}\n\n{content}")
    return True


def main():
    try:
        articles = get_random_articles(MAX_ARTICLES)
        saved_count = 0

        print(f"Скачиваем и сохраняем статьи в {DOCUMENTS_DIR}...")
        for title in tqdm(articles, desc="Обработка статей"):
            try:
                page = wikipedia.page(title, auto_suggest=False)
                if save_article(title, page.content):
                    saved_count += 1
            except (wikipedia.exceptions.PageError,
                    wikipedia.exceptions.DisambiguationError):
                continue

        print(f"\nУспешно сохранено {saved_count} статей")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
