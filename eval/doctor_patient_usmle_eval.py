import os
from json import JSONDecodeError

from langchain_core.prompts import load_prompt

from tools import patient_agent, doctor_agent
from langchain.prompts import load_prompt
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json
import re

# loop over all the folders in data_virtual_hospital

cases = [case for case in os.listdir("../data/USMLE/cases")]
max_iter = 20

def eval(info: str, model_name: str):
    prompt = load_prompt("../prompts/Virtual_hospital_eval/QA_eval_write_physician_note.yaml")

    llm = ChatOpenAI(model_name=model_name, temperature=0.5)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"chat_history": info})
    return response


if __name__ == "__main__":
    output = ""
    for i in range(1, 45):
    # for case in cases:
    #     if '32' in case:
    #         continue
        if i == 32:
            continue
        file_content = ""
        print("Running case ", f"case{i}")
        # with open(f"../output/doctor_patient_usmle_physical_exams/{case}", "r") as f:
        #     info = f.read()

        # filename = f"../data/USMLE/gt/QA/case{i}.txt"
        filename = f"../output/doctor_patient_usmle_physical_exams/case{i}.txt"
        with open(filename, "r") as f:
            info = f.read()

        res = eval(
            info=info,
            model_name="gpt-4-1106-preview"
        )['text']

        if res[0] == "`":
            res = res[7: -4]

        res_json = json.loads(res)



        output += f"Case{i} : Score: {res_json['Final_Score']}, Unsatisfied metrics: {res_json['Unsatisfied_Cases']}\n"


        with open(f"../output/eval/doctor_patient_usmle_physical_exams.txt", "w") as f:
            f.write(output)

