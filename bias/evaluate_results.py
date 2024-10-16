import csv
import random
import os
from prompts import PROMPTS

import matplotlib.pyplot as plt
import numpy as np

class Pair:
    def __init__(self, prompt, A, B, expected):
        self.prompt = prompt
        self.A = A
        self.B = B
        self.expected = expected
        self.results = {}
    def add_result(self, pronoun, result):
        self.results[pronoun] = result
    def is_consistent(self, binary=False):
        if binary:
            return self.results["he"] == self.results["she"]
        if self.results["he"] != self.results["she"]:
            return False
        if self.results["she"] != self.results["they"]:
            return False
        return True
    def correct(self):
        n = 0
        for k in self.results:
            if self.results[k] == self.expected: 
                n += 1
        return n




def accumulate_results(results):
    responses = {}
    inconsistent = {}
    for r in results:
        if r["pair"] not in responses:
            responses[r["pair"]] = Pair(r["prompt"], r["A"], r["B"], r["expected"])
        responses[r["pair"]].add_result(r["pronoun"], r["result"])
        
    correct = 0
    consistent = 0
    consistent_binary = 0
    
    for r in responses:
        if responses[r].is_consistent():
            consistent += 1
        else:
           if responses[r].A not in inconsistent:
               inconsistent[responses[r].A] = 0
           inconsistent[responses[r].A] += 1
           if responses[r].B not in inconsistent:
               inconsistent[responses[r].B] = 0
           inconsistent[responses[r].B] += 1
        if responses[r].is_consistent(True):
            consistent_binary += 1
        correct += responses[r].correct()
        
    return (correct,consistent,consistent_binary,len(responses),inconsistent)


def topk(d, k):
    values = list(d.items())
    values.sort(key=lambda ke: -ke[1])
    return "\n".join(map(lambda ke: ke[0] + ": " + str(ke[1]), values[:k]))

log = open("table.log", "w")

def f(n):
    return "%.1f"%n

def main(directory=".", version=""):
    correct = 0 
    consistent = 0
    consistent_binary = 0
    total = 0
    inconsistent = {}
    plot_incorrect = []
    plot_inconsistent = []
    plot_names = []
    for fname in os.listdir(directory):
        if fname.startswith("result_") and fname.endswith(".csv"):
            idx = int(fname.split("_")[1].split(".")[0])
            fname = os.path.join(directory, fname)
            
            results = []
            with open(fname, 'r') as data:
                csv_reader = csv.DictReader(data)

                for row in csv_reader:
                    results.append(row)
            
            acc = accumulate_results(results)
            
            correct += acc[0]
            consistent += acc[1]
            consistent_binary += acc[2]
            total += acc[3]
            for i in acc[4]:
                if i not in inconsistent:
                    inconsistent[i] = 0
                inconsistent[i] += acc[4][i]
            
            print(fname)
            print(PROMPTS[idx][0])
            print(f"   incorrect: {acc[3]*3 - acc[0]}/{acc[3]*3}  ({100-acc[0]*100.0/(acc[3]*3)}%)")
            print(f"   inconsistent: {acc[3] - acc[1]}/{acc[3]}  ({100-acc[1]*100.0/acc[3]}%)")
            print(f"   inconsistent (binary): {acc[3]- acc[2]}/{acc[3]}  ({100-acc[2]*100.0/acc[3]}%)")
            print(topk(acc[4], 10))
            print()
            print(f"{PROMPTS[idx][3]} & {version} & ${f(100-acc[0]*100.0/(acc[3]*3))}\\%$ & ${f(100-acc[1]*100.0/acc[3])}\\%$ & $ {f(100-acc[2]*100.0/acc[3])}\\%$ \\\\\\hline", file=log)
            plot_names.append(PROMPTS[idx][3])
            plot_incorrect.append(1-acc[0]*1.0/(acc[3]*3.0))
            plot_inconsistent.append(1-acc[1]*1.0/acc[3])
            
    print("summary:")
    print(f"   incorrect: {total*3 - correct}/{total*3}  ({100-correct*100.0/(total*3)}%)")
    print(f"   inconsistent: {total - consistent}/{total}  ({100-consistent*100.0/total}%)")
    print(f"   inconsistent (binary): {total- consistent_binary}/{total}  ({100-consistent_binary*100.0/total}%)")
    print(topk(inconsistent, 20))
    
    return (plot_names, plot_inconsistent, plot_incorrect)
            
            

if __name__ == "__main__":
    ind = np.arange(len(PROMPTS))
    width = 0.35
    fig, ax = plt.subplots()
    barnames = [ "ChatGPT 3.5", "ChatGPT 4o"]
    bars = []
    i = 0
    for dir in ["chatgpt_3.5_many", "chatgpt_4o_many"]:
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