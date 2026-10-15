"""Инструменты для ИИ-агента на основе GigaChat-2-Max."""

from typing import List, Dict, Any
from langchain_core.tools import tool


@tool
def read_emails() -> List[Dict[str, Any]]:
    """Чтение и фильтрация всех писем из папки data/inbox.
    Возвращает список словарей с полями filename и text."""
    
    from src.email_reader import read_all
    from src.config import INBOX_DIR
    return read_all(INBOX_DIR)


@tool
def get_order_facts(order_id_normalized: str) -> Dict[str, Any]:
    """Обогащение классифицированного JSON фактами из orders.json по нормализованному номеру заказа.
    Принимает номер заказа (только цифры).
    Возвращает словарь с полями: order_status, expected_delivery, delivered_at,days_overdue, total, tracking_stale_days, payment_status, payment_reserve_until, refund_status, refund_pending_days, items."""
    
    from src.orders import load_orders, enrich
    from src.config import ORDERS_FILE
    orders = load_orders(ORDERS_FILE)
    email = {"order_id_normalized": order_id_normalized}
    return enrich(email, orders)


@tool
def save_results(emails: List[Dict[str, Any]], summary: str) -> str:
    """Сохраняет результаты в JSON и Markdown. Принимает список писем и строку сводки. Возвращает пути к сохранённым файлам."""
    
    from src.summary import save_results as save
    return save(emails, summary, suffix="_agent")