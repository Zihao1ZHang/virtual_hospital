import os
import re
from datetime import datetime
import dotenv
import json
import numpy as np

# a set of evaluation functions
from langchain.prompts import load_prompt
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from tools import extract_json_data, read_file, save_result


def run_model(prompt_path, model_name, input_data):
    prompt = load_prompt(prompt_path)
    llm = ChatOpenAI(model_name=model_name, temperature=0)

    eval_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
    )

    result = eval_chain.invoke(input_data)

    return result["text"]


def assessment(case, model_name):
    hpi_path = f"data/data_virtual_hospital/{case}/modified/2_physician/HPI.txt"
    exams_path = f"data/data_virtual_hospital/{case}/modified/2_physician/exams.txt"

    # extract the generated conversation and target conversation
    hpi = read_file(hpi_path)
    exams = read_file(exams_path)

    result = run_model(
        "prompts/diagnosis.yaml",
        model_name=model_name,
        input_data={"hpi": hpi, "exams": exams},
    )

    result_dict = extract_json_data(result)
    diagnosis_json = result_dict

    output = ""
    index = 1
    for key in diagnosis_json.keys():
        output += (
            "Diagnosis #" + str(index) + ": " + diagnosis_json[key]["diagnosis"] + "\n"
        )
        output += "Historical Finding(s): \n"
        if type(diagnosis_json[key]["Historical Findings"]) == str:
            output += "N/A \n"
        else:
            for hist_finding in diagnosis_json[key]["Historical Findings"]:
                output += hist_finding + "\n"
        output += "\n"

        output += "Historical reasons: \n"
        if type(diagnosis_json[key]["Historical reasons"]) == str:
            output += "N/A \n"
        else:
            for hist_finding in diagnosis_json[key]["Historical reasons"]:
                output += hist_finding + "\n"
        output += "\n"

        output += "Physical Exam Finding(s): \n"
        if type(diagnosis_json[key]["Physical exam data"]) == str:
            output += "N/A \n"
        else:
            for hist_finding in diagnosis_json[key]["Physical exam data"]:
                output += hist_finding + "\n"
        output += "\n"

        output += "Physical exam data reasons: \n"
        if type(diagnosis_json[key]["Physical exam data reasons"]) == str:
            output += "N/A \n"
        else:
            for hist_finding in diagnosis_json[key]["Physical exam data reasons"]:
                output += hist_finding + "\n"
        output += "\n\n"
        index += 1

    output_dir = f"output/assessment/{model_name}"
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    output_path = f"{output_dir}/{case}-{curr_time}.txt"
    save_result(output_path, output)

    print(json.dumps(result_dict, indent=2))

    print("\n\n")


def assessment_eval(case, model_name, assessment_model):
    pred_path = f"output/assessment/{assessment_model}/{case}.txt"
    target_path = f"data/data_virtual_hospital/{case}/modified/2_physician/assessment.txt"

    # extract the generated conversation and target conversation
    pred = read_file(pred_path)
    target = read_file(target_path)

    result = run_model(
        "prompts/diagnosis_eval.yaml",
        model_name=model_name,
        input_data={"pred": pred, "target": target},
    )

    result_dict = extract_json_data(result)

    output_dir = f"output/assessment_eval/{assessment_model}"
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    output_path = f"{output_dir}/{case}-{curr_time}.txt"
    save_result(output_path, json.dumps(result_dict, indent=2))

    print(json.dumps(result_dict, indent=2))

    print("\n\n")


if __name__ == "__main__":
    dotenv.load_dotenv()

    gpt4 = "gpt-4-1106-preview"
    gpt4_turbo = "gpt-4-turbo-preview"
    model_name = gpt4_turbo
    cases = [int(case) for case in os.listdir("data/data_virtual_hospital")]
    cases.sort()

    curr_time = datetime.now().strftime("%m-%d-%H-%M")
    for case in cases[:1]:
        print(f"case: {case}")
        # assessment(case, model_name)
        assessment_eval(case, model_name, assessment_model=gpt4_turbo)
