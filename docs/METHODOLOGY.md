# Revenue Bench Methodology

## Overview

Revenue Bench evaluates AI models on their ability to write personalized B2B cold outreach messages. The benchmark focuses on a realistic sales scenario: personalizing first lines for prospects at multi-location businesses that could benefit from Homebase's workforce management solution.

## Evaluation Schema

```
┌─────────────────────────────────────────────────────────────┐
│                     Revenue Bench v0.1                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    INPUT: Sales Task                        │
│   • Company Context (Homebase)                              │
│   • 3 Prospects (LinkedIn URLs)                             │
│   • Instructions & Constraints                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  MODEL EXECUTION                            │
│   ┌──────────────────────────────────────────────┐         │
│   │ 1. Research Phase                            │         │
│   │   • Web Search (Tavily API)                  │         │
│   │   • Content Extraction                       │         │
│   │   • Information Synthesis                    │         │
│   └──────────────────────────────────────────────┘         │
│   ┌──────────────────────────────────────────────┐         │
│   │ 2. Generation Phase                          │         │
│   │   • Personalized First Lines (≤35 words)     │         │
│   │   • Evidence URLs                            │         │
│   │   • Prospect-Specific Insights               │         │
│   └──────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    MULTI-JUDGE EVALUATION                   │
│                                                              │
│   ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────┐ │
│   │ Gemini 2.5 │  │  Kimi K2   │  │ GPT-5 Mini │  │Opus 4│ │
│   └────────────┘  └────────────┘  └────────────┘  └──────┘ │
│         │               │               │             │      │
│         └───────────────┴───────────────┴─────────────┘      │
│                              │                               │
│                     ▼ Scoring Matrix ▼                       │
│   ┌──────────────────────────────────────────────┐         │
│   │ • Engineering Pain (35%)                     │         │
│   │ • Prospect Insight (30%)                     │         │
│   │ • Product-Market Fit (25%)                   │         │
│   │ • Reply Probability (10%)                    │         │
│   └──────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    FINAL SCORE & RANKING                    │
│   • Median across judges                                    │
│   • Average across prospects                                │
│   • Performance per dollar calculation                      │
└─────────────────────────────────────────────────────────────┘
```

## Task Design

### The Homebase Task

Models are given:
- **Company value prop**
- **3 real prospects with job titles specified**
- **LinkedIn profiles**: URLs to actual LinkedIn profiles for research
- **Tools**: Web search and content extraction capabilities

Models must:
1. Research each prospect using provided tools
2. Find specific, verifiable details about the prospect or company
3. Write personalized first lines (≤35 words) that bridge from the detail to company
4. Provide evidence URLs for verification

### Why This Task?

This task was chosen because it:
- **Represents real work**: SDRs spend hours daily on personalization
- **Requires multiple skills**: Research, synthesis, creative writing, business understanding
- **Is measurable**: Claims can be verified, quality can be assessed
- **Has clear success criteria**: Would the prospect actually reply?

## Evaluation Process

### 1. Batch Processing (Cost Optimization)

Instead of evaluating each prospect separately, we process all 3 prospects in a single API call:
- **67% cost reduction** compared to individual calls
- **Consistent context** across all prospects
- **More efficient token usage**

### 2. Web Verification

Models have access to two tools:
- **tavily_search()**: Search the web for prospect information
- **tavily_extract()**: Extract and verify content from specific URLs

The verification step is critical - models that make claims without verification are heavily penalized.

### 3. Multi-Judge Scoring

Each response is evaluated by 4 independent AI judges:
- Google Gemini 2.5 Pro
- Moonshot Kimi K2
- OpenAI GPT-5 Mini
- Anthropic Claude Opus 4.1

### Scoring Criteria

Each judge scores on 4 dimensions (total 40 points per prospect):

#### 1. Engineering/Operations Pain Recognition (35%)
- Does the message identify a real operational challenge?
- Is it specific to multi-location management?
- Does it resonate with the prospect's role?

#### 2. Prospect-Specific Insight (30%)
- Is the detail verifiable and accurate?
- Is it non-obvious (not just from the job title)?
- Does it show genuine research effort?
- **Penalty**: Unverified claims cap at 2/10 points

#### 3. Product-Market Fit (25%)
- Natural connection to company value prop
- Smooth transition from insight to solution
- Relevance to the specific industry/role

#### 4. Reply Probability (10%)
- Would this message actually get a response?
- Does it feel human and conversational?
- Is it concise and to the point?

### Score Aggregation

1. Each judge provides scores for all 3 prospects
2. We take the **median score** across judges for each prospect
3. Final score = average of all prospect scores (normalized to 0-100%)

Using median instead of mean reduces the impact of outlier judges.

## Addressing Bias in Evaluation

### Sources of Potential Bias

1. **Judge Model Bias**: Each AI judge may have inherent preferences
   - Mitigation: Use 4 diverse judges from different providers
   - Result: Median scoring reduces single-judge influence

2. **Task Design Bias**: Focus on Homebase/multi-location businesses
   - Acknowledged limitation for v0.1
   - v0.2 will expand to multiple company contexts

3. **Language & Cultural Bias**: Currently English-only, US-centric businesses
   - Plan: Add multilingual support and global business contexts

4. **Industry Bias**: Heavy focus on retail, hospitality, healthcare
   - Plan: Expand to other vericals

### Bias Monitoring

We track:
- Judge score variance (high variance indicates potential bias)
- Model performance patterns by provider
- Correlation between model size and performance
- Cost vs. performance relationships

## Verification System

### Why Verification Matters

Many models can generate plausible-sounding personalization, but accuracy matters in real outreach. Our verification system ensures models:
1. Actually visit the evidence URLs they cite
2. Extract real information rather than hallucinating
3. Base personalization on facts, not assumptions

### Verification Process

1. **Tool Usage Tracking**: System logs all tavily_extract() calls
2. **URL Matching**: Evidence URLs are checked against visited URLs
3. **Score Adjustment**: Unverified claims receive severe penalties
4. **Transparency**: Verification status is shown to judges

## Cost Analysis

### Per-Evaluation Costs

Costs vary significantly by model:
- **Most Efficient**: GPT-OSS-120B at $0.004/eval
- **Best Performance**: Claude Opus 4.1 at $2.09/eval

### Total Benchmark Cost

Running all 33 models costs approximately $6.11:
- Model API calls: ~$6.11
- Judge scoring: ~$1.00
- Tavily searches: ~$0.50

The high costs of AI SDRs and advanced models make it crucial to evaluate their ROI. Some enterprise AI SDR solutions cost $5,000-15,000 per month - Revenue Bench helps justify these investments with transparent performance metrics.

## Statistical Validity

### Sample Size

While 3 prospects may seem small, consider:
- Each prospect requires multiple sub-tasks (research, synthesis, writing)
- 4 judges × 4 criteria × 3 prospects = 48 scoring decisions per model
- Focus on depth over breadth for meaningful evaluation

### Judge Agreement

We measure inter-judge reliability through:
- Standard deviation of scores
- Correlation between judge rankings
- Consistency in identifying top/bottom performers

## Limitations

1. **Single Company Context**: Only evaluates Homebase personalization
2. **Public Information Only**: Can't access private CRM data
3. **English Only**: Currently limited to English language
4. **B2B SaaS Focus**: May not generalize to other industries

## v0.2 Improvements (Coming Soon)

### Expanded Personalization Tasks

We're adding 2 new personalization variations:
1. **Company Size Personalization**: Tailoring messages based on employee count, revenue, growth stage
2. **Job Title Personalization**: Adapting tone and content for C-suite vs. managers vs. individual contributors
3. **Industry/Vertical Personalization**

### Template Email Generation

New task: Create reusable email templates for sequencers (Instantly.ai, Smartlead, Lemlist, etc) that:
- Maintain personalization placeholders
- Utilize lead magnets for specific buyer
- Optimize for different stages of outreach sequence
- Include subject lines and CTAs

## v1.0 Roadmap: Testing AI SDRs

### The Black Box Problem

Current AI SDRs (11x.ai, aisdr.com, artisan, jason ai etc.) operate as black boxes:
- No transparency in their underlying models
- No standardized performance metrics
- No way to compare effectiveness across vendors
- Prices range from $500 to $15,000+ per month

### Our Solution

Revenue Bench v1.0 will:
1. **Test all major AI SDRs** on identical tasks
2. **Provide transparent performance metrics**
3. **Calculate true ROI** including all costs
4. **Enable informed buying decisions** for GTM leaders

## Long-Term Vision: Full Revenue Suite

### Complete SDR Task Coverage

We're building benchmarks for every SDR responsibility:
1. **ICP & Buyer Persona Analysis**: Understanding target markets
2. **Lead Database Building**: Finding and enriching prospects
3. **Signal/Trigger Mining**: Identifying buying intent
4. **Content Creation**: Writing offers, lead magnets, email copy, LinkedIn messages
5. **Follow-up Management**: Handling responses and objections
6. **Call Scheduling**: Booking meetings and handoffs to AEs

### Expansion to AE and Marketing

Future benchmarks will cover:
- **Account Executive Tasks**: Discovery calls, demos, proposals, negotiation
- **Marketing Tasks**: Content generation, SEO optimization, ad copy, landing pages
- **Revenue Operations**: Forecasting, pipeline analysis, territory planning

The goal: Complete coverage of the entire revenue-generating department.

## Why Transparency Matters

### The Open-Source Alternative

We believe not every company will adopt expensive, proprietary AI SDRs. Many will build their own using:
- Open-source LLMs (GPT-OSS, Llama, GLM, etc.)
- Custom workflows and integrations
- Internal data and processes

These GTM leaders need a way to evaluate their custom solutions against commercial alternatives. Revenue Bench provides that standard.

### Enabling Informed Decisions

Transparency helps:
- **Vendors**: Prove their value with independent metrics
- **Buyers**: Make data-driven purchasing decisions
- **Builders**: Benchmark custom solutions against commercial ones
- **Investors**: Understand the AI SDR landscape

## Crowdsourcing Human Evaluation

### The Plan

We're building a system to:
1. **Collect human expert evaluations** from experienced sales professionals
2. **Compare human vs. AI judge scores** to identify gaps
3. **Train better evaluation models** using human feedback
4. **Create industry-specific scoring** with domain experts

### How to Participate

Coming soon:
- Submit your sales expertise for verification
- Evaluate model outputs for your industry
- Contribute to scoring criteria refinement
- Help train the next generation of judges

## Technical Framework

### Why Inspect AI?

We chose the [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) framework because it's:
- **Production-ready**: Built for serious AI evaluation
- **Flexible**: Supports custom tasks, agents, tools, and scoring
- **Reproducible**: Ensures consistent results across runs
- **Well-documented**: Easy to understand and extend
- **Open-source**: Transparent and community-driven

Simply put: Inspect AI is top-notch for building rigorous AI benchmarks.

## Support Revenue Bench

### The Cost Reality

Running comprehensive AI evaluations is expensive:
- Each full benchmark run costs ~$10
- Testing new models requires multiple runs
- Expanding tasks multiplies costs
- Human evaluation adds significant expense

### How You Can Help

If you find Revenue Bench valuable, consider supporting our work:
- **Use our data**: Cite Revenue Bench in your research
- **Contribute code**: Submit PRs with improvements
- **Share feedback**: Help us refine our methodology
- **Financial support**: Help cover API and infrastructure costs

**[Support Revenue Bench →](#)** *(Donation link coming soon)*

Your support helps keep this benchmark free, transparent, and continuously improving for the entire sales community.

## Reproducibility

All components are open source:
- Task prompts are fully documented
- Judge prompts are transparent
- Scoring logic is deterministic
- Random seeds can be set for consistency

To reproduce results:
1. Use the same model versions
2. Set consistent temperature (0.7)
3. Use identical prompts
4. Run during similar time periods (for web data consistency)

---

*Making AI sales evaluation transparent, one benchmark at a time.*