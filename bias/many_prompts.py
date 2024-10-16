import csv
import pandas as pd
from openai import OpenAI
import apikey
import random

from prompts import PROMPTS



def make_pairs(dataset, n):
    pairs = []
    professions = []

    with open(dataset, 'r') as data:
        csv_reader = csv.DictReader(data)

        # Constructs prompts using csv data
        for row in csv_reader:
            professions.append(row["Occupations"])
    
    for i in range(n):
        a = ""
        b = ""
        while a == b:
            a = random.choice(professions)
            b = random.choice(professions)
        pairs.append((a,b))
    return pairs
        
def make_prompts(pairs, prompt, answer, expected):
    prompts = []
    for i,p in enumerate(pairs):
        for prn in [("he", "his"), ("she", "her"), ("they", "their")]:
            professionA = p[0]
            professionB = p[1]
            pronoun = prn[0]
            possessive = prn[1]
            # Minor prompt change due to grammar rules for pronoun 'they'
            pr = f'Answer in one sentence and in this format "{answer}". {prompt}'.replace("$A", professionA).replace("$B", professionB).replace("$PRONOUN", pronoun).replace("$POSSESSIVE", possessive).replace("$WAS", "were" if pronoun == "they" else "was")
        
            prompts.append((i,professionA,professionB,pronoun,pr,expected))
    # Returns list of prompts
    return prompts



def main(directory=".", n=5, dataset = 'Test_datasets/occupations_common.csv'):
    if not dataset:
        dataset = 'Test_datasets/occupations_common.csv'
    pairs = make_pairs(dataset, n)

    
    # Prompts generated from information from dataset
    for i,p in enumerate(PROMPTS):
        prompts = make_prompts(pairs, p[0], p[1], p[2])
        with open(f"{directory}/prompt_{i}.csv", "w", newline='') as f:
            wr = csv.writer(f)
            wr.writerow(["pair","A","B","pronoun","prompt","expected"])
            for p in prompts:
                wr.writerow(p)


if __name__ == "__main__":
    main()