#!/usr/bin/env python3
"""
Example: Compare multiple models
"""

import json
from pathlib import Path


def main():
    # Load leaderboard
    leaderboard_path = Path(__file__).parent.parent / "results" / "leaderboard.json"
    
    with open(leaderboard_path, 'r') as f:
        data = json.load(f)
    
    print("🏆 Revenue Bench Leaderboard")
    print("=" * 70)
    print(f"{'Rank':<6} {'Model':<30} {'Score':<8} {'Cost':<10} {'Perf/$':<10}")
    print("-" * 70)
    
    for entry in data['leaderboard'][:10]:  # Top 10
        rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(entry['rank'], "")
        print(f"{rank_emoji}{entry['rank']:<5} {entry['model']:<30} "
              f"{entry['score']:.1%}   ${entry['cost_per_eval']:<8.2f} "
              f"{entry['performance_per_dollar']:<10.2f}")
    
    print("\n📊 Summary Statistics")
    print("-" * 40)
    summary = data['summary']
    print(f"Best Overall: {summary['best_overall']}")
    print(f"Best Value: {summary['best_value']} ")
    print(f"Average Score: {summary['average_score']:.1%}")
    print(f"Median Score: {summary['median_score']:.1%}")
    
    # Performance tiers
    print("\n🎯 Performance Tiers")
    print("-" * 40)
    
    tier_1 = [e for e in data['leaderboard'] if e['score'] >= 0.80]
    tier_2 = [e for e in data['leaderboard'] if 0.70 <= e['score'] < 0.80]
    tier_3 = [e for e in data['leaderboard'] if e['score'] < 0.70]
    
    print(f"Tier 1 (80%+): {len(tier_1)} models")
    for e in tier_1[:3]:
        print(f"  • {e['model']}: {e['score']:.1%}")
    
    print(f"\nTier 2 (70-80%): {len(tier_2)} models")
    for e in tier_2[:3]:
        print(f"  • {e['model']}: {e['score']:.1%}")
    
    print(f"\nTier 3 (<70%): {len(tier_3)} models")
    
    # Cost analysis
    print("\n💰 Cost Analysis")
    print("-" * 40)
    
    costs = [e['cost_per_eval'] for e in data['leaderboard']]
    print(f"Most Expensive: ${max(costs):.2f}")
    print(f"Least Expensive: ${min(costs):.4f}")
    print(f"Average Cost: ${sum(costs)/len(costs):.2f}")
    
    # Best value models (high score, low cost)
    print("\n⭐ Best Value Models (Score/Cost Ratio)")
    print("-" * 40)
    
    sorted_by_value = sorted(data['leaderboard'], 
                           key=lambda x: x['performance_per_dollar'], 
                           reverse=True)
    
    for e in sorted_by_value[:5]:
        print(f"  • {e['model']}: {e['performance_per_dollar']:.1f} "
              f"(Score: {e['score']:.1%}, Cost: ${e['cost_per_eval']:.3f})")


if __name__ == "__main__":
    main()