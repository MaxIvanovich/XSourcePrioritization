""" Модуль записи результатов в файлы. """

from typing import Dict
from parser import SourceFile


def update_source_file(source: SourceFile, priority_level: str) -> bool:
    """ Обновление исходного файла с соответствующим маркером приоритета.
    
    Args:
        source: Объект файла 
        priority_level: Приоритет ('highest', 'high', 'medium', 'low', 'lowest')
        
    Returns:
        True при удачном обновление, иначе False
    """
    # Маска приоритетов
    markers = {'highest': '🔺',
               'high': '⏫',
               'medium': '🔼',
               'low': '🔽',
               'lowest': '⏬'}
    
    # Получение соответствующего маркера
    marker = markers.get(priority_level)
    if not marker:
        return False  # Некорректный уровень приоритета
    
    # Определение статуса чек-бокса опираясь на приоритет
    # highest получает [/], остальные получают [ ]
    if priority_level == 'highest':
        new_checkbox = '- [/]'
    else:
        new_checkbox = '- [ ]'
    
    # Формирование новой строки заголовка
    # Удаление чек-бокса
    original_title = source.title
    if original_title.startswith('- [ ]') or original_title.startswith('- [/]'):
        # Извлечение строки сразу за чек-боксом
        content_part = original_title[5:].strip()
    else:
        content_part = original_title.strip()
    
    new_title = f"{new_checkbox} {content_part} {marker}".strip()
    
    try:
        # Чтение содержимого текущего файла
        content = source.path.read_text(encoding='utf-8')
        
        # Разбивка содержимого по строкам
        lines = content.split('\n')
        
        # Определение и замена строки заголовка
        updated_lines = []
        title_replaced = False
        
        # Пропуск метаданных, если есть
        in_frontmatter = False
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    # Окончание метаданных
                    in_frontmatter = False
                
            # Проверьте, является ли это строкой заголовка за пределами frontmatter
            if not in_frontmatter:
                stripped_line = line.strip()
                if (stripped_line.startswith('- [ ] ') or stripped_line.startswith('- [/] ')) and not title_replaced:
                    updated_lines.append(new_title)
                    title_replaced = True
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        # Запись обновленного содержимого обратно в файл
        if title_replaced:
            updated_content = '\n'.join(updated_lines)
            source.path.write_text(updated_content, encoding='utf-8')
            return True
        else:
            # Строка заголовка не найдена
            return False
            
    except Exception:
        # Ошибка чтения/записи файла
        return False


def update_source_files(prioritized_sources: Dict[SourceFile, str]) -> int:
    """ Обновление нескольких исходных файлов с указанием их маркеров приорита.
    
    Args:
        prioritized_sources: Словарь с объектами файлов сопоставленными с приоритетами
        
    Returns:
        Число успешно обновлённых файлов
    """
    success_count = 0
    
    for source, priority_level in prioritized_sources.items():
        if update_source_file(source, priority_level):
            success_count += 1
    
    return success_count
