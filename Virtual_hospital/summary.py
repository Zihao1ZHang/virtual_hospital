from langchain.tools import StructuredTool
from tools import *


if __name__ == "__main__":
    visit_id = ['152223.0', '124321.0']
    patient_id = ['23']

    root_path = "D:/projects/virtual_hospital/data"

    flag = True
    for patient in patient_id:
        for visit in visit_id:
            data_path = root_path + "/" + patient + "/" + visit

            f = open(data_path + ".txt", "r")
            radi_list = ""
            radi_list += f.read() + "\n"
            for path in os.listdir(data_path):
                if "Physician" not in path:
                    if "summary" not in path:
                        f = open(data_path + "/" + path, "r")
                        radi_list += f.read() + "\n"
                        flag = False
            if flag:
                break
            # print(radi_list)

        diff_tool = StructuredTool.from_function(diff_func)

        input = {"exam_history": radi_list}
        summary = diff_tool.run(input)
        file_name = "../data/23/opening.txt"
        f = open(file_name, "w")
        f.write(summary)
        f.close()
        print(summary)