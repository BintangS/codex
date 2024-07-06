import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

# TODO: implement simple chat history to keep track of the conversation
class ChatbotModels:
    # store the chat history in memory
    # TODO: implement a way to store the chat history in a database
    store = {}

    def __init__(self):
        self.model = None
        # need to have env variable "GOOGLE_API_KEY" loaded to make the gemini AI works
        self.model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
        self.with_message_history = RunnableWithMessageHistory(self.model, self.get_session_history)

    def handle_chat(self: object, prompt: str):
        return self.model.invoke([
            HumanMessage(content="Hi! I'm Ichwan"),
            AIMessage(content="Hello Ichwan! How can I assist you today?"),
            HumanMessage(content=prompt)
        ]).content
    
    def handle_chat_with_history(self: object, prompt: str, sessionId: str):
        if sessionId is None:
            return "Session ID is required to use history feature."
        
        print(f"Session ID: {sessionId}")

        config = {"configurable": {"session_id": sessionId}}

        return self.with_message_history.invoke([
            HumanMessage(content=prompt),
        ], config=config).content
    
    def get_session_history(self: object, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]