#!/usr/bin/env python3
"""
Example: Run evaluation on a single model
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from benchmark.tasks.homebase import HomebaseTask
from benchmark.judges.multi_judge_scorer import MultiJudgeScorer


def main():
    # Model to evaluate
    model = "openrouter/openai/gpt-5-mini"
    
    print(f"🚀 Running Revenue Bench on {model}")
    print("-" * 50)
    
    # Initialize task
    task = HomebaseTask()
    
    # Run evaluation
    print("📝 Running Homebase task...")
    result = task.evaluate(model, verbose=True)
    
    if not result:
        print("❌ Evaluation failed")
        return
    
    # Score with judges
    print("\n⚖️ Scoring with multi-judge panel...")
    scorer = MultiJudgeScorer()
    scores = scorer.score(result, verbose=True)
    
    # Display results
    print("\n" + "=" * 50)
    print("📊 RESULTS")
    print("=" * 50)
    print(f"Model: {model}")
    print(f"Final Score: {scores.get('final_score', 0):.1%}")
    print(f"Cost: ${scores.get('cost', 0):.4f}")
    
    if 'breakdown' in scores:
        print("\nScore Breakdown:")
        for criterion, score in scores['breakdown'].items():
            print(f"  • {criterion}: {score:.1f}/10")
    
    print("\n✅ Evaluation complete!")


if __name__ == "__main__":
    main()