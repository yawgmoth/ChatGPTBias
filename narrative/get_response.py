import csv
import pandas as pd
from openai import OpenAI
import apikey
import random
import os
import sys


def get_response(prompts, model="gpt-4o"):
    # Add your API key
    

    # Ask ChatGPT our generated prompts
    for prompt in prompts:
        response = client.chat.completions.create(
            model=model,
            messages=[
                      {"role": "system",
                       "content": "You are a storyteller writing a novel."},
                      {"role": "user",
                       "content": "Continue the story exactly as given for about one chapter."},
                      {"role": "user", 
                       "content": prompt["prompt"]}],
            temperature=0.6,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        prompt_response = response.choices[0].message.content
        
        #print(prompt_response) # Print response to view progress
        responses.append(prompt_response)
    return responses


def main(directory=".", force=False, model="gpt-3.5-turbo-0125"):
    for fname in os.listdir(directory):
        if fname.startswith("prompt_") and fname.endswith(".csv"):
            fname = os.path.join(directory, fname)
            outf = fname.replace("prompt_", "response_")
            if os.path.exists(outf) and not force:
                print(outf, "already exists. Skipping. Use -f to force overwrite")
                continue
            prompts = []
            with open(fname, 'r') as data:
                csv_reader = csv.DictReader(data)

                # Constructs prompts using csv data
                for row in csv_reader:
                    prompts.append(row)
            
            client = OpenAI(api_key=apikey.API_KEY)
            responses = []
            
            with open(outf, "w", newline="", encoding="utf-8") as f:
                wr = csv.writer(f)
                wr.writerow(["sample","repetition","promptname","profession","prompt","response"])
                for prompt in prompts:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                                  {"role": "system",
                                   "content": "You are a storyteller writing a novel."},
                                  {"role": "user",
                                   "content": "Continue the story exactly as given for about one chapter."},
                                  {"role": "user", 
                                   "content": prompt["prompt"]}],
                        temperature=0.6,
                        max_tokens=3000,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )
                    prompt_response = response.choices[0].message.content
                    
                    row = []
                    for k in ["sample","repetition","promptname","profession","prompt"]:
                        row.append(prompt[k])
                    row.append(prompt_response)
                    try:
                        wr.writerow(row)
                    except Exception:
                        print("ERROR writing", row)
                        breakpoint()
                    

                        
            #breakpoint()
            

if __name__ == "__main__":
    main(force="-f" in sys.argv)