# Either agent_template can decide to end
from typing import Literal

from dotenv import load_dotenv
# loading variables from .env file
load_dotenv()


def router(state) -> Literal["call_tool", "__end__", "continue"]:
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        # The previous agent_template is invoking a tool
        return "__call_tool__"
    if "end" in last_message.content or "END" in last_message.content:
        # Any agent_template decided the work is done
        return "__end__"
    return "continue"


def chat_senario(state) -> Literal["call_tool", "__end__", "continue"]:
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if "end" in last_message.content or "END" in last_message.content:
        # Any agent_template decided the work is done
        return "__end__"
    return "continue"