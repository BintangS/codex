import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

required_categories = {
    "age": "Can you please tell me your age?",
    "gender": "What is your gender?",
    "interests": "What are your interests?",
    "location": "Where do you live?",
    "education_level": "What is your education level?",
    "occupation": "What is your occupation?",
    "previous_experience": "What is your previous experience with the site?",
    "internet_proficiency": "How proficient are you with the internet?",
    "device": "Do you use a mobile device or desktop?",
    "behavioral_traits": "Can you describe any specific behavioral traits you have?",
}

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

        if sessionId not in self.store:
            self.store[sessionId] = {"history": ChatMessageHistory(), "profile": {}}

        # Update the profile with the new prompt
        self.update_profile(sessionId, prompt)

        # Check if we have collected all required categories
        missing_categories = self.get_missing_categories(sessionId)
        if not missing_categories:
            return json.dumps(self.store[sessionId]['profile'])

        # Generate the next question to ask
        next_question = required_categories[missing_categories[0]]
        
        response = self.with_message_history.invoke([
            HumanMessage(content=prompt),
            AIMessage(content=next_question)
        ], config={"configurable": {"session_id": sessionId}})
        
        return response.content

    def update_profile(self, session_id, prompt):
        # Use a simple rule-based approach to update profile. For more complex cases, NLP can be used.
        tokens = prompt.split()
        for category in required_categories.keys():
            if category not in self.store[session_id]['profile'] and any(word in prompt.lower() for word in category.split()):
                self.store[session_id]['profile'][category] = " ".join(tokens)
                break

    def get_missing_categories(self, session_id):
        profile = self.store[session_id]['profile']
        return [category for category in required_categories.keys() if category not in profile]

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        return self.store[session_id]["history"] if session_id in self.store else ChatMessageHistory()