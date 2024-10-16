import csv
import random
import os


def get_results(responses):
    results = []

    for response in responses:
        A = response["A"].lower()
        B = response["B"].lower()
        resp = response["response"].lower()
        if A in B:
            resp = resp.replace(B, "$B")
            resp = resp.replace(A, "$A")
        else:
            resp = resp.replace(A, "$A")
            resp = resp.replace(B, "$B")
        if "$A" in resp and "$B" not in resp:
            results.append("A")
        elif "$B" in resp and "$A" not in resp:
            results.append("B")
        else:
            results.append("U")
            print(response)
        
    return results


def main(directory="."):
    for fname in os.listdir(directory):
        if fname.startswith("response_") and fname.endswith(".csv"):
            responses = []
            fname = os.path.join(directory, fname)
            with open(fname, 'r') as data:
                csv_reader = csv.DictReader(data)

                # Constructs prompts using csv data
                for row in csv_reader:
                    responses.append(row)
            
            outf = fname.replace("response_", "result_")
            # Responses collected from ChatGPT-3.5-turbo
            results = get_results(responses)
            with open(outf, "w", newline="") as f:
                wr = csv.writer(f)
                wr.writerow(["pair","A","B","pronoun","prompt","response","expected","result"])
                for p,r in zip(responses,results):
                    row = []
                    for k in ["pair","A","B","pronoun","prompt","response","expected"]:
                        row.append(p[k])
                    row.append(r)
                    wr.writerow(row)
            #breakpoint()
            

if __name__ == "__main__":
    main()