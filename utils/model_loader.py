# import os
# from dotenv import load_dotenv
# from typing import Literal, Optional, Any
# from pydantic import BaseModel, Field
# from utils.config_loader import load_config
# from langchain_google_genai import ChatGoogleGenerativeAI


# class ConfigLoader:
#     def __init__(self):
#         print(f"Loaded config.....")
#         self.config = load_config()
    
#     def __getitem__(self, key):
#         return self.config[key]

# class ModelLoader(BaseModel):
#     model_provider: Literal["gemini", "groq", "openai"] = "gemini"
#     config: Optional[ConfigLoader] = Field(default=None, exclude=True)

#     def model_post_init(self, __context: Any) -> None:
#         self.config = ConfigLoader()
    
#     class Config:
#         arbitrary_types_allowed = True
    
#     def load_llm(self):
#         """
#         Load and return the LLM model.
#         """
#         print("LLM loading...")
#         print(f"Loading model from provider: {self.model_provider}")
#         if self.model_provider == "gemini":
#             print("Loading LLM from Google Gemini..............")
#             # Try GOOGLE_API_KEY first, then GEMINI_API_KEY
#             google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
#             if not google_api_key:
#                 raise ValueError(
#                     "API key required for Gemini Developer API. "
#                     "Provide GOOGLE_API_KEY or GEMINI_API_KEY environment variable."
#                 )
#             model_name = self.config["llm"]["gemini"]["model_name"]
#             llm = ChatGoogleGenerativeAI(
#                 model=model_name,
#                 google_api_key=google_api_key,
#                 temperature=0.7,
#                 convert_system_message_to_human=True,
#                 max_retries=10,
#             )
#         elif self.model_provider == "groq":
#             print("Loading LLM from Groq..............")
#             from langchain_groq import ChatGroq
#             groq_api_key = os.getenv("GROQ_API_KEY")
#             if not groq_api_key:
#                 raise ValueError(
#                     "API key required for Groq. "
#                     "Provide GROQ_API_KEY environment variable."
#                 )
#             model_name = self.config["llm"]["groq"]["model_name"]
#             llm = ChatGroq(model=model_name, api_key=groq_api_key)
#         # elif self.model_provider == "openai":
#         #     print("Loading LLM from OpenAI..............")
#         #     from langchain_openai import ChatOpenAI
#         #     openai_api_key = os.getenv("OPENAI_API_KEY")
#         #     if not openai_api_key:
#         #         raise ValueError(
#         #             "API key required for OpenAI. "
#         #             "Provide OPENAI_API_KEY environment variable."
#         #         )
#         #     model_name = self.config["llm"]["openai"]["model_name"]
#         #     llm = ChatOpenAI(model_name=model_name, api_key=openai_api_key)
        
#         # return llm
#         elif self.model_provider == "groq":
#             print("Loading LLM from Groq..............")
#             from langchain_groq import ChatGroq
#             groq_api_key = os.getenv("GROQ_API_KEY")
#             if not groq_api_key:
#                 raise ValueError(
#                     "API key required for Groq. "
#                     "Provide GROQ_API_KEY environment variable."
#                 )
            
#             # --- NEXT LINES KO UPDATE KIYA HAI TO BYPASS CONFIG FILE ---
#             # Pehle .env mein GROQ_MODEL check karega, agar nahi mila toh config file uthayega
#             model_name = os.getenv("GROQ_MODEL") or self.config["llm"]["groq"]["model_name"]
            
#             # Agar dono jagah purana model ho, toh fallback lagakar safe side rakhte hain
#             if model_name == "mixtral-8x7b-32768":
#                 model_name = "llama-3.3-70b-versatile"
                
#             llm = ChatGroq(model=model_name, api_key=groq_api_key)

import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_google_genai import ChatGoogleGenerativeAI

class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["gemini", "groq", "openai"] = "gemini"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")
        
        llm = None  # Initialize variable to avoid unbound errors

        if self.model_provider == "gemini":
            print("Loading LLM from Google Gemini..............")
            google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            if not google_api_key:
                raise ValueError(
                    "API key required for Gemini Developer API. "
                    "Provide GOOGLE_API_KEY or GEMINI_API_KEY environment variable."
                )
            model_name = self.config["llm"]["gemini"]["model_name"]
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=google_api_key,
                temperature=0.7,
                convert_system_message_to_human=True,
                max_retries=10,
            )

        elif self.model_provider == "groq":
            print("Loading LLM from Groq..............")
            from langchain_groq import ChatGroq
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError(
                    "API key required for Groq. "
                    "Provide GROQ_API_KEY environment variable."
                )
            
            # Pehle .env se check karega, nahi toh config file uthayega
            model_name = os.getenv("GROQ_MODEL") or self.config["llm"]["groq"]["model_name"]
            
            # Decommissioned model ke liye safety fallback
            if model_name == "mixtral-8x7b-32768":
                model_name = "llama-3.3-70b-versatile"
                
            print(f"Using Groq Model: {model_name}")
            llm = ChatGroq(model=model_name, api_key=groq_api_key)

        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI..............")
            from langchain_openai import ChatOpenAI
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError(
                    "API key required for OpenAI. "
                    "Provide OPENAI_API_KEY environment variable."
                )
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(model_name=model_name, api_key=openai_api_key)
        
        # Check if LLM was successfully initialized
        if llm is None:
            raise ValueError(f"Failed to load LLM for provider: {self.model_provider}")

        return llm  # 👈 Yeh line sabse important hai, ab har block se valid object return hoga!