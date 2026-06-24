# FIRST TRIAL: THIS IS NOT THE FINAL NOTEBOOK. FOR FINAL NOTEBOOK CHECK HUGO'S FOLDER - The LLAMA of WallStreet

## OvervieW:

This repository contains my solution for the **Big Data Laboratory Team Project**:

**The LLAMA of WallStreet: LLM Data Extraction and Sentiment Analysis**

The objective of the project is to build a pipeline capable of:

1. Filtering irrelevant Reddit comments
2. Identifying publicly traded companies mentioned in comments
3. Associating comments with stock tickers
4. Performing sentiment analysis
5. Computing daily sentiment statistics
6. Visualizing sentiment trends over time
7. Designing a SLURM-based agent for automated execution on Leonardo HPC

---

## Dataset

The dataset consists of approximately **100,000 Reddit comments**.

Available columns:

| Column | Description |
|----------|----------|
| datetime | Timestamp of the comment |
| subreddits | Source subreddit |
| submission_id | Reddit post identifier |
| comments | Text of the comment |

---

## Methodology

### 1. Comment Filtering

Comments not referring to publicly traded companies are discarded.

### 2. Ticker Extraction

Company names are mapped to stock tickers.

Examples:

| Company | Ticker |
|----------|----------|
| Apple | AAPL |
| Tesla | TSLA |
| Amazon | AMZN |
| Meta | META |
| Boeing | BA |
| Nvidia | NVDA |

The notebook explores both rule-based approaches and LLM-assisted extraction.

### 3. Sentiment Analysis

Sentiment is computed using:

```python
cardiffnlp/twitter-roberta-base-sentiment-latest
```

The sentiment is mapped into five levels:

| Sentiment | Score |
|------------|---------|
| Very Positive | +2 |
| Positive | +1 |
| Neutral | 0 |
| Negative | -1 |
| Very Negative | -2 |

### 4. Aggregation

Daily statistics are computed for each ticker:

- Average sentiment
- Minimum sentiment
- Maximum sentiment
- Comment count

### 5. Visualization

The notebook generates:

- Most discussed stocks
- Sentiment distributions
- Daily sentiment trends

---

## Notebook

Main notebook:

```text
The_LLAMA_of_WallStreet_Sofi.ipynb
```

---

## SLURM Agent Design

The project also proposes an agent capable of interacting with Leonardo through natural language.

### Available Tools

- submit_job
- check_queue
- read_logs
- cancel_job
- schedule_nightly_run

### Workflow

```text
Natural Language Request
            │
            ▼
        LLM Agent
            │
            ▼
     SLURM Commands
      (sbatch/squeue)
            │
            ▼
      Leonardo Cluster
            │
            ▼
         Results
```

---

## Limitations

- Sarcasm and irony
- Multiple companies in the same comment
- Company aliases and ambiguous names
- Noisy Reddit discussions
- Domain mismatch between generic sentiment models and financial language

---

## Future Improvements

- FinBERT integration
- Financial-specific datasets
- Retrieval-Augmented ticker extraction
- Correlation with stock prices
- Entity-level sentiment analysis
- Automated nightly execution on Leonardo

---

## Author

**Sofia Silingardi**

Big Data Laboratory – University Project
