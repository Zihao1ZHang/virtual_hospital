import os
from tools import patient_agent, doctor_agent

# loop over all the folders in data_virtual_hospital

cases = [case for case in os.listdir("data/data_virtual_hospital")]
max_iter = 20


for case in cases:
    file_content = ""
    print("Running case ", case)
    with open(f"data/data_virtual_hospital/{case}/modified/2_physician/HPI.txt", "r") as f:
        hpi = f.read()

    chat_history = ""
    for i in range(max_iter):

        doctor_question = doctor_agent(
            chat_history=chat_history, model_name="gpt-4-1106-preview"
        )

        # print(doctor_question)

        print("Doctor:", doctor_question["question"])
        file_content += "Turn: " + str(i) + "\n"
        file_content += f"Doctor: {doctor_question['question']}\n"

        patient_response = patient_agent(
            hpi=hpi,
            chat_history=chat_history,
            question=doctor_question,
            model_name="gpt-4-turbo-preview",
        )
        print("Patient:", patient_response["response"], "\n")

        file_content += f"Patient: {patient_response['response']}\n"

        chat_history += f"Doctor: {doctor_question['question']}\nPatient: {patient_response['response']}\n"


    with open(f"output/QA/{case}.txt", "w") as f:
        f.write(file_content)
