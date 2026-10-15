import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.email_reader import read_all
from src.classifier import classify
from src.orders import load_orders, enrich
from src.summary import refine_priority, make_summary, save_results


def run_pipeline(test_files=None):
    """Полный прогон всей цепочки."""
    
    all_emails = read_all("data/inbox")
    
    if test_files:
        emails = [e for e in all_emails if e["filename"] in test_files]
    else:
        emails = all_emails
    
    print(f"Загружено писем: {len(emails)}")
    
    # 3. Загружаем заказы
    orders = load_orders("data/orders.json")
    print(f"Загружено заказов: {len(orders)}")
    
    # 4. Первый проход — классификация
    print(f"\nПервый проход (GigaChat-2)...")
    classified = []
    for e in emails:
        print(f"   Классифицирую: {e['filename']}")
        c = classify(e["text"], e["filename"])
        c["text"] = e["text"]  # сохраняем текст для второго прохода
        classified.append(c)
    
    # 5. Обогащение
    print(f"\nОбогащение (orders.json)...")
    enriched = [enrich(e, orders) for e in classified]
    
    # 6. Второй проход — refine
    print(f"\nВторой проход (GigaChat-2-Max)...")
    refined = []
    for e in enriched:
        print(f"   Ревью: {e.get('file', '?')}")
        refined.append(refine_priority(e))
    
    # 7. Сводка
    print(f"\nФормирование сводки...")
    summary = make_summary(refined)
    
    # 8. Сохранение
    print(f"\nСохранение результатов...")
    save_results(refined, summary, suffix="_run_ppl")
    
    # 9. Вывод сводки
    print("\n" + "=" * 70)
    print("СВОДКА")
    print("=" * 70)
    print(summary)
    
    return refined, summary


if __name__ == "__main__":
    # Тестовый прогон на 4 файлах
    test_files = ["011.txt", "001.txt", "009.txt", "007.txt"]
    run_pipeline(test_files)