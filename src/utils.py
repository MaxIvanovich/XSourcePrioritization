""" Вспомогательные функции для CLI и другие. """

import math
from typing import List, Tuple
from .parser import SourceFile


def display_type_menu(type_counts: dict) -> int:
    """ Меню для выбора типа источника.
    
    Args:
        type_counts: Словарь типов источников с количеством
        
    Returns:
        Выбранный индекс типа (0 до len(type_counts)), где 0 означает выход
    """
    print("Выберите тип источника для приоритезации:")
    
    types = list(type_counts.keys())
    for i, type_name in enumerate(types, 1):
        count = type_counts[type_name]
        print(f"{i}. {type_name} ({count})")
    
    print("0. Выход")
    
    while True:
        try:
            choice = int(input("Ваш выбор: "))
            if 0 <= choice <= len(types):
                return choice
        except ValueError:
            pass
        print("Пожалуйста, введите допустимый номер.")


def display_group_selection(group: List[SourceFile]) -> int:
    """ Меню выбора приоритетного источника из группы.
    
    Args:
        group: Список объектов файлов в группе
        
    Returns:
        Выбранный индекс типа (0 до len(type_counts)), где 0 означает выход
    """
    print("Выберите приоритетный источник:")
    
    for i, source in enumerate(group, 1):
        print(f"{i}. {source.title}")
    
    print("0. Выход")
    
    while True:
        try:
            choice = int(input("Ваш выбор: "))
            if 0 <= choice <= len(group):
                return choice
        except ValueError:
            pass
        print("Пожалуйста, введите допустимый номер.")


def get_pair_comparison(source_a: SourceFile, source_b: SourceFile) -> int:
    """ Меню перекрёстной приоритезации.
    
    Args:
        source_a: Первый объект
        source_b: Второй объект
        
    Returns:
        1 Если выбран source_a, 2 если выбран source_b, 0 - Выход
    """
    print(f"Какой источник приоритетнее:")
    print(f"1. {source_a.title}")
    print(f"2. {source_b.title}")
    print("0. Выход")
    
    while True:
        try:
            choice = int(input("Ваш выбор: "))
            if choice in [0, 1, 2]:
                return choice
        except ValueError:
            pass
        print("Пожалуйста, введите 0, 1 или 2.")


def calculate_alpha(count: int) -> int:
    """ Вычисление значения alpha для определения размера группы.
    
    Args:
        count: Общее число источников
        
    Returns:
        Значение alpha (минимум 1)
    """
    if count == 0:
        return 1
    alpha = math.ceil(count / 25)
    return max(1, alpha)


def divide_into_priority_groups(sources_with_scores: List[Tuple[SourceFile, int]], num_groups: int = 5) -> List[List[SourceFile]]:
    """ Разделение источников по группа приоритета в зависимости от набранных баллов.
    
    Args:
        sources_with_scores: Список кортежей (SourceFile, score) отсортированный по убыванию баллов
        num_groups: Количество групп приоритетов (default 5)
        
    Returns:
        List of lists, each containing SourceFiles for a priority level
    """
    if not sources_with_scores:
        return [[] for _ in range(num_groups)]
    
    # Определение базового размера групп
    total_count = len(sources_with_scores)
    base_size = total_count // num_groups
    remainder = total_count % num_groups
    
    groups = []
    start_idx = 0
    
    for i in range(num_groups):
        # Добавьте один дополнительный элемент к первым группам "остаток", чтобы распределить остаток
        group_size = base_size + (1 if i < remainder else 0)
        end_idx = start_idx + group_size
        group_sources = [item[0] for item in sources_with_scores[start_idx:end_idx]]
        groups.append(group_sources)
        start_idx = end_idx
    
    return groups
