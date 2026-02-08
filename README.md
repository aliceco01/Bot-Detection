# Bot Detection System

A comprehensive bot detection system for social media platforms that separates legitimate user activity from automated or malicious bot activity.

## Features

- **Multi-Method Detection**: Combines rule-based and machine learning approaches for robust bot detection
- **Feature Extraction**: Analyzes 20+ behavioral and profile features
- **Flexible Configuration**: Customizable thresholds and detection parameters
- **Batch Processing**: Efficient detection for multiple users
- **Detailed Explanations**: Human-readable reports explaining detection decisions
- **Extensible**: Easy to add custom rules or train custom ML models

## Installation

```bash
# Clone the repository
git clone https://github.com/aliceco01/Bot-Detection.git
cd Bot-Detection

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
from bot_detector import BotDetector
from datetime import datetime, timedelta

# Initialize the detector
detector = BotDetector(use_ml=True, use_rules=True)

# Prepare user data
user_data = {
    'username': 'john_doe',
    'created_at': (datetime.now() - timedelta(days=365)).isoformat(),
    'has_profile_image': True,
    'bio': 'Software engineer and photography enthusiast.',
    'verified': False,
    'post_count': 250,
    'follower_count': 450,
    'following_count': 320,
    'recent_posts': [
        {
            'content': 'Beautiful sunset today! #photography',
            'timestamp': datetime.now().isoformat()
        }
    ],
    'avg_reply_time_seconds': 120,
}

# Detect if user is a bot
result = detector.detect(user_data)

print(f\"Is Bot: {result['is_bot']}\")
print(f\"Confidence: {result['confidence']:.2%}\")
print(f\"Method: {result['method']}\")

# Get detailed explanation
print(detector.get_explanation(user_data))
```

## Detection Methods

### 1. Rule-Based Detection

Uses heuristic rules to identify suspicious patterns:

- **New accounts with high activity**: Recently created accounts posting excessively
- **Poor follower ratios**: Following many but having few followers
- **Missing profile elements**: No profile image or bio
- **Random username patterns**: Usernames with random character sequences
- **Excessive posting**: Unrealistic posting frequencies
- **Duplicate content**: High ratio of repeated posts
- **URL spam**: Excessive link sharing
- **Fast reply times**: Suspiciously quick automated responses
- **Low interaction diversity**: Repeatedly interacting with same accounts

### 2. Machine Learning Detection

Uses trained models (or heuristics when no model is loaded) to classify users based on:

- Account age and verification status
- Profile completeness
- Username characteristics
- Posting behavior patterns
- Engagement metrics
- Content analysis

### 3. Combined Detection

Weights both methods for optimal accuracy:
- ML detection: 60% weight
- Rule-based detection: 40% weight

## User Data Format

The system expects user data in the following format:

```python
{
    # Profile Information
    'username': str,              # Username
    'created_at': str,            # ISO format datetime
    'has_profile_image': bool,    # Profile image present
    'bio': str,                   # User bio/description
    'verified': bool,             # Verification badge
    
    # Activity Metrics
    'post_count': int,            # Total posts
    'follower_count': int,        # Number of followers
    'following_count': int,       # Number following
    
    # Recent Posts (list of dicts)
    'recent_posts': [
        {
            'content': str,        # Post content
            'timestamp': str       # ISO format datetime
        }
    ],
    
    # Interaction Data
    'avg_reply_time_seconds': float,  # Average reply time
    'interactions': {
        'replies': list,          # User IDs replied to
        'mentions': list          # User IDs mentioned
    }
}
```

## Advanced Usage

### Custom Configuration

```python
from bot_detector import BotDetector

# Custom rule thresholds
custom_config = {
    'min_account_age_days': 30,
    'max_post_frequency': 30.0,
    'bot_score_threshold': 0.5,
}

detector = BotDetector(
    use_ml=True,
    use_rules=True,
    rule_config=custom_config
)
```

### Rule-Based Only

```python
detector = BotDetector(use_ml=False, use_rules=True)
result = detector.detect(user_data)
```

### Machine Learning Only

```python
detector = BotDetector(use_ml=True, use_rules=False)
result = detector.detect(user_data)
```

### Batch Detection

```python
users_data = [user1_data, user2_data, user3_data]
results = detector.detect_batch(users_data)

for i, result in enumerate(results):
    print(f\"User {i+1}: {'Bot' if result['is_bot'] else 'Legitimate'}\")
```

### Feature Extraction

```python
from bot_detector import FeatureExtractor

extractor = FeatureExtractor()
features = extractor.extract_features(user_data)

# View all extracted features
for feature_name, value in features.items():
    print(f\"{feature_name}: {value}\")
```

### Training Custom ML Models

```python
from bot_detector.ml_detector import MLBotDetector
import numpy as np

# Prepare training data
X_train = np.array([...])  # Feature vectors
y_train = np.array([...])  # Labels (0=legitimate, 1=bot)

# Train model
ml_detector = MLBotDetector()
ml_detector.train(X_train, y_train, algorithm='random_forest')

# Save model
ml_detector.save_model('my_bot_model.pkl')

# Use trained model
detector = BotDetector(use_ml=True, model_path='my_bot_model.pkl')
```

## Extracted Features

The system extracts and analyzes 20+ features:

| Feature | Description |
|---------|-------------|
| `account_age_days` | Account age in days |
| `has_profile_image` | Profile image present (0/1) |
| `has_bio` | Bio present (0/1) |
| `bio_length` | Length of bio |
| `has_verified_badge` | Verified status (0/1) |
| `username_has_numbers` | Username contains numbers (0/1) |
| `username_length` | Length of username |
| `username_random_pattern` | Random pattern detected (0/1) |
| `post_count` | Total number of posts |
| `follower_count` | Number of followers |
| `following_count` | Number following |
| `follower_following_ratio` | followers/following ratio |
| `post_follower_ratio` | posts/followers ratio |
| `avg_post_length` | Average post length |
| `post_frequency` | Posts per day |
| `duplicate_content_ratio` | Ratio of duplicate posts |
| `url_ratio` | Ratio of posts with URLs |
| `hashtag_ratio` | Average hashtags per post |
| `avg_reply_time` | Average reply time (seconds) |
| `interaction_diversity` | Diversity of interactions |

## Examples

The `examples/` directory contains:

- `basic_usage.py`: Simple examples demonstrating core functionality
- `advanced_usage.py`: Advanced features and custom configurations

Run examples:

```bash
# Add src to Python path and run
export PYTHONPATH=\"${PYTHONPATH}:./src\"
python examples/basic_usage.py
python examples/advanced_usage.py
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
# or
python -m unittest discover tests/
```

## Project Structure

```
Bot-Detection/
├── src/
│   └── bot_detector/
│       ├── __init__.py         # Package initialization
│       ├── detector.py         # Main BotDetector class
│       ├── features.py         # Feature extraction
│       ├── rule_detector.py    # Rule-based detection
│       └── ml_detector.py      # ML-based detection
├── tests/
│   └── test_bot_detector.py    # Unit tests
├── examples/
│   ├── basic_usage.py          # Basic examples
│   └── advanced_usage.py       # Advanced examples
├── requirements.txt            # Dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Detection Output

The `detect()` method returns a dictionary with:

```python
{
    'is_bot': bool,              # True if detected as bot
    'confidence': float,         # Confidence score (0-1)
    'method': str,               # Detection method used
    'features': dict,            # Extracted features
    'details': {
        'ml': {                  # ML detection details
            'is_bot': bool,
            'confidence': float
        },
        'rules': {               # Rule-based details
            'is_bot': bool,
            'confidence': float,
            'triggered_rules': list
        }
    }
}
```

## Use Cases

- **Social Media Platforms**: Identify and flag bot accounts
- **Content Moderation**: Filter automated spam
- **Analytics**: Separate real engagement from bot activity
- **Security**: Detect malicious automation
- **Research**: Study bot behavior patterns

## Customization

### Adding Custom Rules

Edit `src/bot_detector/rule_detector.py` to add new detection rules.

### Training Custom Models

Use your own labeled dataset to train specialized models:

1. Collect labeled data (bot vs. legitimate users)
2. Extract features using `FeatureExtractor`
3. Train model using `MLBotDetector.train()`
4. Save and load for production use
