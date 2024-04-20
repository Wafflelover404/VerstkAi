import requests
import re
import streamlit

hf_token = st.secrets["text_writer"]["hf_token"] # replace with your HuggingFace API key

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {hf_token}"}

def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  return response.json()

def replace_assistant(strin):
  e = re.sub(r'<\|system\|>.*<\|assistant\|>', '', strin, flags=re.DOTALL)
  e = re.sub(r'(?<=\?waffle\?)\S+', '', e)
  return e.strip()
 
def send(prompt):
  for i in range(0, 10):
    try:
      prompt = f"""
          <|system|>
          Assistant is an extremely intelligent and precise copywriter, who has 20 years of experience. His task is to read user's company name and some info on it. And write a typical text for "About us page". Text should consist of 2-3 sentences and be brief and encouraging. If request seems to illegal (Drugs, Weaponry, etc...) Assistant should write: "Error 001". If assistant was not provided with necessary info, or was asked for a friendly talk: "Error 002" Assistant can respond with any language. But it's strongly recommended to respond with the same language as user provided: whether it's russian, english, chinese, etc.
          </s>
          <|user|>
          {prompt}
          </s>
          <|assistant|>
          """
      response = query({
        "inputs": prompt,
        "parameters": {"max_new_tokens": 8000, "use_cache": False, "max_time": 120.0},
        "options": {"wait_for_model": True}
      })
      full_response = replace_assistant(response[0]["generated_text"])
      return full_response
      break
    except Exception as e:
      print(e)
      pass
  return "Error"

# Get user prompt and optional requested information
