from langchain.tools import StructuredTool
import json
from tools import *
import os


if __name__ == "__main__":

    for case in range(33, 45):
        print("case" + str(case))
        opening_path = "USMLE_txt/opening/case" + str(case) + ".txt"
        with open(opening_path, "r") as f:
            opening = f.read()
        chat_history_path = "USMLE_txt/QA_mark/case" + str(case) + ".txt"
        with open(chat_history_path, "r") as f:
            chat_history = f.read()
        QA = StructuredTool.from_function(QA_func)

        conversations = chat_history.split("#")

        if not os.path.exists("output/QA/case" + str(case)):
            os.mkdir("output/QA/case" + str(case))
        chat_history = ""
        turn = 0
        # for i in range(15):
        #     chat_history += conversations[i] + "\n"
        for iter in range(len(conversations)):
            print(iter)
            input = {"opening": opening, "chat_history": chat_history}
            question = QA.run(input)
            question_dict = json.loads(question)

            output = chat_history + "\n"
            output += question_dict["symptom"] + "\n"
            output += "Reason: " + question_dict['reason'] + "\n"
            output += "Doctor: " + question_dict['question']
            with open("output/QA/case" + str(case) + "/turn" + str(iter) + ".txt", "w") as f:
                f.write(output)

            chat_history += conversations[iter] + "\n"




