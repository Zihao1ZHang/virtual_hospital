import os

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

def summarize(info: str, model_name: str):
    prompt = load_prompt("USMLE_to_Patient_actor.yaml")

    llm = ChatOpenAI(model_name=model_name, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"information": info})
    return response


if __name__ == "__main__":
    for case in cases:
        if '32' in case:
            continue

        file_content = ""
        print("Running case ", case)
        with open(f"../data/USMLE/cases/{case}", "r") as f:
            info = f.read()

        summary = summarize(
            info=info,
            model_name="gpt-4-1106-preview"
        )


        with open(f"../data/USMLE/patient_info1/{case}", "w") as f:
            f.write(summary['text'])

