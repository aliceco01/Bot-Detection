"""
Basic usage example for the bot detection system.
"""

from datetime import datetime, timedelta
from bot_detector import BotDetector


def main():
    # Initialize the bot detector
    detector = BotDetector(use_ml=True, use_rules=True)
    
    print("Bot Detection System - Example Usage")
    print("=" * 60)
    print()
    
    # Example 1: Legitimate user
    print("Example 1: Analyzing a legitimate user...")
    legitimate_user = {
        'username': 'john_doe',
        'created_at': (datetime.now() - timedelta(days=365)).isoformat(),
        'has_profile_image': True,
        'bio': 'Software engineer and photography enthusiast. Love hiking and coffee.',
        'verified': False,
        'post_count': 250,
        'follower_count': 450,
        'following_count': 320,
        'recent_posts': [
            {
                'content': 'Beautiful sunset today! #photography #nature',
                'timestamp': (datetime.now() - timedelta(hours=2)).isoformat()
            },
            {
                'content': 'Just finished a great book on ML. Highly recommend!',
                'timestamp': (datetime.now() - timedelta(days=1)).isoformat()
            },
            {
                'content': 'Coffee and code - the perfect combination ☕',
                'timestamp': (datetime.now() - timedelta(days=3)).isoformat()
            }
        ],
        'avg_reply_time_seconds': 120,
        'interactions': {
            'replies': ['user1', 'user2', 'user3', 'user4'],
            'mentions': ['user5', 'user6', 'user7']
        }
    }
    
    result = detector.detect(legitimate_user)
    print(f"Result: {'🤖 BOT' if result['is_bot'] else '✓ LEGITIMATE'}")
    print(f"Confidence: {result['confidence']:.2%}")
    print()
    print(detector.get_explanation(legitimate_user))
    print()
    
    # Example 2: Suspicious bot account
    print("\n" + "=" * 60)
    print("Example 2: Analyzing a suspicious bot account...")
    bot_user = {
        'username': 'user_12345_bot',
        'created_at': (datetime.now() - timedelta(days=3)).isoformat(),
        'has_profile_image': False,
        'bio': '',
        'verified': False,
        'post_count': 500,
        'follower_count': 10,
        'following_count': 2000,
        'recent_posts': [
            {
                'content': 'Check out this amazing product! https://spam-link.com #ad #buy',
                'timestamp': (datetime.now() - timedelta(minutes=5)).isoformat()
            },
            {
                'content': 'Check out this amazing product! https://spam-link.com #ad #buy',
                'timestamp': (datetime.now() - timedelta(minutes=10)).isoformat()
            },
            {
                'content': 'Limited time offer! Click here: https://spam-link.com #sale',
                'timestamp': (datetime.now() - timedelta(minutes=15)).isoformat()
            },
            {
                'content': 'Check out this amazing product! https://spam-link.com #ad #buy',
                'timestamp': (datetime.now() - timedelta(minutes=20)).isoformat()
            }
        ],
        'avg_reply_time_seconds': 2,
        'interactions': {
            'replies': ['target_user', 'target_user', 'target_user'],
            'mentions': ['target_user']
        }
    }
    
    result = detector.detect(bot_user)
    print(f"Result: {'🤖 BOT' if result['is_bot'] else '✓ LEGITIMATE'}")
    print(f"Confidence: {result['confidence']:.2%}")
    print()
    print(detector.get_explanation(bot_user))
    print()
    
    # Example 3: Batch detection
    print("\n" + "=" * 60)
    print("Example 3: Batch detection of multiple users...")
    users = [legitimate_user, bot_user]
    results = detector.detect_batch(users)
    
    for i, result in enumerate(results, 1):
        username = users[i-1]['username']
        status = '🤖 BOT' if result['is_bot'] else '✓ LEGITIMATE'
        print(f"User {i} ({username}): {status} - Confidence: {result['confidence']:.2%}")


if __name__ == '__main__':
    main()
