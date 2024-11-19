import os
import re

def extract_categories(plan_content):
    categories = []
    previous_line = None

    # Split the content into lines
    lines = plan_content.split('\n')

    for line in lines:
        if "1. Tests:" in line:
            if previous_line is not None:
                cleaned_line = re.sub(r'^\*\*|\*\*$', '', previous_line.strip())
                categories.append(cleaned_line)
        previous_line = line  # This should be outside the if block to update on each iteration

    return categories

cases = [case for case in os.listdir("data/data_virtual_hospital")]

categories_all = set()
for case in cases:
    print("Running case ", case)
    with open(f"data/data_virtual_hospital/{case}/modified/2_physician/plan.txt", "r") as f:
        plan_content = f.read()

    categories = extract_categories(plan_content)
    # print(categories)
    categories_all.update(categories)

print(categories_all)

with open("categories_summary.txt", "w") as file:
    for category in categories_all:
        file.write(category + "\n")
