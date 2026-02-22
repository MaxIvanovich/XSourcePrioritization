""" Модуль чтения файлов markdown. Извлекает тип, статус чтения и заголовок из файлов markdown. """

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class SourceFile:
    """Базовый класс для файла-источника с мета-данными и названием"""
    path: Path
    type: str
    readed: bool
    title: str

    def __eq__(self, other):
        """ Проверка равенства на основе path, type, readed, и title. """
        if not isinstance(other, SourceFile):
            return False
        return (self.path == other.path and 
                self.type == other.type and 
                self.readed == other.readed and 
                self.title == other.title)

    def __hash__(self):
        """ Делает SourceFile хешируемым на основе его аттрибутов. """
        return hash((self.path, self.type, self.readed, self.title))


def parse_frontmatter(content: str) -> dict:
    """ Извлечение метаданных из файлов.
    Args:
        content: Полное содержимое файла
        
    Returns:
        Словарь метаданных.
    """
    lines = content.split('\n')
    if len(lines) < 3 or lines[0] != '---':
        return {}
    
    # Поиск окончания метаданных
    end_index = -1
    for i in range(1, len(lines)):
        if lines[i] == '---':
            end_index = i
            break
    
    if end_index == -1:
        return {}
    
    frontmatter_lines = lines[1:end_index]
    frontmatter_content = '\n'.join(frontmatter_lines)
    
    # Извлечение YAML-подобных данных
    result = {}
    for line in frontmatter_content.split('\n'):
        line = line.strip()
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Обработка булевых значений
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            
            result[key] = value
    
    return result


def extract_title(content: str) -> Optional[str]:
    """ Извлечение наименования документа после метаданных.
    
    Args:
        content: Содержимое файла
        
    Returns:
        Строку названия или None, если отсутствует
    """
    lines = content.split('\n')
    
    # Пропуск метаданных, если есть
    skip_frontmatter = False
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not skip_frontmatter:
                skip_frontmatter = True
            else:
                # End of frontmatter, look for title after this
                for j in range(i+1, len(lines)):
                    line_content = lines[j].strip()
                    if line_content.startswith('- [ ] ') or line_content.startswith('- [/] '):
                        return line_content
                break
    else:
        # После метаданных, поиск начала строки
        for line in lines:
            line_content = line.strip()
            if line_content.startswith('- [ ] ') or line_content.startswith('- [/] '):
                return line_content
    
    return None


def parse_source_file(file_path: Path) -> Optional[SourceFile]:
    """ Извлечение каждого файла источника.
    
    Args:
        file_path: Путь к файлу
        
    Returns:
        Объект файла источника или None если извлечение не удалось
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        
        frontmatter = parse_frontmatter(content)
        
        # Извлечение требуемых полей
        source_type = frontmatter.get('type', '')
        readed = frontmatter.get('readed', False)
        
        # Преобразование строки в булево значение
        if isinstance(readed, str):
            readed = readed.lower() == 'true'
        
        title = extract_title(content)
        
        if not source_type or title is None:
            return None
        
        return SourceFile(path=file_path,
                          type=source_type,
                          readed=readed,
                          title=title)

    except Exception:
        # Файл не прочитан
        return None


def find_source_files(directory: Path) -> list[SourceFile]:
    """ Чтение файлов из указанной директории
    
    Args:
        directory: Директория, содержащая файлы
        
    Returns:
        Список прочитанных файлов
    """
    sources = []
    
    for md_file in directory.glob('*.md'):
        source = parse_source_file(md_file)
        if source:
            sources.append(source)
    
    return sources