# The LLAMA of WallStreet: LLM data extraction and sentiment analysis

You have just been hired as a data scientists at a new company.
Your boss wants to create a sentiment analysis pipeline for Reddit posts: his goal is to analyze reddit comments to find useful insights about stocks to be bought or sold.
In particular, he wants a dataset with the `ticker` (or stock symbol: AAPL for Apple, TSLA for Tesla etc...) of the company and the general sentiment (In 5 levels) towards that ticker.

Moreover, he wants to be able to analyze comments every night using Leonardo and `SLURM`, **BUT**, unfortunately, he does not know how to write or execute code.
He only wants to send prompt in natural english.

In the pipeline you have to:

1. Remove non relevant comments (i.e. comments not about companies);
2. Associate a ticker to each comment talking about companies quotated in a stock exchange;
3. Add a sentiment score to each comment
4. Save the new data on disk
5. Visualize some results
6. _Design_ an agent capable of checking jobs and sending directives to launch your script on Leonardo
   - Which **tools** should it have available?
   - How would you write the **system prompt**?
7. (optional) Write the actual agent implementation

## STEP 1: Configuring the environment

The first step is to clone the repository in a directory of your choice.
First, connect to Leonardo and `cd` to the directory you want.
Then you just need to run the following command:

```bash
git clone https://gitlab.hpc.cineca.it/rmioli00/hpc_bbs_26.git
```

or in general, with any git repository:

```bash
git clone <repo_https_url>`
```

If you have already cloned the repository previously in your working directory, you can `cd` into it and download the updates with:

```bash
cd path/to/hpc_bbs_26
```

and then:

```bash
git pull
```

After you cloned and updated the repository, `cd` into the newly created directory and run the `venv` configuration script.

The script `config/1_configure_environment.sh` will create e virtualenv for you, and it will download the llm.
To start the script, you simply need to run the following command:

```bash
bash config/1_configure_environment.sh
```

The dependencies installed into this virtualenv are specified in the `requirements.txt` file.
You can add more libraries in that file, or you can install them after the environment creation.
To install additional libraries by hand, you simply need to issue the command: `pip3 install <lib_name>==<version>`.

## STEP 2: Starting the programming environment

The script `config/LLM_start_jupyter.job` will start a jupyter environment with an llm already loaded.

You can use the jupyter environment on your browser by opening an ssh tunnel from your pc to the worker node.
Just copy-paste in a terminal the instructions you see printed in the `.out` file when you start the job.

To start the jupyter server, simply run `sbatch config/LLM_start_jupyter.job`.
You can see when your environment will be provisioned by running the `squeue --me -i 5` command.
When you see your job is running, press control-c and start the ssh tunnel on a terminal on your pc.
**DO NOT START AN SSH TUNNEL ON A LEONARDO TERMINAL, PAY ATTENTION TO THIS**.
