import os
from dotenv import load_dotenv
from typing import List
from pathlib import Path
import sys

from langchain_astradb import AstraDBVectorStore
from langchain_core.documents import Document

# from utils.config_loader import load_config
# from utils.model_loader import ModelLoader

from prod_assistant.utils.config_loader import load_config
from prod_assistant.utils.model_loader import ModelLoader

# Add the project root to the Python path for direct script execution
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))


class Retriever:
    def __init__(self):
        """ 
        """
        print("Initialalizing DataIngestion Pipeline...")
        self.model_loader = ModelLoader()
        self.config = load_config()
        self._load_env_variables()
        self.vstore = None
        self.retriever = None


    def _load_env_variables(self):
        """"Load required environemnt variables from .env file"""
        load_dotenv()
        required_vars =  ["GOOGLE_API_KEY", "ASTRA_DB_API_ENDPOINT", "ASTRA_DB_APPLICATION_TOKEN", "ASTRA_DB_KEYSPACE"]
        missing_vars = [var for var in required_vars if os.getenv(var) is None]

        if missing_vars:
                raise EnvironmentError(f"Missing Environment Variables:{missing_vars}")

        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.db_api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
        self.db_application_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        self.db_keyspace = os.getenv("ASTRA_DB_KEYSPACE")

    def load_retriever(self):
        """"
        load the retriever
        """
        if not self.vstore:
             collection_name = self.config["astra_db"]["collection_name"]

             self.vstore = AstraDBVectorStore(
                  embedding  =self.model_loader.load_embeddings(),
                  collection_name= collection_name,
                  api_endpoint=self.db_api_endpoint,
                  token=self.db_application_token,
                  namespace=self.db_keyspace
             )
   
        if not self.retriever:
             top_k = self.config ["retriever"]["top_k"] if "retriever" in self.config else 3
             retriever = self.vstore.as_retriever(search_kwargs={"k":top_k})
             print("Retriever loaded successfully.")
             return retriever

        

    def call_retriever(self,query):
        """
        call the retriever
        """
        retriever= self.load_retriever()
        output = retriever.invoke(query)
        return output 



# docstring

if __name__ =='__main__':
    retriever_obj = Retriever()
    user_query = "can you share only one user rating of iPhone 16 Pro ?"
    results = retriever_obj.call_retriever(user_query)
    
    print(results)
    for idex,doc in enumerate(results,1):
        print(f"Result {idex}: {doc.page_content}\n Metadata: {doc.metadata}\n")