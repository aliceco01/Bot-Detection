"""
Feature extraction module for bot detection.
Extracts relevant features from user activity data.
"""

from typing import Dict, List, Any
import re
from datetime import datetime


class FeatureExtractor:
    """Extract features from user activity for bot detection."""
    
    def extract_features(self, user_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract features from user data.
        
        Args:
            user_data: Dictionary containing user information and activity
            
        Returns:
            Dictionary of extracted features
        """
        features = {}
        
        # Account age features
        features['account_age_days'] = self._get_account_age(user_data)
        
        # Profile features
        features['has_profile_image'] = float(user_data.get('has_profile_image', False))
        features['has_bio'] = float(bool(user_data.get('bio', '')))
        features['bio_length'] = len(user_data.get('bio', ''))
        features['has_verified_badge'] = float(user_data.get('verified', False))
        
        # Username features
        features['username_has_numbers'] = float(self._has_numbers(user_data.get('username', '')))
        features['username_length'] = len(user_data.get('username', ''))
        features['username_random_pattern'] = float(self._is_random_pattern(user_data.get('username', '')))
        
        # Activity features
        features['post_count'] = user_data.get('post_count', 0)
        features['follower_count'] = user_data.get('follower_count', 0)
        features['following_count'] = user_data.get('following_count', 0)
        
        # Engagement ratios
        features['follower_following_ratio'] = self._safe_ratio(
            features['follower_count'], 
            features['following_count']
        )
        features['post_follower_ratio'] = self._safe_ratio(
            features['post_count'], 
            features['follower_count']
        )
        
        # Posting behavior
        posts = user_data.get('recent_posts', [])
        features['avg_post_length'] = self._get_avg_post_length(posts)
        features['post_frequency'] = self._get_post_frequency(posts)
        features['duplicate_content_ratio'] = self._get_duplicate_ratio(posts)
        features['url_ratio'] = self._get_url_ratio(posts)
        features['hashtag_ratio'] = self._get_hashtag_ratio(posts)
        
        # Interaction patterns
        features['avg_reply_time'] = user_data.get('avg_reply_time_seconds', 0)
        features['interaction_diversity'] = self._get_interaction_diversity(user_data)
        
        return features
    
    def _get_account_age(self, user_data: Dict[str, Any]) -> float:
        """Calculate account age in days."""
        created_at = user_data.get('created_at')
        if not created_at:
            return 0.0
        
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            except:
                return 0.0
        
        age = (datetime.now(created_at.tzinfo) - created_at).days
        return float(max(0, age))
    
    def _has_numbers(self, text: str) -> bool:
        """Check if text contains numbers."""
        return bool(re.search(r'\d', text))
    
    def _is_random_pattern(self, username: str) -> bool:
        """Detect random-looking username patterns."""
        # Check for long sequences of numbers or random characters
        if re.search(r'\d{5,}', username):
            return True
        if re.search(r'[a-z]{2}\d{2,}[a-z]{2}\d{2,}', username.lower()):
            return True
        return False
    
    def _safe_ratio(self, numerator: float, denominator: float) -> float:
        """Calculate ratio safely, avoiding division by zero."""
        if denominator == 0:
            return 0.0
        return numerator / denominator
    
    def _get_avg_post_length(self, posts: List[Dict[str, Any]]) -> float:
        """Calculate average post length."""
        if not posts:
            return 0.0
        lengths = [len(post.get('content', '')) for post in posts]
        return sum(lengths) / len(lengths)
    
    def _get_post_frequency(self, posts: List[Dict[str, Any]]) -> float:
        """Calculate posting frequency (posts per day)."""
        if len(posts) < 2:
            return 0.0
        
        timestamps = []
        for post in posts:
            timestamp = post.get('timestamp')
            if timestamp:
                if isinstance(timestamp, str):
                    try:
                        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    except:
                        continue
                timestamps.append(timestamp)
        
        if len(timestamps) < 2:
            return 0.0
        
        timestamps.sort()
        time_span = (timestamps[-1] - timestamps[0]).total_seconds() / 86400  # days
        if time_span == 0:
            return len(posts)
        return len(posts) / time_span
    
    def _get_duplicate_ratio(self, posts: List[Dict[str, Any]]) -> float:
        """Calculate ratio of duplicate/similar posts."""
        if len(posts) < 2:
            return 0.0
        
        contents = [post.get('content', '') for post in posts]
        unique_contents = set(contents)
        return 1.0 - (len(unique_contents) / len(contents))
    
    def _get_url_ratio(self, posts: List[Dict[str, Any]]) -> float:
        """Calculate ratio of posts containing URLs."""
        if not posts:
            return 0.0
        
        url_pattern = r'https?://[^\s]+'
        posts_with_urls = sum(1 for post in posts if re.search(url_pattern, post.get('content', '')))
        return posts_with_urls / len(posts)
    
    def _get_hashtag_ratio(self, posts: List[Dict[str, Any]]) -> float:
        """Calculate average hashtag usage ratio."""
        if not posts:
            return 0.0
        
        hashtag_counts = [len(re.findall(r'#\w+', post.get('content', ''))) for post in posts]
        return sum(hashtag_counts) / len(posts)
    
    def _get_interaction_diversity(self, user_data: Dict[str, Any]) -> float:
        """Calculate diversity of user interactions."""
        interactions = user_data.get('interactions', {})
        if not interactions:
            return 0.0
        
        # Count unique users interacted with
        unique_users = set()
        for interaction_list in interactions.values():
            if isinstance(interaction_list, list):
                unique_users.update(interaction_list)
        
        total_interactions = sum(len(v) if isinstance(v, list) else 0 for v in interactions.values())
        if total_interactions == 0:
            return 0.0
        
        return len(unique_users) / total_interactions
