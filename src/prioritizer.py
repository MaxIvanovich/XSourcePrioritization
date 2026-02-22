"""
Module for implementing the two-stage prioritization algorithm.
Stage 1: Group selection for large sets (>50 sources)
Stage 2: Pairwise comparisons with scoring
"""

from typing import List, Tuple, Dict
from .parser import SourceFile
from .utils import calculate_alpha, display_group_selection, get_pair_comparison, divide_into_priority_groups


def prepare_sources_for_prioritization(sources: List[SourceFile]) -> List[SourceFile]:
    """
    Prepare sources for prioritization by cleaning title lines and ensuring proper format.
    
    Args:
        sources: List of SourceFile objects to prepare
        
    Returns:
        List of SourceFile objects with cleaned titles
    """
    prepared_sources = []
    
    for source in sources:
        # Remove any existing priority markers from the title
        clean_title = source.title
        for marker in ['🔺', '⏫', '🔼', '🔽', '⏬']:
            clean_title = clean_title.replace(marker, '').strip()
        
        # Replace [/] with [ ] if needed
        if clean_title.startswith('- [/]'):
            clean_title = '- [ ]' + clean_title[5:]  # Replace '- [/]' with '- [ ]'
        
        # Create a new SourceFile with the cleaned title
        prepared_source = SourceFile(
            path=source.path,
            type=source.type,
            readed=source.readed,
            title=clean_title
        )
        
        prepared_sources.append(prepared_source)
    
    return prepared_sources


def stage_one_group_selection(sources: List[SourceFile]) -> List[SourceFile]:
    """
    Stage 1: Group selection for large sets (>50 sources).
    Groups sources and asks user to select one from each group.
    Sources not selected in their group immediately get lowest status.
    
    Args:
        sources: List of SourceFile objects to process
        
    Returns:
        List of SourceFile objects that were selected in their group (proceed to stage 2)
    """
    if len(sources) <= 50:
        # No group selection needed for small sets
        return sources.copy()
    
    alpha = calculate_alpha(len(sources))
    
    # Group sources
    grouped_sources = []
    for i in range(0, len(sources), alpha):
        group = sources[i:i+alpha]
        grouped_sources.append(group)
    
    selected_sources = []
    
    for group in grouped_sources:
        # Display group selection menu
        choice = display_group_selection(group)
        
        if choice == 0:  # User chose to exit
            return []  # Return empty list to indicate exit requested
        
        # Add selected source (subtract 1 because menu is 1-indexed)
        if choice > 0:
            selected_sources.append(group[choice - 1])
    
    return selected_sources


def stage_two_pairwise_comparison(sources: List[SourceFile]) -> Dict[SourceFile, int]:
    """
    Stage 2: Pairwise comparisons with scoring.
    Each pair is presented to user, winner gets +1 point.
    Results are divided into 5 equal groups with priority markers.
    
    Args:
        sources: List of SourceFile objects to compare
        
    Returns:
        Dictionary mapping SourceFile to score
    """
    if not sources:
        return {}
    
    # Initialize scores for each source
    scores = {source: 0 for source in sources}
    
    # Generate all unique pairs
    source_pairs = []
    for i in range(len(sources)):
        for j in range(i + 1, len(sources)):
            source_pairs.append((sources[i], sources[j]))
    
    # Compare each pair
    for source_a, source_b in source_pairs:
        comparison_result = get_pair_comparison(source_a, source_b)
        
        if comparison_result == 0:  # User chose to exit
            # Return current scores without completing remaining comparisons
            return scores
        
        # Award point to winner
        if comparison_result == 1:
            scores[source_a] += 1
        elif comparison_result == 2:
            scores[source_b] += 1
    
    return scores


def prioritize_sources(sources: List[SourceFile]) -> Dict[SourceFile, str]:
    """
    Main function to execute the two-stage prioritization algorithm.
    
    Args:
        sources: List of SourceFile objects to prioritize
        
    Returns:
        Dictionary mapping SourceFile to priority level ('highest', 'high', 'medium', 'low', 'lowest')
    """
    # Prepare sources for prioritization
    prepared_sources = prepare_sources_for_prioritization(sources)
    
    # Stage 1: Group selection (if needed)
    stage_one_results = stage_one_group_selection(prepared_sources)
    
    # If user exited during stage 1, return empty dict
    if len(stage_one_results) == 0 and len(prepared_sources) > 50:
        return {}
    
    # Stage 2: Pairwise comparison
    scores = stage_two_pairwise_comparison(stage_one_results)
    
    # If user exited during stage 2, return empty dict
    if len(scores) != len(stage_one_results):
        return {}
    
    # Convert scores dict to list of tuples and sort by score (descending)
    sources_with_scores = [(source, scores[source]) for source in scores]
    sources_with_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Divide into 5 priority groups
    priority_groups = divide_into_priority_groups(sources_with_scores, 5)
    
    # Create result dictionary mapping source to priority level
    result = {}
    
    # Define priority levels
    priority_levels = ['highest', 'high', 'medium', 'low', 'lowest']
    
    # Assign priority levels to each group
    for i, group in enumerate(priority_groups):
        for source in group:
            result[source] = priority_levels[i]
    
    return result