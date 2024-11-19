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


def assistant(chat_history: str, patient_info: str):
    """
        Tool that calls a chain to find the missing information,
            valid parameter include "chat_history": chat_history, "patient_info": patient's background
        """
    prompt = load_prompt("prompts/Virtual_hospital/Conversation_self_critic.yaml")

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"chat_history": chat_history, "patient_info": patient_info})
    return response["text"]


if __name__ == "__main__":

    # root_dir = "./data/virtual_hospital/MIMIC_Modified2"
    # list = os.listdir(root_dir)
    
    with open("data/virtual_hospital/MIMIC_Modified.json", "r") as f:
        notes = json.load(f) 
    assistant_ = StructuredTool.from_function(assistant)
    
    counter = 0

    for data in notes:
        ROW_ID = data['ROW_ID']
        SUBJECT_ID = data['SUBJECT_ID']
        output_filename = f"{SUBJECT_ID}_{ROW_ID}.txt"
        
        if os.path.exists(f"output/MIMIC/Conversation_0925/{output_filename}"):
            continue
        # print(f"{len(os.listdir('output/MIMIC/Conversation2'))}/{len(os.listdir(root_dir))}: {file}")
        # with open(f"{root_dir}/{file}") as json_file:
        #     data = json.load(json_file)
        #     json_file.close()
        try:
            doctor_info = (f"Patient's Age: {data['Doctor_Actor']['Age']},"
                        f"Patient's Gender: {data['Doctor_Actor']['Gender']},"
                        f"Reason for Visit: {data['Doctor_Actor']['Reason_for_visit']}"
                        f"Physical Examination Findings: {data['Patient_Actor']['Physical_Examination_Findings']}"
                        f"Vital Signs: {data['Patient_Actor']['Vital_Signs']}"
                        f"Review of Systems: {data['Patient_Actor']['Review_of_Systems']} "
                        )
        except:
            doctor_info = (f"Patient's Age: {data['Doctor_Actor']['Age']},"
                        f"Patient's Gender: {data['Doctor_Actor']['Gender']},"
                        f"Reason for Visit: {data['Doctor_Actor']['Reason_for_visit']}"
                        f"Physical Examination Findings: {data['Patient_Actor']['Physical_Examination_Findings']}"
                        # f"Vital Signs: {data['Patient_Actor']['Vital_Signs']}"
                        f"Review of Systems: {data['Patient_Actor']['Review_of_Systems']} "
                        )
        patient_info = "".join(f"Patient's {key}: {data['Patient_Actor'][key]}," for key in data['Patient_Actor'].keys())

        # try:
        #     patient_info = (f"Chief_Complaint: {data['Patient_Actor']['Chief_Complaint']}"
        #                     f"History of Present Illness: {data['Patient_Actor']['HPI']}"
        #                     f"24 Hour events: {data['Patient_Actor']['24_Hour_Event']}"
        #                     f"Allergies: {data['Patient_Actor']['Allergies']}"
        #                     f"Past Medical_History: {data['Patient_Actor']['Past_Medical_History']}"
        #                     f"Current Medical: {data['Patient_Actor']['Current_Medical']}"
        #                     f"Family History: {data['Patient_Actor']['Family_History']}"
        #                     f"Social History: {data['Patient_Actor']['Social_History']}"
        #                     f"Physical Examination Findings: {data['Patient_Actor']['Physical_Examination_Findings']}"
        #                     f"Vital Signs: {data['Patient_Actor']['Vital_Signs']}"
        #                     f"Review of Systems: {data['Patient_Actor']['Review_of_Systems']}"
        #                     )
        # except:
        #     patient_info = (f"Chief_Complaint: {data['Patient_Actor']['Chief_Complaint']}"
        #                     f"History of Present Illness: {data['Patient_Actor']['HPI']}"
        #                     f"Allergies: {data['Patient_Actor']['Allergies']}"
        #                     f"Past Medical_History: {data['Patient_Actor']['Past_Medical_History']}"
        #                     f"Current Medical: {data['Patient_Actor']['Current_Medical']}"
        #                     f"Family History: {data['Patient_Actor']['Family_History']}"
        #                     f"Social History: {data['Patient_Actor']['Social_History']}"
        #                     f"Physical Examination Findings: {data['Patient_Actor']['Physical_Examination_Findings']}"
        #                     f"Vital Signs: {data['Patient_Actor']['Vital_Signs']}"
        #                     f"Review of Systems: {data['Patient_Actor']['Review_of_Systems']}"
        #                     )
            

        chat_history = ""
        file_content = ""
        for i in range(max_iter):

            for iteration in range(10):
                try:
                    if self_critic:
                        note = assistant_.run({"chat_history": chat_history, "patient_info": doctor_info})
                        chat_history_input = f"{chat_history} \n Notes:{note} is missing"
                    chat_history_input = chat_history

                    # print(f"Turn: {i}")
                    doctor_question = doctor_agent(
                        chat_history=chat_history_input,
                        info=doctor_info,
                        model_name="gpt-4o-mini"
                    )

                    # print(doctor_question)

                    # print("Doctor:", doctor_question["question"])
                    file_content += "Turn: " + str(i) + "\n"
                    file_content += f"Doctor: {doctor_question['question']}\n"

                    patient_response = patient_agent(
                        hpi=patient_info,
                        chat_history=chat_history,
                        question=doctor_question,
                        model_name="gpt-4o-mini",
                    )
                    # print("Patient:", patient_response["response"], "\n")
                    file_content += f"Patient: {patient_response['response']}\n"

                    break
                except:
                    pass

            chat_history += f"Doctor: {doctor_question['question']}\nPatient: {patient_response['response']}\n"




        # save outputs to file
        if not os.path.exists(f"output/MIMIC/Conversation_0925"):
            os.mkdir(f"output/MIMIC/Conversation_0925")

        with open(f"output/MIMIC/Conversation_0925/{output_filename}", "w") as f:
            f.write(chat_history)

        print(f"{len(os.listdir(f'output/MIMIC/Conversation_0925'))}/5074: {output_filename}")
        