"""
Unit tests for the bot detection system.
"""

import unittest
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bot_detector import BotDetector, FeatureExtractor, RuleBasedDetector, MLBotDetector


class TestFeatureExtractor(unittest.TestCase):
    """Test the feature extraction functionality."""
    
    def setUp(self):
        self.extractor = FeatureExtractor()
    
    def test_basic_feature_extraction(self):
        """Test basic feature extraction."""
        user_data = {
            'username': 'test_user',
            'created_at': (datetime.now() - timedelta(days=100)).isoformat(),
            'has_profile_image': True,
            'bio': 'Test bio',
            'verified': False,
            'post_count': 50,
            'follower_count': 100,
            'following_count': 80,
        }
        
        features = self.extractor.extract_features(user_data)
        
        self.assertIn('account_age_days', features)
        self.assertIn('has_profile_image', features)
        self.assertIn('post_count', features)
        self.assertEqual(features['has_profile_image'], 1.0)
        self.assertGreater(features['account_age_days'], 90)
    
    def test_username_patterns(self):
        """Test username pattern detection."""
        # Test username with numbers
        user_data = {'username': 'user123', 'created_at': datetime.now().isoformat()}
        features = self.extractor.extract_features(user_data)
        self.assertEqual(features['username_has_numbers'], 1.0)
        
        # Test random pattern
        user_data = {'username': 'ab12cd34', 'created_at': datetime.now().isoformat()}
        features = self.extractor.extract_features(user_data)
        self.assertEqual(features['username_random_pattern'], 1.0)
    
    def test_post_features(self):
        """Test post-related feature extraction."""
        user_data = {
            'username': 'test',
            'recent_posts': [
                {
                    'content': 'Check this out! https://example.com #test',
                    'timestamp': datetime.now().isoformat()
                },
                {
                    'content': 'Check this out! https://example.com #test',
                    'timestamp': (datetime.now() - timedelta(hours=1)).isoformat()
                },
            ]
        }
        
        features = self.extractor.extract_features(user_data)
        
        self.assertGreater(features['duplicate_content_ratio'], 0.9)
        self.assertEqual(features['url_ratio'], 1.0)
        self.assertGreater(features['hashtag_ratio'], 0)


class TestRuleBasedDetector(unittest.TestCase):
    """Test the rule-based detection."""
    
    def setUp(self):
        self.detector = RuleBasedDetector()
    
    def test_legitimate_user(self):
        """Test detection of legitimate user."""
        features = {
            'account_age_days': 365,
            'has_profile_image': 1.0,
            'has_bio': 1.0,
            'bio_length': 50,
            'username_random_pattern': 0.0,
            'post_frequency': 2.0,
            'duplicate_content_ratio': 0.1,
            'url_ratio': 0.2,
            'follower_following_ratio': 1.5,
            'avg_reply_time': 120,
            'interaction_diversity': 0.8,
        }
        
        is_bot, score, rules = self.detector.detect(features)
        
        self.assertFalse(is_bot)
        self.assertLess(score, 0.6)
    
    def test_bot_user(self):
        """Test detection of bot user."""
        features = {
            'account_age_days': 2,
            'has_profile_image': 0.0,
            'has_bio': 0.0,
            'bio_length': 0,
            'username_random_pattern': 1.0,
            'post_frequency': 100.0,
            'duplicate_content_ratio': 0.9,
            'url_ratio': 0.9,
            'follower_following_ratio': 0.01,
            'avg_reply_time': 2,
            'interaction_diversity': 0.05,
        }
        
        is_bot, score, rules = self.detector.detect(features)
        
        self.assertTrue(is_bot)
        self.assertGreater(score, 0.6)
        self.assertGreater(len(rules), 3)


class TestMLBotDetector(unittest.TestCase):
    """Test the ML-based detection."""
    
    def setUp(self):
        self.detector = MLBotDetector()
    
    def test_heuristic_detection(self):
        """Test heuristic detection when no model is loaded."""
        # Legitimate user features
        features = {
            'has_profile_image': 1.0,
            'has_bio': 1.0,
            'has_verified_badge': 0.0,
            'account_age_days': 100,
            'username_random_pattern': 0.0,
            'post_frequency': 2.0,
            'duplicate_content_ratio': 0.1,
            'url_ratio': 0.2,
            'follower_following_ratio': 1.2,
        }
        
        is_bot, confidence = self.detector.detect(features)
        
        # Should detect as legitimate
        self.assertIsInstance(is_bot, bool)
        self.assertIsInstance(confidence, float)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)


class TestBotDetector(unittest.TestCase):
    """Test the main bot detector."""
    
    def setUp(self):
        self.detector = BotDetector(use_ml=True, use_rules=True)
    
    def test_detect_legitimate_user(self):
        """Test detection of a legitimate user."""
        user_data = {
            'username': 'john_doe',
            'created_at': (datetime.now() - timedelta(days=365)).isoformat(),
            'has_profile_image': True,
            'bio': 'Software engineer and photography enthusiast.',
            'verified': False,
            'post_count': 200,
            'follower_count': 400,
            'following_count': 300,
            'recent_posts': [
                {
                    'content': 'Beautiful day today!',
                    'timestamp': datetime.now().isoformat()
                },
            ],
            'avg_reply_time_seconds': 120,
        }
        
        result = self.detector.detect(user_data)
        
        self.assertIn('is_bot', result)
        self.assertIn('confidence', result)
        self.assertIn('method', result)
        self.assertIn('features', result)
        self.assertIsInstance(result['is_bot'], bool)
    
    def test_detect_bot_user(self):
        """Test detection of a bot user."""
        user_data = {
            'username': 'bot_12345',
            'created_at': (datetime.now() - timedelta(days=2)).isoformat(),
            'has_profile_image': False,
            'bio': '',
            'verified': False,
            'post_count': 1000,
            'follower_count': 5,
            'following_count': 2000,
            'recent_posts': [
                {
                    'content': 'Check this out! https://spam.com',
                    'timestamp': datetime.now().isoformat()
                },
                {
                    'content': 'Check this out! https://spam.com',
                    'timestamp': (datetime.now() - timedelta(minutes=5)).isoformat()
                },
            ],
            'avg_reply_time_seconds': 2,
        }
        
        result = self.detector.detect(user_data)
        
        self.assertTrue(result['is_bot'])
        self.assertGreater(result['confidence'], 0.5)
    
    def test_batch_detection(self):
        """Test batch detection."""
        users = [
            {'username': 'user1', 'created_at': datetime.now().isoformat()},
            {'username': 'user2', 'created_at': datetime.now().isoformat()},
        ]
        
        results = self.detector.detect_batch(users)
        
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertIn('is_bot', result)
            self.assertIn('confidence', result)
    
    def test_get_explanation(self):
        """Test explanation generation."""
        user_data = {
            'username': 'test_user',
            'created_at': datetime.now().isoformat(),
        }
        
        explanation = self.detector.get_explanation(user_data)
        
        self.assertIsInstance(explanation, str)
        self.assertIn('test_user', explanation)


if __name__ == '__main__':
    unittest.main()
