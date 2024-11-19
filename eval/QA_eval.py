import os
from langchain_core.prompts import load_prompt

from tools import patient_agent, doctor_agent
from langchain.prompts import load_prompt
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json
import re
import pandas as pd


def write_physician_note(info: str, conversation: str, model_name: str):
    prompt = load_prompt("../prompts/Virtual_hospital_eval/QA_eval_write_physician_note.yaml")

    llm = ChatOpenAI(model_name=model_name, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"info": info, "conversation": conversation})
    return response


def Compare(note: str, gt: str, model_name: str):
    prompt = load_prompt("../prompts/Virtual_hospital_eval/QA_eval_compare.yaml")

    llm = ChatOpenAI(model_name=model_name, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"physician_note": note, "gt": gt})
    return response

if __name__ == "__main__":
    root_dir = "../output/MIMIC/Conversation_LTSBT/"
    basicInfo_dir = "../data/virtual_hospital/MIMIC_Patient_Actor"

    file_name = "../data/virtual_hospital/orginal_VP_data/physician.csv"
    physician_notes = pd.read_csv(file_name)

    root_list = ["Setting1",
                 "Setting2/",
                 "Setting3/",
                 "SelfCritic_Setting1/",
                 "SelfCritic_Setting2/",
                 "SelfCritic_Setting3/"]
    for root in root_list:
        print(root)
        root_dir = f"../output/MIMIC/Conversation_{root}"
        for file in os.listdir(root_dir):
            print(file)
            # if file == "316237.txt":
            #     continue
            with open(f"{root_dir}/{file}", "r") as f:
                conversation = f.read()

            with open(f"{basicInfo_dir}/{file[:-4]}.json") as json_file:
                data = json.load(json_file)
                json_file.close()
            #
            # doctor_info = (f"Patient's Age: {data['Doctor_Actor']['Age']},"
            #                f"Patient's Gender: {data['Doctor_Actor']['Gender']},"
            #                f"Reason for Visit: {data['Doctor_Actor']['Reason_for_visit']}"
            #                f"Vital Signs: {data['Patient_Actor']['Vital_Signs']}"
            #                f"Physical Examination Findings: {data['Patient_Actor']['Physical_Examination_Findings']}"
            #                f"Review of Systems: {data['Patient_Actor']['Review_of_Systems']}")
            #
            # physician_note_llm = write_physician_note(
            #     info=doctor_info,
            #     conversation=conversation,
            #     model_name="gpt-4o"
            # )
            #
            # if not os.path.exists(f"../output/eval/{root}/"):
            #     os.mkdir(f"../output/eval/{root}/")
            # with open(f"../output/eval/{root}/{file}", "w") as f:
            #     f.write(physician_note_llm['text'])

            gt = physician_notes[physician_notes['ROW_ID'] == int(file[:-4])]['TEXT'].iloc[0]
            # score = Compare(
            #     note=physician_note_llm['text'],
            #     gt=gt,
            #     model_name="gpt-4o"
            # )
            # if type(score) is not str:
            #     score = score['text']
            # if score[0] == '`':
            #     score = score[7:-4]
            # # score_json = json.loads(score)
            # with open(f"../output/eval/{root}/Score_{file}", "w") as f:
            #     f.write(score)

            with open(f"../output/eval/{root}/GT_{file}", "w") as f:
                f.write(gt)



