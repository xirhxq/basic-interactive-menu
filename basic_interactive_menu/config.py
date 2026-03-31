"""Configuration file support for InteractiveMenu.

This module provides functionality for loading menu definitions from
JSON and YAML configuration files.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class MenuConfig:
    """Configuration loader for menu definitions from files.

    Supports JSON and optional YAML (if pyyaml is installed).

    Example JSON format:
    {
        "title": "Select a Fruit",
        "key": "fruit",
        "multiple": false,
        "options": ["Apple", "Banana", "Orange"]
    }
    """

    @staticmethod
    def from_json(file_path: Union[str, Path]) -> Dict[str, Any]:
        """Load menu configuration from a JSON file.

        Args:
            file_path: Path to the JSON file.

        Returns:
            Dictionary containing menu configuration.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the JSON is invalid or missing required fields.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        try:
            with open(path, "r") as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")

        return config

    @staticmethod
    def from_yaml(file_path: Union[str, Path]) -> Dict[str, Any]:
        """Load menu configuration from a YAML file.

        Args:
            file_path: Path to the YAML file.

        Returns:
            Dictionary containing menu configuration.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If YAML is not installed or the file is invalid.
        """
        try:
            import yaml
        except ImportError:
            raise ValueError(
                "PyYAML is required for YAML config files. "
                "Install it with: pip install pyyaml"
            )

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        try:
            with open(path, "r") as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {file_path}: {e}")

        return config

    @staticmethod
    def from_file(file_path: Union[str, Path]) -> Dict[str, Any]:
        """Load menu configuration from a file (JSON or YAML).

        Detects file type based on extension (.json or .yaml/.yml).

        Args:
            file_path: Path to the configuration file.

        Returns:
            Dictionary containing menu configuration.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the file type is unsupported or content is invalid.
        """
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".json":
            return MenuConfig.from_json(path)
        elif suffix in (".yaml", ".yml"):
            return MenuConfig.from_yaml(path)
        else:
            raise ValueError(
                f"Unsupported file type: {suffix}. "
                "Supported types: .json, .yaml, .yml"
            )

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> None:
        """Validate a menu configuration dictionary.

        Args:
            config: Configuration dictionary to validate.

        Raises:
            ValueError: If required fields are missing or invalid.
        """
        if "options" not in config:
            raise ValueError("Config must contain 'options' field")

        options = config["options"]
        if not isinstance(options, list):
            raise ValueError("'options' must be a list")

        if not options:
            raise ValueError("'options' cannot be empty")

        for i, option in enumerate(options):
            if isinstance(option, str):
                continue
            elif isinstance(option, dict):
                if "name" not in option:
                    raise ValueError(f"Option at index {i} must contain 'name' field")
            else:
                raise ValueError(f"Option at index {i} must be a string or dict, got {type(option)}")

        if "multiple" in config and not isinstance(config["multiple"], bool):
            raise ValueError("'multiple' must be a boolean")
