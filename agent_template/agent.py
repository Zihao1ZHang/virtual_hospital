from langchain_core.messages import (
    BaseMessage,
    ToolMessage,
    HumanMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, StateGraph

import functools



def create_agent(llm, tools, system_message: str, information: str):
    """Create an agent_template."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_message
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(information=information)
    if len(tools) > 0:
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    return prompt | llm.bind_tools(tools)