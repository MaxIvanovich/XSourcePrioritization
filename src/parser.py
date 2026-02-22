"""
Module for parsing markdown files with frontmatter.
Extracts type, readed status, and title from markdown files.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class SourceFile:
    """Represents a source file with metadata and title."""
    path: Path
    type: str
    readed: bool
    title: str


def parse_frontmatter(content: str) -> dict:
    """
    Parse frontmatter from markdown content.
    
    Args:
        content: Full markdown file content
        
    Returns:
        Dictionary with parsed frontmatter fields
    """
    lines = content.split('\n')
    if len(lines) < 3 or lines[0] != '---':
        return {}
    
    # Find end of frontmatter
    end_index = -1
    for i in range(1, len(lines)):
        if lines[i] == '---':
            end_index = i
            break
    
    if end_index == -1:
        return {}
    
    frontmatter_lines = lines[1:end_index]
    frontmatter_content = '\n'.join(frontmatter_lines)
    
    # Simple YAML-like parsing
    result = {}
    for line in frontmatter_content.split('\n'):
        line = line.strip()
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Handle boolean values
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            
            result[key] = value
    
    return result


def extract_title(content: str) -> Optional[str]:
    """
    Extract title from markdown content after frontmatter.
    
    Args:
        content: Full markdown file content
        
    Returns:
        Title string or None if not found
    """
    lines = content.split('\n')
    
    # Skip frontmatter if present
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
        # No frontmatter, look from beginning
        for line in lines:
            line_content = line.strip()
            if line_content.startswith('- [ ] ') or line_content.startswith('- [/] '):
                return line_content
    
    return None


def parse_source_file(file_path: Path) -> Optional[SourceFile]:
    """
    Parse a single markdown source file.
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        SourceFile object or None if parsing fails
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        
        frontmatter = parse_frontmatter(content)
        
        # Extract required fields
        source_type = frontmatter.get('type', '')
        readed = frontmatter.get('readed', False)
        
        # Convert readed to boolean if it's a string
        if isinstance(readed, str):
            readed = readed.lower() == 'true'
        
        title = extract_title(content)
        
        if not source_type or title is None:
            return None
        
        return SourceFile(
            path=file_path,
            type=source_type,
            readed=readed,
            title=title
        )
    except Exception:
        # Could not parse file
        return None


def find_source_files(directory: Path) -> list[SourceFile]:
    """
    Find and parse all markdown source files in directory.
    
    Args:
        directory: Directory to search for markdown files
        
    Returns:
        List of parsed SourceFile objects
    """
    sources = []
    
    for md_file in directory.glob('*.md'):
        source = parse_source_file(md_file)
        if source:
            sources.append(source)
    
    return sources