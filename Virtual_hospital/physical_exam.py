from langchain.tools import StructuredTool
from tools import *

if __name__ == "__main__":

    opening_path = "D:/projects/virtual_hospital/data/23/opening.txt"
    with open(opening_path, "r") as f:
        opening = f.read()
    # QA_path = "USMLE_txt/QA/case" + str(i) + ".txt"
    # with open(QA_path, "r") as f:
    #     QA = f.read()
    QA = ""
    physical = StructuredTool.from_function(physical_func)
    input = {"opening": opening, "chat_history": QA}
    physical_exams = physical.run(input)
    physical_exams_json = json.loads(physical_exams)
    output = ""
    for key in physical_exams_json.keys():
        output += physical_exams_json[key]['physical exam'] + ": " + physical_exams_json[key]['maneuver'] + "\n"
        output += "reason: " + physical_exams_json[key]['reason'] + "\n"

    output_path = "D:/projects/virtual_hospital/data/23/physical_exam.txt"
    with open (output_path, "w") as f:
        f.write(output)


