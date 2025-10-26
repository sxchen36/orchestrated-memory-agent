"""
AI Companion Agent using LangGraph
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
import operator
import json

from langgraph.graph.message import AnyMessage
import utils


class AgentState(TypedDict):
    """State for the Companion agent"""
    messages: Annotated[list[AnyMessage], operator.add]
    user_input: str
    response: str
    summary: str

class CompanionAgent:
    """An AI Companion agent using LangGraph"""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo", system_prompt: str = None):
        """Initialize the agent with OpenAI model"""
        self.llm = ChatOpenAI(model=model_name, temperature=0.7)
        # Set default system prompt if none provided
        self.system_prompt = system_prompt or "You are a helpful AI companion that assists users with their questions and tasks."
        self.in_memory_saver = InMemorySaver()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("process_input", self._process_input)
        workflow.add_node("generate_response", self._generate_response)
        workflow.add_node("format_output", self._format_output)
        workflow.add_node("summarize_context", self.summarize_context)
        
        # Add edges
        workflow.set_entry_point("process_input")
        workflow.add_edge("process_input", "generate_response")
        workflow.add_edge("generate_response", "format_output")
        workflow.add_conditional_edges("generate_response", self.should_summarize, {
            True: "summarize_context",
            False: END,
        })
        workflow.add_edge("generate_response", "format_output")
        
        return workflow.compile(checkpointer=self.in_memory_saver)
    
    def _process_input(self, state: AgentState) -> AgentState:
        """Process the user input"""
        user_input = state["user_input"]
        
        return {
            "messages": [HumanMessage(content=user_input)],
            "user_input": user_input,
        }
    
    def _generate_response(self, state: AgentState) -> AgentState:
        """Generate AI response"""
        messages = state["messages"]
        
        # Generate response using LLM
        response = self.llm.invoke(messages)
        
        return {
            "messages": [AIMessage(content=response.content)],
            "response": response.content
        }
    
    def _format_output(self, state: AgentState) -> AgentState:
        """Format the final output"""
        response = state["response"]
        
        # Add a friendly greeting prefix
        formatted_response = f"🤖 Hello! {response}"
        
        return {
            "response": formatted_response
        }

    def summarize_context(self,state: AgentState):
        conversation_text = "\n".join(
            [f"{m.type}: {m.content}" for m in state["messages"]]
        )
        prompt = (
            f"Summarize this conversation in under 80 words. "
            f"Keep track of key facts, goals, or changes:\n\n{conversation_text}\n\n"
        )
        summary_msg = self.llm.invoke([SystemMessage(content=prompt)])

        state_to_print = utils.serialize_agent_state(state)
        print(f"screenshot of current state: {json.dumps(state_to_print, indent=4)}")
        
        print(f"adding summary: {summary_msg.content}")
        return {
            "summary": summary_msg.content
        }

    def should_summarize(self, state: AgentState):
        return len(state["messages"]) % 10 == 0  # every 5 user+AI pairs
    
    def run(self, user_input: str) -> str:
        """Run the agent with user input"""
        initial_state = {
            "messages": [],
            "user_input": user_input,
            "response": ""
        }
        memory_thread = {
            "configurable": {"thread_id": "companion_thread"},
        }
        
        result = self.graph.invoke(
            initial_state,
            memory_thread
            )
        return result["response"]


def main():
    """Main function to demonstrate the agent"""
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set your OPENAI_API_KEY in the .env file")
        return
    
    # Initialize the agent
    agent = CompanionAgent()
    
    print("🤖 AI Companion is ready!")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        try:
            response = agent.run(user_input)
            print(f"Agent: {response}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()
