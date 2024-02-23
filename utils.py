api_key = "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"

if __name__ == "__main__":

    for case in range(33, 45):
        print(case)
        opening_path = "USMLE_txt/cases/case" + str(case) + ".txt"

        with open(opening_path, "r") as f:
            opening = f.read()
        opening_list = opening.split("Differential Diagnosis")

        output = opening_list[0]
        output_path = "USMLE_txt/diagnosis_input1/case" + str(case) + ".txt"
        with open(output_path, "w") as f:
            f.write(output)



