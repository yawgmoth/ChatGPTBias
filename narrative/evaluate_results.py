import csv
import random
import os
from prompts import PROMPTS

import matplotlib.pyplot as plt
import numpy as np

def accumulate_results(results):
    distributions = {}
    used_names = {}
    for r in results:
        profession = r["profession"]
        if profession not in distributions:
            distributions[profession] = {"M": 0, "F": 0, "U": 0}
            used_names[profession] = {}
        distributions[profession][r["gender"]] += 1
        if r["gender"] != "U":
            if r["used_name"] not in used_names[profession]:
                used_names[profession][r["used_name"]] = 0
            used_names[profession][r["used_name"]] += 1
    return distributions, used_names


def topk(d, k):
    values = list(d.items())
    values.sort(key=lambda ke: -ke[1])
    return "\n".join(map(lambda ke: ke[0] + ": " + str(ke[1]), values[:k]))

def f(n):
    return "%.1f"%n
    
def f1(n):
    return "%.0f"%n
    
def show_frequent(names, perc=0.2):
    total = sum(names.values())
    found = False
    for n in names:
        if names[n] >= perc*total:
            if not found:
                print(f"   Frequent names:")
            found = True
            print(f"      {n}: {f(names[n]*100.0/total)}%")
            
    if not found:
        print("   No outlier names")
    

def main(directory=".", model=""):
    distributions = {}
    used_names = {}
    ltx = ""
    by_profession = {}
    for fname in os.listdir(directory):
        if fname.startswith("result_") and fname.endswith(".csv"):
            idx = int(fname.split("_")[1].split(".")[0])
            fname = os.path.join(directory, fname)
            
            results = []
            with open(fname, 'r') as data:
                csv_reader = csv.DictReader(data)

                for row in csv_reader:
                    results.append(row)
            
            dist, un = accumulate_results(results)
            for d in dist:
                if d not in distributions:
                    distributions[d] = dist[d]
                    used_names[d] = un[d]
                else:
                    for g in "MFU":
                        distributions[d][g] += dist[d][g]
                    for n in un[d]:
                        if n not in used_names[d]:
                            used_names[d][n] = 0
                        used_names[d][n] += un[d][n]
            
           
            
            print(fname)
            print(PROMPTS[idx][0])
            for d in dist:
                perc = dist[d]['F']*100.0/(dist[d]['F'] + dist[d]['M']+dist[d]['U'])
                print(f"   {d}: {dist[d]['M']} male, {dist[d]['F']} female; female percentage: {f(perc)}")
                show_frequent(un[d])
                if d not in by_profession:
                    by_profession[d] = {}
                by_profession[d][PROMPTS[idx][1]] = perc
                
            
    print("summary:")
    for d in distributions:
        print(f"   {d}: {distributions[d]['M']} male, {distributions[d]['F']} female; female percentage: {f(distributions[d]['F']*100.0/(distributions[d]['F'] + distributions[d]['M']+distributions[d]['U']))}%")
        show_frequent(used_names[d])
        by_profession[d]["overall"] = distributions[d]['F']*100.0/(distributions[d]['F'] + distributions[d]['M']+distributions[d]['U'])
        
        
    for p in by_profession:
        print(p, end=" & ")
        print(model, end=" & ")
        for pr in PROMPTS:
            print(f" ${f1(by_profession[p][pr[1]])}\\%$",end=" &")
        print(f" ${f1(by_profession[p]['overall'])}\\%$",end=" ")
        print(r"\\\hline")
   
            
            

if __name__ == "__main__":
    ind = np.arange(len(PROMPTS))
    width = 0.35
    fig, ax = plt.subplots()
    barnames = [ "ChatGPT 3.5", "ChatGPT 4"]
    bars = []
    i = 0
    for dir in ["chatgpt_3.5_many", "chatgpt_4_many"]:
        names, incons, incorr = main(dir, barnames[i])
        i += 1
        bars.append(ax.bar(ind, incons, width=width))
        ind =  ind + width
    ax.set_xticks(ind - width*1.5 )
    
    ax.set_xticklabels(names)
    ax.tick_params(axis='x', labelrotation=45)
    ax.legend(bars, barnames)
    #plt.title("Inconsistent Results (percentage) for Different Pronouns")
    fig.tight_layout()
    
    plt.show()