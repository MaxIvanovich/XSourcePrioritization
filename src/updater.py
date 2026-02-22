"""
Module for updating source files with priority markers.
"""

from typing import Dict
from .parser import SourceFile


def update_source_file(source: SourceFile, priority_level: str) -> bool:
    """
    Update a source file with the appropriate priority marker.
    
    Args:
        source: SourceFile object to update
        priority_level: Priority level ('highest', 'high', 'medium', 'low', 'lowest')
        
    Returns:
        True if update was successful, False otherwise
    """
    # Define marker mapping
    markers = {
        'highest': '🔺',
        'high': '⏫',
        'medium': '🔼',
        'low': '🔽',
        'lowest': '⏬'
    }
    
    # Get the appropriate marker
    marker = markers.get(priority_level)
    if not marker:
        return False  # Invalid priority level
    
    # Determine the checkbox state based on priority level
    # highest gets [/], others get [ ]
    if priority_level == 'highest':
        new_checkbox = '- [/]'
    else:
        new_checkbox = '- [ ]'
    
    # Construct the new title line
    # Remove any existing checkbox from the original title
    original_title = source.title
    if original_title.startswith('- [ ]') or original_title.startswith('- [/]'):
        # Extract just the content part after the checkbox
        content_part = original_title[5:].strip()
    else:
        content_part = original_title.strip()
    
    new_title = f"{new_checkbox} {content_part} {marker}".strip()
    
    try:
        # Read the current file content
        content = source.path.read_text(encoding='utf-8')
        
        # Split content into lines
        lines = content.split('\n')
        
        # Find and replace the title line
        updated_lines = []
        title_replaced = False
        
        # Skip frontmatter if present
        in_frontmatter = False
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    # End of frontmatter
                    in_frontmatter = False
                
            # Check if this is the title line outside of frontmatter
            if not in_frontmatter:
                stripped_line = line.strip()
                if (stripped_line.startswith('- [ ] ') or stripped_line.startswith('- [/] ')) and not title_replaced:
                    updated_lines.append(new_title)
                    title_replaced = True
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        # Write the updated content back to the file
        if title_replaced:
            updated_content = '\n'.join(updated_lines)
            source.path.write_text(updated_content, encoding='utf-8')
            return True
        else:
            # Title line was not found
            return False
            
    except Exception:
        # Error occurred while reading/writing file
        return False


def update_source_files(prioritized_sources: Dict[SourceFile, str]) -> int:
    """
    Update multiple source files with their priority markers.
    
    Args:
        prioritized_sources: Dictionary mapping SourceFile to priority level
        
    Returns:
        Number of successfully updated files
    """
    success_count = 0
    
    for source, priority_level in prioritized_sources.items():
        if update_source_file(source, priority_level):
            success_count += 1
    
    return success_count