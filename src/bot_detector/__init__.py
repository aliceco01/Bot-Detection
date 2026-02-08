"""
Bot Detection System
A comprehensive bot detection system for social media platforms.
"""

from .detector import BotDetector
from .features import FeatureExtractor
from .ml_detector import MLBotDetector
from .rule_detector import RuleBasedDetector

__version__ = "1.0.0"
__all__ = ["BotDetector", "FeatureExtractor", "MLBotDetector", "RuleBasedDetector"]
