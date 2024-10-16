# Bias Evaluation for ChatGPT

This repository contains the public code accompanying our paper "Towards Evaluating Profession-based Gender Bias in ChatGPT and its Impact on Narrative Generation" by Marin, A., and Eger, M., published at the AAAI AIIDE Workshop on Intelligent Narrative Technologies, 2024 (paper link to be added soon). As described in the paper, we evaluate gender bias in ChatGPT in two ways: First, we put pairs of professions into everyday situations and ask ChatGPT a question about it, comparing its response across three variations of the same prompt, that only differ in the pronoun being used. Second, we ask ChatGPT to generate a story with a protagonist of a particular profession, and then determine how often the protagonist chosen by the model uses a traditionally male or female name.

## How to Use

Each of the two evaluation efforts exists in its own directory: [`bias`](bias) contains the code that creates the variation-based prompts, and [`narrative`](narrative) contains the narrative-generation tasks. The structure of both is the same: The main file is `pipeline.py` that can be used to **m**ake the prompts, **g**et a response from ChatGPT, **p**arse that response, and **e**valuate the results, in that order, by passing the corresponding flag, e.g. `pipeline.py -mg` would only make the prompts and get a response, but not parse or evaluate it. The **g**et step requires an API key, which must be placed in a file called `apikey.py` in each of the two directories. This file should contain the API key as a string, i.e. the file should look like this:
```python
API_KEY = "YOUR API KEY GOES HERE"
```

By using the API key, the **g**et step will require funds in the OpenAI account associated with the API key. To avoid requesting the same requests over and over, responses that already exist will be skipped, unless the **f**orce-flag is passed to `pipeline.py`. Other useful flags are `-4` to use ChatGPT 4 and `-o` to use ChatGPT 4o. More details can be obtained with `--help`.

Each step of the pipeline will produce its own output files in a separate directory for each ChatGPT version and dataset (see below) being used.

## Datasets

The `datasets`-directory contains files with the profession dataset used by our experiments. As the full `occupations.csv` contains many very obscure or random occupations, `occupations_selection.csv` or `occupations_common.csv`, which were manually trimmed to exclude (subjectively) weirder occupations from the full dataset. `biased.csv` contains a selection of occupations for which the models have shown particular high bias. Which dataset is used can be controlled with the `-d` flag, followed by the path to the desired dataset file, allowing users to also provide their own.