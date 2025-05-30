import dotenv
from typing import List
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os

from ..services.vinted_scraper import VintedScraperService
from ..services.filter_service import VintedFilterService
from ..services.llm_service import LLMService
from ..models.types import StatusType

dotenv.load_dotenv("env")

class GetInformation(BaseModel):
    "Get the missing information from user"
    question: str = Field(
        description="Get missing information like brand, price, size, colour and status from user regarding the attire they want",
    )

class GetConfirmation(BaseModel):
    "Get confirmation from user regarding the returned items"
    question: str 
    product_title: str
    product_url: str

class End(BaseModel):
    "End the conversation"
    pass

@tool
def get_vinted_results(price: int,
                       condition: StatusType,
                      outfit_title: str = "", 
                      brand: str = "", 
                      size: str = "", 
                      colour: str = ""):
    "Search for items on Vinted based on the provided parameters. All parameters are optional with default values."
    print("\n=== Starting Vinted Search ===")
    customer_request = f"Searching for: {outfit_title} from {brand} in {colour}, size {size}, condition {condition}, max price {price}"
    print(f"Customer request: {customer_request}")

    missing_fields = []

    if not outfit_title:
        missing_fields.append("outfit_title")
    if not brand:
        missing_fields.append("brand")
    if not size:
        missing_fields.append("size")
    if not colour:
        missing_fields.append("colour")

    if missing_fields:
        print(f"❌ Missing required parameters: {', '.join(missing_fields)}")
        return f"Missing required parameters: {', '.join(missing_fields)}"
    
    print("\n🔍 Searching Vinted...")
    search_list = scraper_service.search_items(outfit_title, brand, price, size, colour, condition)
    print(f"Found {len(search_list)} initial results")
    
    print("\n🔧 Filtering results...")
    filter_service = VintedFilterService(search_list)
    filtered_items = filter_service.filter_by_multiple_criteria(
        brand=brand,
        min_price=0,
        max_price=price,
        size=size,
        status=condition
    )
    print(f"Filtered down to {len(filtered_items)} items")
    
    print("\n📝 Getting detailed information...")
    filtered_items_with_details = []
    for item in filtered_items:
        print(f"  - Getting details for: {item['title']}")
        description = scraper_service.get_item_description(item["url"])
        color = scraper_service.get_item_color(item["url"])
        data = {
            "id": item["id"],
            "title": item["title"],
            "description": description,
            "colour": color,
            "url": item["url"]
        }
        filtered_items_with_details.append(data)
    
    print("\n🤖 Using AI to match items with your preferences...")
    result = llm_service.filter_items_by_description(customer_request, filtered_items_with_details)
    print("✅ Search complete!")
    return result

class FashionSearchApp:
    def __init__(self):
        self.scraper_service = VintedScraperService()
        self.llm_service = LLMService()
        self.memory = MemorySaver()
        self.llm = ChatGroq(model=os.getenv("Gemma"))
        self._setup_workflow()

    def _setup_workflow(self):
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                You are a fashion search assistant of a thrift store. You task is to help user find an outfit by returning the product.
                You must keep calling `Get_Information` until you get all the missing critierias needed, get all the information in one sentence
                Call `get_vinted_results` to search for the items and return the product.
                Check if the user is satisfied before ending.
                """
            ),
            ("placeholder", "{messages}"),
        ])

        # Make the services available to the tool
        global scraper_service, llm_service
        scraper_service = self.scraper_service
        llm_service = self.llm_service

        self.tools = [get_vinted_results]
        self.model_with_tools = self.prompt | self.llm.bind_tools(
            self.tools + [GetInformation, GetConfirmation, End], 
            tool_choice="any"
        )
        self.tool_node = ToolNode(self.tools)
        self._setup_graph()

    def _setup_graph(self):
        self.workflow = StateGraph(MessagesState)
        self.workflow.add_node("agent", self.agent_node)
        self.workflow.add_node("tool", self.tool_node)
        self.workflow.add_node("get_information", self.get_information)
        self.workflow.add_node("get_confirmation", self.get_confirmation)
        self.workflow.add_node("end", self.end)

        self.workflow.set_entry_point("agent")
        self.workflow.add_conditional_edges(
            "agent",
            self.route_tools,
            ["tool", "get_information", "get_confirmation", "end"]
        )
        self.workflow.add_edge("tool", "agent")
        self.workflow.add_edge("get_information", "agent")
        self.workflow.add_edge("get_confirmation", "agent")
        self.workflow.add_edge("end", END)

        self.app = self.workflow.compile(checkpointer=self.memory, interrupt_before=["get_information", "get_confirmation"])

    def agent_node(self, state):
        return {"messages": [self.model_with_tools.invoke({"messages": state["messages"]})]}

    def route_tools(self, state):
        ai_message = state["messages"][-1]
        first_tool_call = ai_message.tool_calls[0]
        tool_name = first_tool_call["name"]

        if tool_name == "get_vinted_results":
            return "tool"
        elif tool_name == "GetInformation":
            return "get_information"
        elif tool_name == "GetConfirmation":
            return "get_confirmation"  
        elif tool_name == "End":
            return "end"
        else:
            raise ValueError(f"Unknown tool name: {tool_name}")

    def get_information(self, state):
        pass

    def get_confirmation(self, state):
        pass

    def end(self, state):
        pass

    def run(self, input_message: str):
        config = {"configurable": {"thread_id": "1"}}
        input_msg = HumanMessage(content=input_message)
        
        for event in self.app.stream({"messages": [input_msg]}, config, stream_mode="values"):
            event["messages"][-1].pretty_print()

        while self.app.get_state(config).next:
            if self.app.get_state(config).next == ("get_information",):
                state = self.app.get_state(config)
                last_message = state.values["messages"][-1]
                
                if isinstance(last_message, AIMessage):
                    tool_calls = getattr(last_message, "tool_calls", [])
                    if tool_calls:
                        tool_call_id = tool_calls[0].get("id")
                        print(f"Tool call ID: {tool_call_id}")
                    else:
                        print("No tool calls found.")
                else:
                    print("The last message is not an AIMessage.")

                human_response = input("Type here...")
                tool_message = [{"tool_call_id": tool_call_id, "type": "tool", "content": human_response}]
                self.app.update_state(config, {"messages": tool_message}, as_node="get_information")

                for event in self.app.stream(None, config, stream_mode="values"):
                    event["messages"][-1].pretty_print()

            elif self.app.get_state(config).next == ("get_confirmation",):
                state = self.app.get_state(config)
                last_message = state.values["messages"][-1]
                
                if isinstance(last_message, AIMessage):
                    tool_calls = getattr(last_message, "tool_calls", [])
                    if tool_calls:
                        tool_call_id = tool_calls[0].get("id")
                        print(f"Tool call ID: {tool_call_id}")
                    else:
                        print("No tool calls found.")
                else:
                    print("The last message is not an AIMessage.")

                human_response = input("Type here...")
                tool_message = [{"tool_call_id": tool_call_id, "type": "tool", "content": human_response}]
                self.app.update_state(config, {"messages": tool_message}, as_node="get_confirmation")

                for event in self.app.stream(None, config, stream_mode="values"):
                    event["messages"][-1].pretty_print()

            elif self.app.get_state(config).next == ("end",):
                break

            else:    
                for event in self.app.stream(None, config, stream_mode="values"):
                    event["messages"][-1].pretty_print() 