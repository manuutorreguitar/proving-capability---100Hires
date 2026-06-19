# Proving Capability — 100Hires Portfolio Project

## Overview
This is a portfolio research project for a Junior Growth Marketing Specialist position. The chosen topic is **Newsletter / Email Marketing for B2B SaaS**.

## Tools Installed
1. Cursor IDE
2. Claude Code add-on
3. Codex add-on
4. Git for Windows

## Steps Completed

### Phase 1 — Setup
1. Installed Cursor IDE
2. Installed Claude Code and Codex add-ons
3. Created a public GitHub repository
4. Opened the repository in Cursor
5. Created this README.md file

### Phase 2 — Research
1. Created the repository folder structure (/research/ with subfolders)
2. Curated a list of 10 experts on newsletter and email marketing for B2B SaaS
3. Built a Python script (get_transcripts.py) using the Supadata API to automatically download YouTube transcripts
4. Downloaded 24 video transcripts from 10 expert channels
5. Manually collected 2 LinkedIn posts from expert sources

## Expert Sources
Experts were selected based on:
- Active YouTube channels with recent content (2024-2026)
- Practitioners who actually do the work, not just theorize
- Specific focus on email marketing and newsletters for B2B SaaS
- Proven track record with real companies and real results

| # | Expert | Why Selected |
|---|--------|-------------|
| 1 | Russell Brunson | ClickFunnels founder, direct-response email marketing |
| 2 | HubSpot Marketing | B2B inbound marketing and email automation |
| 3 | Alex Hormozi | Audience building and email list monetization |
| 4 | Adam Robinson | CEO of RB2B, B2B email and newsletter growth |
| 5 | Instantly | Cold email platform, deliverability and outreach |
| 6 | Dave Gerhardt | Exit Five founder, B2B SaaS email strategy |
| 7 | Dan Martell | SaaS coach, email onboarding and retention |
| 8 | Ann Handley | MarketingProfs CCO, newsletter writing and B2B storytelling |
| 9 | Louis Nicholls | SparkLoop co-founder, newsletter growth and monetization |
| 10 | Matt McGarry | GrowLetter founder, grew The Hustle to 2M+ subscribers |

## Repository Structure

```
/research/
  sources.md                  — Full list of experts with links and annotations
  youtube-transcripts/        — 24 transcripts organized by author
  linkedin-posts/             — 2 LinkedIn posts from Russell Brunson and Matt McGarry
  other/                      — Additional materials
get_transcripts.py            — Script to download YouTube transcripts via Supadata API
```

## Issues Encountered and How They Were Solved
- **Unfamiliar with coding tools:** Used ChatGPT for more detailed steps on cloning the repository. Had to try a couple of times due to errors, which led to installing Git for Windows.
- **Git initialized locally while repo already existed on GitHub:** Solved with `git pull --allow-unrelated-histories` and `git push --force`.
- **Python not installed:** Installed Python 3.14 and added to PATH.
- **pip not available directly:** Solved by using `python -m pip` instead of `pip`.
