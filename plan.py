import os
from tools import plan_run
from tools import plan_eval_run

from tools import plan2_1_run
from tools import plan2_2_run
from tools import plan2_1_eval_run
from tools import plan2_2_eval_run


def plan():
    cases = [case for case in os.listdir("data/data_virtual_hospital")]
    cases = cases[:5]

    with open("categories_summary.txt", "r") as f:
        categories_summary = f.read()

    for case in cases:
        print("Running case ", case)
        with open(f"data/data_virtual_hospital/{case}/modified/2_physician/HPI.txt", "r") as f:
            hpi = f.read()
        with open(f"data/data_virtual_hospital/{case}/modified/2_physician/exams.txt", "r") as f:
            exams = f.read()
        with open(f"data/data_virtual_hospital/{case}/modified/2_physician/assessment.txt", "r") as f:
            assessment = f.read()

        plan_output = plan_run(
            exams=exams, hpi=hpi, assessment=assessment, categories_summary=categories_summary,model_name="gpt-4-1106-preview"
        )

        print(plan_output)

        # save outputs to file
        with open(f"output/plan/{case}.txt", "w") as f:
            f.write(plan_output)


def plan2_1():
    cases = [case for case in os.listdir("data/data_virtual_hospital")]
    cases = cases[:1]

    with open("plan_categories/categories_summary.txt", "r") as f:
        categories_summary = f.read()

    for case in cases:
        print("Running case ", case)
        with open(f"data/data_virtual_hospital/{case}/modified/2_physician/HPI.txt", "r") as f:
            hpi = f.read()
        with open(f"data/data_virtual_hospital/{case}/modified/2_physician/exams.txt", "r") as f:
            exams = f.read()
        with open(f"data/data_virtual_hospital/{case}/modified/2_physician/assessment.txt", "r") as f:
            assessment = f.read()

        plan_output = plan2_1_run(
            exams=exams, hpi=hpi, assessment=assessment, categories_summary=categories_summary,model_name="gpt-4-1106-preview"
        )

        print(plan_output)

        # save outputs to file
        with open(f"output/plan2/plan2-1/{case}.txt", "w") as f:
            f.write(plan_output)


def plan2_2():
    cases = [case for case in os.listdir("data/data_virtual_hospital")]
    cases = cases[:1]

    for case in cases:
        print("Running case ", case)
        with open(f"data/data_virtual_hospital/{case}/modified/2_physician/HPI.txt", "r") as f:
            hpi = f.read()
        with open(f"data/data_virtual_hospital/{case}/modified/2_physician/exams.txt", "r") as f:
            exams = f.read()
        with open(f"data/data_virtual_hospital/{case}/modified/2_physician/assessment.txt", "r") as f:
            assessment = f.read()
        with open(f"plan_categories/each_case/{case}.txt", "r") as f:
            plan_categories = f.read()

        plan_output = plan2_2_run(
            exams=exams, hpi=hpi, assessment=assessment, plan_categories=plan_categories,model_name="gpt-4-1106-preview"
        )

        print(plan_output)

        # save outputs to file
        with open(f"output/plan2/plan2-2/{case}.txt", "w") as f:
            f.write(plan_output)


def plan_eval():
    cases = [case for case in os.listdir("data/data_virtual_hospital")]
    cases = cases[1:5]

    for case in cases:
        print("Running case ", case)
        with open(f"output/plan/{case}.txt", "r") as f:
            generated_plan = f.read()
        with open(f"data/data_virtual_hospital/{case}/modified/2_physician/plan.txt", "r") as f:
            target_plan = f.read()

        eval_output = plan_eval_run(
            generated_plan=generated_plan, target_plan=target_plan, model_name="gpt-4-1106-preview"
        )

        print(eval_output)

        # save outputs to file
        with open(f"output/plan_eval/{case}.txt", "w") as f:
            f.write(eval_output)

def plan2_1_eval():
    cases = [case for case in os.listdir("data/data_virtual_hospital")]
    cases = cases[:1]

    for case in cases:
        print("Running case ", case)
        with open(f"output/plan2/plan2-1/{case}.txt", "r") as f:
            generated_categories = f.read()
        with open(f"plan_categories/each_case/{case}.txt", "r") as f:
            target_categories = f.read()

        eval_output = plan2_1_eval_run(
            generated_categories=generated_categories, target_categories=target_categories, model_name="gpt-4-1106-preview"
        )

        print(eval_output)

        # save outputs to file
        with open(f"output/plan2_eval/plan2-1/{case}.txt", "w") as f:
            f.write(eval_output)

def plan2_2_eval():
    cases = [case for case in os.listdir("data/data_virtual_hospital")]
    cases = cases[:1]

    for case in cases:
        print("Running case ", case)
        with open(f"output/plan2/plan2-1/{case}.txt", "r") as f:
            generated_plan = f.read()
        with open(f"plan_categories/each_case/{case}.txt", "r") as f:
            target_plan = f.read()

        eval_output = plan2_1_eval_run(
            generated_plan=generated_plan, target_plan=target_plan, model_name="gpt-4-1106-preview"
        )

        print(eval_output)

        # save outputs to file
        with open(f"output/plan2_eval/plan2-2/{case}.txt", "w") as f:
            f.write(eval_output)


if __name__ == "__main__":
    # plan()
    # plan_eval()
    
    plan2_1()
    # plan2_2()
    # plan2_1_eval()
    # plan2_2_eval()
    
    pass
