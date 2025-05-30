import os
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

class LLMService:
    def __init__(self):
        model = os.getenv("Gemma")
        if not model:
            raise ValueError("Gemma model environment variable not set. Please check your env file.")
        self.llm = ChatGroq(model=model)

    def filter_items_by_description(self, user_description: str, search_list: list) -> str:
        """Filter items based on user description using LLM"""
        system_prompt = SystemMessage(content=(
            "You are a fashion search assistant. Given a user's description of desired clothing and a list of clothing items "
            "(each with title, color, and description), identify and return only the items that closely match the user's preferences."
        ))

        prompt = ChatPromptTemplate.from_messages([
            system_prompt,
            ("human", "{input}")
        ])

        chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
        )

        input_data = {
            "input": f"User Description: {user_description}\nClothing Items: {search_list}"
        }

        res = chain.invoke(input_data)
        return res["text"] 