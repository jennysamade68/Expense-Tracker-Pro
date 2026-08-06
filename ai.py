import requests
import json


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "mistral"


def ask_ollama(prompt):

    response = requests.post(

        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                 "temperature": 0,
                 "num_predict": 200
            }
       }
    )


    if response.status_code != 200:

        raise Exception(
            "Ollama connection error"
        )


    result = response.json()


    return result["response"]




# --------------------------------
# Receipt Analysis
# --------------------------------

def analyze_receipt(receipt_text):


    prompt = f"""

You are an expense extraction AI.

Read this receipt text:

{receipt_text}


Extract the information.

Return ONLY JSON:

{{
"date": "YYYY-MM-DD",
"merchant": "",
"category": "",
"amount": 0,
"description": ""
}}

Rules:

- amount must be a number
- category should be one of:
Food,
Transport,
Shopping,
Bills,
Healthcare,
Entertainment,
Other

Receipt text:

{receipt_text}

"""


    answer = ask_ollama(
        prompt
    )


    try:

        data = json.loads(
            answer
        )

        return data


    except:

        return {

            "date": "",
            "merchant": "Unknown",
            "category": "Other",
            "amount": 0,
            "description": answer

        }





# --------------------------------
# Financial Assistant
# --------------------------------

def financial_advice(expenses, question):


    prompt = f"""

You are a personal finance assistant.


Here are user expenses:

{expenses}


Answer this question:

{question}


Give practical financial advice.

"""


    return ask_ollama(
        prompt
    )