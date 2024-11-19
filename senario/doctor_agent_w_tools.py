from langchain_core.messages import SystemMessage

from agent_template.agent import *
from agent_template.state import *
from agent_template.tools import *
from agent_template.edge import *
from langgraph.prebuilt import ToolNode
import os

from dotenv import load_dotenv
# loading variables from .env file
from dotenv import dotenv_values
config = dotenv_values("../.env")
api_key = config["OPENAI_API_KEY"]


if __name__ == "__main__":
    workflow = StateGraph(AgentState)

    # Get patient information
    hpi_path = "../data/data_virtual_hospital/old_version/23/modified/2_physician/HPI.txt"
    with open(hpi_path, "r") as f:
        hpi = f.read()
    exams_path = "../data/data_virtual_hospital/old_version/23/modified/2_physician/exams.txt"
    with open(exams_path, "r") as f:
        exams = f.read()
    patient_info = f"{hpi} \n {exams}"

    # Define agent nodes
    llm = ChatOpenAI(model="gpt-4-1106-preview", api_key=api_key)
    # Doctor agent and node
    doctor_persona_path = "../agents/doctor/persona_with_tools.txt"
    with open(doctor_persona_path, "r") as f:
        doctor_persona = f.read()
    doctor_agent = create_agent(
        llm,
        [get_patient_info, question_generate, make_assessment, make_plan],
        system_message=doctor_persona,
        information=""
    )
    doctor_node = functools.partial(agent_node, agent=doctor_agent, name="doctor")

    # Patient agent and node
    patient_persona_path = "../agents/patient/persona.txt"
    with open(patient_persona_path, "r") as f:
        patient_persona = f.read()
    patient_agent = create_agent(
        llm,
        [get_patient_info],
        system_message=patient_persona,
        information=patient_info
    )
    patient_node = functools.partial(agent_node, agent=patient_agent, name="patient")

    # Tool Node
    tools = [get_patient_info, question_generate, make_assessment, make_plan]
    tool_node = ToolNode(tools)

    # Define Graph
    workflow = StateGraph(AgentState)
    workflow.add_node("doctor", doctor_node)
    workflow.add_node("patient", patient_node)
    workflow.add_node("call_tool", tool_node)

    workflow.add_conditional_edges(
        "doctor",
        router,
        {"continue": "patient", "__call_tool__": "call_tool", "__end__": END},
    )

    # workflow.add_conditional_edges(
    #     "patient",
    #     router,
    #     {"continue": "doctor", "call_tool": "call_tool", "__end__": END},
    # )

    workflow.add_edge("call_tool", "doctor")
    workflow.add_edge("patient", "doctor")

    workflow.set_entry_point("doctor")
    graph = workflow.compile()

    events = graph.stream(
        {
            "messages": [
                SystemMessage(
                    content="The patient 0 just enter the room."
                )
            ],
        },
        # Maximum number of steps to take in the graph
        {"recursion_limit": 60},
    )

    conversation = ""
    counter = 0
    for s in events:
        print(s.keys())
        # if 'doctor' in s.keys() and s['doctor']['messages'][0].content != '':
        #     conversation = conversation + f"Doctor: {s['doctor']['messages'][0].content} \n"
        # if 'patient' in s.keys():
        #     conversation = conversation + f"Patient: {s['patient']['messages'][0].content} \n"
        conversation = conversation + f"Turn{counter} :\n {s.keys()} \n" \
                                      f"{s[next(iter(s.keys()))]['messages'][0].content}\n\n"
        counter +=1
        print(f"{s[next(iter(s.keys()))]['messages'][0]} \n")
        output_path = "./infoGather_assessment_plan4.txt"
        with open(output_path, "w") as f:
            f.write(conversation)
