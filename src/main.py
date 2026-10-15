"""Точка входа: запуск пайплайна обработки обращений."""

import argparse
from src.email_reader import read_all
from src.classifier import classify
from src.orders import load_orders, enrich
from src.summary import refine_priority, make_summary, save_results
from src.config import INBOX_DIR, ORDERS_FILE


def run_pipeline(test_files=None, suffix=""):
    """Полный прогон всей цепочки действий."""
    
    all_emails = read_all(INBOX_DIR)
    
    if test_files:
        emails = [e for e in all_emails if e["filename"] in test_files]
    else:
        emails = all_emails
    
    print(f"Загружено писем: {len(emails)}")
    
    orders = load_orders(ORDERS_FILE)
    print(f"Загружено заказов: {len(orders)}")
    
    print(f"\nПервый проход (GigaChat-2)...")
    classified = []
    for e in emails:
        print(f"   Классифицирую: {e['filename']}")
        c = classify(e["text"], e["filename"])
        c["text"] = e["text"]
        classified.append(c)
    
    print(f"\nОбогащение (orders.json)...")
    enriched = [enrich(e, orders) for e in classified]
    

    print(f"\nВторой проход (GigaChat-2-Max)...")
    refined = []
    for e in enriched:
        print(f"   Ревью: {e.get('file', '?')}")
        refined.append(refine_priority(e))
    

    print(f"\nФормирование сводки...")
    summary = make_summary(refined)
    

    print(f"\nСохранение результатов...")
    save_results(refined, summary, suffix=suffix)
    


def main():
    """Парсит флаги и запускает пайплайн."""
    
    parser = argparse.ArgumentParser(
        description="Обработка обращений в поддержку интернет-магазина"
    )
    parser.add_argument(
        "--agent",
        action="store_true",
        help="Использовать агентный подход (GigaChat-2-Max)"
    )
    parser.add_argument(
        "--test",
        nargs="+",
        help="Список файлов для тестового прогона (например: --test 001.txt 007.txt)"
    )
    parser.add_argument(
        "--suffix",
        default="",
        help="Суффикс для имён файлов (например: --suffix _test)"
    )
    
    args = parser.parse_args()
    
    if args.agent:
        from src.agent import run_agent
        run_agent()
    else:
        run_pipeline(test_files=args.test, suffix=args.suffix)

if __name__ == "__main__":
    main()