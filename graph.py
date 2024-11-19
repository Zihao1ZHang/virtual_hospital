from nodes import *
from langgraph.checkpoint.sqlite import SqliteSaver


if __name__ == "__main__":
    builder = StateGraph(State)
    builder.add_node("doctor", doctor_node)
    builder.set_entry_point("doctor")
    builder.add_node("patient", patient_node)
    builder.add_node("evaluation", evaluation_node)

    builder.add_edge("doctor", "evaluation")
    builder.add_edge("patient", "doctor")

    builder.add_conditional_edges(
        "evaluation",
        control_edge,
        {END: END, "doctor": "doctor"}
    )
    memory = SqliteSaver.from_conn_string(":memory:")
    graph = builder.compile(checkpointer=memory)



