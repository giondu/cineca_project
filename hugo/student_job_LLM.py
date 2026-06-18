"""
Standalone batch version of the LLAMA of WallStreet pipeline.
Connects to a running vLLM server, processes Reddit comments, and saves results.
Designed to be launched by SLURM (and by the agent) as a nightly job.
"""
import argparse
import os
import pandas as pd
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_openai import ChatOpenAI
import warnings
warnings.filterwarnings("ignore")

# ---- Configuration via command-line arguments ----
parser = argparse.ArgumentParser()
parser.add_argument("--endpoint", required=True, help="vLLM server endpoint, e.g. http://lrdn2874:8000/v1")
parser.add_argument("--input", default="reddit_comments.csv")
parser.add_argument("--output", default="../../hugo/nightly_results.csv")
parser.add_argument("--n", type=int, default=0, help="Number of comments to process (0 = all)")
parser.add_argument("--workers", type=int, default=16)
args = parser.parse_args()

MODEL_NAME = "mistralai/Mistral-Small-3.2-24B-Instruct-2506"
API_KEY = "password"
llm = ChatOpenAI(base_url=args.endpoint, api_key=API_KEY, model=MODEL_NAME, request_timeout=30)

# ---- Ticker extraction ----
class TickerExtraction(BaseModel):
    is_about_company: bool
    tickers: list[str]

TICKER_PROMPT = """You are a financial analyst assistant. Given a Reddit comment, decide whether it is about a publicly traded company. If it is, return the stock tickers mentioned or clearly implied. Use the broad interpretation: include a ticker when news about it could plausibly move the stock, even indirectly. Do not guess tickers from isolated unrelated words. Return valid US-listed tickers only."""

def load_valid_tickers(*paths) -> set:
    valid = set()
    for path in paths:
        with open(path) as f:
            for line in f:
                symbol = line.strip().upper()
                if symbol:
                    valid.add(symbol)
    return valid

VALID_TICKERS = load_valid_tickers("../../hugo/nasdaqlisted.txt", "../../hugo/nyselisted.txt")

def extract_tickers(comment: str):
    return llm.with_structured_output(TickerExtraction).invoke(
        input=[{"role": "system", "content": TICKER_PROMPT},
               {"role": "user", "content": comment}],
        temperature=0,
    )

def validate_tickers(tickers):
    return [t for t in tickers if t in VALID_TICKERS]

# ---- Sentiment ----
class Sentiment(str, Enum):
    VERY_POSITIVE = "Very Positive"
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"
    VERY_NEGATIVE = "Very Negative"

class SentimentResult(BaseModel):
    sentiment: Sentiment

SENTIMENT_PROMPT = """You are a financial analyst assistant. Given a Reddit comment about a company, classify the sentiment towards that company as an investment, on a five-point scale: Very Positive, Positive, Neutral, Negative, Very Negative. Judge the sentiment towards the stock, not the tone of the writing. If the comment mentions the company but expresses no clear view, classify it as Neutral."""

SENTIMENT_TO_SCORE = {
    Sentiment.VERY_POSITIVE: 2,
    Sentiment.POSITIVE: 1,
    Sentiment.NEUTRAL: 0,
    Sentiment.NEGATIVE: -1,
    Sentiment.VERY_NEGATIVE: -2,
}

def classify_sentiment(comment: str) -> Sentiment:
    result = llm.with_structured_output(SentimentResult).invoke(
        input=[{"role": "system", "content": SENTIMENT_PROMPT},
               {"role": "user", "content": comment}],
        temperature=0,
    )
    return result.sentiment

# ---- Per-comment pipeline ----
def process_comment(comment: str) -> list[dict]:
    try:
        extraction = extract_tickers(comment)
        valid = validate_tickers(extraction.tickers)
        if not valid:
            return []
        sentiment = classify_sentiment(comment)
        score = SENTIMENT_TO_SCORE[sentiment]
        return [{"ticker": t, "sentiment": sentiment.value, "score": score} for t in valid]
    except Exception:
        return []
    
# ---- Main: read data, run pipeline in parallel, save ----
def main():
    df = pd.read_csv(args.input)
    if args.n > 0:
        df = df.sample(args.n, random_state=42)

    print(f"Processing {len(df)} comments using endpoint {args.endpoint}")

    rows = []
    records = df.to_dict("records")

    def handle(rec):
        out = []
        for row in process_comment(rec["comments"]):
            row["datetime"] = rec["datetime"]
            out.append(row)
        return out

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = [ex.submit(handle, rec) for rec in records]
        for f in as_completed(futures):
            rows.extend(f.result())

    results = pd.DataFrame(rows)
    results.to_csv(args.output, index=False)
    print(f"Done. {len(results)} ticker rows saved to {args.output}")

if __name__ == "__main__":
    main()