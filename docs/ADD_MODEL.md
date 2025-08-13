# Adding Your Model to Revenue Bench

## Quick Start

To test a new model on Revenue Bench:

```bash
python run_evaluation.py --model openrouter/<provider>/<model-name>
```

## Supported Providers

Revenue Bench uses OpenRouter for unified access to models. Supported providers include:
- OpenAI (gpt-5, gpt-4.1, etc.)
- Anthropic (claude-opus-4.1, claude-sonnet-4)
- Google (gemini-2.5-flash, gemini-2.5-pro)
- Meta (llama-3.1-70b, llama-4-maverick)
- And much more providers

## Model Requirements

Your model must:
1. Support function calling (tool use)
2. Handle at least 8K context window
3. Generate structured JSON output
4. Be available via OpenRouter API

## Configuration

### 1. Get OpenRouter API Key

Sign up at [OpenRouter](https://openrouter.ai) and get your API key.

### 2. Set Environment Variables

```bash
export OPENROUTER_API_KEY="your-key-here"
export TAVILY_API_KEY="your-tavily-key"
```

### 3. Run Evaluation

```bash
python run_evaluation.py --model openrouter/your-provider/your-model
```

## Custom Model Parameters

You can customize model behavior:

```python
# In config.yaml
models:
  your-model:
    temperature: 0.7
    max_tokens: 4096
    top_p: 0.95
```

## Batch Testing

Test multiple models at once:

```yaml
# batch_config.yaml
models:
  - openrouter/openai/gpt-5
  - openrouter/anthropic/claude-opus-4.1
  - openrouter/google/gemini-2.5-flash
```

```bash
python run_evaluation.py --batch batch_config.yaml
```

## Understanding Results

After evaluation, you'll get:
- **Score**: 0-100% accuracy on the task
- **Cost**: Total API cost for evaluation
- **Performance/$**: Score per dollar spent
- **Detailed breakdown**: Per-prospect and per-judge scores

## Submitting Results

To add your model to the official leaderboard:

1. Run the full evaluation
2. Save the output JSON
3. Create a PR with:
   - Your evaluation results
   - Model configuration used
   - Any special setup required

## Troubleshooting

### Model Not Found
```
Error: Model 'your-model' not found on OpenRouter
```
Check the exact model name on OpenRouter's model list.

### Insufficient Context
```
Error: Context window exceeded
```
Your model needs at least 8K context. Try a larger model variant.

### Tool Use Not Supported
```
Error: Model does not support function calling
```
Not all models support tool use. Check OpenRouter documentation.

## Model-Specific Tips

### OpenAI Models
- Use `gpt-5` for best performance
- `gpt-5-mini` for cost efficiency

### Anthropic Models
- `claude-opus-4.1` excels at research tasks
- `claude-sonnet-4` balances cost and quality

### Google Models
- `gemini-2.5-flash` for speed
- `gemini-2.5-pro` for complex reasoning

## Need Help?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Open an [issue on GitHub](https://github.com/revenuebench/revenue-bench/issues)
- Contact us at team@revenuebench.ai