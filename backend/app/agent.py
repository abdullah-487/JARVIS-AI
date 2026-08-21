from google import genai
from app.config import GEMINI_API_KEY
from app.search import search_web
from app.trade import build_trade_prompt

client = genai.Client(api_key=GEMINI_API_KEY)

MODELS = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash"
]


def get_mode_prompt(mode: str):
    prompts = {
        "news": """
You are in NEWS MODE.

Create a concise news briefing.

Structure:
# JARVIS NEWS BRIEF
## Top Headlines
## Why It Matters
## What To Watch Next
""",

        "report": """
You are in INTELLIGENCE REPORT MODE.

Structure:
# JARVIS INTELLIGENCE REPORT
## Executive Summary
## Current Situation
## Key Findings
## Risks
## Opportunities
## Analysis
## Future Outlook
## Conclusion
""",

        "history": """
You are in HISTORY MODE.

Structure:
# HISTORICAL ANALYSIS
## Background
## Timeline
## Major Events
## Causes
## Consequences
## Historical Significance
""",

        "research": """
You are in DEEP RESEARCH MODE.

Structure:
# JARVIS RESEARCH ANALYSIS
## Research Question
## Key Findings
## Evidence
## Different Perspectives
## Risks and Limitations
## JARVIS Analysis
## Conclusion
""",

        "trade": """
You are in GLOBAL IMPORT-EXPORT TRADE INTELLIGENCE MODE.

Create a professional trade report using the live internet results.

Focus on:
## Product Overview
## Major Exporting Countries
## Major Importing Countries
## High-Demand Markets
## Potential Buyers / Importers / Distributors
## Competitors
## Price Range
## Trade Opportunities
## Market Risks
## Shipping & Logistics
## Documents & Certifications
## Relevant HS Code
## Step-by-Step Trade Plan

Never invent buyers, prices, statistics, certifications, or trade data.
Clearly state when information cannot be verified.

Always answer in Roman Urdu.

""",

        "auto": """
Determine the best response format automatically.
"""
    }

    return prompts.get(mode.lower(), prompts["auto"])


def build_search_queries(question: str, mode: str):
    mode = mode.lower()

    queries = [question]

    if mode == "news":
        queries.extend([
            "Pakistan latest news today",
            "world latest breaking news today",
            "top international news today"
        ])

    elif mode == "trade":
        queries.extend([
            question + " import export market",
            question + " importers buyers distributors",
            question + " trade statistics demand",
            question + " HS code export requirements"
        ])

    elif mode == "report":
        queries.append(question + " latest statistics report")

    elif mode == "research":
        queries.append(question + " latest research analysis")

    return queries


def search_multiple(question: str, mode: str):
    queries = build_search_queries(question, mode)

    all_results = []
    seen_urls = set()

    for query in queries:
        print(f"JARVIS searching: {query}")

        try:
            results = search_web(query, max_results=4)

            for item in results:
                url = item.get("url", "")

                if url and url not in seen_urls:
                    seen_urls.add(url)
                    all_results.append(item)

        except Exception as e:
            print(f"Search failed: {e}")

    return all_results[:8]


def format_search_results(results):
    if not results:
        return "No live internet results were found."

    text = ""

    for index, item in enumerate(results, start=1):
        text += f"""
SOURCE {index}
Title: {item.get('title', '')}
URL: {item.get('url', '')}
Content:
{item.get('content', '')}
"""

    return text


def ask_ai(prompt):
    for model_name in MODELS:
        try:
            print(f"JARVIS AI trying: {model_name}")

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if response.text:
                return response.text, model_name

        except Exception as e:
            print(f"Model {model_name} failed: {e}")

    return None, None


def fallback_answer(question, results, mode):
    if not results:
        return (
            "# JARVIS STATUS\n\n"
            "Sir, internet search se is waqt results nahi mile. "
            "Please dobara try karein."
        )

    if mode.lower() == "news":
        answer = "# JARVIS NEWS BRIEF\n\n"

        for index, item in enumerate(results[:5], start=1):
            answer += f"## {index}. {item.get('title', 'Latest News')}\n\n"
            answer += f"{item.get('content', '')}\n\n"

        answer += "### Note\nAI analysis temporarily unavailable hai, lekin yeh live internet sources se results hain."

        return answer

    answer = f"# JARVIS LIVE INTERNET RESULTS\n\n**Question:** {question}\n\n"

    for index, item in enumerate(results, start=1):
        answer += f"## {index}. {item.get('title', 'Unknown Source')}\n\n"
        answer += f"{item.get('content', '')}\n\n"

    return answer


def ask_jarvis(question: str, mode: str = "auto"):
    print(f"JARVIS MODE: {mode}")
    print("JARVIS starting live internet research...")

    results = search_multiple(question, mode)

    print(f"JARVIS found {len(results)} unique sources")

    search_context = format_search_results(results)
    mode_prompt = get_mode_prompt(mode)

    trade_instruction = build_trade_prompt(question) if mode.lower() == "trade" else ""

    prompt = f"""
You are JARVIS, an extremely intelligent AI assistant.

Speak naturally in Roman Urdu.

IMPORTANT:
- Use ONLY the provided search results for current facts.
- Never invent current news, statistics or events.
- If search results are limited, clearly say so.
- Separate facts from analysis.

{mode_prompt}

{trade_instruction}

USER QUESTION:
{question}

LIVE INTERNET RESULTS:
{search_context}

Now answer the user.
"""

    ai_answer, model_used = ask_ai(prompt)

    if ai_answer:
        return {
            "answer": ai_answer,
            "sources": results,
            "model": model_used,
            "internet_enabled": True,
            "ai_status": "online",
            "mode": mode
        }

    return {
        "answer": fallback_answer(question, results, mode),
        "sources": results,
        "model": None,
        "internet_enabled": True,
        "ai_status": "temporarily unavailable",
        "mode": mode
    }




