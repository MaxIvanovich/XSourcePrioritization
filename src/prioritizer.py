""" Модуль реализации двухэтапного алгоритма приоритизации.
Этап 1: Групповой выбор для большого количества файлов (>50)
Этап 2: Перекрёстная приоритезация
"""

from typing import List, Tuple, Dict
from .parser import SourceFile
from .utils import calculate_alpha, display_group_selection, get_pair_comparison, divide_into_priority_groups


def prepare_sources_for_prioritization(sources: List[SourceFile]) -> List[SourceFile]:
    """ Подготовка файлов к приоритезации путём очистки строки заголовка и проверки форматирования.
    
    Args:
        sources: Список объектов файлов-источников
        
    Returns:
        Список объектов файлов-источников с очищенной строкой заголовка
    """
    prepared_sources = []
    
    for source in sources:
        # Удаление маркеров приоритета при наличии
        clean_title = source.title
        for marker in ['🔺', '⏫', '🔼', '🔽', '⏬']:
            clean_title = clean_title.replace(marker, '').strip()
        
        # Замена [/] на [ ] если требуется
        if clean_title.startswith('- [/]'):
            clean_title = '- [ ]' + clean_title[5:]
        
        # Обновлённый объект файла с очищеным названием
        prepared_source = SourceFile(path=source.path,
                                     type=source.type,
                                     readed=source.readed,
                                     title=clean_title)
        
        prepared_sources.append(prepared_source)
    
    return prepared_sources


def stage_one_group_selection(sources: List[SourceFile]) -> List[SourceFile]:
    """ Этап 1: Групповой выбор при большом количестве файлов (>50).
    Группирует источники и запрашивает приоритетный у пользователя.
    Для невыбранных - устанавливает статус "lowest".
    
    Args:
        sources: Список объектов файлов-источников
        
    Returns:
        Список объектов отобранных для этапа 2
    """
    if len(sources) <= 50:
        # Групповой этап не нуже для малого количества
        return sources.copy()
    
    alpha = calculate_alpha(len(sources))
    
    # Групповые источники
    grouped_sources = []
    for i in range(0, len(sources), alpha):
        group = sources[i:i+alpha]
        grouped_sources.append(group)
    
    selected_sources = []
    
    for group in grouped_sources:
        # Отображение меню группового выбора
        choice = display_group_selection(group)
        
        if choice == 0:  # Елсли выбран выход
            return []  # Возвращает пустой список означающий выход
        
        # Формирование списка выбранных сточников
        if choice > 0:
            selected_sources.append(group[choice - 1])
    
    return selected_sources


def stage_two_pairwise_comparison(sources: List[SourceFile]) -> Dict[SourceFile, int]:
    """ Этап 2: Перекрёстная приоритезация с подсчётом очков.
    Каждый выбранный источник получает +1 очко.
    И по набранным очкам источники делятся на 5 равных групп - приоритетов.
    
    Args:
        sources: Список объектов источников для сравнения
        
    Returns:
        Словарь объектов файлов с набранными очками
    """
    if not sources:
        return {}
    
    # Инициализация баллов для каждого источника
    scores = {source: 0 for source in sources}
    
    # Составление всех уникальных пар
    source_pairs = []
    for i in range(len(sources)):
        for j in range(i + 1, len(sources)):
            source_pairs.append((sources[i], sources[j]))
    
    # Сравнение каждой пары
    for source_a, source_b in source_pairs:
        comparison_result = get_pair_comparison(source_a, source_b)
        
        if comparison_result == 0:  # Выход
            # Возвращает текущие баллы 
            return scores
        
        # Добавление 1 балла
        if comparison_result == 1:
            scores[source_a] += 1
        elif comparison_result == 2:
            scores[source_b] += 1
    
    return scores


def prioritize_sources(sources: List[SourceFile]) -> Dict[SourceFile, str]:
    """ Функция реализующая двухэтапную приоритезацию.
    
    Args:
        sources: Список объектов файлов для приоритезации
        
    Returns:
        Словарь соотнесённых приоритетов ('highest', 'high', 'medium', 'low', 'lowest')
    """
    # Подготовка источников для приоритезации
    prepared_sources = prepare_sources_for_prioritization(sources)
    
    # Этап 1: Групповой выбор, если необходимо
    stage_one_results = stage_one_group_selection(prepared_sources)
    
    # При выходе (прерывании) на первом этапе, возвращает пустой словарь
    if len(stage_one_results) == 0 and len(prepared_sources) > 50:
        return {}
    
    # Этап 2: Попарная перекрёстная приоритезация
    scores = stage_two_pairwise_comparison(stage_one_results)
    
    # При выходе (прерывании) на втором этапе, возвращает пустой словарь
    if len(scores) != len(stage_one_results):
        return {}
    
    # Преобразование словаря в список кортежей и сортировка по баллам (по убыванию)
    sources_with_scores = [(source, scores[source]) for source in scores]
    sources_with_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Разбивка на 5 групп
    priority_groups = divide_into_priority_groups(sources_with_scores)
    
    # Создание результирующего словаря по приоритетам
    result = {}
    
    # Уровни приоритетов
    priority_levels = ['highest', 'high', 'medium', 'low', 'lowest']
    
    # Назначение уровней для каждой из групп
    for i, group in enumerate(priority_groups):
        for source in group:
            result[source] = priority_levels[i]
    
    return result