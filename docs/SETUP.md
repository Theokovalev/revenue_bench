# Setup Guide

This guide will help you get Revenue Bench running on your system.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (for cloning the repository)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/revenue-bench/revenue-bench.git
cd revenue-bench
```

### 2. Create Virtual Environment

We recommend using a virtual environment to avoid dependency conflicts:

```bash
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

You'll need API keys from two services:

#### OpenRouter API Key
1. Sign up at [OpenRouter](https://openrouter.ai)
2. Go to [API Keys](https://openrouter.ai/keys)
3. Create a new API key
4. Add credits to your account (minimum $10 recommended)

#### Tavily API Key
1. Sign up at [Tavily](https://tavily.com)
2. Get your API key from the dashboard
3. Free tier includes 1000 searches/month

#### Set Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
OPENROUTER_API_KEY=your_openrouter_key_here
TAVILY_API_KEY=your_tavily_key_here
```

## Running Your First Evaluation

### Quick Test

Test with a single model:

```bash
python run_evaluation.py --model openrouter/openai/gpt-5-mini
```

This will:
1. Run the Homebase task with 3 prospects
2. Use Tavily for web search and verification
3. Score responses with 4 AI judges
4. Save results to `results/` directory

### View Available Models

```bash
python run_evaluation.py --list-models
```

### Verbose Mode

For detailed output during evaluation:

```bash
python run_evaluation.py --model openrouter/openai/gpt-5-mini --verbose
```

## Using with Inspect AI

If you have Inspect AI installed, you can also run evaluations directly:

```bash
inspect eval benchmark/tasks/homebase.py --model openrouter/openai/gpt-5-mini
```

## Cost Estimates

Typical costs per evaluation:
- GPT-5-mini: ~$0.01
- GPT-5: ~$0.08
- Claude Opus 4.1: ~$2.09
- Gemini 2.5 Pro: ~$0.17

Full benchmark (33 models): ~$7.50

## Troubleshooting

### Common Issues

1. **Import Error: inspect_ai not found**
   ```bash
   pip install inspect-ai
   ```

2. **API Key Error**
   - Ensure your `.env` file exists and contains valid keys
   - Check that you have credits in your OpenRouter account

3. **Rate Limiting**
   - Tavily free tier: 1000 searches/month
   - OpenRouter: depends on your account tier
   - Consider upgrading if you hit limits

4. **Timeout Errors**
   - Some models take longer to respond
   - You can increase timeout in `.env`:
   ```bash
   TIMEOUT=180  # 3 minutes
   ```

### Getting Help

- Check the [FAQ](FAQ.md)
- Open an issue on [GitHub](https://github.com/revenue-bench/revenue-bench/issues)
- Join our [Discord community](https://discord.gg/revenue-bench)

## Next Steps

- Read the [Methodology](METHODOLOGY.md) to understand how scoring works
- Check [Adding Models](ADDING_MODELS.md) to test your own models
- Review [Results Format](RESULTS_FORMAT.md) to understand output structure