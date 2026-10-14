from datetime import datetime
import json

def load_orders(orders_path = "data/orders.json"):
    '''Загружает заказы из orders.json и создает список'''
    
    with open(orders_path, 'r', encoding = 'utf-8') as file:
        return json.load(file)
    
def find_order(orders, order_id_normalized):
    '''Находит заказ в orders.json по order_id из json от Гигачата'''
    
    for order in orders:
        normalized = "".join(filter(str.isdigit, order["order_id"]))
        if normalized == order_id_normalized:
            return order
    return None

def calculate_overdue(expected_delivery):
    '''Считает просрочку заказа'''
    
    if not expected_delivery:
        return 0
    
    expected = datetime.strptime(expected_delivery, '%Y-%m-%d').date()
    today = datetime(2026, 10, 12).date()

    if today > expected:
        return (today - expected).days
    return 0

def enrich(email, orders):
    '''Добавляет в json от Гигачата данные из orders.json'''
    
    order_id = email.get('order_id_normalized')
    
    if not order_id:
        email["order_status"] = None
        email["expected_delivery"] = None
        email["delivered_at"] = None
        email["days_overdue"] = 0
        return email
    
    order = find_order(orders, order_id)
    
    if not order:
        email['order_status'] = 'не найден'
        email["expected_delivery"] = None
        email["delivered_at"] = None
        email["days_overdue"] = 0
        return email
    
    email['order_status'] = order.get('status')
    email['expected_delivery'] = order.get('expected_delivery')
    email['delivered_at'] = order.get('delivered_at')
    
    if order.get("delivered_at"):
        email["days_overdue"] = 0
    else:
        email["days_overdue"] = calculate_overdue(order.get("expected_delivery"))
    
    return email


if __name__ == "__main__":
    orders = load_orders("data/orders.json")
    print(f"Загружено заказов: {len(orders)}")
    
    test_email = {"filename": "001.txt", "order_id_normalized": "48213"}
    enriched = enrich(test_email, orders)
    print(enriched)