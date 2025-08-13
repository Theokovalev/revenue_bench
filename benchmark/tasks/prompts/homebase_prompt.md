# Homebase Task - Personalized Cold Outreach

## Context

You're an SDR (Sales Development Representative) at Homebase (joinhomebase.com).

**Company**: Homebase provides workforce management software for small businesses with hourly workers.

**Value Proposition**: Cut labor cost & chaos across multi-location hourly teams with simple scheduling, time tracking, payroll, and labor-law compliance.

## Your Task

Write one first line (≤35 words) for EACH of the 3 prospects below that:
1. Cites a specific, verifiable detail about the prospect or their company
2. Naturally bridges to Homebase's value proposition
3. Sounds human and authentic, not templated

**Important**: You have access to web search tools. Use them to find and verify specific information about each prospect.

## The 3 Prospects

### Prospect 1: Matthew Christy
- **Title**: VP, Northeast Operations
- **Company**: Bluestone Lane
- **LinkedIn**: https://www.linkedin.com/in/matthew-christy-62ba7440/
- **Company Context**: Australian-inspired coffee chain with 50+ locations across the Northeast

### Prospect 2: Isaac Reback
- **Title**: Talent Resourcing Specialist
- **Company**: sweetgreen
- **LinkedIn**: https://www.linkedin.com/in/isaac-reback-3a136277/
- **Company Context**: Fast-casual restaurant chain focused on healthy, sustainable food

### Prospect 3: Tiffany Porter
- **Title**: Regional Operations Manager
- **Company**: Massage Envy
- **LinkedIn**: https://www.linkedin.com/in/tiffany-porter-95462095/
- **Company Context**: Wellness franchise with 1,000+ locations nationwide

## Output Format

Return your response as valid JSON with this exact structure:

```json
{
  "prospects": [
    {
      "name": "Matthew Christy",
      "first_line": "Your personalized first line here (max 35 words)",
      "evidence_url": "https://source-where-you-found-the-information.com",
      "evidence_quote": "Optional: The specific quote or data point you referenced"
    },
    {
      "name": "Isaac Reback",
      "first_line": "Your personalized first line here (max 35 words)",
      "evidence_url": "https://source-where-you-found-the-information.com",
      "evidence_quote": "Optional: The specific quote or data point you referenced"
    },
    {
      "name": "Tiffany Porter",
      "first_line": "Your personalized first line here (max 35 words)",
      "evidence_url": "https://source-where-you-found-the-information.com",
      "evidence_quote": "Optional: The specific quote or data point you referenced"
    }
  ]
}
```

## Evaluation Criteria

Your first lines will be evaluated on:
- **Specificity**: Uses real, verifiable information about the prospect/company
- **Relevance**: Natural connection to scheduling/labor management challenges
- **Authenticity**: Sounds like a real person wrote it, not a template
- **Evidence**: Includes source URL to back up claims

## Examples of Good First Lines

✅ **Good**: "Noticed Bluestone Lane just opened 5 new Manhattan locations this quarter - coordinating schedules across 50+ cafes during this expansion must be complex."

✅ **Good**: "Saw sweetgreen's recent push into suburban markets with 30 new locations planned - managing hourly staff compliance across multiple states is likely getting challenging."

## Examples of Bad First Lines

❌ **Bad**: "Hi Matthew, I help companies like yours save time and money." (Too generic)

❌ **Bad**: "Managing multiple locations is hard, right?" (No specific detail)

❌ **Bad**: "I saw you work at Bluestone Lane." (No value, just stating obvious)