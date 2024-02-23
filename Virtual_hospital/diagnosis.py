from langchain.tools import StructuredTool
from tools import *

if __name__ == "__main__":

    opening_path = "D:/projects/virtual_hospital/data/23/opening.txt"
    with open(opening_path, "r") as f:
        opening = f.read()
    physical_exam_path = "D:/projects/virtual_hospital/data/23/physical_exam.txt"
    with open(physical_exam_path, "r") as f:
        physical_exam = f.read()

    input = {"opening": opening + physical_exam}

    diagnosis_tool = StructuredTool.from_function(diagnosis_func)
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

    output_path = "D:/projects/virtual_hospital/data/23/diagnosis.txt"
    with open (output_path, "w") as f:
        f.write(output)


