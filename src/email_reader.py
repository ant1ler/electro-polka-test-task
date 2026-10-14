from pathlib import Path

def read_all(inbox_path = 'data/inbox'):
    '''Читает все доступные письма, отфильтровывает пустые или неверные, возвращает словарь с названием файла и содержимым'''
    
    emails = []
    
    inbox = Path(inbox_path)
    
    for filepath in inbox.iterdir():
        if not filepath.is_file(): # проверяем что это файл
            continue
        if filepath.suffix != '.txt': # проверяем, что формата .txt
            continue
        if filepath.name.startswith('.'): # проверяем, что не начинается с '.'
            continue
        if filepath.stat().st_size == 0: # проверяем, что не пустой
            continue
        
        raw = filepath.read_bytes() # обрабатываем все файлы байтово, так как один был в кодировке cp1251
        
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = raw.decode("cp1251")
            except UnicodeDecodeError:
                text = raw.decode("utf-8", errors="replace")

        if not text.strip(): # удаляем пробелы вначала и конце и проверяем размер
            continue
        
        emails.append({ #добавляем в словарь нужные файлы
            "filename" : filepath.name,
            "text" : text
        })
        
    return emails

if __name__ == "__main__":
    emails = read_all()
    print(f"Найдено писем: {len(emails)}")