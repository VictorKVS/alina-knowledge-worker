"""Учебный лексический поиск для первого курса. Не LLM и не полноценный RAG."""
import re
import sys

DOCUMENTS = [
    ("rag", "RAG ищет информацию в документах и передает найденные фрагменты модели для ответа."),
    ("gpu", "Видеопамять GPU для инференса зависит от весов модели, KV cache, длины контекста и пакетирования."),
    ("security", "Безопасный агент обязан проверять полномочия перед вызовом инструмента и журналировать действия."),
]

STOP = {"что", "такое", "как", "это", "для", "и", "на", "в", "по", "о", "ли", "мне"}

def tokenize(text):
    return {w for w in re.findall(r"[a-zа-яё0-9]+", text.lower()) if len(w) > 1 and w not in STOP}

def search(question, documents=DOCUMENTS):
    words = tokenize(question)
    if not words:
        return []
    scored = []
    for doc_id, body in documents:
        matches = len(words & tokenize(body))
        if matches:
            scored.append((matches, doc_id, body))
    return sorted(scored, key=lambda x: (-x[0], x[1]))

def main():
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        print("Пример: python search.py 'Что такое RAG?'")
        return
    hits = search(question)
    if not hits:
        print("Источник не найден. Нельзя придумывать факты.")
        return
    for score, doc_id, body in hits:
        print(f"[{doc_id}] score={score}: {body}")

if __name__ == "__main__":
    main()
