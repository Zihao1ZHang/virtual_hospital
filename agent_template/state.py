import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage, ToolMessage
from typing_extensions import TypedDict

from dotenv import load_dotenv
# loading variables from .env file
load_dotenv()

# This defines the object that is passed between each node
# in the graph. We will create different nodes for each agent_template and tool
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str

import functools
from langchain_core.messages import AIMessage


# Helper function to create a node for a given agent_template
def agent_node(state, agent, name):
    messages = []
    for message in state['messages']:
        if message.type != "system":
            messages.append(f"{message.name}: {message.content}")
            # print(f"{message.name}: {message.content}")
    result = agent.invoke(messages)
    # We convert the agent_template output into a format that is suitable to append to the global state
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        # Since we have a strict workflow, we can
        # track the sender, so we know who to pass to next.
        "sender": name,
    }


