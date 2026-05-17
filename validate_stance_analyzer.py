"""
Validation Script for Improved Stance Analyzer
==============================================

Tests the improved analyzer against ground truth examples.

Created: 2026-05-17
Last Updated: 2026-05-17
Version: 1.0

Usage:
    python validate_stance_analyzer.py
    
Or programmatically:
    from validate_stance_analyzer import validate_analyzer
    metrics = validate_analyzer(analyzer)
"""

import pandas as pd
from typing import Dict, List, Tuple
import json
import sys
from improved_stance_analyzer import ImprovedStanceAnalyzer


# Ground truth validation examples
GROUND_TRUTH_EXAMPLES = [
    # NEGATIVE EXAMPLES (Should classify as NEGATIVE)
    {
        "id": "neg_001",
        "text": "@Menlu_RI Menteri paling gak becus.",
        "expected": "Negative",
        "reason": "Direct insult using slang",
    },
    {
        "id": "neg_002",
        "text": "@Menlu_RI Mentri tolol",
        "expected": "Negative",
        "reason": "Direct insult - tolol (stupid)",
    },
    {
        "id": "neg_003",
        "text": "@P3gEl Emang mulut pejabat kita ini kayak kurang makan sekolahan. Buruk sekali public speakingnya & seringkali malah bikin blunder...",
        "expected": "Negative",
        "reason": "Criticism with idiom + multiple negative words",
    },
    {
        "id": "neg_004",
        "text": "@P3gEl Maaf ya kak, Presiden, wapres dan pejabat di negeri ini memang gak punya otak semua, mohon dimaklumi",
        "expected": "Negative",
        "reason": "Passive-aggressive sarcasm with strong insult",
    },
    {
        "id": "neg_005",
        "text": "@kompascom Melayani & mengayomi rakyat aja gak becus, pake ditambah tugasnya jadi petani jagung??",
        "expected": "Negative",
        "reason": "Rhetorical question with criticism",
    },
    {
        "id": "neg_006",
        "text": "@BILLRAY2019 GOBLOGnya presiden @prabowo gk ada obatnya di dunia international!!!...",
        "expected": "Negative",
        "reason": "Slang insult (goblog) with ALL CAPS + multiple !",
    },
    {
        "id": "neg_007",
        "text": "@susipudjiastuti @prabowo lha dia punya jg buanyaak bgt bu gmana MALING bs tangkap maling?? @prabowo",
        "expected": "Negative",
        "reason": "Corruption accusation metaphor with rhetorical question",
    },
    {
        "id": "neg_008",
        "text": "Semakin hari semakin terbuka kalau Presiden @prabowo tidak independen dan ada sosok yang atur beliau dalam menjalankan roda pemerintahan.",
        "expected": "Negative",
        "reason": "Political criticism - accusations of being controlled",
    },
    {
        "id": "neg_009",
        "text": "#intinyadeh lebih dr 100 org Indonesia kabur dr Chrey Thum Kamboja. Mereka ngaku ditipu agen penyalur kerja diperlakukan dgn kekerasan sama perusahaan salah satu pekerja wanita dicambuk.",
        "expected": "Negative",
        "reason": "Multiple abuse keywords (ditipu, kekerasan, dicambuk)",
    },
    {
        "id": "neg_010",
        "text": "Melayani rakyat gak becus, pake yang lain-lain",
        "expected": "Negative",
        "reason": "Direct institutional criticism",
    },
    
    # POSITIVE EXAMPLES (Should classify as POSITIVE)
    {
        "id": "pos_001",
        "text": "@KotaNusantara Program renovasi rumah dari Presiden Prabowo bikin hati lega masa depan makin terjamin",
        "expected": "Positive",
        "reason": "Positive idiom: bikin hati lega",
    },
    {
        "id": "pos_002",
        "text": "@KotaNusantara Langkah Presiden Prabowo ini keren banget bikin makin optimis soal masa depan kepemilikan rumah",
        "expected": "Positive",
        "reason": "Positive slang + optimism",
    },
    {
        "id": "pos_003",
        "text": "@kusuma4a Hanya bisa berkata terima kasih baktimu TNI ku",
        "expected": "Positive",
        "reason": "Gratitude + appreciation for service",
    },
    {
        "id": "pos_004",
        "text": "@kusuma4a Bangga kami atas kinerja TNI",
        "expected": "Positive",
        "reason": "Direct positive emotion: bangga (proud)",
    },
    {
        "id": "pos_005",
        "text": "Dukungan penuh untuk kebijakan internasional Indonesia yang forward-thinking seperti ini!",
        "expected": "Positive",
        "reason": "Explicit support with forward-thinking",
    },
    {
        "id": "pos_006",
        "text": "Setuju 100% dengan kebijakan ini! Ini keputusan yang bijak untuk Indonesia",
        "expected": "Positive",
        "reason": "Explicit agreement + positive assessment",
    },
    {
        "id": "pos_007",
        "text": "Langkah maju yang sangat bagus untuk negara kita",
        "expected": "Positive",
        "reason": "Positive assessment of policy",
    },
    {
        "id": "pos_008",
        "text": "Mantap jiwa! Ini yang kami tunggu-tunggu",
        "expected": "Positive",
        "reason": "Positive slang + anticipation",
    },
    
    # NEUTRAL EXAMPLES
    {
        "id": "neu_001",
        "text": "Presiden membuat keputusan ini setelah konsultasi menyeluruh. Implementasi dimulai bulan depan.",
        "expected": "Neutral",
        "reason": "Factual, informative statement",
    },
    {
        "id": "neu_002",
        "text": "Jumlah peserta mencapai 5000 orang di lokasi acara itu.",
        "expected": "Neutral",
        "reason": "Pure factual information",
    },
    {
        "id": "neu_003",
        "text": "Program ini berlaku mulai tanggal 1 Juni 2026",
        "expected": "Neutral",
        "reason": "Announcement without sentiment",
    },
    {
        "id": "neu_004",
        "text": "Hmm, sebagian setuju sebagian tidak. Ada pro dan kontra yang perlu dipertimbangkan.",
        "expected": "Neutral",
        "reason": "Balanced, ambiguous perspective",
    },
    {
        "id": "neu_005",
        "text": "Saya tidak yakin apakah ini keputusan yang tepat atau tidak. Perlu waktu untuk lihat hasilnya.",
        "expected": "Neutral",
        "reason": "Uncertain/wait-and-see approach",
    },
]


def validate_analyzer(analyzer: ImprovedStanceAnalyzer = None) -> Dict:
    """
    Validate analyzer against ground truth examples.
    
    Args:
        analyzer: ImprovedStanceAnalyzer instance (creates default if None)
        
    Returns:
        Metrics dictionary with detailed results
    """
    
    if analyzer is None:
        analyzer = ImprovedStanceAnalyzer(debug=False)
    
    results = {
        'total': 0,
        'correct': 0,
        'incorrect': 0,
        'by_class': {
            'Positive': {'total': 0, 'correct': 0},
            'Negative': {'total': 0, 'correct': 0},
            'Neutral': {'total': 0, 'correct': 0},
        },
        'errors': [],
        'predictions': [],
    }
    
    # Run predictions
    for example in GROUND_TRUTH_EXAMPLES:
        text = example['text']
        expected = example['expected']
        
        stance, confidence, reasoning = analyzer.analyze(text)
        
        results['total'] += 1
        results['by_class'][expected]['total'] += 1
        results['predictions'].append({
            'id': example['id'],
            'text': text[:80] + ('...' if len(text) > 80 else ''),
            'expected': expected,
            'predicted': stance,
            'confidence': confidence,
            'reasoning': reasoning,
        })
        
        if stance == expected:
            results['correct'] += 1
            results['by_class'][expected]['correct'] += 1
        else:
            results['incorrect'] += 1
            results['errors'].append({
                'id': example['id'],
                'text': text,
                'expected': expected,
                'predicted': stance,
                'confidence': confidence,
                'reason': example['reason'],
            })
    
    # Calculate metrics
    results['accuracy'] = results['correct'] / results['total']
    
    for stance_class in ['Positive', 'Negative', 'Neutral']:
        total = results['by_class'][stance_class]['total']
        correct = results['by_class'][stance_class]['correct']
        if total > 0:
            results['by_class'][stance_class]['accuracy'] = correct / total
        else:
            results['by_class'][stance_class]['accuracy'] = 0.0
    
    return results


def print_validation_report(results: Dict) -> None:
    """Print formatted validation report."""
    
    print("\n" + "=" * 80)
    print("IMPROVED STANCE ANALYZER - VALIDATION REPORT")
    print("=" * 80)
    
    print(f"\n📊 OVERALL RESULTS")
    print("-" * 80)
    print(f"Total Examples:     {results['total']}")
    print(f"Correct:           {results['correct']} ({results['accuracy']*100:.1f}%)")
    print(f"Incorrect:         {results['incorrect']}")
    
    print(f"\n📈 ACCURACY BY CLASS")
    print("-" * 80)
    for stance_class in ['Positive', 'Negative', 'Neutral']:
        stats = results['by_class'][stance_class]
        total = stats['total']
        acc = stats['accuracy']
        print(f"{stance_class:10s}: {stats['correct']:2d}/{total:2d} ({acc*100:5.1f}%)")
    
    if results['errors']:
        print(f"\n❌ MISCLASSIFIED EXAMPLES ({len(results['errors'])})")
        print("-" * 80)
        for i, error in enumerate(results['errors'][:10], 1):  # Show first 10
            print(f"\n{i}. ID: {error['id']}")
            print(f"   Text: {error['text'][:70]}...")
            print(f"   Expected: {error['expected']} | Got: {error['predicted']} ({error['confidence']:.2f})")
            print(f"   Reason: {error['reason']}")
        
        if len(results['errors']) > 10:
            print(f"\n   ... and {len(results['errors']) - 10} more errors")
    
    print("\n" + "=" * 80)


def export_results_to_csv(results: Dict, output_file: str = "stance_validation_results.csv") -> None:
    """Export predictions to CSV for detailed analysis."""
    
    df = pd.DataFrame(results['predictions'])
    df.to_csv(output_file, index=False)
    print(f"\n✓ Results exported to {output_file}")


def export_results_to_json(results: Dict, output_file: str = "stance_validation_results.json") -> None:
    """Export full results to JSON."""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✓ Results exported to {output_file}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n🔄 Starting validation of Improved Stance Analyzer...")
    
    # Create analyzer
    analyzer = ImprovedStanceAnalyzer(
        confidence_threshold=0.45,
        use_signals=True,
        use_sarcasm_detection=True,
        debug=False,
    )
    
    # Run validation
    results = validate_analyzer(analyzer)
    
    # Print report
    print_validation_report(results)
    
    # Export results
    export_results_to_csv(results)
    export_results_to_json(results)
    
    # Return status
    if results['accuracy'] >= 0.80:
        print("\n✓ Validation PASSED (accuracy >= 80%)")
        sys.exit(0)
    else:
        print(f"\n✗ Validation FAILED (accuracy {results['accuracy']*100:.1f}% < 80%)")
        sys.exit(1)
