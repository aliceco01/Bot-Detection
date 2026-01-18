"""
Main bot detector module that combines rule-based and ML approaches.
"""

from typing import Dict, Any, Optional, Tuple, List
from .features import FeatureExtractor
from .rule_detector import RuleBasedDetector
from .ml_detector import MLBotDetector


class BotDetector:
    """
    Main bot detection system combining multiple detection methods.
    """
    
    def __init__(self, 
                 use_ml: bool = True,
                 use_rules: bool = True,
                 model_path: Optional[str] = None,
                 rule_config: Optional[Dict[str, Any]] = None):
        """
        Initialize bot detector.
        
        Args:
            use_ml: Whether to use ML-based detection
            use_rules: Whether to use rule-based detection
            model_path: Path to pre-trained ML model (optional)
            rule_config: Configuration for rule-based detector (optional)
        """
        self.use_ml = use_ml
        self.use_rules = use_rules
        
        self.feature_extractor = FeatureExtractor()
        
        if use_ml:
            self.ml_detector = MLBotDetector(model_path)
        else:
            self.ml_detector = None
        
        if use_rules:
            self.rule_detector = RuleBasedDetector(rule_config)
        else:
            self.rule_detector = None
    
    def detect(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect if a user is a bot.
        
        Args:
            user_data: Dictionary containing user information and activity
            
        Returns:
            Dictionary containing detection results:
                - is_bot: Boolean indicating if user is detected as a bot
                - confidence: Confidence score (0-1)
                - method: Detection method used
                - details: Additional detection details
        """
        # Extract features
        features = self.feature_extractor.extract_features(user_data)
        
        results = {
            'is_bot': False,
            'confidence': 0.0,
            'method': 'none',
            'details': {},
            'features': features
        }
        
        ml_result = None
        rule_result = None
        
        # Run ML detection
        if self.use_ml and self.ml_detector:
            is_bot_ml, confidence_ml = self.ml_detector.detect(features)
            ml_result = {
                'is_bot': is_bot_ml,
                'confidence': confidence_ml
            }
            results['details']['ml'] = ml_result
        
        # Run rule-based detection
        if self.use_rules and self.rule_detector:
            is_bot_rule, confidence_rule, triggered_rules = self.rule_detector.detect(features)
            rule_result = {
                'is_bot': is_bot_rule,
                'confidence': confidence_rule,
                'triggered_rules': triggered_rules
            }
            results['details']['rules'] = rule_result
        
        # Combine results
        if ml_result and rule_result:
            # Both methods available - use weighted combination
            combined_confidence = (0.6 * ml_result['confidence'] + 
                                 0.4 * rule_result['confidence'])
            results['is_bot'] = combined_confidence > 0.5
            results['confidence'] = combined_confidence
            results['method'] = 'combined'
        elif ml_result:
            # Only ML available
            results['is_bot'] = ml_result['is_bot']
            results['confidence'] = ml_result['confidence']
            results['method'] = 'ml'
        elif rule_result:
            # Only rules available
            results['is_bot'] = rule_result['is_bot']
            results['confidence'] = rule_result['confidence']
            results['method'] = 'rules'
        
        return results
    
    def detect_batch(self, users_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect bots in a batch of users.
        
        Args:
            users_data: List of user data dictionaries
            
        Returns:
            List of detection results
        """
        return [self.detect(user_data) for user_data in users_data]
    
    def get_explanation(self, user_data: Dict[str, Any]) -> str:
        """
        Get human-readable explanation of detection result.
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            Explanation string
        """
        result = self.detect(user_data)
        
        explanation = f"Detection Result for user '{user_data.get('username', 'Unknown')}'\n"
        explanation += "=" * 60 + "\n\n"
        
        if result['is_bot']:
            explanation += f"⚠️  BOT DETECTED (Confidence: {result['confidence']:.2%})\n\n"
        else:
            explanation += f"✓ Likely Legitimate User (Bot score: {result['confidence']:.2%})\n\n"
        
        explanation += f"Detection Method: {result['method']}\n\n"
        
        # Add rule-based details
        if 'rules' in result['details']:
            rule_details = result['details']['rules']
            explanation += "Rule-Based Analysis:\n"
            explanation += f"  Score: {rule_details['confidence']:.2%}\n"
            if rule_details.get('triggered_rules'):
                explanation += "  Triggered Rules:\n"
                for rule in rule_details['triggered_rules']:
                    explanation += f"    - {rule}\n"
            explanation += "\n"
        
        # Add ML details
        if 'ml' in result['details']:
            ml_details = result['details']['ml']
            explanation += "Machine Learning Analysis:\n"
            explanation += f"  Confidence: {ml_details['confidence']:.2%}\n"
            explanation += f"  Classification: {'Bot' if ml_details['is_bot'] else 'Legitimate'}\n\n"
        
        # Add key features
        explanation += "Key Features:\n"
        features = result['features']
        explanation += f"  Account Age: {features.get('account_age_days', 0):.0f} days\n"
        explanation += f"  Profile Image: {'Yes' if features.get('has_profile_image') else 'No'}\n"
        explanation += f"  Bio: {'Yes' if features.get('has_bio') else 'No'}\n"
        explanation += f"  Followers: {features.get('follower_count', 0):.0f}\n"
        explanation += f"  Following: {features.get('following_count', 0):.0f}\n"
        explanation += f"  Post Frequency: {features.get('post_frequency', 0):.2f} posts/day\n"
        
        return explanation
    
    def update_config(self, rule_config: Optional[Dict[str, Any]] = None) -> None:
        """
        Update detector configuration.
        
        Args:
            rule_config: New configuration for rule-based detector
        """
        if rule_config and self.rule_detector:
            self.rule_detector.config.update(rule_config)
