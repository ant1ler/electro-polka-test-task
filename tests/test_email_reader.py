import sys
sys.path.insert(0, ".")

from src.email_reader import read_all


def test_read_all_returns_list():
    """read_all возвращает список."""
    
    emails = read_all("data/inbox")
    assert isinstance(emails, list)
    print(f"read_all вернул список из {len(emails)} элементов")


def test_read_all_not_empty():
    """read_all находит письма."""
    
    emails = read_all("data/inbox")
    assert len(emails) > 0
    print(f"Найдено писем: {len(emails)}")


def test_email_structure():
    """Каждое письмо имеет filename и text."""
    
    emails = read_all("data/inbox")
    for email in emails:
        assert "filename" in email
        assert "text" in email
        assert isinstance(email["filename"], str)
        assert isinstance(email["text"], str)
    print("Все письма имеют поля filename и text")


def test_skip_empty_files():
    """Пустой файл (010.txt) пропущен."""
    
    emails = read_all("data/inbox")
    filenames = [e["filename"] for e in emails]
    assert "010.txt" not in filenames
    print("Пустой файл 010.txt пропущен")


def test_all_txt():
    """Все файлы — .txt."""
    
    emails = read_all("data/inbox")
    for email in emails:
        assert email["filename"].endswith(".txt")
    print("Все файлы .txt")


def test_text_not_empty():
    """Текст каждого письма не пустой."""
    
    emails = read_all("data/inbox")
    for email in emails:
        assert email["text"].strip()
    print("Текст всех писем не пустой")
