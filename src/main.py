"""
Main module for the source prioritization CLI application.
"""

import argparse
from pathlib import Path
from .parser import find_source_files
from .filter import filter_unread_sources, count_sources_by_type, group_sources_by_type
from .utils import display_type_menu
from .prioritizer import prioritize_sources
from .updater import update_source_files


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Console application for source prioritization")
    parser.add_argument("--path", required=True, help="Path to directory with markdown source files")
    parser.add_argument("--count", action="store_true", help="Show count of unread sources by type and exit")
    
    args = parser.parse_args()
    
    directory_path = Path(args.path)
    
    if not directory_path.exists() or not directory_path.is_dir():
        print(f"Error: Directory '{args.path}' does not exist.")
        return
    
    # Find all source files in the directory
    all_sources = find_source_files(directory_path)
    
    if not all_sources:
        print("No valid source files found in the specified directory.")
        return
    
    # Filter to only unread sources
    unread_sources = filter_unread_sources(all_sources)
    
    if not unread_sources:
        print("No unread source files found in the specified directory.")
        return
    
    # If --count flag is specified, show statistics and exit
    if args.count:
        type_counts = count_sources_by_type(unread_sources)
        print("Непрочитанных источников:")
        for source_type, count in sorted(type_counts.items()):
            print(f"{source_type}: {count}")
        return
    
    # Group sources by type
    grouped_sources = group_sources_by_type(unread_sources)
    
    if not grouped_sources:
        print("No valid unread source files with types found in the specified directory.")
        return
    
    # Show type selection menu
    type_counts = count_sources_by_type(unread_sources)
    choice = display_type_menu(type_counts)
    
    if choice == 0:  # Exit option selected
        print("Exiting without changes.")
        return
    
    # Get selected type
    selected_type = list(type_counts.keys())[choice - 1]
    sources_to_prioritize = grouped_sources[selected_type]
    
    if not sources_to_prioritize:
        print(f"No unread sources of type '{selected_type}' found.")
        return
    
    # Perform prioritization
    prioritized_sources = prioritize_sources(sources_to_prioritize)
    
    # If empty result, it means user exited during prioritization
    if not prioritized_sources:
        print("Exiting without changes.")
        return
    
    # Update source files with priority markers
    updated_count = update_source_files(prioritized_sources)
    
    print(f"Successfully updated {updated_count} files with priority markers.")


if __name__ == "__main__":
    main()