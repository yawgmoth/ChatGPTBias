import many_prompts
import get_response
import parse_response
import evaluate_results
import argparse
import os


def main(directory, phases=["make", "get", "parse", "evaluate"], n=5, m=10, force=False, df=None, model="gpt-3.5-turbo-0125", mname="ChatGPT 3.5"):
    if "make" in phases:
        many_prompts.main(directory, n, m, df)
    if "get" in phases:
        get_response.main(directory, force, model)
    if "parse" in phases:
        parse_response.main(directory)
    if "evaluate" in phases:
        evaluate_results.main(directory, mname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='ChatGPT Evaluation Pipeline',
                    description='Generate prompts, get ChatGPT responses, parse response, evaluate results; by default all phases are run, but if any phase is explicitly provided on the command line, only the provided phases are run.')
    parser.add_argument("-n", "--count", default=5, type=int, dest="count", help="How many prompts to generate (phase: make)")
    parser.add_argument("-r", "--repetitions", default=10, type=int, dest="reps", help="How many repetitions of each prompt to generate (phase: make)")
    parser.add_argument("-m", "--make", help="Run the 'make' phase.", dest="make", action="store_true")
    parser.add_argument("-g", "--get", help="Run the 'get' phase.", dest="get", action="store_true")
    parser.add_argument("-p", "--parse", help="Run the 'parse' phase.", dest="parse", action="store_true")
    parser.add_argument("-e", "--evaluate", help="Run the 'evaluate' phase.", dest="evaluate", action="store_true")
    parser.add_argument("-4", "--chatgpt-4", help="Use ChatGPT version 4", dest="v4", action="store_true")
    parser.add_argument("-o", "--chatgpt-4o", help="Use ChatGPT version 4o", dest="v4o", action="store_true")
    parser.add_argument("-f", "--force", help="Overwrite prompt response files if they already exist.", dest="force", action="store_true")
    parser.add_argument("-d", "--data", help="Which data file to use.", dest="data", action="store")
    phases = []
    args = parser.parse_args()
    if args.make:
        phases.append("make")
    if args.get:
        phases.append("get")
    if args.parse:
        phases.append("parse")
    if args.evaluate:
        phases.append("evaluate")
    if not phases:
        phases = ["make", "get", "parse", "evaluate"]
    
    directory = "chatgpt_3.5"
    model = "gpt-3.5-turbo-0125"
    mname = "ChatGPT 3.5"
    if args.v4:
        directory = "chatgpt_4"
        model = "gpt-4"
        mname = "ChatGPT 4"
    if args.v4o:
        directory = "chatgpt_4o"
        model = "gpt-4o"
        mname = "ChatGPT 4o"
    if args.data:
        directory += "_" + os.path.basename(args.data).split(".")[0]
    else: 
        directory += "_many"
    if not os.path.exists(directory):
        os.makedirs(directory)
    main(directory, phases, args.count, args.reps, args.force, args.data, model, mname)