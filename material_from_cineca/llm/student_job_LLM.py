from datetime import datetime
from glob import glob
from pathlib import Path

import pandas as pd
from openai import OpenAI

INPUT_FILES = glob("/leonardo_scratch/fast/tra25_bbs/rmioli00/data/*")
MODEL_NAME = "mistralai/Mistral-Small-3.1-24B-Instruct-2503"

VLLM_ENDPOINT = "http://127.0.0.1:8000/v1"
API_KEY = "password"
LIMIT = int(2_000)  # Maximum is ~100_000


def read_data(input_file: Path | str, limit: int, seed: int = 32) -> pd.DataFrame:
    """
    Reads data from input_file with a read_csv function in python

    Args:
        input_file: path to the input file.

    Return:
        Returns a pandas dataframe.
    """
    df = pd.read_csv(input_file).sample(n=limit, replace=False, random_state=seed)
    return df


if __name__ == "__main__":
    # Wait the llm becomes available. A while loop with a network request and check over the
    # status would be better, but for sake of simplicity we will use a sleep.

    t0 = datetime.now()

    # OpenAI client pointing to our local model
    client = OpenAI(base_url=VLLM_ENDPOINT, api_key=API_KEY)

    # Read data files
    df = read_data(INPUT_FILES, LIMIT)

    # YOUR PIPELINE GOES HERE
