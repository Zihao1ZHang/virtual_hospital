from langchain.tools import StructuredTool
import json
from tools import *
import os

api_key = "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"

if __name__ == "__main__":
    for i in range(1, 45):
        if i == 32:
            continue
        print(i)
        opening_path = "USMLE_txt/opening/case" + str(i) + ".txt"
        with open(opening_path, "r") as f:
            opening = f.read()
        QA_path = "USMLE_txt/QA/case" + str(i) + ".txt"
        with open(QA_path, "r") as f:
            QA = f.read()

        physical = StructuredTool.from_function(physical_func)
        input = {"opening": opening, "chat_history": QA}
        physical_exams = physical.run(input)
        physical_exams_json = json.loads(physical_exams)
        output = ""
        for key in physical_exams_json.keys():
            output += physical_exams_json[key]['physical exam'] + ": " + physical_exams_json[key]['maneuver'] + "\n"
            output += "reason: " + physical_exams_json[key]['reason'] + "\n"

        output_path = "output/physical_wo_example/case" + str(i) + ".txt"
        with open (output_path, "w") as f:
            f.write(output)


