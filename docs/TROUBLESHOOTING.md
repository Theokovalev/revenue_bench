# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Python Version Error
```
Error: Python 3.8+ required
```
**Solution**: Upgrade Python to 3.8 or later:
```bash
python --version  # Check current version
# Install Python 3.8+ from python.org or use pyenv
```

#### Missing Dependencies
```
ModuleNotFoundError: No module named 'inspect_ai'
```
**Solution**: Install all requirements:
```bash
pip install -r requirements.txt
```

### API Key Issues

#### OpenRouter API Key Not Found
```
Error: OPENROUTER_API_KEY environment variable not set
```
**Solution**: Set your API key:
```bash
export OPENROUTER_API_KEY="sk-or-..."
# Or add to .env file
```

#### Tavily API Key Missing
```
Error: TAVILY_API_KEY not configured
```
**Solution**: Get a free key from [Tavily](https://tavily.com):
```bash
export TAVILY_API_KEY="tvly-..."
```

### Model Errors

#### Model Not Available
```
Error: Model 'xxx' not found on OpenRouter
```
**Solution**: Check available models:
- Visit [OpenRouter Models](https://openrouter.ai/models)
- Use exact model path: `openrouter/provider/model-name`

#### Rate Limiting
```
Error: Rate limit exceeded
```
**Solution**: 
- Wait 60 seconds and retry
- Upgrade your OpenRouter plan
- Use `--delay` flag: `python run_evaluation.py --model xxx --delay 5`

#### Context Length Exceeded
```
Error: Maximum context length exceeded
```
**Solution**:
- Use a model with larger context window
- Reduce prompt size in configuration
- Split evaluation into smaller batches

### Evaluation Issues

#### No Output Generated
```
Warning: Model produced no valid output
```
**Possible causes**:
1. Model doesn't support JSON generation
2. Tool calling not supported
3. Prompt incompatibility

**Solution**: Try a different model or check model capabilities

#### Low Scores
Common reasons for low scores:
1. **No web search performed**: Model didn't use Tavily tools
2. **Generic personalization**: Not specific to prospect
3. **Unverified claims**: No evidence URLs provided
4. **Exceeds word limit**: First lines too long

#### Judge Disagreement
High variance in judge scores indicates:
- Edge case in evaluation
- Ambiguous output quality
- Model output format issues

### Performance Issues

#### Slow Evaluation
**Solutions**:
- Use faster models (gemini-2.5-flash)
- Reduce number of retries
- Check network connection

#### High Costs
**Cost reduction strategies**:
- Use batch processing (67% savings)
- Test with cheaper models first
- Use `--dry-run` flag for testing

### Data Issues

#### Web Search Failures
```
Error: Tavily search failed
```
**Solutions**:
- Check Tavily API status
- Verify API key is valid
- Check rate limits

#### LinkedIn Access Blocked
Some models may fail to access LinkedIn:
- This is expected behavior
- Models should fall back to web search
- Score adjustment is automatic

### Output Issues

#### JSON Parse Errors
```
JSONDecodeError: Expecting value
```
**Solution**: Check model output format:
```python
# Expected format
{
  "prospects": [
    {
      "name": "...",
      "first_line": "...",
      "evidence_url": "...",
      "evidence_quote": "..."
    }
  ]
}
```

#### Missing Results Files
Results not saving properly:
- Check write permissions
- Ensure `results/` directory exists
- Check disk space

## Debug Mode

Run with verbose output:
```bash
python run_evaluation.py --model xxx --debug
```

This provides:
- Detailed API calls
- Tool usage logs
- Judge scoring details
- Error stack traces

## Getting Help

### Before Asking for Help

1. Check this troubleshooting guide
2. Search [existing issues](https://github.com/revenuebench/revenue-bench/issues)
3. Try with a known working model (gpt-5)
4. Collect debug output

### Information to Provide

When reporting issues, include:
- Python version: `python --version`
- Package versions: `pip freeze`
- Error message (full traceback)
- Model being tested
- Debug output if available

### Contact Channels

- **GitHub Issues**: Best for bugs and feature requests
- **Twitter**: [@kesselmanf](https://twitter.com/kesselmanf) for quick questions
- **Email**: team@revenuebench.ai for private concerns

## Known Limitations

### Current Limitations
- English language only
- B2B SaaS focus
- Public information only
- 3 prospects per evaluation

### Platform-Specific Issues

#### macOS
- May need to install certificates: `/Applications/Python*/Install Certificates.command`

#### Windows
- Use PowerShell or WSL for best compatibility
- Path separators: Use forward slashes in configs

#### Linux
- May need to install python3-dev: `sudo apt-get install python3-dev`

## FAQ

**Q: Can I test models not on OpenRouter?**
A: Not directly, but you can proxy through OpenRouter or modify the code.

**Q: Why do some models score 0%?**
A: Usually indicates the model doesn't support required features (tool use, JSON).

**Q: Can I customize the evaluation task?**
A: Yes, see `benchmark/tasks/prompts/` for task definitions.

**Q: How reproducible are results?**
A: Very reproducible with same model version and temperature settings.

**Q: Can I run offline?**
A: No, web search and API calls require internet connection.