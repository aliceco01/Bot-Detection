"""
Machine learning-based bot detection module.
Uses trained models to classify users as bots or legitimate.
"""

from typing import Dict, Any, Tuple, Optional
import numpy as np


class MLBotDetector:
    """Machine learning-based bot detector."""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize ML-based detector.
        
        Args:
            model_path: Path to pre-trained model (optional)
        """
        self.model = None
        self.feature_names = [
            'account_age_days',
            'has_profile_image',
            'has_bio',
            'bio_length',
            'has_verified_badge',
            'username_has_numbers',
            'username_length',
            'username_random_pattern',
            'post_count',
            'follower_count',
            'following_count',
            'follower_following_ratio',
            'post_follower_ratio',
            'avg_post_length',
            'post_frequency',
            'duplicate_content_ratio',
            'url_ratio',
            'hashtag_ratio',
            'avg_reply_time',
            'interaction_diversity'
        ]
        
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path: str) -> None:
        """
        Load a pre-trained model.
        
        Args:
            model_path: Path to model file
        """
        try:
            import joblib
            self.model = joblib.load(model_path)
        except Exception as e:
            raise ValueError(f"Failed to load model from {model_path}: {e}")
    
    def detect(self, features: Dict[str, float]) -> Tuple[bool, float]:
        """
        Detect if user is a bot using ML model.
        
        Args:
            features: Dictionary of extracted features
            
        Returns:
            Tuple of (is_bot, confidence_score)
        """
        if self.model is None:
            # Use simple heuristic if no model is loaded
            return self._simple_heuristic(features)
        
        # Prepare feature vector
        feature_vector = self._prepare_features(features)
        
        try:
            # Get prediction and probability
            prediction = self.model.predict([feature_vector])[0]
            probabilities = self.model.predict_proba([feature_vector])[0]
            
            is_bot = bool(prediction)
            confidence = probabilities[1] if is_bot else probabilities[0]
            
            return is_bot, float(confidence)
        except Exception as e:
            # Fallback to heuristic if prediction fails
            return self._simple_heuristic(features)
    
    def _prepare_features(self, features: Dict[str, float]) -> np.ndarray:
        """
        Prepare feature vector for model input.
        
        Args:
            features: Dictionary of features
            
        Returns:
            Numpy array of features in correct order
        """
        feature_vector = []
        for name in self.feature_names:
            value = features.get(name, 0.0)
            feature_vector.append(value)
        
        return np.array(feature_vector)
    
    def _simple_heuristic(self, features: Dict[str, float]) -> Tuple[bool, float]:
        """
        Simple heuristic when no model is available.
        
        Args:
            features: Dictionary of features
            
        Returns:
            Tuple of (is_bot, confidence_score)
        """
        # Calculate a simple weighted score
        score = 0.0
        
        # Negative indicators (good signs)
        if features.get('has_profile_image', 0):
            score -= 0.1
        if features.get('has_bio', 0):
            score -= 0.1
        if features.get('has_verified_badge', 0):
            score -= 0.3
        if features.get('account_age_days', 0) > 30:
            score -= 0.15
        
        # Positive indicators (bot signs)
        if features.get('username_random_pattern', 0):
            score += 0.2
        if features.get('post_frequency', 0) > 20:
            score += 0.2
        if features.get('duplicate_content_ratio', 0) > 0.5:
            score += 0.25
        if features.get('url_ratio', 0) > 0.7:
            score += 0.2
        if features.get('follower_following_ratio', 1.0) < 0.1:
            score += 0.15
        
        # Normalize to 0-1 range
        normalized_score = max(0.0, min(1.0, (score + 0.5)))
        is_bot = normalized_score > 0.6
        
        return is_bot, normalized_score
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, algorithm: str = 'random_forest') -> None:
        """
        Train a new model.
        
        Args:
            X_train: Training features
            y_train: Training labels
            algorithm: Algorithm to use ('random_forest', 'svm', 'gradient_boosting')
        """
        if algorithm == 'random_forest':
            from sklearn.ensemble import RandomForestClassifier
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif algorithm == 'svm':
            from sklearn.svm import SVC
            self.model = SVC(probability=True, random_state=42)
        elif algorithm == 'gradient_boosting':
            from sklearn.ensemble import GradientBoostingClassifier
            self.model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        self.model.fit(X_train, y_train)
    
    def save_model(self, model_path: str) -> None:
        """
        Save the trained model.
        
        Args:
            model_path: Path to save model
        """
        if self.model is None:
            raise ValueError("No model to save")
        
        import joblib
        joblib.dump(self.model, model_path)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from trained model.
        
        Returns:
            Dictionary mapping feature names to importance scores
        """
        if self.model is None:
            return {}
        
        if not hasattr(self.model, 'feature_importances_'):
            return {}
        
        importances = self.model.feature_importances_
        return dict(zip(self.feature_names, importances))
