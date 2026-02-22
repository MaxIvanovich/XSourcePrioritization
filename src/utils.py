"""
Utility functions for CLI interactions and other helpers.
"""

import math
from typing import List, Tuple
from .parser import SourceFile


def display_type_menu(type_counts: dict) -> int:
    """
    Display menu for selecting source type.
    
    Args:
        type_counts: Dictionary mapping type to count
        
    Returns:
        Selected index (0 to len(type_counts)), where 0 means exit
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
    """
    Display menu for selecting the most important source in a group.
    
    Args:
        group: List of SourceFile objects in the group
        
    Returns:
        Selected index (0 to len(group)), where 0 means exit
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
    """
    Ask user to compare two sources.
    
    Args:
        source_a: First SourceFile
        source_b: Second SourceFile
        
    Returns:
        1 if source_a is more important, 2 if source_b is more important, 0 to exit
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
    """
    Calculate alpha value for group size based on total count.
    
    Args:
        count: Total number of sources
        
    Returns:
        Alpha value (minimum 1)
    """
    if count == 0:
        return 1
    alpha = math.ceil(count / 25)
    return max(1, alpha)  # Ensure at least 1


def divide_into_priority_groups(sources_with_scores: List[Tuple[SourceFile, int]], num_groups: int = 5) -> List[List[SourceFile]]:
    """
    Divide sources into priority groups based on scores.
    
    Args:
        sources_with_scores: List of tuples (SourceFile, score) sorted by score descending
        num_groups: Number of groups to create (default 5)
        
    Returns:
        List of lists, each containing SourceFiles for a priority level
    """
    if not sources_with_scores:
        return [[] for _ in range(num_groups)]
    
    # Calculate base size for each group
    total_count = len(sources_with_scores)
    base_size = total_count // num_groups
    remainder = total_count % num_groups
    
    groups = []
    start_idx = 0
    
    for i in range(num_groups):
        # Add one extra item to the first 'remainder' groups to distribute remainder
        group_size = base_size + (1 if i < remainder else 0)
        end_idx = start_idx + group_size
        group_sources = [item[0] for item in sources_with_scores[start_idx:end_idx]]
        groups.append(group_sources)
        start_idx = end_idx
    
    return groups