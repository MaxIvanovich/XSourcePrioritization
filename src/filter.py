""" Модуль для фильтрации исходных файлов по статусу чтения и группировки по типу. """

from typing import Dict, List
from .parser import SourceFile


def filter_unread_sources(sources: List[SourceFile]) -> List[SourceFile]:
    """ Выбор непрочитанных источников - файлов с readed=False.
    Args:
        sources: список файлов
    Returns:
        Список файлов с readed=False
    """
    return [source for source in sources if not source.readed]


def group_sources_by_type(sources: List[SourceFile]) -> Dict[str, List[SourceFile]]:
    """ Группировка источников по типу.
    Args:
        sources: список файлов
    Returns:
        Словарь с сопоставленными файлами и их типами
    """
    groups = {}
    for source in sources:
        if source.type not in groups:
            groups[source.type] = []
        groups[source.type].append(source)
    
    return groups


def count_sources_by_type(sources: List[SourceFile]) -> Dict[str, int]:
    """ Подсчет количества источников по типу.
    Args:
        sources: Список файлов
    Returns:
        Словарь сопоставлений типов и количества файлов
    """
    counts = {}
    for source in sources:
        if source.type not in counts:
            counts[source.type] = 0
        counts[source.type] += 1
    
    return counts
