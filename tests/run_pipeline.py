import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.email_reader import read_all
from src.classifier import classify
from src.orders import load_orders, enrich


def run_pipeline(filenames):
    """Прогоняет указанные файлы через всю цепочку."""
    
    all_emails = read_all("data/inbox")
    emails_by_name = {e["filename"]: e for e in all_emails}
    
    orders = load_orders("data/orders.json")
    
    results = []
    
    for filename in filenames:
        print(f"\n{'=' * 70}")
        print(f"ФАЙЛ: {filename}")
        print('=' * 70)
        
        email = emails_by_name.get(filename)
        if not email:
            print(f"Файл {filename} не найден")
            continue
        
        print(f"\nТЕКСТ ПИСЬМА:")
        print(email["text"][:500] + ("..." if len(email["text"]) > 500 else ""))
        
        
        print(f"\nКЛАССИФИКАЦИЯ (GigaChat):")
        classified = classify(email["text"], filename)
        print(json.dumps(classified, ensure_ascii=False, indent=2))
        
        
        print(f"\nОБОГАЩЕНИЕ (orders.json):")
        enriched = enrich(classified, orders)
        print(json.dumps(enriched, ensure_ascii=False, indent=2))
        
        results.append(enriched)
    
    return results


if __name__ == "__main__":
    test_files = ["011.txt", "001.txt", "009.txt", "007.txt"]
    run_pipeline(test_files)