import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.summary import fallback_refine, make_summary


def test_fallback_refine_critical_overdue():
    """Просрочка > 3 дней - critical."""
    
    email = {"days_overdue": 9, "priority_draft": "urgent"}
    result = fallback_refine(email)
    assert result["final_priority"] == "critical"
    print("Просрочка 9 дней - critical")


def test_fallback_refine_critical_double_charge():
    """Двойное списание - critical."""
    
    email = {"mentions_double_charge": True, "priority_draft": "urgent"}
    result = fallback_refine(email)
    assert result["final_priority"] == "critical"
    print("Двойное списание - critical")


def test_fallback_refine_critical_legal_threat():
    """Угроза суда - critical."""
    
    email = {"has_legal_threat": True, "priority_draft": "urgent"}
    result = fallback_refine(email)
    assert result["final_priority"] == "critical"
    print("Угроза суда - critical")


def test_fallback_refine_critical_payment_pending():
    """Оплата зависла - critical."""
    
    email = {"payment_status": "pending", "priority_draft": "urgent"}
    result = fallback_refine(email)
    assert result["final_priority"] == "critical"
    print("Оплата зависла - critical")


def test_fallback_refine_critical_refund_pending():
    """Возврат идёт > 10 дней - critical."""
    
    email = {"refund_pending_days": 22, "priority_draft": "urgent"}
    result = fallback_refine(email)
    assert result["final_priority"] == "critical"
    print("Возврат 22 дня - critical")


def test_fallback_refine_critical_tracking_stale():
    """Трек молчит > 5 дней - critical."""
    
    email = {"tracking_stale_days": 8, "priority_draft": "urgent"}
    result = fallback_refine(email)
    assert result["final_priority"] == "critical"
    print("Трек молчит 8 дней - critical")


def test_fallback_refine_critical_expensive_damage():
    """Дорогой товар повреждён - critical."""
    
    email = {
        "total": 89990,
        "topics": [{"department": "warranty", "category": "defect", "is_primary": True}],
        "priority_draft": "urgent"
    }
    result = fallback_refine(email)
    assert result["final_priority"] == "critical"
    print("Дорогой товар повреждён - critical")


def test_fallback_refine_urgent_overdue_1_3():
    """Просрочка 1-3 дня - urgent."""
    
    email = {"days_overdue": 2, "priority_draft": "normal"}
    result = fallback_refine(email)
    assert result["final_priority"] == "urgent"
    print("Просрочка 2 дня - urgent")


def test_fallback_refine_urgent_defect():
    """Брак - urgent."""
    
    email = {
        "topics": [{"department": "warranty", "category": "defect", "is_primary": True}],
        "priority_draft": "normal"
    }
    result = fallback_refine(email)
    assert result["final_priority"] == "urgent"
    print("Брак - urgent")


def test_fallback_refine_urgent_tracking_3_5():
    """Трек молчит 3-5 дней - urgent."""
    
    email = {"tracking_stale_days": 4, "priority_draft": "normal"}
    result = fallback_refine(email)
    assert result["final_priority"] == "urgent"
    print("Трек молчит 4 дня - urgent")


def test_fallback_refine_normal():
    """Всё спокойно - normal."""
    
    email = {"priority_draft": "normal"}
    result = fallback_refine(email)
    assert result["final_priority"] == "normal"
    print("Всё спокойно - normal")


def test_make_summary_structure():
    """Сводка содержит ключевые блоки."""
    
    emails = [
        {
            "file": "001.txt",
            "department": "logistics",
            "final_priority": "critical",
            "summary": "Просрочка доставки",
            "next_step": "Связаться немедленно",
            "order_id_normalized": "48213",
            "needs_order_lookup": False,
            "days_overdue": 9,
            "tracking_stale_days": 8
        }
    ]
    summary = make_summary(emails)
    assert "# Сводка обращений" in summary
    assert "### По отделам" in summary
    assert "## КРИТИЧНО" in summary
    assert "Логистика" in summary
    assert "TD-48213" not in summary  # raw нет, есть normalized
    assert "48213" in summary
    print("Структура сводки корректна")


def test_make_summary_empty():
    """Пустой список - сводка без ошибок."""
    
    summary = make_summary([])
    assert "# Сводка обращений" in summary
    assert "Всего писем: 0" in summary
    print("Пустой список обработан")