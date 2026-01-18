"""
Advanced usage example showing custom configuration and model training.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from datetime import datetime, timedelta
from bot_detector import BotDetector
import numpy as np


def example_custom_configuration():
    """Example of using custom rule configuration."""
    print("Example: Custom Rule Configuration")
    print("=" * 60)
    
    # Create detector with custom thresholds
    custom_config = {
        'min_account_age_days': 30,  # Stricter account age requirement
        'max_post_frequency': 30.0,  # Lower posting frequency threshold
        'bot_score_threshold': 0.5,  # Lower threshold for bot detection
    }
    
    detector = BotDetector(use_ml=False, use_rules=True, rule_config=custom_config)
    
    test_user = {
        'username': 'test_user',
        'created_at': (datetime.now() - timedelta(days=15)).isoformat(),
        'has_profile_image': True,
        'bio': 'Just a regular user',
        'verified': False,
        'post_count': 100,
        'follower_count': 50,
        'following_count': 60,
        'recent_posts': [
            {'content': 'Post 1', 'timestamp': datetime.now().isoformat()},
            {'content': 'Post 2', 'timestamp': (datetime.now() - timedelta(hours=1)).isoformat()},
        ],
        'avg_reply_time_seconds': 60,
    }
    
    result = detector.detect(test_user)
    print(detector.get_explanation(test_user))
    print()


def example_ml_only():
    """Example of using only ML-based detection."""
    print("Example: ML-Only Detection")
    print("=" * 60)
    
    # Use only ML detector (with heuristic fallback since no model is loaded)
    detector = BotDetector(use_ml=True, use_rules=False)
    
    verified_user = {
        'username': 'verified_celeb',
        'created_at': (datetime.now() - timedelta(days=2000)).isoformat(),
        'has_profile_image': True,
        'bio': 'Official account. Verified user.',
        'verified': True,
        'post_count': 5000,
        'follower_count': 1000000,
        'following_count': 500,
        'recent_posts': [
            {'content': 'Hello everyone!', 'timestamp': datetime.now().isoformat()},
        ],
        'avg_reply_time_seconds': 300,
    }
    
    result = detector.detect(verified_user)
    print(f"User: {verified_user['username']}")
    print(f"Result: {'🤖 BOT' if result['is_bot'] else '✓ LEGITIMATE'}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Method: {result['method']}")
    print()


def example_feature_extraction():
    """Example of extracting and examining features."""
    print("Example: Feature Extraction")
    print("=" * 60)
    
    from bot_detector.features import FeatureExtractor
    
    extractor = FeatureExtractor()
    
    user = {
        'username': 'feature_test',
        'created_at': (datetime.now() - timedelta(days=100)).isoformat(),
        'has_profile_image': True,
        'bio': 'Testing feature extraction',
        'verified': False,
        'post_count': 50,
        'follower_count': 200,
        'following_count': 150,
        'recent_posts': [
            {
                'content': 'First post with #hashtag',
                'timestamp': (datetime.now() - timedelta(days=1)).isoformat()
            },
            {
                'content': 'Second post with link https://example.com',
                'timestamp': (datetime.now() - timedelta(days=2)).isoformat()
            },
        ],
    }
    
    features = extractor.extract_features(user)
    
    print("Extracted Features:")
    for feature_name, feature_value in sorted(features.items()):
        print(f"  {feature_name}: {feature_value}")
    print()


def example_simulation():
    """Simulate detection on multiple account types."""
    print("Example: Detection Simulation on Various Account Types")
    print("=" * 60)
    
    detector = BotDetector(use_ml=True, use_rules=True)
    
    # Various account types
    accounts = [
        {
            'name': 'Established User',
            'data': {
                'username': 'established_user',
                'created_at': (datetime.now() - timedelta(days=1000)).isoformat(),
                'has_profile_image': True,
                'bio': 'Long-time user sharing thoughts and photos',
                'verified': False,
                'post_count': 2000,
                'follower_count': 800,
                'following_count': 600,
                'recent_posts': [
                    {'content': 'Just a normal post', 'timestamp': datetime.now().isoformat()},
                ],
            }
        },
        {
            'name': 'New Legitimate User',
            'data': {
                'username': 'new_user',
                'created_at': (datetime.now() - timedelta(days=10)).isoformat(),
                'has_profile_image': True,
                'bio': 'New here! Excited to connect',
                'verified': False,
                'post_count': 5,
                'follower_count': 10,
                'following_count': 20,
                'recent_posts': [
                    {'content': 'First post!', 'timestamp': datetime.now().isoformat()},
                ],
            }
        },
        {
            'name': 'Spam Bot',
            'data': {
                'username': 'bot_spam_123',
                'created_at': (datetime.now() - timedelta(days=1)).isoformat(),
                'has_profile_image': False,
                'bio': '',
                'verified': False,
                'post_count': 1000,
                'follower_count': 5,
                'following_count': 5000,
                'recent_posts': [
                    {'content': 'BUY NOW! https://spam.com', 'timestamp': datetime.now().isoformat()},
                    {'content': 'BUY NOW! https://spam.com', 'timestamp': datetime.now().isoformat()},
                    {'content': 'BUY NOW! https://spam.com', 'timestamp': datetime.now().isoformat()},
                ],
            }
        },
    ]
    
    for account in accounts:
        result = detector.detect(account['data'])
        print(f"\n{account['name']}:")
        print(f"  Username: {account['data']['username']}")
        print(f"  Detection: {'🤖 BOT' if result['is_bot'] else '✓ LEGITIMATE'}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Method: {result['method']}")


def main():
    """Run all examples."""
    example_custom_configuration()
    print("\n")
    
    example_ml_only()
    print("\n")
    
    example_feature_extraction()
    print("\n")
    
    example_simulation()


if __name__ == '__main__':
    main()
