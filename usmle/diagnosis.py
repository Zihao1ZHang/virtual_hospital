from langchain.tools import StructuredTool
import json
from tools import *
import os


if __name__ == "__main__":
    for case in range(26, 45):
        if case == 32:
            continue
        print("case" + str(case))
        opening_path = "USMLE_txt/diagnosis_input/case" + str(case) + ".txt"
        with open(opening_path, "r") as f:
            opening = f.read()

        diagnosis_tool = StructuredTool.from_function(diagnosis_func)



        input = {"opening": opening}
        diagnosis = diagnosis_tool.run(input)
        diagnosis_json = json.loads(diagnosis)

        output = ""
        index = 1
        for key in diagnosis_json.keys():
            output += "Diagnosis #" + str(index) + ": " + diagnosis_json[key]['diagnosis'] + "\n"
            output += "Historical Finding(s): \n"
            if type(diagnosis_json[key]['Historical Findings']) == str:
                output += "N/A \n"
            else:
                for hist_finding in diagnosis_json[key]['Historical Findings']:
                    output += hist_finding + "\n"
            output += "\n"

            output += "Historical reasons: \n"
            if type(diagnosis_json[key]['Historical reasons']) == str:
                output += "N/A \n"
            else:
                for hist_finding in diagnosis_json[key]['Historical reasons']:
                    output += hist_finding + "\n"
            output += "\n"

            output += "Physical Exam Finding(s): \n"
            if type(diagnosis_json[key]['Physical exam data']) == str:
                output += "N/A \n"
            else:
                for hist_finding in diagnosis_json[key]['Physical exam data']:
                    output += hist_finding + "\n"
            output += "\n"

            output += "Physical exam data reasons: \n"
            if type(diagnosis_json[key]['Physical exam data reasons']) == str:
                output += "N/A \n"
            else:
                for hist_finding in diagnosis_json[key]['Physical exam data reasons']:
                    output += hist_finding + "\n"
            output += "\n\n"
            index += 1

        output_path = "output/diagnosis/case" + str(case) + ".txt"
        with open(output_path, "w") as f:
            f.write(output)



