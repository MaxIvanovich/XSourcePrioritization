"""
Module for filtering source files by read status and grouping by type.
"""

from typing import Dict, List
from .parser import SourceFile


def filter_unread_sources(sources: List[SourceFile]) -> List[SourceFile]:
    """
    Filter sources to include only those with readed=False.
    
    Args:
        sources: List of SourceFile objects
        
    Returns:
        List of SourceFile objects with readed=False
    """
    return [source for source in sources if not source.readed]


def group_sources_by_type(sources: List[SourceFile]) -> Dict[str, List[SourceFile]]:
    """
    Group sources by their type field.
    
    Args:
        sources: List of SourceFile objects
        
    Returns:
        Dictionary mapping type to list of sources of that type
    """
    groups = {}
    for source in sources:
        if source.type not in groups:
            groups[source.type] = []
        groups[source.type].append(source)
    
    return groups


def count_sources_by_type(sources: List[SourceFile]) -> Dict[str, int]:
    """
    Count the number of sources for each type.
    
    Args:
        sources: List of SourceFile objects
        
    Returns:
        Dictionary mapping type to count of sources of that type
    """
    counts = {}
    for source in sources:
        if source.type not in counts:
            counts[source.type] = 0
        counts[source.type] += 1
    
    return counts