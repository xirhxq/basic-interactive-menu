"""Search functionality for InteractiveMenu.

This module provides zero-dependency search capabilities for filtering
menu options by user query.
"""

from __future__ import annotations

from typing import List


class SearchEngine:
    """Zero-dependency fuzzy search engine for menu options.

    Provides character-based indexing for efficient substring matching.
    """

    def __init__(self, options: List[str]) -> None:
        """Initialize the search engine with menu options.

        Args:
            options: List of option strings to search through.
        """
        self.options = options
        self._index = self._build_index()

    def _build_index(self) -> dict[str, List[int]]:
        """Build a character-to-indices mapping for fast lookup.

        Returns:
            Dictionary mapping each character to list of option indices
            containing that character.
        """
        index: dict[str, List[int]] = {}
        for i, option in enumerate(self.options):
            # Index by lowercase characters for case-insensitive search
            for char in option.lower():
                if char.isalnum():
                    if char not in index:
                        index[char] = []
                    if i not in index[char]:
                        index[char].append(i)
        return index

    def search(self, query: str) -> List[int]:
        """Search for options matching the query.

        Args:
            query: Search string to match against options.

        Returns:
            List of indices matching the search query.
        """
        if not query:
            return list(range(len(self.options)))

        query = query.lower()

        # Use character index to efficiently collect candidate indices
        candidates: set[int] = set()
        for char in query:
            if char.isalnum() and char in self._index:
                candidates.update(self._index[char])

        # Validate candidates with actual substring matching
        result: list[int] = []
        for i in candidates:
            if query in self.options[i].lower():
                result.append(i)

        # Also check any options that might match but weren't in index
        for i, option in enumerate(self.options):
            if i not in candidates and query in option.lower():
                result.append(i)

        return sorted(result)

    def get_matches_summary(self, query: str) -> str:
        """Get a human-readable summary of search results.

        Args:
            query: The search query.

        Returns:
            Summary string describing the matches.
        """
        matches = self.search(query)
        count = len(matches)

        if count == 0:
            return "No matches found"
        elif count == 1:
            return f"1 match: {self.options[matches[0]]}"
        elif count <= 3:
            matched_names = [self.options[i] for i in matches]
            return f"{count} matches: {', '.join(matched_names)}"
        else:
            return f"{count} matches available"
