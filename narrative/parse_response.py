import csv
import random
import os

def clean(name):
    return name.strip(",.'")
    
genders = {}
with open("../datasets/name_gender_dataset.csv", 'r') as data:
    csv_reader = csv.DictReader(data)

    for row in csv_reader:
        name = row["Name"].lower()
        if name not in genders:
            genders[name] = row["Gender"]


def get_results(responses):
    results = []

    for response in responses:
        resp = response["response"].lower()
        if resp.startswith(response["prompt"].lower()):
            resp = resp[len(response["prompt"].lower()):].strip()
        items = resp.split()[:2]
        first = clean(items[0])
        last = clean(items[1])
        if last in ["who", "which", "that"]:
            last = ""
        name = first 
        if name in ["the", "dr", "detective"]:
            name = last
        gender = genders.get(name, "U")
        if gender == "U":
            gender = genders.get(last, "U")
            name = last
        results.append((first,last,name,gender))
        
    return results
    
def truncate(item):
    return item.split("\n")[0][:75]


def main(directory="."):

    for fname in os.listdir(directory):
        if fname.startswith("response_") and fname.endswith(".csv"):
            responses = []
            fname = os.path.join(directory, fname)
            with open(fname, 'r', encoding="utf-8") as data:
                csv_reader = csv.DictReader(data)

                # Constructs prompts using csv data
                for row in csv_reader:
                    responses.append(row)
            
            outf = fname.replace("response_", "result_")
            # Responses collected from ChatGPT-3.5-turbo
            results = get_results(responses)
            with open(outf, "w", newline="") as f:
                wr = csv.writer(f)
                wr.writerow(["sample","repetition","promptname","profession","prompt","response","result","token2","used_name","gender"])
                for p,r in zip(responses,results):
                    row = []
                    for k in ["sample","repetition","promptname","profession","prompt","response"]:
                        row.append(truncate(p[k]))
                    row.extend(r)
                    wr.writerow(row)
            #breakpoint()
            

if __name__ == "__main__":
    main()