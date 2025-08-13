#!/usr/bin/env python3
"""
Revenue Bench - Main evaluation runner
Run evaluations on AI models for sales tasks
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add benchmark to path
sys.path.append(str(Path(__file__).parent))

from benchmark.tasks.homebase import HomebaseTask
from benchmark.judges.multi_judge_scorer import MultiJudgeScorer


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent / 'config.yaml'
    if config_path.exists():
        import yaml
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


def main():
    parser = argparse.ArgumentParser(
        description='Revenue Bench - Evaluate AI models on sales tasks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_evaluation.py --model openrouter/openai/gpt-5
  python run_evaluation.py --model openrouter/anthropic/claude-opus-4.1 --task homebase
  python run_evaluation.py --list-models
        """
    )
    
    parser.add_argument('--model', help='Model to evaluate (e.g., openrouter/openai/gpt-5)')
    parser.add_argument('--task', default='homebase', help='Task to run (default: homebase)')
    parser.add_argument('--output', default='results/', help='Output directory')
    parser.add_argument('--list-models', action='store_true', help='List available models')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    
    # List models if requested
    if args.list_models:
        print("\n📊 Available Models:")
        print("\nRecommended (Top Performers):")
        for model in config.get('models', {}).get('recommended', []):
            print(f"  • {model}")
        print("\nAll Models:")
        for model in config.get('models', {}).get('all', []):
            print(f"  • {model}")
        return
    
    # Check if model is provided
    if not args.model:
        parser.print_help()
        return
    
    # Check API keys
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ Error: OPENROUTER_API_KEY not set in environment")
        print("   Get your key at: https://openrouter.ai/keys")
        print("   Then add to .env file or export OPENROUTER_API_KEY=your_key")
        return
    
    if not os.getenv('TAVILY_API_KEY'):
        print("❌ Error: TAVILY_API_KEY not set in environment")
        print("   Get your key at: https://tavily.com")
        print("   Then add to .env file or export TAVILY_API_KEY=your_key")
        return
    
    print(f"\n🚀 Revenue Bench Evaluation")
    print(f"   Model: {args.model}")
    print(f"   Task: {args.task}")
    print("-" * 50)
    
    try:
        # Initialize task
        if args.task == 'homebase':
            task = HomebaseTask()
        else:
            print(f"❌ Unknown task: {args.task}")
            print("   Available tasks: homebase")
            return
        
        # Run evaluation
        print(f"\n📝 Running {args.task} task...")
        result = task.evaluate(args.model, verbose=args.verbose)
        
        if not result:
            print("❌ Evaluation failed - no result returned")
            return
        
        # Score with judges
        print("\n⚖️ Scoring with multi-judge panel...")
        scorer = MultiJudgeScorer()
        scores = scorer.score(result, verbose=args.verbose)
        
        # Prepare output
        output_data = {
            'model': args.model,
            'task': args.task,
            'timestamp': datetime.now().isoformat(),
            'result': result,
            'scores': scores,
            'metadata': {
                'version': '0.1.0',
                'judges': config.get('judges', [])
            }
        }
        
        # Save results
        output_dir = Path(args.output)
        output_dir.mkdir(exist_ok=True, parents=True)
        
        model_name = args.model.split('/')[-1]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = output_dir / f"{model_name}_{timestamp}.json"
        
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        # Display results
        print("\n" + "=" * 50)
        print("📊 RESULTS")
        print("=" * 50)
        print(f"Model: {args.model}")
        print(f"Final Score: {scores.get('final_score', 0):.1%}")
        print(f"Cost: ${scores.get('cost', 0):.4f}")
        
        if 'breakdown' in scores:
            print("\nScore Breakdown:")
            for criterion, score in scores['breakdown'].items():
                print(f"  • {criterion}: {score:.1f}/10")
        
        print(f"\n💾 Results saved to: {output_path}")
        
        # Update leaderboard
        update_leaderboard(output_data)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Evaluation interrupted by user")
        return
    except Exception as e:
        print(f"\n❌ Error during evaluation: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return


def update_leaderboard(result_data):
    """Update the leaderboard with new results"""
    leaderboard_path = Path('results/leaderboard.json')
    
    # Load existing leaderboard
    if leaderboard_path.exists():
        with open(leaderboard_path, 'r') as f:
            leaderboard = json.load(f)
    else:
        leaderboard = {'models': {}, 'updated': None}
    
    # Add or update model
    model_name = result_data['model']
    leaderboard['models'][model_name] = {
        'score': result_data['scores'].get('final_score', 0),
        'cost': result_data['scores'].get('cost', 0),
        'timestamp': result_data['timestamp']
    }
    leaderboard['updated'] = datetime.now().isoformat()
    
    # Save updated leaderboard
    leaderboard_path.parent.mkdir(exist_ok=True, parents=True)
    with open(leaderboard_path, 'w') as f:
        json.dump(leaderboard, f, indent=2)
    
    print(f"✅ Leaderboard updated: {leaderboard_path}")


if __name__ == '__main__':
    main()