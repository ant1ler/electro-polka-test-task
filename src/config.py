import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv() # для загрузки ключа в окружение

# Пути для основных файлов
BASE_DIR = Path(__file__).resolve().parent.parent
INBOX_DIR = BASE_DIR / "data" / "inbox"
ORDERS_FILE = BASE_DIR / "data" / "orders.json"
OUTPUT_DIR = BASE_DIR / "output"

# Текущая для задания дата
CURRENT_DATE = "2026-10-12"

# Данные для классификации Гигачатом
DEPARTMENTS = ["logistics", "finance", "warranty", "tech", "manual"]
DEPARTMENTS_RU = {
    "logistics": "Логистика",
    "finance": "Финансы",
    "warranty": "Гарантия",
    "tech": "Техподдержка",
    "manual": "Ручная обработка"
}

PRIORITIES = ["critical", "urgent", "normal"]
PRIORITY_RU = {
    "critical": "Критично",
    "urgent": "Срочно",
    "normal": "Обычное"
}

CATEGORIES = {
    "logistics": ["status", "delay", "reschedule", "address_change", "pickup"],
    "finance": ["double_charge", "payment_pending", "refund_missing", "refund_request", "bonus_missing"],
    "warranty": ["defect", "damage_delivery", "wrong_item", "return_request", "warranty_info", "warranty_document"],
    "tech": ["setup", "instruction"],
    "manual": ["spam", "duplicate", "unclear", "feedback"]
}

CATEGORIES_RU = {
    "status": "Статус заказа",
    "delay": "Просрочка",
    "reschedule": "Перенос доставки",
    "address_change": "Смена адреса",
    "pickup": "Самовывоз",
    "double_charge": "Двойное списание",
    "payment_pending": "Оплата зависла",
    "refund_missing": "Возврат не пришёл",
    "refund_request": "Запрос возврата",
    "bonus_missing": "Бонусы не начислены",
    "defect": "Брак",
    "damage_delivery": "Повреждение при доставке",
    "wrong_item": "Не тот товар",
    "return_request": "Запрос обмена/возврата",
    "warranty_info": "Вопрос про гарантию",
    "warranty_document": "Гарантийный талон",
    "setup": "Настройка",
    "instruction": "Инструкция",
    "spam": "Спам",
    "duplicate": "Дубликат",
    "unclear": "Непонятно",
    "feedback": "Благодарность"
}

# Настройки Гигачатаы
GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")
os.environ["GIGACHAT_CREDENTIALS"] = GIGACHAT_CREDENTIALS

GIGACHAT_MODEL = "GigaChat-2"
GIGACHAT_SCOPE = "GIGACHAT_API_PERS"
VERIFY_SSL_CERTS = False
GIGACHAT_TIMEOUT = 120

if __name__ == "__main__":
    print(f"INBOX_DIR: {INBOX_DIR}")
    print(f"GIGACHAT_CREDENTIALS: {'OK' if GIGACHAT_CREDENTIALS else 'НЕ НАЙДЕН'}")
    print(f"Длина: {len(GIGACHAT_CREDENTIALS)}")
    print(f"Начало: '{GIGACHAT_CREDENTIALS[:10]}'")
    print(f"Конец: '{GIGACHAT_CREDENTIALS[-10:]}'")
    print(f"Есть пробелы: {GIGACHAT_CREDENTIALS != GIGACHAT_CREDENTIALS.strip()}")