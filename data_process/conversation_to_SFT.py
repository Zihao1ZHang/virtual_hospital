import json
import os
from tqdm import tqdm
import pandas as pd

if __name__ == "__main__":


    # Initialize an empty DataFrame with columns 'prompts' and 'completion'
    df = pd.DataFrame(columns=['prompt', 'completion'])

    with open(f"data/virtual_hospital/MIMIC_update_1007.json", 'r') as f:
        physician_notes = json.load(f)

    with open("data_process/SFT_dataset_utils/InfoGatherQA_instruction.txt", 'r') as f:
        instruction_template = f.read()
    # print(instruction)
    instruction = instruction_template.replace("<info>", "Patient's information").replace("<chat_history>", "How's your feeling?")
    # print(instruction)

    conversation_size = len(os.listdir("data/virtual_hospital/conversation"))
    downsample_ratio = 0.1
    sample_size = int(conversation_size * downsample_ratio)
    iter = 0
    for filename in tqdm(os.listdir("data/virtual_hospital/conversation"), desc="Processing files"):
        if iter > sample_size:
            break
        iter += 1
        # get the conversation data
        with open(f"data/virtual_hospital/conversation/{filename}", 'r', encoding="ISO-8859-1") as f:
            conversation = f.read()

        # get patient's information
        filename = filename[:-4]
        ROW_ID = filename.split("_")[1]
        SUBJECT_ID = filename.split("_")[0]
        id = f"{SUBJECT_ID}_{ROW_ID}"

        patient_info = str(physician_notes[id]['Doctor_Actor'])
        instruction_template = instruction_template.replace("<info>", patient_info)
        iterations = conversation.split("\n")
    

        conversations = ""
        for i in range(0, len(iterations), 2):
            instruction = instruction_template.replace("<chat_history>", conversations)

            if "Doctor" in iterations[i]:
                output = iterations[i]
                new_row = pd.DataFrame([[instruction, output.replace("Doctor: ", "")]], columns=['prompt', 'completion'])
                df = pd.concat([df, new_row], ignore_index=True)
            else: 
                # print(f"break at {i} th iteration Due to missing doctor")
                # print(iterations[i])

                break
            
            if i+1 < len(iterations)-1 and "Doctor" in iterations[i] and "Patient" in iterations[i+1]:
                conversations += f"{iterations[i]}\n"
                conversations += f"{iterations[i+1]}\n"
            else:
                # print(f"break at {i} th iteration")
                break
    df.to_csv('data/SFT_dataset/conversation_0.1.csv')


