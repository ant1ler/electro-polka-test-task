import sys
sys.path.insert(0, ".")

from src.orders import load_orders, find_order, calculate_overdue, enrich


def test_load_orders():
    """Загружает заказы из orders.json."""
    
    orders = load_orders("data/orders.json")
    assert len(orders) > 0
    assert isinstance(orders, list)
    print(f"Загружено заказов: {len(orders)}")


def test_find_order_found():
    """Находит заказ по нормализованному номеру."""
    
    orders = load_orders("data/orders.json")
    order = find_order(orders, "48213")
    assert order is not None
    assert order["order_id"] == "TD-48213"
    print(f"Заказ 48213 найден: {order['status']}")


def test_find_order_not_found():
    """Возвращает None для несуществующего заказа."""
    
    orders = load_orders("data/orders.json")
    order = find_order(orders, "99999")
    assert order is None
    print("Заказ 99999 не найден (ожидаемо)")


def test_calculate_overdue():
    """Считает просрочку: 2026-10-03 - 2026-10-12 = 9 дней."""
    
    days = calculate_overdue("2026-10-03")
    assert days == 9
    print(f"Просрочка для 2026-10-03: {days} дней")


def test_calculate_overdue_not_overdue():
    """Не просрочен — 0 дней."""
    
    days = calculate_overdue("2026-10-15")
    assert days == 0
    print("Заказ не просрочен (0 дней)")


def test_calculate_overdue_no_date():
    """Нет даты — 0 дней."""
    
    days = calculate_overdue(None)
    assert days == 0
    print("Нет даты — 0 дней")


def test_enrich_with_order():
    """Обогащает письмо данными из заказа."""
    
    orders = load_orders("data/orders.json")
    email = {"file": "001.txt", "order_id_normalized": "48213"}
    enriched = enrich(email, orders)
    
    assert enriched["order_status"] == "shipped"
    assert enriched["days_overdue"] == 9
    print(f"Обогащено: статус={enriched['order_status']}, просрочка={enriched['days_overdue']}")


def test_enrich_no_order_id():
    """Письмо без номера заказа — поля None, просрочка 0."""
    
    orders = load_orders("data/orders.json")
    email = {"file": "004.txt", "order_id_normalized": None}
    enriched = enrich(email, orders)
    
    assert enriched["order_status"] is None
    assert enriched["days_overdue"] == 0
    print("Письмо без номера — поля None, просрочка 0")


def test_enrich_order_not_found():
    """Заказ не найден — order_status='не найден'."""
    
    orders = load_orders("data/orders.json")
    email = {"file": "014.txt", "order_id_normalized": "99999"}
    enriched = enrich(email, orders)
    
    assert enriched["order_status"] == "не найден"
    assert enriched["days_overdue"] == 0
    print("Заказ не найден — пометка 'не найден'")

def test_enrich_total():
    """total добавляется из заказа."""
    
    orders = load_orders("data/orders.json")
    email = {"file": "001.txt", "order_id_normalized": "48213"}
    enriched = enrich(email, orders)
    assert enriched["total"] == 11580
    print(f"total: {enriched['total']}")


def test_enrich_tracking_stale():
    """tracking_stale_days считается правильно."""
    
    orders = load_orders("data/orders.json")
    email = {"file": "001.txt", "order_id_normalized": "48213"}
    enriched = enrich(email, orders)
    assert enriched["tracking_stale_days"] == 8
    print(f"tracking_stale_days: {enriched['tracking_stale_days']}")


def test_enrich_payment():
    """payment_status и payment_reserve_until добавляются."""
    
    orders = load_orders("data/orders.json")
    email = {"file": "016.txt", "order_id_normalized": "48244"}
    enriched = enrich(email, orders)
    assert enriched["payment_status"] == "pending"
    assert enriched["payment_reserve_until"] == "2026-10-13"
    print(f"payment: {enriched['payment_status']}, резерв: {enriched['payment_reserve_until']}")


def test_enrich_refund():
    """refund_status и refund_pending_days добавляются."""
    
    orders = load_orders("data/orders.json")
    email = {"file": "017.txt", "order_id_normalized": "48222"}
    enriched = enrich(email, orders)
    assert enriched["refund_status"] == "processing"
    assert enriched["refund_pending_days"] == 22
    print(f"refund: {enriched['refund_status']}, дней: {enriched['refund_pending_days']}")


def test_enrich_items():
    """items добавляется из заказа."""
    
    orders = load_orders("data/orders.json")
    email = {"file": "001.txt", "order_id_normalized": "48213"}
    enriched = enrich(email, orders)
    assert len(enriched["items"]) > 0
    assert enriched["items"][0]["name"] == "Фен Aero Style"
    print(f"items: {len(enriched['items'])} товаров")


def test_enrich_no_order_id_new_fields():
    """Письмо без номера — все новые поля None."""
    
    orders = load_orders("data/orders.json")
    email = {"file": "004.txt", "order_id_normalized": None}
    enriched = enrich(email, orders)
    assert enriched["total"] is None
    assert enriched["payment_status"] is None
    assert enriched["refund_status"] is None
    assert enriched["tracking_stale_days"] is None
    assert enriched["items"] == []
    print("Письмо без номера — новые поля None")


def test_enrich_order_not_found_new_fields():
    """Заказ не найден — все новые поля None."""
    
    orders = load_orders("data/orders.json")
    email = {"file": "014.txt", "order_id_normalized": "99999"}
    enriched = enrich(email, orders)
    assert enriched["total"] is None
    assert enriched["payment_status"] is None
    assert enriched["refund_status"] is None
    print("Заказ не найден — новые поля None")
