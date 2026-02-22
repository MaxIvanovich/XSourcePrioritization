""" Основной модуль консольной утилиты приоритезации источников из базы знаний Obsidian """

import argparse
from pathlib import Path
from .parser import find_source_files
from .filter import filter_unread_sources, count_sources_by_type, group_sources_by_type
from .utils import display_type_menu
from .prioritizer import prioritize_sources
from .updater import update_source_files


def main():
    """Точка входа в приложение"""
    parser = argparse.ArgumentParser(description="Приложение перекрёстной приоритезации книг, статей и т.д.")
    parser.add_argument("--path", required=True, help="Путь к директории, содержащей markdown-файлы")
    parser.add_argument("--count", action="store_true", help="Вывести типы непрочитанных источников и их количество")
    
    args = parser.parse_args()
    
    directory_path = Path(args.path)
    
    if not directory_path.exists() or not directory_path.is_dir():
        print(f"Error: Directory '{args.path}' does not exist.")
        return
    
    # Все файлы в директории
    all_sources = find_source_files(directory_path)
    
    if not all_sources:
        print("В директории не найдено подходящих файлов.")
        return
    
    # Фильтр не прочитанных источников
    unread_sources = filter_unread_sources(all_sources)
    
    if not unread_sources:
        print("В директории нет непрочитанных источников.")
        return
    
    # Для аргумента --count показ статистики и выход
    if args.count:
        type_counts = count_sources_by_type(unread_sources)
        print("Непрочитанных источников:")
        for source_type, count in sorted(type_counts.items()):
            print(f"{source_type}: {count}")
        return
    
    # Группировка по типам
    grouped_sources = group_sources_by_type(unread_sources)
    
    if not grouped_sources:
        print("В директории нет непрочитанных источников, указанного типа.")
        return
    
    # Меню выбора типа источника
    type_counts = count_sources_by_type(unread_sources)
    choice = display_type_menu(type_counts)
    
    if choice == 0:  # Выход
        print("Выход без изменений.")
        return
    
    # Фильтр источников по выбранному типу
    selected_type = list(type_counts.keys())[choice - 1]
    sources_to_prioritize = grouped_sources[selected_type]
    
    if not sources_to_prioritize:
        print(f"Нет источников типа '{selected_type}'.")
        return
    
    # Приоритезация
    prioritized_sources = prioritize_sources(sources_to_prioritize)
    
    # Пустой результат - прервано пользователем
    if not prioritized_sources:
        print("Выход без изменений.")
        return
    
    # Обновление файлов в соответствии с приоритезацией
    updated_count = update_source_files(prioritized_sources)
    
    print(f"Успешно промаркировано {updated_count} файлов в соответствии с приоритезацией.")


if __name__ == "__main__":
    main()
