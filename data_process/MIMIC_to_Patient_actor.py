import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from langchain_core.prompts import load_prompt

from tools import patient_agent, doctor_agent
from langchain.prompts import load_prompt
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json
import re
import pandas as pd

# loop over all the folders in data_virtual_hospital

max_iter = 30

def summarize(info: str, model_name: str):
    prompt = load_prompt("MIMIC_to_Patient_actor.yaml")
    llm = ChatOpenAI(model_name=model_name, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"information": info})
    return response


if __name__ == "__main__":
    file_name = "../data/virtual_hospital/MIMIC_unique_notes.json"
    with open(file_name, "r") as f:
        data = json.load(f)


    counter = 0
    previous_id = 0
    iter = 0
    for note in data:
        # HADM_ID = str(row['ROW_ID'])
        SUBJECT_ID = note['SUBJECT_ID']
        ROW_ID = note['ROW_ID']
        output_name = f"{SUBJECT_ID}_{ROW_ID}"

        counter = 0
        # while os.path.isfile(f"../data/virtual_hospital/MIMIC_Modified/{output_name}.json"):
        #     if '_' in HADM_ID:
        #         HADM_ID = HADM_ID.split('_')[0]
        #         counter += 1
        #     HADM_ID = f"{HADM_ID}_{counter}"


        # if previous_id == HADM_ID:
        #     previous_id = HADM_ID
        #     HADM_ID = f"{HADM_ID}_{counter}"
        #     counter += 1
        # else:
        #     previous_id = HADM_ID
        #     counter = 0


        if os.path.isfile(f"../data/virtual_hospital/MIMIC_Modified/{output_name}.json"):
            continue
        input = note['s_and_o']

        for i in range(10):
            try:
                summary = summarize(
                    info=input,
                    model_name="gpt-4o-mini"
                )

                if type(summary) is not str:
                    summary = summary['text']

                if summary[0] == '`':
                    summary = summary[7:-3]
                summary_json = json.loads(summary)
                output_path = f"../data/virtual_hospital/MIMIC_Modified/{output_name}.json"
                with open(output_path, "w") as f:
                    json.dump(summary_json, f)
            except:
                pass

        iter += 1
        print(f"{len(os.listdir('../data/virtual_hospital/MIMIC_Modified'))}/5074: {output_name}")
        if len(os.listdir('../data/virtual_hospital/MIMIC_Modified')) == 5074:
            break

