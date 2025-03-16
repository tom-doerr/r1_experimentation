"""Shared configuration constants and settings."""

from typing import Dict

DEFAULT_MODEL = "openrouter/google/gemini-2.0-flash-001"

global_settings: Dict[str, float] = {
    'starting_cash': 1000.0,
    'max_net_worth': 10000.0,
    'min_net_worth': 0.0,
    'cash_penalty': 0.1,
    'initial_net_worth': 1000.0
}
