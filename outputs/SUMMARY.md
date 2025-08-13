# Revenue Bench Outputs Summary

## Overview

This directory contains the actual outputs from AI models evaluated on the Revenue Bench benchmark, along with their evaluation scores from our multi-judge panel.

## What's Included

### 1. Model Responses (`model_responses/`)
Complete outputs from each model including:
- The personalized first lines generated for each prospect
- Evidence URLs used for verification
- Tool usage logs (searches and extractions)

### 2. Evaluations (`evaluations/`)
Detailed scoring from the multi-judge panel:
- Final scores and rankings
- Individual judge responses
- Verification results (whether claims were verified)
- Score breakdowns across criteria

### 3. Combined Files
- `complete_outputs.json` - All data in structured format
- `README.md` - Detailed documentation

## Key Findings

### Top Performers

1. **Claude Opus 4.1** (82.5%)
   - Best overall quality
   - Strong verification of claims
   - Natural, personalized messaging

2. **GPT-5** (82.1%)
   - Close second place
   - Excellent value at $0.08/eval
   - Strong prospect research

3. **Gemini 2.5 Flash** (80.0%)
   - Good balance of quality and cost
   - Fast response times
   - Solid personalization

### Example High-Quality Output (Claude Opus 4.1)

**For Matthew Christy (Bluestone Lane):**
> "Matthew, managing 52+ Bluestone Lane locations across the Northeast must require incredible coordination - how are you handling scheduling across all those cafes?"

This demonstrates:
- ✅ Specific, verified detail (52+ locations)
- ✅ Role-relevant pain point (scheduling coordination)
- ✅ Natural conversation starter
- ✅ Clear connection to Homebase value prop

### Evaluation Process

Each model output was scored by 4 AI judges on:

| Criterion | Weight | Focus |
|-----------|--------|-------|
| Engineering Pain | 35% | Identifies real operational challenges |
| Prospect Insight | 30% | Specific, verifiable details |
| Product Fit | 25% | Natural bridge to Homebase |
| Reply Probability | 10% | Would they actually respond? |

### Verification

Models that used `tavily_extract()` to verify their claims scored significantly higher. Unverified claims were heavily penalized in the "Prospect Insight" category.

## Usage

These outputs can be used to:
1. **Compare model capabilities** - See how different models approach the same task
2. **Understand scoring** - Learn what makes a high-quality sales personalization
3. **Improve prompts** - Use successful patterns in your own implementations
4. **Train models** - Use as examples for fine-tuning

## File Structure

```
outputs/
├── README.md                     # Main documentation
├── SUMMARY.md                    # This file
├── complete_outputs.json         # All data combined
├── model_responses/              # Individual model outputs
│   ├── 01_claude-opus-4.1_response.json
│   ├── 03_gemini-2.5-flash_response.json
│   └── ...
└── evaluations/                  # Detailed scores
    ├── 01_claude-opus-4.1_eval.json
    ├── 03_gemini-2.5-flash_eval.json
    └── ...
```

## Notes

- Some models (GPT-OSS-120b, GLM-4.5, Kimi-K2) logs were from later runs and not included
- All outputs are from the same evaluation prompt and task
- Costs shown are per evaluation (3 prospects in one call)