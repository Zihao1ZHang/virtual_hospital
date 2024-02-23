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
        closure_path = "USMLE_txt/pre_closure/case" + str(i) + ".txt"
        with open(QA_path, "r") as f:
            closure_input = f.read()
        closure = StructuredTool.from_function(closure_func)
        input = {"opening": opening, "chat_history": QA, "pre_closure": closure_input}
        closure_output = closure.run(input)


        output_path = "output/closure/case" + str(i) + ".txt"
        with open (output_path, "w") as f:
            f.write(closure_output)


