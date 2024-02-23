from langchain.tools import StructuredTool
import json
from tools import *
import os
import pandas as pd
import numpy as np
from pyspark.sql.functions import col

if __name__ == "__main__":
    # get the list of patient with physician notes
    data = pd.read_csv("../data/NOTEEVENTS.csv", index_col=0)
    cate = np.unique(list(data["CATEGORY"]))

    data1 = data.loc[data["CATEGORY"] == 'Physician ']
    patients_list = np.unique(list(data1['SUBJECT_ID']))
    print(patients_list[0:15])
    # filtered_patient = data[data.SUBJECT_ID.isin(patients_list)]
    print(1)

    # extract patient's data
    patients_list = [23, 109, 111, 124, 188, 199, 222, 249, 291, 305, 329, 357, 384, 402, 406]
    for patient in patients_list:
        patient_data = data.loc[data["SUBJECT_ID"] == patient]
        prev_date = patient_data["CHARTDATE"].iloc[0]
        counter = 0
        start = True
        for index, row in patient_data.iterrows():
            text = row["TEXT"]
            if prev_date != row["CHARTDATE"] or start:
                time = row["CHARTDATE"]
                start = False
                counter = 0
            else:
                counter += 1
                time = row["CHARTDATE"] + "_" + str(counter)
            # time = row["CHARTDATE"] if prev_date != row["CHARTDATE"] else str(row["CHARTDATE"]) + str(row["CHARTTIME"])
            prev_date = row["CHARTDATE"]
            if not os.path.isdir("data/" + str(patient)):
                os.mkdir("data/" + str(patient))
            if not os.path.isdir("data/" + str(patient) + "/" + str(row["HADM_ID"])):
                os.mkdir("data/" + str(patient) + "/" + str(row["HADM_ID"]))
            cate_name = row["CATEGORY"].replace("/", "_")
            text_file = open("data/" + str(patient) + "/" + str(row["HADM_ID"]) + "/" + time + "_" + cate_name + str(".txt"), "w")
            text_file.write(text)
            text_file.close()

    # load file into time order
    # data = pd.read_csv("data/4.csv", index_col=0)
    # prev_date = data["CHARTDATE"].iloc[0]
    # counter = 0
    # start = True
    # for index, row in data.iterrows():
    #     text = row["TEXT"]
    #     if prev_date != row["CHARTDATE"] or start:
    #         time = row["CHARTDATE"]
    #         start = False
    #         counter = 0
    #     else:
    #         counter += 1
    #         time = row["CHARTDATE"] + "_" + str(counter)
    #     # time = row["CHARTDATE"] if prev_date != row["CHARTDATE"] else str(row["CHARTDATE"]) + str(row["CHARTTIME"])
    #     prev_date = row["CHARTDATE"]
    #     text_file = open("data/4/" + time + str(".txt"), "w")
    #     text_file.write(text)
    #     text_file.close()
    #
    # print(1)
    # patient_list = [3, 4]
    #
    # for patient in patient_list:
    #     data = pd.read_csv("data/" + str(patient) + ".csv")
    #     data = data.sort_values(['CHARTDATE'])
    #     data.to_csv("data/" + str(patient) + ".csv")
    #     print(1)
    #    # filtered_patient = data[data.SUBJECT_ID.isin([patient])]
    #     # filtered_patient.to_csv("data/" + str(patient) + ".csv")
    # # data = pd.read_csv("data/NOTEEVENTS.csv")
    # # data = pd.read_csv("data/NOTEEVENTS.csv")
    # # patient_list = [2, 3, 4]
    # # filtered_patient = data[data.SUBJECT_ID.isin(patient_list)]
    # # filtered_patient.to_csv("filtered.csv")
    # # data.to_csv("data/lite.csv")
    # # patient_id = data['SUBJECT_ID'].tolist()
    # #
    # # patient_id = np.array(patient_id)
    # # patient_id_unique = np.unique(patient_id)
    # # print(1)