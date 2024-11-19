from langchain.prompts import load_prompt
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json
import re

load_dotenv()

def patient_agent(hpi: str, chat_history: str, question: str, model_name: str):
    prompt = load_prompt("prompts/QA_patient.yaml")

    llm = ChatOpenAI(model_name=model_name, temperature=0.7)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    return extract_json_data(
        chain.invoke({"chat_history": chat_history, "hpi": hpi, "question": question})[
            "text"
        ]
    )


def doctor_agent(chat_history: str, info: str, model_name: str):
    prompt = load_prompt("prompts/QA_doctor.yaml")

    llm = ChatOpenAI(model_name=model_name, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    return extract_json_data(chain.invoke({"chat_history": chat_history, "info": info})["text"])


def extract_json_data(text):
    json_text = re.search(r"```json\n?({[\w\W]+})[\n]?```", text)  # find ```json{}```
    if json_text:
        return json.loads(json_text.group(1))
    else:
        json_text = re.search(r"{[\w\W]+}", text)  # only find {}
        if json_text:
            return json.loads(json_text.group(0))
        else:
            print("No JSON found in text")
            return None


def read_file(path: str):
    with open(path, "r", encoding="UTF-8") as f:
        return f.read()


def save_result(path: str, result: str):
    with open(path, "w", encoding="UTF-8") as f:
        f.write(result)


# print(doctor_agent(chat_history="", model_name="gpt-4-1106-preview"))

def plan_run(exams: str, hpi: str, assessment: str, categories_summary: str, model_name: str):
    prompt = load_prompt("prompts/plan.yaml")

    llm = ChatOpenAI(model_name=model_name, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"exams": exams, "hpi": hpi, "assessment": assessment, "categories_summary": categories_summary})
    return response["text"]

def plan2_1_run(exams: str, hpi: str, assessment: str, categories_summary: str, model_name: str):
    prompt = load_prompt("prompts/plan2-1.yaml")

    llm = ChatOpenAI(model_name=model_name, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"exams": exams, "hpi": hpi, "assessment": assessment, "categories_summary": categories_summary})
    return response["text"]

def plan2_2_run(exams: str, hpi: str, assessment: str, plan_categories: str, model_name: str):
    prompt = load_prompt("prompts/plan2-2.yaml")

    llm = ChatOpenAI(model_name=model_name, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"exams": exams, "hpi": hpi, "assessment": assessment, "plan_categories": plan_categories})
    return response["text"]

def plan_eval_run(generated_plan: str, target_plan: str, model_name: str):
    prompt = load_prompt("prompts/plan_eval.yaml")

    llm = ChatOpenAI(model_name=model_name, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"generated_plan": generated_plan, "target_plan": target_plan})
    return response["text"]

def plan2_1_eval_run(generated_categories: str, target_categories: str, model_name: str):
    prompt = load_prompt("prompts/plan2-1_eval.yaml")

    llm = ChatOpenAI(model_name=model_name, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"generated_categories": generated_categories, "target_categories": target_categories})
    return response["text"]

def plan2_2_eval_run(generated_plan: str, target_plan: str, model_name: str):
    prompt = load_prompt("prompts/plan2-2_eval.yaml")

    llm = ChatOpenAI(model_name=model_name, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"generated_plan": generated_plan, "target_plan": target_plan})
    return response["text"]


def check_infoGather_end(hpi: str, exams: str, chat_history: str, model_name: str):
    prompt = load_prompt("prompts/check_infoGather_end.yaml")

    llm = ChatOpenAI(model_name=model_name, temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = chain.invoke({"hpi": hpi, "exams": exams, "chat_history": chat_history})
    return response["text"]


