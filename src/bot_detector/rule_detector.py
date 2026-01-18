"""
Rule-based bot detection module.
Uses heuristic rules to identify bot-like behavior.
"""

from typing import Dict, Any, List, Tuple


class RuleBasedDetector:
    """Rule-based bot detector using heuristics."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize rule-based detector.
        
        Args:
            config: Configuration dictionary for thresholds
        """
        self.config = config or self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration thresholds."""
        return {
            'min_account_age_days': 7,
            'max_following_ratio': 10.0,  # following/followers
            'min_follower_following_ratio': 0.1,  # followers/following
            'max_post_frequency': 50.0,  # posts per day
            'max_duplicate_ratio': 0.5,
            'max_url_ratio': 0.8,
            'max_username_length': 20,
            'min_bio_length': 10,
            'suspicious_post_frequency': 20.0,
            'bot_score_threshold': 0.6
        }
    
    def detect(self, features: Dict[str, float]) -> Tuple[bool, float, List[str]]:
        """
        Detect if user is a bot based on rules.
        
        Args:
            features: Dictionary of extracted features
            
        Returns:
            Tuple of (is_bot, confidence_score, triggered_rules)
        """
        triggered_rules = []
        bot_score = 0.0
        max_score = 0.0
        
        # Rule 1: Very new account with high activity
        if features.get('account_age_days', 0) < self.config['min_account_age_days']:
            if features.get('post_frequency', 0) > self.config['suspicious_post_frequency']:
                triggered_rules.append("New account with suspicious posting frequency")
                bot_score += 0.3
        max_score += 0.3
        
        # Rule 2: Suspicious follower/following ratio
        follower_following_ratio = features.get('follower_following_ratio', 0)
        if follower_following_ratio < self.config['min_follower_following_ratio']:
            triggered_rules.append("Low follower to following ratio")
            bot_score += 0.2
        max_score += 0.2
        
        # Rule 3: No profile image or bio
        if not features.get('has_profile_image', False):
            triggered_rules.append("No profile image")
            bot_score += 0.1
        max_score += 0.1
        
        if not features.get('has_bio', False) or features.get('bio_length', 0) < self.config['min_bio_length']:
            triggered_rules.append("Missing or very short bio")
            bot_score += 0.1
        max_score += 0.1
        
        # Rule 4: Random username pattern
        if features.get('username_random_pattern', False):
            triggered_rules.append("Random username pattern")
            bot_score += 0.15
        max_score += 0.15
        
        # Rule 5: Very high posting frequency
        if features.get('post_frequency', 0) > self.config['max_post_frequency']:
            triggered_rules.append("Extremely high posting frequency")
            bot_score += 0.25
        max_score += 0.25
        
        # Rule 6: High duplicate content
        if features.get('duplicate_content_ratio', 0) > self.config['max_duplicate_ratio']:
            triggered_rules.append("High duplicate content ratio")
            bot_score += 0.2
        max_score += 0.2
        
        # Rule 7: Excessive URL posting
        if features.get('url_ratio', 0) > self.config['max_url_ratio']:
            triggered_rules.append("Excessive URL posting")
            bot_score += 0.15
        max_score += 0.15
        
        # Rule 8: Very fast reply times (likely automated)
        if features.get('avg_reply_time', 0) < 5:  # Less than 5 seconds
            if features.get('avg_reply_time', 0) > 0:  # But not zero (which might be missing data)
                triggered_rules.append("Suspiciously fast reply times")
                bot_score += 0.2
        max_score += 0.2
        
        # Rule 9: Low interaction diversity (talking to same accounts)
        if features.get('interaction_diversity', 1.0) < 0.1:
            triggered_rules.append("Low interaction diversity")
            bot_score += 0.15
        max_score += 0.15
        
        # Normalize score
        if max_score > 0:
            normalized_score = bot_score / max_score
        else:
            normalized_score = 0.0
        
        is_bot = normalized_score >= self.config['bot_score_threshold']
        
        return is_bot, normalized_score, triggered_rules
    
    def get_explanation(self, features: Dict[str, float]) -> str:
        """
        Get human-readable explanation of detection result.
        
        Args:
            features: Dictionary of extracted features
            
        Returns:
            Explanation string
        """
        is_bot, score, rules = self.detect(features)
        
        if is_bot:
            explanation = f"Bot detected with confidence {score:.2%}.\n"
            explanation += "Triggered rules:\n"
            for rule in rules:
                explanation += f"  - {rule}\n"
        else:
            explanation = f"Likely legitimate user (bot score: {score:.2%}).\n"
            if rules:
                explanation += "Minor concerns:\n"
                for rule in rules:
                    explanation += f"  - {rule}\n"
        
        return explanation
