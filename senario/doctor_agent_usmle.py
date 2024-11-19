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
model = "gpt-4o-mini"

if __name__ == "__main__":
    for i in range(1, 45):
        # if i == 32:
        #     continue
        # if os.path.exists(f"../output/doctor_patient_usmle_pe_gpt4omini/case{i}.txt") or i == 32:
        #     continue
        if i != 40 :
            continue
        print(f"Case{i}")
        # Get patient information
        patient_info_path = f"../data/USMLE/patient_info_json/case{i}.json"
        with open(patient_info_path, "r") as f:
            info = json.load(f)

        patient_info = (f"Demographic: {info['Patient_Actor']['Demographic']} \n"
                        f"History: {info['Patient_Actor']['History']}\n"
                        f"Symptoms: {str(info['Patient_Actor']['Symptoms'])}\n"
                        f"Past Medical History: {info['Patient_Actor']['Past_Medical_History']}\n"
                        f"Social History: {info['Patient_Actor']['Social_History']}" )

        # Get Doorway information
        doorway_info = (f"{info['Doctor_Actor']['Reason_for_visit']}"
                        f"Physical Exam Findings: {info['Patient_Actor']['Physical_Examination_Findings']}")
        # doorway_info = ""
        # f"Vital Sign: {info['Patient_Actor']['Physical_Examination_Findings']['Vital_Signs']}"

        # Define agent nodes
        llm = ChatOpenAI(model=model, api_key=api_key)
        # Doctor agent and node
        doctor_persona_path = "../agents/doctor/persona_usmle.txt"
        with open(doctor_persona_path, "r") as f:
            doctor_persona = f.read()

        doctor_agent = create_agent(
            llm,
            [make_assessment, make_plan],
            system_message=doctor_persona,
            information=doorway_info,
        )
        doctor_node = functools.partial(agent_node, agent=doctor_agent, name="doctor")

        # Patient agent and node
        patient_persona_path = "../agents/patient/persona.txt"
        with open(patient_persona_path, "r") as f:
            patient_persona = f.read()
        patient_agent = create_agent(
            llm,
            [make_assessment],
            system_message=patient_persona,
            information=patient_info,
        )
        patient_node = functools.partial(agent_node, agent=patient_agent, name="patient")

        # Tool Node
        tools = [make_assessment, make_plan]
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
                        content=f"The patient with patient id {i} just enter the room."
                    )
                ],
            },
            # Maximum number of steps to take in the graph
            {"recursion_limit": 40},
        )

        conversation = ""
        counter = 0
        for s in events:
            # print(s.keys())
            # if 'doctor' in s.keys() and s['doctor']['messages'][0].content != '':
            #     conversation = conversation + f"Doctor: {s['doctor']['messages'][0].content} \n"
            # if 'patient' in s.keys():
            #     conversation = conversation + f"Patient: {s['patient']['messages'][0].content} \n"

            counter +=1
            type = s[next(iter(s.keys()))]['messages'][0].type
            content = s[next(iter(s.keys()))]['messages'][0].content
            name = s[next(iter(s.keys()))]['messages'][0].name
            # print(f"{name}: {s[next(iter(s.keys()))]['messages'][0].content}")

            if type == 'ai':
                conversation = conversation + f"Turn{counter} :\n {name}: {content} \n\n"
            output_path = f"../output/doctor_patient_usmle_pe_gpt4omini/case{i}.txt"
            with open(output_path, "w") as f:
                f.write(conversation)
