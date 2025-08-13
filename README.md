# Revenue Bench - AI Sales Performance Benchmark

Evaluate AI models on real-world B2B sales tasks. Open-source, transparent, and reproducible.

## 🏆 Current Leaderboard (Homebase Task)

| Rank | Model | Score | Cost/Eval | Performance/$ |
|------|-------|-------|-----------|---------------|
| 🥇 1 | Claude Opus 4.1 | 82.5% | $2.09 | 0.39 |
| 🥈 2 | GPT-5 | 82.1% | $0.08 | 10.24 |
| 🥉 3 | Gemini 2.5 Flash | 80.0% | $0.08 | 9.49 |
| 4 | Claude Opus 4 | 78.8% | $0.98 | 0.80 |
| 5 | GPT-OSS-120B | 78.7% | $0.004 | 203.91 |
| 6 | GLM-4.5 | 77.9% | $0.12 | 6.44 |
| 7 | Grok-4 | 77.5% | $0.31 | 2.49 |
| 8 | Claude Sonnet 4 | 75.8% | $0.47 | 1.61 |
| 9 | Kimi-K2 | 74.6% | $0.09 | 7.91 |
| 10 | O3 | 73.3% | $0.08 | 9.68 |
| 11 | Grok-3 | 72.5% | $0.34 | 2.11 |
| 12 | GLM-4-32B | 72.1% | $0.07 | 10.45 |
| 13 | GPT-4.1 | 67.9% | $0.07 | 9.06 |
| 14 | GPT-5-Mini | 64.2% | $0.07 | 8.94 |
| 15 | Gemini 2.5 Flash Lite | 62.9% | $0.07 | 9.58 |
| 16 | O3-Mini | 60.0% | $0.07 | 8.65 |
| 17 | Qwen3-235B-A22B-Thinking | 54.6% | $0.07 | 8.19 |
| 18 | DeepSeek-R1 | 52.1% | $0.08 | 6.85 |
| 19 | Qwen3-30B-A3B-Instruct | 51.3% | $0.06 | 8.34 |
| 20 | Sonar-Pro | 47.1% | $0.08 | 5.68 |
| 21 | Qwen-2.5-72B-Instruct | 46.2% | $0.07 | 6.88 |
| 22 | Gemma-3-27B-IT | 45.8% | $0.07 | 6.22 |
| 23 | Jamba-Large-1.7 | 45.4% | $0.07 | 6.59 |
| 24 | Mixtral-8x22B-Instruct | 43.8% | $0.06 | 6.78 |
| 25 | Llama-3.1-70B-Instruct | 43.3% | $0.07 | 5.81 |
| 26 | Mixtral-8x7B-Instruct | 42.9% | $0.06 | 6.64 |
| 27 | Llama-4-Maverick | 40.8% | $0.06 | 6.69 |
| 28 | Jamba-Mini-1.7 | 30.8% | $0.07 | 4.40 |
| 29 | GPT-OSS-20B | 2.5% | $0.04 | 0.57 |
| 30 | Gemini-2.5-Pro | 2.5% | $0.08 | 0.31 |
| 31 | GPT-5-Nano | 0.0% | $0.05 | 0.00 |
| 32 | Grok-3-Mini | 0.0% | $0.05 | 0.00 |
| 33 | GLM-4.5-Air:Free | 0.0% | $0.05 | 0.00 |

**33 Models Evaluated** - Total Cost: $6.11 | Average Score: 52.4%  
**Best Value**: GPT-OSS-120B (203.9 performance per dollar)  
**Most Accurate**: Claude Opus 4.1 (82.5% accuracy)  
[Full Results →](results/leaderboard.md)

## 🚀 Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/revenuebench/revenue-bench.git
   cd revenue-bench
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up API keys:
   ```bash
   cp .env.example .env
   # Edit .env with your OPENROUTER_API_KEY and TAVILY_API_KEY
   ```

4. Run evaluation:
   ```bash
   python run_evaluation.py --model openrouter/openai/gpt-5
   ```

## 📖 Documentation

- [Setup Guide](docs/SETUP.md) - Detailed setup instructions
- [Methodology](docs/METHODOLOGY.md) - How we evaluate
- [Add Your Model](docs/ADD_MODEL.md) - Test new models
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues

## 🎯 What We Test

**Current Task: Homebase - Personalized Cold Outreach**

Models write personalized first lines for B2B cold emails to multi-location businesses. Each line must:
- Reference specific, verifiable details about the prospect
- Connect naturally to the product value proposition
- Sound authentic and human

[See Task Details →](benchmark/tasks/prompts/homebase_prompt.md)

## 📊 Evaluation Methodology

We use a multi-judge system with 4 AI judges scoring on:
- **Engineering Pain Recognition** (35%) - Identifies real operational challenges
- **Prospect-Specific Insight** (30%) - Uses verified information
- **Product-Solution Fit** (25%) - Natural connection to value prop
- **Reply Probability** (10%) - Would you actually reply?

[See Judge Criteria →](benchmark/judges/prompts/judge_prompt.md)

## 🤝 Contributing

We welcome contributions! You can:
- Add new AI models to test
- Propose new sales tasks
- Improve evaluation methodology
- Fix bugs or improve documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📈 Results

All evaluation results are stored in `results/` with:
- `leaderboard.json` - Latest results in JSON format
- `leaderboard.md` - Human-readable leaderboard
- `historical/` - Previous evaluation runs

## 🔧 Advanced Usage

### Test a single model:
```bash
python run_evaluation.py --model openrouter/anthropic/claude-opus-4.1
```

### Run batch evaluation:
```bash
python run_evaluation.py --batch config.yaml
```

### Use custom task:
```bash
python run_evaluation.py --model openrouter/openai/gpt-5 --task custom.yaml
```

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with:
- [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) - Evaluation framework
- [OpenRouter](https://openrouter.ai) - Unified API for AI models
- [Tavily](https://tavily.com) - Web search and verification

## 🚧 Roadmap

### v0.2 (Coming Soon)
- **3 New Personalization Tasks**: Company size, job titles, industry verticals
- **Email Template Generation**: Reusable templates for sequencers
- **Expanded Prospects**: More diverse industries and roles

### v1.0 (2026)
- **AI SDR Testing**: Benchmark all major AI SDRs (11x.ai, aisdr.com, artisan, jason ai etc.)
- **Full SDR Suite**: ICP analysis, lead enrichment, signal mining, follow-ups
- **Human Evaluation**: Crowdsourced expert scoring

### Long-term Vision
Complete coverage of revenue-generating roles:
- **SDR Tasks**: Full prospecting and outreach workflow
- **AE Tasks**: Discovery, demos, proposals, negotiation
- **Marketing Tasks**: Content, SEO, ads, landing pages
- **RevOps**: Forecasting, pipeline analysis, territory planning

## 💡 Why Revenue Bench?

### The Problem
AI SDRs are expensive black boxes:
- Prices range from $500 to $15,000+ per month
- No transparency in underlying models
- No standardized performance metrics
- No way to compare vendors objectively

### Our Solution
- **Transparent Benchmarks**: Open methodology and scoring
- **Real Tasks**: Based on actual SDR workflows
- **Cost Analysis**: Performance per dollar metrics
- **Vendor-Neutral**: No bias, just data

### For Open-Source Builders
Not everyone will adopt proprietary AI SDRs. Many companies are building custom solutions with open-source LLMs. Revenue Bench provides the standard to evaluate these custom implementations against commercial alternatives.

## 🤝 Support Revenue Bench

### The Cost Reality
Running comprehensive AI evaluations is expensive:
- Each full benchmark run costs ~$10
- Testing new models requires multiple runs
- Infrastructure and API costs add up quickly

### How You Can Help
- **Use Our Data**: Cite Revenue Bench in your research
- **Contribute**: Submit PRs with improvements
- **Share**: Spread the word about transparent AI evaluation
- **Donate**: Help cover API and infrastructure costs

**[Support Revenue Bench →](#)** *(Donation link coming soon)*

## 📧 Contact

- GitHub Issues: [Report bugs or request features](https://github.com/revenuebench/revenue-bench/issues)
- Twitter: [@kesselmanf](https://twitter.com/kesselmanf)

---

*Making AI sales evaluation transparent, one benchmark at a time.*