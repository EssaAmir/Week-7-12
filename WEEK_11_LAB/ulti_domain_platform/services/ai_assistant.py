from typing import List, Dict
from openai import OpenAI  
import streamlit as st

class AIAssistant:
    """Wrapper around OpenAI API for domain-specific assistance."""

    def __init__(self, system_prompt: str = "You are a helpful assistant."):
        self._system_prompt = system_prompt
        self._history: List[Dict[str, str]] = []
        
        # - Initialize Client with API Key from secrets
        # Ensure you have .streamlit/secrets.toml set up with openai_api_key
        try:
            self._client = OpenAI(api_key=st.secrets["openai_api_key"]) #ensure lowercase
        except Exception:
            self._client= None #Handle case where key is missing

    def set_system_prompt(self, prompt: str):
        self._system_prompt =prompt

    def send_message(self, user_message: str) -> str:
        """Send a message to OpenAI and get a response."""
        if not self._client:
            return "Error: OpenAI API Key not found in secrets."

        #Adduser message to history
        self._history.append({"role": "user", "content": user_message})

        #Construct message list with system prompt
        messages= [{"role": "system", "content": self._system_prompt}] + self._history

        try:
            #Call OpenAI API
            response= self._client.chat.completions.create(
                model= "gpt-3.5-turbo", # Use GPT-3.5 Turbo model
                messages=messages
            )
            
            ai_reply =response.choices[0].message.content
            
            #Add AI reply to history
            self._history.append({"role": "assistant", "content": ai_reply})
            return ai_reply
            
        except Exception as e:
            return f"Error communicating with AI: {str(e)}"

    def clear_history(self):
        self._history.clear()
        
        #error occurs only when typing something because of quota exceeded, need to handle that