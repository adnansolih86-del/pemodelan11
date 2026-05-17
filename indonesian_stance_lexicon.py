"""
Indonesian Stance Analysis Lexicon
====================================

Comprehensive lexicon for detecting sentiment in Indonesian political discourse.
Focus: Slang, idioms, and colloquial expressions.

Created: 2026-05-17
Last Updated: 2026-05-17
Version: 1.0

Usage:
    from indonesian_stance_lexicon import (
        INDONESIAN_NEGATIVE_LEXICON,
        INDONESIAN_POSITIVE_LEXICON,
        SARCASM_PATTERNS,
        RHETORICAL_MARKERS
    )
"""

import re

# ============================================================================
# NEGATIVE SENTIMENT LEXICON
# ============================================================================

INDONESIAN_NEGATIVE_LEXICON = {
    # SLANG - Strong Negatives (Confidence: VERY HIGH)
    'tolol': -1.0,              # stupid/idiot (very strong)
    'goblog': -1.0,             # idiot - makian kuat
    'goblok': -1.0,             # idiot - alternative spelling
    'gak becus': -0.95,         # not competent/useless
    'gak punya otak': -0.95,    # brainless/stupid
    'gk punya otak': -0.95,     # alt spelling
    'tidak punya otak': -0.95,  # formal version
    'maling': -0.95,            # thief (corruption metaphor)
    'koruptor': -0.95,          # corrupt person
    'penipu': -0.90,            # fraud/deceiver
    'gak ada obatnya': -0.95,   # hopeless/no cure
    'gk ada obatnya': -0.95,    # alt spelling
    'blunder': -0.85,           # mistake/blunder
    
    # FORMAL NEGATIVES
    'buruk': -0.85,
    'buruk sekali': -0.90,
    'sangat buruk': -0.92,
    'jelek': -0.80,
    'sangat jelek': -0.88,
    'gagal': -0.85,
    'kegagalan': -0.85,
    'merugikan': -0.85,
    'tidak independen': -0.80,
    'negatif': -0.75,
    'mengecewakan': -0.80,
    'mengecewa': -0.80,
    'kekecewaan': -0.80,
    
    # ABUSE & VIOLENCE KEYWORDS (CRITICAL)
    'kekerasan': -0.95,         # violence/abuse
    'dicambuk': -0.98,          # whipped (physical abuse - strongest)
    'dianiaya': -0.95,          # tortured/mistreated
    'disiksa': -0.95,           # tortured
    'dipukul': -0.92,           # beaten
    'ditipu': -0.90,            # deceived
    'diperdaya': -0.90,         # deceived
    'penipuan': -0.90,          # deception
    'love scamming': -0.95,     # romance scam
    
    # IDIOMS & COMPOUND PHRASES
    'kurang makan sekolahan': -0.85,      # not well-educated (idiom)
    'kurang makan sekolah': -0.85,        # alt spelling
    'gak nyambung': -0.75,                # incoherent
    'berbicara sembarangan': -0.80,      # speak carelessly
    'bikin malu': -0.85,                  # embarrassing
    'memalukan': -0.80,                   # embarrassing
    'tidak cocok': -0.70,
    'tidak pantas': -0.75,
    'tidak mampu': -0.75,
    'tidak bisa': -0.70,
    'tidak sanggup': -0.75,
    'tidak layak': -0.80,
    'tidak wajar': -0.75,
    
    # FAILURE & INCOMPETENCE
    'kegagalan': -0.85,
    'tidak efektif': -0.80,
    'tidak efisien': -0.80,
    'tidak produktif': -0.80,
    'pemborosan': -0.85,
    'pemborosan anggaran': -0.90,
    'korupsi': -0.95,
    'suap': -0.95,
    'mark up': -0.90,
    'kolusi': -0.95,
}

# ============================================================================
# POSITIVE SENTIMENT LEXICON
# ============================================================================

INDONESIAN_POSITIVE_LEXICON = {
    # SLANG - Strong Positives (Confidence: VERY HIGH)
    'keren': 0.85,              # cool/awesome
    'keren banget': 0.95,       # really cool
    'keren sekali': 0.95,       # really cool
    'gokil': 0.90,              # crazy good (slang)
    'gokil banget': 0.95,       # really crazy good
    'mantap': 0.90,             # solid/good
    'mantap jiwa': 0.95,        # solid as hell
    'asik': 0.85,               # fun/good
    'asik banget': 0.92,        # really fun
    'ciamik': 0.85,             # nice/good (slang)
    'oke': 0.75,                # okay/good
    'super': 0.85,              # great
    'super bagus': 0.92,        # really great
    'hebat': 0.85,              # great/awesome
    'hebat sekali': 0.92,       # very awesome
    'bagus': 0.80,              # good
    'bagus sekali': 0.90,       # very good
    'sangat bagus': 0.90,       # very good
    
    # EXCELLENCE & ACHIEVEMENT
    'luar biasa': 0.90,         # extraordinary
    'luar biasa bagus': 0.95,   # extraordinarily good
    'sempurna': 0.85,           # perfect
    'kesempurnaan': 0.85,       # perfection
    'istimewa': 0.85,           # special/excellent
    'unggul': 0.80,             # superior
    'terbaik': 0.90,            # best
    'terbagus': 0.90,           # best (informal)
    'paling bagus': 0.90,       # the best
    'canggih': 0.80,            # advanced/sophisticated
    'modern': 0.75,             # modern/up-to-date
    
    # IDIOMS & POSITIVE PHRASES
    'bikin hati lega': 0.90,    # brings relief/peace of mind
    'hati lega': 0.85,          # relieved/at peace
    'hati senang': 0.90,        # happy/glad
    'senang hati': 0.85,        # pleased
    'masa depan cerah': 0.85,   # bright future
    'cerah': 0.75,              # bright/positive
    'langkah maju': 0.85,       # step forward
    'maju': 0.75,               # progress/advance
    'makin terjamin': 0.75,     # more secure/assured
    'terjamin': 0.70,           # secured/assured
    'aman': 0.70,               # safe/secure
    'nyaman': 0.70,             # comfortable
    
    # EMOTION & APPRECIATION
    'bangga': 0.90,             # proud
    'bangga atas': 0.95,        # proud of
    'bangga dengan': 0.95,      # proud of
    'terima kasih': 0.75,       # thank you
    'terima kasih banyak': 0.80, # thank you very much
    'terima kasih bakti': 0.85, # grateful for service
    'apresiasi': 0.80,          # appreciation
    'hormat': 0.75,             # respect
    'hormat kepada': 0.80,      # respect for
    'kagum': 0.85,              # admire
    'kagum pada': 0.90,         # admire towards
    'keajaiban': 0.75,          # miracle/wonder
    
    # OPTIMISM & CONFIDENCE
    'optimis': 0.80,            # optimistic
    'sangat optimis': 0.85,     # very optimistic
    'harapan': 0.75,            # hope
    'percaya': 0.70,            # believe/trust
    'percaya diri': 0.75,       # confident
    'yakin': 0.75,              # confident
    'yakin dapat': 0.80,        # confident can achieve
    
    # SUCCESS & ACHIEVEMENT
    'sukses': 0.85,             # success
    'berhasil': 0.80,           # successful
    'berhasil besar': 0.90,     # major success
    'tercapai': 0.75,           # achieved
    'terwujud': 0.75,           # materialized/realized
    'nyata': 0.70,              # real/concrete (in positive context)
    
    # SUPPORT & ALIGNMENT
    'dukungan penuh': 0.90,     # full support
    'setuju': 0.80,             # agree
    'setuju 100': 0.92,         # 100% agree
    'sangat setuju': 0.85,      # strongly agree
    'mendukung': 0.85,          # support
    'mendukung penuh': 0.92,    # fully support
    'amin': 0.70,               # amen/agree
}

# ============================================================================
# INTENSITY MODIFIERS
# ============================================================================

INTENSITY_BOOSTERS = {
    'sangat': 1.5,              # very
    'banget': 1.5,              # very (slang)
    'sekali': 1.5,              # very
    'amat': 1.4,                # very
    'gila': 1.4,                # crazy (intensifier)
    'parah': 1.3,               # severe
    'luar biasa': 1.4,          # extraordinary
    'super': 1.3,               # super
}

INTENSITY_REDUCERS = {
    'agak': 0.7,                # somewhat
    'sedikit': 0.7,             # a bit
    'kurang': 0.7,              # less/lacking
    'cukup': 0.8,               # quite
    'mungkin': 0.6,             # maybe
    'sepertinya': 0.7,          # seems like
}

# ============================================================================
# NEGATION WORDS
# ============================================================================

NEGATION_WORDS = {
    'tidak',
    'gak',
    'gk',
    'tidak pernah',
    'bukan',
    'belum',
    'jangan',
    'tidak akan',
    'tidak bisa',
}

# ============================================================================
# SARCASM & PASSIVE-AGGRESSIVE PATTERNS
# ============================================================================

SARCASM_PATTERNS = [
    r'maaf ya.*(?:tapi|namun|justru|malah)',      # maaf ya + contradiction = sarcasm
    r'maaf kak.*(?:tapi|namun|justru)',
    r'mohon dimaklumi',                             # fake politeness = passive-aggressive
    r'mohon maaf',                                  # followed by criticism = sarcasm
    r'tidak ada masalah',                           # fake acceptance
    r'tidak apa-apa',                               # fake acceptance
    r'ya sudahlah',                                 # resigned/sarcastic acceptance
    r'terserah',                                    # dismissive/sarcastic
    r'ok deh',                                      # dismissive sarcasm
    r'oke deh',                                     # dismissive sarcasm
    r'sure\b',                                      # English sarcasm
    r'yeah right',                                  # English sarcasm
    r'halah',                                       # dismissive/mocking
    r'pffft',                                       # dismissive sound
]

# ============================================================================
# RHETORICAL QUESTION PATTERNS
# ============================================================================

RHETORICAL_MARKERS = {
    r'\?\?',                                        # Multiple question marks = frustration
    r'gmana.*bs\s',                                 # gmana X bs Y (how can X do Y)
    r'bagaimana.*bisa',                             # formal version
    r'kenapa.*gak',                                 # kenapa gak (why not - rhetorical)
    r'kenapa.*tidak',                               # formal version
    r'siapa yang.*',                                # siapa yang bisa... (who could...)
}

# ============================================================================
# CORRUPTION & POLITICAL CRITICISM KEYWORDS
# ============================================================================

POLITICAL_CRITICISM_KEYWORDS = {
    'maling',                   # thief (corruption metaphor)
    'korupsi',                  # corruption
    'koruptor',                 # corrupt person
    'suap',                     # bribe
    'kolusi',                   # collusion
    'nepotisme',                # nepotism
    'mark up',                  # markup (overpricing)
    'manipulasi',               # manipulation
    'mengontrol',               # controlling
    'ada sosok yang atur',      # someone controlling (conspiracy)
    'di balik layar',           # behind the scenes (conspiracy)
    'permainan',                # game/manipulation
    'rekayasa',                 # rigged/manipulated
    'tidak adil',               # unfair/unjust
    'tidak jujur',              # dishonest
    'curang',                   # cheating
    'bohong',                   # lie
    'berbohong',                # lying
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_sentiment_score(word: str, default: float = 0.0) -> float:
    """
    Get sentiment score for a word.
    
    Args:
        word: Word to look up
        default: Default score if not found
        
    Returns:
        Sentiment score (-1.0 to 1.0)
    """
    word_lower = word.lower()
    
    if word_lower in INDONESIAN_NEGATIVE_LEXICON:
        return INDONESIAN_NEGATIVE_LEXICON[word_lower]
    elif word_lower in INDONESIAN_POSITIVE_LEXICON:
        return INDONESIAN_POSITIVE_LEXICON[word_lower]
    else:
        return default


def find_sentiment_words(text: str, polarity: str = 'both') -> dict:
    """
    Find all sentiment words in text.
    
    Args:
        text: Input text
        polarity: 'positive', 'negative', or 'both'
        
    Returns:
        Dictionary with found words and their scores
    """
    text_lower = text.lower()
    found = {'positive': [], 'negative': [], 'neutral': []}
    
    if polarity in ['positive', 'both']:
        for word, score in INDONESIAN_POSITIVE_LEXICON.items():
            if word in text_lower:
                found['positive'].append((word, score))
    
    if polarity in ['negative', 'both']:
        for word, score in INDONESIAN_NEGATIVE_LEXICON.items():
            if word in text_lower:
                found['negative'].append((word, score))
    
    return found


def detect_sarcasm_pattern(text: str) -> bool:
    """
    Detect if text contains sarcasm patterns.
    
    Args:
        text: Input text
        
    Returns:
        True if sarcasm pattern detected
    """
    for pattern in SARCASM_PATTERNS:
        if re.search(pattern, text.lower()):
            return True
    return False


def detect_rhetorical_question(text: str) -> bool:
    """
    Detect if text contains rhetorical question markers.
    
    Args:
        text: Input text
        
    Returns:
        True if rhetorical question detected
    """
    for pattern in RHETORICAL_MARKERS:
        if re.search(pattern, text.lower()):
            return True
    return False


# ============================================================================
# MODULE METADATA
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("INDONESIAN STANCE ANALYSIS LEXICON")
    print("=" * 70)
    print(f"\n✓ Negative words loaded: {len(INDONESIAN_NEGATIVE_LEXICON)}")
    print(f"✓ Positive words loaded: {len(INDONESIAN_POSITIVE_LEXICON)}")
    print(f"✓ Sarcasm patterns: {len(SARCASM_PATTERNS)}")
    print(f"✓ Rhetorical patterns: {len(RHETORICAL_MARKERS)}")
    print(f"✓ Political keywords: {len(POLITICAL_CRITICISM_KEYWORDS)}")
    
    # Test examples
    print("\n" + "=" * 70)
    print("TEST EXAMPLES")
    print("=" * 70)
    
    test_texts = [
        "Menteri paling gak becus",
        "Program bikin hati lega",
        "Gmana maling bisa tangkap maling??",
        "Maaf ya, tapi ini gak becus",
    ]
    
    for text in test_texts:
        print(f"\nText: {text}")
        words = find_sentiment_words(text)
        print(f"  Positive: {words['positive']}")
        print(f"  Negative: {words['negative']}")
        print(f"  Sarcasm: {detect_sarcasm_pattern(text)}")
        print(f"  Rhetorical: {detect_rhetorical_question(text)}")
