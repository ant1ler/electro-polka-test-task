import sys
sys.path.insert(0, ".")

from src.classifier import validate, fallback_rules


def test_validate_correct_json():
    """Правильный JSON проходит валидацию без изменений."""
    
    result = {
        "file": "001.txt",
        "department": "logistics",
        "priority_draft": "urgent",
        "order_id_raw": "TD-48213",
        "order_id_normalized": "48213",
        "needs_order_lookup": False,
        "mentions_double_charge": False,
        "topics": [
            {"department": "logistics", "category": "delay", "is_primary": True}
        ],
        "is_multi_topic": False,
        "has_legal_threat": False,
        "summary": "Просрочка доставки"
    }
    filename = result["file"]
    validated = validate(result, filename)
    assert validated["department"] == "logistics"
    assert validated["priority_draft"] == "urgent"
    print("Правильный JSON прошёл валидацию")


def test_validate_missing_field():
    """Отсутствие обязательного поля — ValueError."""
    
    result = {"file": "001.txt"}
    filename = result["file"]
    try:
        validate(result, filename)
        assert False, "Должен был быть ValueError"
    except ValueError as e:
        print(f"ValueError для отсутствующего поля: {e}")


def test_validate_bad_department():
    """Отдел не из списка - manual."""
    
    result = {
        "file": "001.txt",
        "department": "Доставка",  # русское, не из списка
        "priority_draft": "urgent",
        "order_id_raw": None,
        "order_id_normalized": None,
        "needs_order_lookup": True,
        "mentions_double_charge": False,
        "topics": [],
        "is_multi_topic": False,
        "has_legal_threat": False,
        "summary": "Тест"
    }
    filename = result["file"]
    validated = validate(result, filename)
    assert validated["department"] == "manual"
    print("Плохой отдел заменён на manual")


def test_validate_bad_priority():
    """Приоритет не из списка - normal."""
    
    result = {
        "file": "001.txt",
        "department": "logistics",
        "priority_draft": "high",  # не из списка
        "order_id_raw": None,
        "order_id_normalized": None,
        "needs_order_lookup": True,
        "mentions_double_charge": False,
        "topics": [],
        "is_multi_topic": False,
        "has_legal_threat": False,
        "summary": "Тест"
    }
    filename = result["file"]
    validated = validate(result, filename)
    assert validated["priority_draft"] == "normal"
    print("Плохой приоритет заменён на normal")


def test_validate_empty_topics():
    """Пустой topics - заглушка manual/unclear."""
    
    result = {
        "file": "001.txt",
        "department": "logistics",
        "priority_draft": "urgent",
        "order_id_raw": None,
        "order_id_normalized": None,
        "needs_order_lookup": True,
        "mentions_double_charge": False,
        "topics": [],
        "is_multi_topic": False,
        "has_legal_threat": False,
        "summary": "Тест"
    }
    filename = result["file"]
    validated = validate(result, filename)
    assert len(validated["topics"]) == 1
    assert validated["topics"][0]["department"] == "manual"
    assert validated["topics"][0]["category"] == "unclear"
    print("Пустой topics заменён на manual/unclear")


def test_validate_needs_order_lookup():
    """needs_order_lookup согласуется с order_id_normalized."""
    
    result = {
        "file": "001.txt",
        "department": "logistics",
        "priority_draft": "urgent",
        "order_id_raw": "TD-48213",
        "order_id_normalized": "48213",
        "needs_order_lookup": True,  # неправильно
        "mentions_double_charge": False,
        "topics": [
            {"department": "logistics", "category": "delay", "is_primary": True}
        ],
        "is_multi_topic": False,
        "has_legal_threat": False,
        "summary": "Тест"
    }
    filename = result["file"]
    validated = validate(result, filename)
    assert validated["needs_order_lookup"] is False
    print("needs_order_lookup согласован с order_id_normalized")


def test_validate_is_multi_topic():
    """is_multi_topic согласуется с len(topics)."""
    
    result = {
        "file": "022.txt",
        "department": "warranty",
        "priority_draft": "urgent",
        "order_id_raw": "TD-48252",
        "order_id_normalized": "48252",
        "needs_order_lookup": False,
        "mentions_double_charge": False,
        "topics": [
            {"department": "warranty", "category": "defect", "is_primary": True},
            {"department": "finance", "category": "bonus_missing", "is_primary": False}
        ],
        "is_multi_topic": False,  # неправильно
        "has_legal_threat": False,
        "summary": "Тест"
    }
    filename = result["file"]
    validated = validate(result, filename)
    assert validated["is_multi_topic"] is True
    print("is_multi_topic согласован с len(topics)")


def test_validate_empty_summary():
    """Пустой summary → заглушка."""
    
    result = {
        "file": "001.txt",
        "department": "logistics",
        "priority_draft": "urgent",
        "order_id_raw": None,
        "order_id_normalized": None,
        "needs_order_lookup": True,
        "mentions_double_charge": False,
        "topics": [
            {"department": "logistics", "category": "delay", "is_primary": True}
        ],
        "is_multi_topic": False,
        "has_legal_threat": False,
        "summary": ""
    }
    filename = result["file"]
    validated = validate(result, filename)
    assert validated["summary"] == "Описание отсутствует"
    print("Пустой summary заменён на заглушку")


def test_fallback_rules_logistics():
    """fallback_rules определяет logistics."""
    
    result = fallback_rules("Где мой заказ TD-48213?", "001.txt")
    assert result["department"] == "logistics"
    print("fallback_rules: logistics")


def test_fallback_rules_finance():
    """fallback_rules определяет finance."""
    
    result = fallback_rules("Двойное списание денег", "002.txt")
    assert result["department"] == "finance"
    print("fallback_rules: finance")


def test_fallback_rules_warranty():
    """fallback_rules определяет warranty."""
    
    result = fallback_rules("Товар сломался, не работает", "003.txt")
    assert result["department"] == "warranty"
    print("fallback_rules: warranty")


def test_fallback_rules_tech():
    """fallback_rules определяет tech."""
    
    result = fallback_rules("Как настроить роутер?", "020.txt")
    assert result["department"] == "tech"
    print("fallback_rules: tech")


def test_fallback_rules_manual():
    """fallback_rules определяет manual."""
    
    result = fallback_rules("Спасибо за всё!", "018.txt")
    assert result["department"] == "manual"
    print("fallback_rules: manual")


def test_fallback_rules_has_threat():
    """fallback_rules определяет угрозу."""
    
    result = fallback_rules("Подаю в суд и Роспотребнадзор", "019.txt")
    assert result["has_legal_threat"] is True
    print("fallback_rules: угроза найдена")
    