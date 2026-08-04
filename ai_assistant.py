import requests


OLLAMA_URL = "http://localhost:11434/api/generate"



def ask_ai(prompt):

    response = requests.post(

        OLLAMA_URL,

        json={

            "model": "mistral",

            "prompt": prompt,

            "stream": False

        }

    )


    result = response.json()


    return result.get(
        "response",
        "No answer"
    )