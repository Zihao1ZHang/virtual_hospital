import langchain
langchain.debug = False
from langchain.prompts import load_prompt
# from agents.question.initialize import *
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
import json
import os

model_name = "gpt-4"
# model_name = "gpt-3.5-turbo-16k" # gpt-4

api_key = "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"

def diff_func(exam_history: str):
    """
    Tools that summarized the change of the previous exmination
        valid parameter include exam_list: a list of examination history
    """
    prompt = load_prompt("../prompt/pre_physician_summary.yaml")
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.9, model_name=model_name)
    winrate_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
    )
    return winrate_chain.run({"exam_history": exam_history})

def QA_func(opening: str, chat_history: str):
    """
    Tool that calls a chain to revise the summary,
        valid parameter include "instruction":instruction, "model1": model1,"model2": model2,"model3": model3,
    """
    prompt = load_prompt("../prompt/QA.yaml")
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.9, model_name=model_name)
    winrate_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
    )
    return winrate_chain.run({"opening": opening, "chat_history": chat_history})

def physical_func(opening: str, chat_history: str):
    """
    Tool that calls a chain to revise the summary,
        valid parameter include "instruction":instruction, "model1": model1,"model2": model2,"model3": model3,
    """
    prompt = load_prompt("../prompt/physical.yaml")
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.9, model_name=model_name)
    winrate_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
    )
    return winrate_chain.run({"opening": opening, "chat_history": chat_history})

def physical_func(opening: str, chat_history: str):
    """
    Tool that calls a chain to revise the summary,
        valid parameter include "instruction":instruction, "model1": model1,"model2": model2,"model3": model3,
    """
    prompt = load_prompt("../prompt/physical.yaml")
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.9, model_name=model_name)
    winrate_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
    )
    return winrate_chain.run({"opening": opening, "chat_history": chat_history})


def closure_func(opening: str, chat_history: str, pre_closure: str):
    """
    Tool that calls a chain to write the closure,
        valid parameter include "opening":instruction, "chat_history": previous dialogue,"pre_closure": physical exam,
    """
    prompt = load_prompt("../prompt/closure.yaml")
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.9, model_name=model_name)
    winrate_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
    )
    return winrate_chain.run({"opening": opening, "chat_history": chat_history, "pre_closure": pre_closure})

def diagnosis_func(opening: str):
    """
    Tool that calls a chain to write the closure,
        valid parameter include "opening":instruction, "chat_history": previous dialogue,"pre_closure": physical exam,
    """
    prompt = load_prompt("../prompt/diagnosis.yaml")
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.9, model_name=model_name)
    winrate_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
    )
    return winrate_chain.run({"opening": opening})

def diagnosis_lite_func(historical: str, physical: str):
    """
    Tool that calls a chain to write the closure,
        valid parameter include "opening":instruction, "chat_history": previous dialogue,"pre_closure": physical exam,
    """
    prompt = load_prompt("../prompt/diagnosis.yaml")
    llm = ChatOpenAI(openai_api_key=api_key, temperature=0.9, model_name=model_name)
    winrate_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
    )
    return winrate_chain.run({"historical": historical, "physical": physical})


