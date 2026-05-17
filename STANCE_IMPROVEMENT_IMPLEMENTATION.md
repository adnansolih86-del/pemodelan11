# 🔧 STANCE ANALYSIS IMPROVEMENT - IMPLEMENTATION GUIDE

Panduan praktis untuk memperbaiki model stance analysis dengan kode siap pakai.

---

## 1. FASE 1: IMMEDIATE FIXES (1-2 Hari)

### 1.1 Indonesian Slang & Idiom Lexicon

**File: `indonesian_stance_lexicon.py`**

```python
"""
Comprehensive Indonesian sentiment lexicon for stance analysis.
Focus: Slang, idioms, and colloquial expressions commonly used in Indonesian political discourse.
"""

INDONESIAN_NEGATIVE_LEXICON = {
    # SLANG - Strong Negatives
    'tolol': -1.0,              # stupid/idiot
    'goblog': -1.0,             # idiot (makian kuat)
    'gak becus': -0.95,         # not competent
    'gak punya otak': -0.95,    # brainless/stupid
    'maling': -0.95,            # thief (corruption metaphor)
    'koruptor': -0.95,          # corrupt person
    'penipu': -0.90,            # fraud/deceiver
    'gk ada obatnya': -0.95,    # hopeless/no cure
    'blunder': -0.85,           # mistake/blunder
    'merugikan': -0.85,         # harmful/disadvantageous
    'ditipu': -0.90,            # deceived
    'kekerasan': -0.95,         # violence/abuse
    'dicambuk': -0.98,          # whipped (physical abuse)
    'love scamming': -0.95,     # romance scam
    
    # FORMAL NEGATIVES
    'buruk': -0.85,
    'buruk sekali': -0.90,
    'jelek': -0.80,
    'tidak independen': -0.80,
    'gagal': -0.85,
    'kegagalan': -0.85,
    'negatif': -0.75,
    
    # IDIOMS
    'kurang makan sekolahan': -0.85,  # not well-educated (idiom)
    'gak nyambung': -0.75,             # incoherent/doesn't make sense
    'berbicara sembarangan': -0.80,    # speak carelessly
    'bikin malu': -0.85,               # embarrassing
    
    # COMPOUND CRITICISMS
    'tidak cocok': -0.70,
    'tidak pantas': -0.75,
    'tidak mampu': -0.75,
}

INDONESIAN_POSITIVE_LEXICON = {
    # SLANG - Strong Positives
    'keren': 0.85,              # cool/awesome
    'keren banget': 0.95,       # really cool
    'gokil': 0.90,              # crazy good (slang)
    'mantap': 0.90,             # solid/good
    'asik': 0.85,               # fun/good
    'ciamik': 0.85,             # nice/good (slang)
    'oke': 0.75,                # okay/good
    'super': 0.85,              # great
    'hebat': 0.85,              # great/awesome
    'bagus': 0.80,              # good
    'bagus sekali': 0.90,       # very good
    
    # IDIOMS
    'bikin hati lega': 0.90,    # brings relief
    'hati senang': 0.90,        # happy/glad
    'masa depan cerah': 0.85,   # bright future
    'langkah maju': 0.85,       # step forward
    'makin terjamin': 0.75,     # more secure
    
    # EMOTIONS & APPRECIATION
    'bangga': 0.90,             # proud
    'bangga atas': 0.95,        # proud of
    'terima kasih bakti': 0.85, # grateful for service
    'apresiasi': 0.80,          # appreciation
    'hormat': 0.75,             # respect
    'kagum': 0.85,              # admire
    'kagum pada': 0.90,         # admire towards
    
    # OPTIMISM & CONFIDENCE
    'optimis': 0.80,            # optimistic
    'harapan': 0.75,            # hope
    'percaya': 0.70,            # believe/trust
    'percaya diri': 0.75,       # confident
    'yakin': 0.75,              # confident
    
    # POSITIVE ACTIONS
    'maju': 0.75,               # progress/advance
    'sukses': 0.85,             # success
    'berhasil': 0.80,           # successful
    'nyata': 0.70,              # real/concrete (in positive context)
}

# Contextual boosters & reducers
INTENSITY_BOOSTERS = {
    'sangat': 1.5,              # very
    'banget': 1.5,              # very (slang)
    'sekali': 1.5,              # very
    'amat': 1.4,                # very
    'gila': 1.4,                # crazy (intensifier)
    'parah': 1.3,               # severe
}

INTENSITY_REDUCERS = {
    'agak': 0.7,                # somewhat
    'sedikit': 0.7,             # a bit
    'kurang': 0.7,              # less/lacking
    'cukup': 0.8,               # quite
}

# Negation words
NEGATION_WORDS = {
    'tidak', 'gak', 'gk', 'tidak pernah', 'bukan', 
    'belum', 'jangan', 'misal', 'seolah'
}

# Sarcasm & Passive-Aggressive Patterns
SARCASM_PATTERNS = [
    r'maaf ya.*(?:tapi|namun|justru|malah)',  # maaf ya + contradiction
    r'mohon dimaklumi',                         # false politeness
    r'tidak ada masalah',                       # fake acceptance
    r'sure', r'yeah right',                     # English sarcasm
]

# Rhetorical question markers
RHETORICAL_MARKERS = {
    r'\?\?',      # Multiple question marks
    r'gmana.*bs', # gmana X bisa Y (how can X do Y)
    r'kenapa.*gak', # kenapa gak (why not - rhetorical)
}

print("✓ Indonesian Stance Lexicon loaded")
print(f"  - Negative words: {len(INDONESIAN_NEGATIVE_LEXICON)}")
print(f"  - Positive words: {len(INDONESIAN_POSITIVE_LEXICON)}")
```

---

### 1.2 Enhanced Preprocessing dengan Signal Preservation

**File: `enhanced_preprocessing.py`**

```python
"""
Enhanced preprocessing that preserves sentiment signals while cleaning text.
"""

import re
from dataclasses import dataclass

@dataclass
class PreprocessingSignals:
    """Track sentiment signals that might be lost during preprocessing."""
    has_multiple_caps: int = 0      # Count of ALL CAPS words
    has_multiple_exclamation: int = 0  # Count of ! sequences
    has_multiple_question: int = 0  # Count of ? sequences
    has_repetition: int = 0         # Repeated characters (e.g., gakkkk)
    has_mention: bool = False       # @mention present
    has_hashtag: bool = False       # #hashtag present
    has_url: bool = False
    clean_text: str = ""

def preprocess_with_signals(text: str) -> PreprocessingSignals:
    """
    Preprocess text while preserving important signals.
    
    Args:
        text: Raw text input
        
    Returns:
        PreprocessingSignals object with clean text + signal counts
    """
    
    signals = PreprocessingSignals()
    
    # 1. Extract signals BEFORE cleaning
    signals.has_multiple_caps = len(re.findall(r'\b[A-Z]{2,}\b', text))
    signals.has_multiple_exclamation = text.count('!') if text.count('!') >= 2 else 0
    signals.has_multiple_question = text.count('?') if text.count('?') >= 2 else 0
    signals.has_repetition = len(re.findall(r'(.)\1{2,}', text))
    signals.has_mention = bool(re.search(r'@\w+', text))
    signals.has_hashtag = bool(re.search(r'#\w+', text))
    signals.has_url = bool(re.search(r'http\S+', text))
    
    # 2. Clean text
    clean = text.lower()
    
    # Preserve abbreviations but standardize
    clean = clean.replace('gk ', 'gak ')
    clean = clean.replace('dgn ', 'dengan ')
    clean = clean.replace('dr ', 'dari ')
    
    # Remove URLs, @mentions, #hashtags (but remember they existed)
    clean = re.sub(r'http\S+', '', clean)
    clean = re.sub(r'@\w+', '', clean)
    clean = re.sub(r'#\w+', '', clean)
    
    # Reduce repeated punctuation to single (but signal preserved)
    clean = re.sub(r'!{2,}', '!', clean)
    clean = re.sub(r'\?{2,}', '?', clean)
    
    # Reduce repeated characters (gakkkk → gak, but signal preserved)
    clean = re.sub(r'(.)\1{2,}', r'\1', clean)
    
    # Remove extra whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    
    signals.clean_text = clean
    return signals


def apply_signal_boost(sentiment_score: float, signals: PreprocessingSignals, 
                       base_sentiment: str) -> tuple[float, str]:
    """
    Apply signal-based boosts/reductions to sentiment score.
    
    Args:
        sentiment_score: Base sentiment score (-1 to 1)
        signals: PreprocessingSignals from preprocessing
        base_sentiment: 'positive', 'negative', or 'neutral'
        
    Returns:
        (adjusted_score, reasoning)
    """
    
    adjusted_score = sentiment_score
    reasons = []
    
    if base_sentiment in ['positive', 'negative']:
        # Multiple punctuation = intensity boost
        if signals.has_multiple_exclamation >= 2:
            adjusted_score *= 1.3
            reasons.append(f"Multiple ! marks (x{signals.has_multiple_exclamation})")
        
        if signals.has_multiple_question >= 2:
            adjusted_score *= 1.3
            reasons.append(f"Multiple ? marks (x{signals.has_multiple_question})")
        
        # ALL CAPS words = emphasis
        if signals.has_multiple_caps >= 2:
            adjusted_score *= 1.3
            reasons.append(f"ALL CAPS words (x{signals.has_multiple_caps})")
        
        # Character repetition = emotion emphasis
        if signals.has_repetition >= 1:
            adjusted_score *= 1.2
            reasons.append(f"Character repetition (x{signals.has_repetition})")
    
    # Clamp to valid range
    adjusted_score = max(-1.0, min(1.0, adjusted_score))
    
    reasoning = "; ".join(reasons) if reasons else "Base score"
    
    return adjusted_score, reasoning
```

---

### 1.3 Stance Analyzer dengan Lexicon & Signal Support

**File: `improved_stance_analyzer.py`**

```python
"""
Improved stance analyzer using lexicon + signal preservation.
"""

import pandas as pd
from typing import Tuple
from enhanced_preprocessing import preprocess_with_signals, apply_signal_boost
from indonesian_stance_lexicon import (
    INDONESIAN_NEGATIVE_LEXICON,
    INDONESIAN_POSITIVE_LEXICON,
    INTENSITY_BOOSTERS,
    INTENSITY_REDUCERS,
    SARCASM_PATTERNS,
    RHETORICAL_MARKERS
)
import re

class ImprovedStanceAnalyzer:
    
    def __init__(self, 
                 confidence_threshold: float = 0.45,
                 use_signals: bool = True):
        self.confidence_threshold = confidence_threshold
        self.use_signals = use_signals
        self.negative_lexicon = INDONESIAN_NEGATIVE_LEXICON
        self.positive_lexicon = INDONESIAN_POSITIVE_LEXICON
        
    def analyze(self, text: str, post_context: str = "") -> Tuple[str, float, str]:
        """
        Analyze stance of text with optional post context.
        
        Args:
            text: Comment/response text
            post_context: Parent post text for context
            
        Returns:
            (stance, confidence, reasoning)
            stance: 'Positive', 'Negative', 'Neutral'
        """
        
        # Step 1: Preprocess with signal preservation
        signals = preprocess_with_signals(text)
        clean_text = signals.clean_text
        
        # Step 2: Check for sarcasm/rhetorical patterns
        if self._detect_sarcasm(text):
            return 'Negative', 0.85, "Sarcasm detected"
        
        # Step 3: Score lexicon matches
        neg_score, neg_words = self._score_lexicon_words(clean_text, 'negative')
        pos_score, pos_words = self._score_lexicon_words(clean_text, 'positive')
        
        # Step 4: Apply intensity boosters/reducers
        neg_score = self._apply_intensity_modifiers(clean_text, neg_score)
        pos_score = self._apply_intensity_modifiers(clean_text, pos_score)
        
        # Step 5: Apply signal boosts
        if self.use_signals:
            neg_score, _ = apply_signal_boost(neg_score, signals, 'negative')
            pos_score, _ = apply_signal_boost(pos_score, signals, 'positive')
        
        # Step 6: Determine stance
        stance, confidence = self._determine_stance(neg_score, pos_score)
        
        # Step 7: Context override (optional)
        if post_context:
            stance, confidence = self._apply_context(stance, confidence, text, post_context)
        
        reasoning = f"Neg: {neg_score:.2f} ({neg_words}) | Pos: {pos_score:.2f} ({pos_words})"
        
        return stance, confidence, reasoning
    
    def _score_lexicon_words(self, text: str, polarity: str) -> Tuple[float, list]:
        """Score text based on lexicon words."""
        
        lexicon = self.negative_lexicon if polarity == 'negative' else self.positive_lexicon
        score = 0.0
        found_words = []
        
        for word, sentiment_value in lexicon.items():
            if word in text:
                score += sentiment_value
                found_words.append(word)
        
        # Normalize score
        if found_words:
            score = score / len(found_words)
        
        return abs(score), found_words
    
    def _apply_intensity_modifiers(self, text: str, base_score: float) -> float:
        """Apply intensity boosters and reducers."""
        
        score = base_score
        
        # Check for boosters before the main word
        for word, multiplier in INTENSITY_BOOSTERS.items():
            if word in text:
                score *= multiplier
        
        # Check for reducers
        for word, multiplier in INTENSITY_REDUCERS.items():
            if word in text:
                score *= multiplier
        
        return min(1.0, score)  # Clamp to [0, 1]
    
    def _detect_sarcasm(self, text: str) -> bool:
        """Detect sarcasm patterns."""
        
        for pattern in SARCASM_PATTERNS:
            if re.search(pattern, text.lower()):
                return True
        
        for pattern in RHETORICAL_MARKERS:
            if re.search(pattern, text.lower()):
                return True
        
        return False
    
    def _determine_stance(self, neg_score: float, pos_score: float) -> Tuple[str, float]:
        """Determine final stance from scores."""
        
        # Check if scores are above minimum threshold
        neg_confident = neg_score > self.confidence_threshold
        pos_confident = pos_score > self.confidence_threshold
        
        if neg_confident and neg_score > pos_score:
            return 'Negative', min(neg_score, 1.0)
        elif pos_confident and pos_score > neg_score:
            return 'Positive', min(pos_score, 1.0)
        else:
            return 'Neutral', max(max(neg_score, pos_score), 0.5)
    
    def _apply_context(self, stance: str, confidence: float, 
                       text: str, post_context: str) -> Tuple[str, float]:
        """Apply post context to adjust stance if needed."""
        
        # Simple context override: if post is positive and comment criticizes it
        post_is_positive = any(word in post_context.lower() 
                              for word in self.positive_lexicon)
        comment_has_criticism = any(word in text.lower() 
                                    for word in ['tapi', 'namun', 'hanya', 'cuma'])
        
        if post_is_positive and comment_has_criticism:
            return 'Negative', 0.80
        
        return stance, confidence


# Example usage:
if __name__ == "__main__":
    analyzer = ImprovedStanceAnalyzer()
    
    test_cases = [
        "@Menlu_RI Menteri paling gak becus.",
        "Program renovasi rumah bikin hati lega",
        "Ini keputusan yang bijak untuk Indonesia",
    ]
    
    for text in test_cases:
        stance, confidence, reasoning = analyzer.analyze(text)
        print(f"Text: {text}")
        print(f"  → Stance: {stance} ({confidence:.2f})")
        print(f"  → Reasoning: {reasoning}\n")
```

---

## 2. FASE 2: MODEL INTEGRATION (2-3 Hari)

### 2.1 Switch dari Transformer ke Lexicon+Gemini Hybrid

**File: `hybrid_stance_analysis.py`**

```python
"""
Hybrid approach: Use improved lexicon for fast classification,
and fall back to Gemini API for uncertain/complex cases.
"""

import os
from improved_stance_analyzer import ImprovedStanceAnalyzer

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class HybridStanceAnalyzer:
    """
    Hybrid stance analyzer:
    1. Fast lexicon-based for confident predictions
    2. Fallback to Gemini API for low-confidence/complex cases
    """
    
    def __init__(self, 
                 gemini_api_key: str = None,
                 confidence_threshold: float = 0.70):
        """
        Initialize hybrid analyzer.
        
        Args:
            gemini_api_key: Google Gemini API key (optional)
            confidence_threshold: Threshold above which to use lexicon result
                                 Below this → use Gemini for validation
        """
        
        self.lexicon_analyzer = ImprovedStanceAnalyzer(confidence_threshold=0.45)
        self.confidence_threshold = confidence_threshold
        self.use_gemini = gemini_api_key is not None and genai is not None
        
        if self.use_gemini:
            genai.configure(api_key=gemini_api_key)
            print("✓ Gemini API configured")
    
    def analyze(self, text: str, post_context: str = "") -> dict:
        """
        Analyze stance using hybrid approach.
        
        Returns:
            {
                'stance': 'Positive'|'Negative'|'Neutral',
                'confidence': float,
                'method': 'lexicon'|'gemini'|'ensemble',
                'reasoning': str
            }
        """
        
        # Step 1: Try fast lexicon analysis
        stance, lexicon_conf, lexicon_reason = self.lexicon_analyzer.analyze(
            text, post_context
        )
        
        # Step 2: If high confidence → return lexicon result
        if lexicon_conf >= self.confidence_threshold:
            return {
                'stance': stance,
                'confidence': lexicon_conf,
                'method': 'lexicon',
                'reasoning': lexicon_reason
            }
        
        # Step 3: If low confidence and Gemini available → validate with Gemini
        if self.use_gemini:
            gemini_result = self._validate_with_gemini(text, post_context, stance)
            
            # If Gemini confidence is higher → use it
            if gemini_result['confidence'] > lexicon_conf:
                gemini_result['method'] = 'gemini'
                return gemini_result
        
        # Step 4: Return ensemble result
        return {
            'stance': stance,
            'confidence': lexicon_conf,
            'method': 'ensemble',
            'reasoning': lexicon_reason
        }
    
    def _validate_with_gemini(self, text: str, post_context: str, 
                             initial_stance: str) -> dict:
        """Validate with Gemini API."""
        
        prompt = f"""Lakukan stance analysis pada teks berikut.

Post Context (jika ada): "{post_context}"

Text to analyze: "{text}"

Initial prediction: {initial_stance}

Klasifikasikan stance menjadi: Mendukung (Positive), Menolak (Negative), atau Netral (Neutral).

Berikan confidence 0-100 dan reasoning singkat.

FORMAT OUTPUT:
STANCE: [Positive|Negative|Neutral]
CONFIDENCE: [0-100]
REASONING: [1 sentence]
"""
        
        try:
            response = genai.GenerativeModel('gemini-1.5-flash').generate_content(prompt)
            result_text = response.text
            
            # Parse response
            stance = self._parse_stance(result_text)
            confidence = self._parse_confidence(result_text)
            
            return {
                'stance': stance,
                'confidence': confidence / 100,  # Convert to 0-1
                'reasoning': self._parse_reasoning(result_text)
            }
        
        except Exception as e:
            print(f"⚠️ Gemini API error: {e}")
            return {'stance': 'Neutral', 'confidence': 0.5, 'reasoning': str(e)}
    
    def _parse_stance(self, text: str) -> str:
        """Extract stance from Gemini response."""
        if 'positive' in text.lower() or 'mendukung' in text.lower():
            return 'Positive'
        elif 'negative' in text.lower() or 'menolak' in text.lower():
            return 'Negative'
        else:
            return 'Neutral'
    
    def _parse_confidence(self, text: str) -> int:
        """Extract confidence from response."""
        import re
        match = re.search(r'CONFIDENCE:\s*(\d+)', text)
        if match:
            return int(match.group(1))
        return 50
    
    def _parse_reasoning(self, text: str) -> str:
        """Extract reasoning from response."""
        import re
        match = re.search(r'REASONING:\s*(.+?)(?:\n|$)', text)
        if match:
            return match.group(1).strip()
        return "Unable to parse reasoning"


# Usage example:
if __name__ == "__main__":
    analyzer = HybridStanceAnalyzer(
        gemini_api_key=os.getenv('GEMINI_API_KEY'),
        confidence_threshold=0.70
    )
    
    text = "@Menlu_RI Menteri paling gak becus."
    result = analyzer.analyze(text)
    
    print(f"Text: {text}")
    print(f"Stance: {result['stance']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Method: {result['method']}")
    print(f"Reasoning: {result['reasoning']}")
```

---

## 3. VALIDATION & TESTING

### 3.1 Validation Script

**File: `validate_improvements.py`**

```python
"""
Validate stance analysis improvements against ground truth.
"""

import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from hybrid_stance_analysis import HybridStanceAnalyzer


def validate_against_ground_truth(ground_truth_csv: str, analyzer: HybridStanceAnalyzer) -> dict:
    """
    Validate improved analyzer against ground truth data.
    
    Args:
        ground_truth_csv: Path to ground truth CSV with columns:
                         'text', 'expected_stance'
        analyzer: Analyzer instance to test
        
    Returns:
        Metrics dictionary with accuracy, precision, recall, F1
    """
    
    df = pd.read_csv(ground_truth_csv)
    
    predictions = []
    confidences = []
    
    for _, row in df.iterrows():
        text = row['text']
        result = analyzer.analyze(text)
        predictions.append(result['stance'])
        confidences.append(result['confidence'])
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(df['expected_stance'], predictions),
        'precision': precision_score(df['expected_stance'], predictions, average='weighted', zero_division=0),
        'recall': recall_score(df['expected_stance'], predictions, average='weighted', zero_division=0),
        'f1': f1_score(df['expected_stance'], predictions, average='weighted', zero_division=0),
        'avg_confidence': sum(confidences) / len(confidences),
    }
    
    return metrics


if __name__ == "__main__":
    analyzer = HybridStanceAnalyzer()
    metrics = validate_against_ground_truth('ground_truth_examples.csv', analyzer)
    
    print("✓ Validation Results:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.3f}")
```

---

## 4. DEPLOYMENT CHECKLIST

- [ ] Implement `indonesian_stance_lexicon.py` with 100+ slang words
- [ ] Implement `enhanced_preprocessing.py` with signal preservation
- [ ] Implement `improved_stance_analyzer.py` and test locally
- [ ] Integrate `hybrid_stance_analysis.py` for Gemini fallback
- [ ] Create ground truth CSV with 50+ examples (if possible: 100+)
- [ ] Run validation against ground truth
- [ ] Update `stance_analysis.py` to use new analyzer
- [ ] Deploy and monitor metrics
- [ ] Collect user feedback on improvements

---

**End of Implementation Guide**
