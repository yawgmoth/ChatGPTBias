import csv
import pandas as pd
from openai import OpenAI
import apikey
import random

from prompts import PROMPTS



def sample(dataset, n):
    result = ["Graduate Student"]
    professions = []

    with open(dataset, 'r') as data:
        csv_reader = csv.DictReader(data)

        # Constructs prompts using csv data
        for row in csv_reader:
            professions.append(row["Occupations"])
    
    for i in range(n-1):
        a = random.choice(professions)
        if a not in result:
            result.append(a)
    return result
        
def make_prompts(pairs, prompt, promptname, m=1):
    prompts = []
    for i,p in enumerate(pairs):
        profession = p.lower()
        pr = prompt.replace("$A", profession).replace("$COUNT", "an" if profession[0].lower() in "aeiou" else "a")
        for j in range(m):
            prompts.append((i,j,promptname,profession,pr))
    # Returns list of prompts
    return prompts



def main(directory=".", n=5, m=10, dataset = '../datasets/occupations_common.csv'):
    if not dataset:
        dataset = '../datasets/occupations_common.csv'
    sam = sample(dataset, n)

    # Prompts generated from information from dataset
    for i,p in enumerate(PROMPTS):
        prompts = make_prompts(sam, p[0], p[1], m)
        with open(f"{directory}/prompt_{i}.csv", "w", newline='') as f:
            wr = csv.writer(f)
            wr.writerow(["sample","repetition","promptname","profession","prompt"])
            for p in prompts:
                wr.writerow(p)


if __name__ == "__main__":
    main()