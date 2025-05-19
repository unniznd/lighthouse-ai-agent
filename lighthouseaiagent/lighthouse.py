import os
from lighthouseweb3 import Lighthouse
from google import genai
from .prompt import summarize_prompt, retrieve_prompt
import json
import ast

class LighthouseAIAgent:
  def __init__(self, token: str = ""):
    self.token = token or os.environ.get("LIGHTHOUSE_TOKEN", "")

  
    if not self.token:
      raise Exception(
        "No token provided: Please provide a token or set the LIGHTHOUSE_TOKEN environment variable"
      )
    self.lh = Lighthouse(self.token)
  
  def upload(self, source: str):
    response = self.lh.upload(source)
    return self._summarize_file(source, response["data"]["Hash"])
  
  def save(self, summary: dict):
    try:
        try:
            with open('indexer.json', 'r') as file:
                indexer = json.load(file)
        except FileNotFoundError:
            indexer = {}
        indexer[summary['cid']] = summary['summary']
        
        with open('indexer.json', 'w') as file:
            json.dump(indexer, file, indent=2)

    except Exception as e:
        raise Exception(f"Failed to save data: {str(e)}")
  
  def query(self, query):
    with open('indexer.json', 'r') as file:
      indexer = json.load(file)
  
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(
      model="gemini-2.0-flash",
      contents=[json.dumps(indexer), retrieve_prompt, query],
    )
    response_text = response.text
    lines = response_text.strip().split('\n')
    list_of_cid = ast.literal_eval(lines[1])
    for key, cid in enumerate(list_of_cid):
      list_of_cid[key] = f"https://gateway.lighthouse.storage/ipfs/{cid}"
    return list_of_cid
  
  def _summarize_file(self, file_path:str, cid: str):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    file = client.files.upload(file=file_path)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[file, summarize_prompt, f"cid of the file is {cid}"],
    )
    response_text = response.text
    lines = response_text.strip().split('\n')
    dict_response = json.loads(lines[1])
    
    return dict_response