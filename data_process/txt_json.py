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

if __name__ == "__main__":
    for case in cases:
        # if '32' in case or os.path.exists(f"../data/USMLE/patient_info_json/{case[:-4]}.json"):
        #     continue
        if '32' in case:
            continue
        file_content = ""
        print("Running case ", case)
        with open(f"../data/USMLE/patient_info1/{case}", "r") as f:
            info = f.read()
        info_json = json.loads(info)
        with open(f"../data/USMLE/patient_info_json/{case[:-4]}.json", "w") as f:
            json.dump(info_json, f)
