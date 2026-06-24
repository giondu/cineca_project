# The LLAMA of WallStreet

An LLM-based sentiment-analysis pipeline that reads Reddit comments, identifies which publicly traded companies they discuss, and scores the financial sentiment toward each one. Built on the Leonardo HPC cluster using Mistral-Small-24B served via vLLM, with a SLURM agent that lets a non-technical user run the whole pipeline from plain English.

## What it does

For each Reddit comment, the pipeline:

1. Decides whether the comment is about a publicly traded company and extracts the relevant stock tickers.
2. Validates each ticker against a NASDAQ and NYSE symbol list.
3. Classifies the sentiment toward the company on a five-point scale (Very Positive to Very Negative) and maps it to a score from +2 to -2.
4. Aggregates the results into a daily mean sentiment per ticker.
5. Visualises sentiment trends and compares them against actual stock prices.

## Key design choices

**Structured output throughout.** Every LLM call uses a Pydantic schema to constrain the model's response, from ticker extraction to sentiment to the agent's tool selection. This makes the pipeline predictable and, as experiments showed, robust to temperature.

**Broad over narrow ticker interpretation.** A broad interpretation (tag a ticker when news could plausibly move the stock) outperformed a narrow one, which chased the literal subject into private, non-traded companies. Borderline noise is smoothed out by daily aggregation.

**Validation catches existence, not correctness.** The static ticker list rejects hallucinated and delisted symbols but cannot detect a valid symbol pointing to the wrong company. This limitation is documented rather than hidden.

**Parallelised, crash-safe batch runs.** Because the work is I/O-bound, the pipeline parallelises requests with a thread pool. A batch version saves to disk incrementally and resumes after interruption, motivated by long runs that outlived the model server.

## The SLURM agent

A natural-language agent lets a non-technical user operate the pipeline on the cluster. It exposes four tools (submit_job, check_status, cancel_job, get_results) and uses structured output to route plain-English requests to the right SLURM command. The LLM interprets; Python executes. The model can only select among predefined tools, never write shell commands directly.

## Honest findings

The lag correlation between sentiment and future stock returns was effectively noise, with signs flipping across lags and only 33 paired days. This is a correct negative result: the data reflects general news opinion (much of it controversy coverage) rather than market analysis, so the sentiment captures public mood more than an investment thesis.

## Tech stack

Mistral-Small-3.2-24B · vLLM · LangChain · Pydantic · pandas · SLURM · Leonardo HPC
