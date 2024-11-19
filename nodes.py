from typing import Annotated, Optional
from typing_extensions import TypedDict

from langgraph.graph.message import AnyMessage, add_messages
from langgraph.graph import END, StateGraph

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from tools import *

model = "gpt-3.5-turbo-0125"

# Define State
class State(TypedDict):
    # doorway information
    hpi: str
    exams: str

    # Append_only chat memory so the agent_template can try to recover from initial mistatkes.
    messages: Annotated[list[AnyMessage], add_messages]
    # From the dataset. These are used for testing.
    runtime_limit: int
    status: str



def doctor_node(state: State):
    doctor_question = doctor_agent(
        chat_history=state["messages"], model_name=model
    )
    return {"messages": [doctor_question]}


def patient_node(state: State):
    patient_response = patient_agent(
            hpi=state["hpi"],
            chat_history=state["chat_history"],
            question=state["messages"][-1],
            model_name=model,
        )
    return {"messages": [f"Patient: {patient_response}"]}


def evaluation_node(state: State):
    result = check_infoGather_end(
        hpi=state["hpi"],
        exams=state["exams"],
        chat_history=state["messages"],
        model_name=model
    )
    status = "finished" if result == "yes" else "continue"
    return {"status": status}


def control_edge(state: State):
    # TODO: Change END to assessment after testing infoGather
    if state.get("status") == "finished":
        return END
        # return "assessment"
    return "doctor"


def plan_node(state: State):
    plan_output = plan2_1_run(
        exams=state["exams"], hpi=state["hpi"], assessment=state["assessment"], categories_summary=state["cate_summary"],
        model_name=model
    )
    return {"messages": [plan_output]}


def assessment_node(state: State):
    # TODO: modified the original code to the graph
    return 0



