import os.path

from langchain_core.tools import tool
from typing import Annotated
# from langchain_experimental.utilities import PythonREPL
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.prompts import load_prompt
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import json
import re

from dotenv import dotenv_values
config = dotenv_values("../.env")
api_key = config["OPENAI_API_KEY"]
gpt4 = 'gpt-4'
gpt4o_mini = 'gpt-4o-mini'
default_model = gpt4o_mini

@tool
def question_generate(
        chat_history: Annotated[str, "The previous conversation between doctor and patient (state['messages'])"],
):
    """Use this tool to generate a question to ask patient based on the chat_history"""
    prompt = load_prompt("../prompts/Virtual_hospital/Conversation.yaml")
    # print("**************************Tool Execution Question Generation**************************")
    # print(chat_history)

    if not len(chat_history):
        chat_history = ""

    llm = ChatOpenAI(model_name=default_model, temperature=0.5, api_key=api_key)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    # return extract_json_data(chain.invoke({"chat_history": chat_history})["text"])
    result = chain.invoke({"chat_history": chat_history})
    # print(result)
    return result


@tool
def get_patient_info(
        patiend_id: Annotated[int, "The patient id"]
    ):
    """Use this tool to get the basic information of the patient, the patient_id is the id of the patient"""
    info = ""
    hpi_path = f"../data/USMLE/patient_info_json/case{str(patiend_id)}.json"
    if os.path.exists(hpi_path):
        with open(hpi_path, "r") as f:
            info = json.load(f)
    # if os.path.exists(hpi_path):
    #     with open(hpi_path, "r") as f:
    #         hpi = f.read()
    #
    # exams = ""
    # exams_path = f"../data_virtual_hospital/{str(patiend_id)}/modified/2_physician/exams.txt"
    # if os.path.exists(exams_path):
    #     with open(exams_path, "r") as f:
    #         exams = f.read()

    # patient_info = f"{hpi} \n {exams}" if hpi != "" and exams != "" else "We cannot find patient's record!"
    patient_info = (f"{info['Doctor_Actor']['Reason_for_visit']}"
                    f"Physical Exam Findings: {info['Patient_Actor']['Physical_Examination_Findings']}")
    return patient_info


@tool
def make_assessment(
        chat_history: Annotated[str, "The conversation you made between patient"],
        patient_info: Annotated[str, "The patient's background information including history of present illness, exam results, vital sign, etc"]
):
    """Use this tool to generate an assessment for the patient"""
    prompt = load_prompt("../prompts/Virtual_hospital/diagnosis.yaml")
    # print("**************************Tool Execution Assessment**************************")
    # print(chat_history)

    if not len(chat_history):
        chat_history = ""

    llm = ChatOpenAI(model_name=default_model, temperature=0.5, api_key=api_key)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    result = chain.invoke({"info": patient_info, "chat_history": chat_history})
    # print(result)
    return str(result)





@tool
def make_plan(
        chat_history: Annotated[str, "The conversation you made between patient"],
        patient_info: Annotated[str, "The patient's background information including history of present illness, exam results, vital sign, etc"],
        assessment: Annotated[str, "The assessment you made based on the patient's situation and physical condition"]
):
    """Use this tool to generate a plan for the patient"""
    prompt = load_prompt("../prompts/Virtual_hospital/plan.yaml")
    # print("**************************Tool Execution plan**************************")

    llm = ChatOpenAI(model_name=default_model, temperature=0.5, api_key=api_key)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    result = chain.invoke({"info": patient_info, "chat_history": chat_history, "assessment": assessment})
    # print(result)
    return str(result)