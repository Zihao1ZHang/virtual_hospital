import os
import json

from langchain.chains.llm import LLMChain
from langchain_core.prompts import load_prompt
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI

from tools import patient_agent, doctor_agent
import tqdm
# loop over all the folders in data_virtual_hospital

gpt4o = "gpt-4o"
max_iter = 30
self_critic = True


def assistant(patient_info: str):
    """
        Tool that calls a chain to find the appropriate physical examinations,
            valid parameter include "patient_info": patient's background
        """
    prompt = load_prompt("prompts/Virtual_hospital/physical_exam.yaml")

    llm = ChatOpenAI(model_name=gpt4o, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"info": patient_info})
    return response["text"]


def compare(exams: str, gt: str):
    """
        Tool that calls a chain to find the appropriate physical examinations,
            valid parameter include "patient_info": patient's background
        """
    prompt = load_prompt("prompts/Virtual_hospital_eval/physical_exam_eval.yaml")

    llm = ChatOpenAI(model_name=gpt4o, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"exams": exams, "gt": gt})
    return response["text"]


if __name__ == "__main__":

    root_dir = "./data/virtual_hospital/MIMIC_Patient_Actor"
    # list = os.listdir(root_dir)
    assistant_ = StructuredTool.from_function(assistant)
    compare_ = StructuredTool.from_function(compare)

    for file in os.listdir(root_dir):
        print(file)
        with open(f"{root_dir}/{file}") as json_file:
            data = json.load(json_file)
            json_file.close()

        doctor_info = (f"Patient's Age: {data['Doctor_Actor']['Age']},"
                       f"Patient's Gender: {data['Doctor_Actor']['Gender']},"
                       f"Reason for Visit: {data['Doctor_Actor']['Reason_for_visit']}"
                       
                       f"Vital Signs: {data['Patient_Actor']['Vital_Signs']}"
                       f"Review of Systems: {data['Patient_Actor']['Review_of_Systems']} "
                       f"Chief_Complaint: {data['Patient_Actor']['Chief_Complaint']}"
                       f"History of Present Illness: {data['Patient_Actor']['HPI']}"
                       f"24 Hour events: {data['Patient_Actor']['24_Hour_Event']}"
                       f"Allergies: {data['Patient_Actor']['Allergies']}"
                       f"Past Medical_History: {data['Patient_Actor']['Past_Medical_History']}"
                       f"Current Medical: {data['Patient_Actor']['Current_Medical']}"
                       f"Family History: {data['Patient_Actor']['Family_History']}"
                       f"Social History: {data['Patient_Actor']['Social_History']}"
                       )

        ground_truth = f"Physical Examination Findings: {data['Patient_Actor']['Physical_Examination_Findings']}"

        physical_exams_res = assistant_.run({"patient_info": doctor_info})


        physical_exams_eval = compare_.run({"exams": physical_exams_res, "gt": ground_truth})



        # save outputs to file
        if not os.path.exists(f"output/MIMIC/physical_exam"):
            os.mkdir(f"output/MIMIC/physical_exam")

        with open(f"output/MIMIC/physical_exam/{file[:-4]}txt", "w") as f:
            f.write(f"{physical_exams_res} \n\n Ground Truth:\n {ground_truth} \n\n Results:\n {physical_exams_eval}")
