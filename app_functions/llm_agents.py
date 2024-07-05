import openai 
from openai import OpenAI
from groq import Groq

openai_client = OpenAI(api_key="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")
groq_client = Groq(api_key = "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")

# OpenAI call
def openai_summarizer(news, ticker):
    prompt = f'News of {ticker}: "{news}"\nIs {ticker} a buy at the moment?'
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "You are a stock market analyser, Your job is to analyse the provided news of a particular stock and recommend if its a right or wrong purchase and also a brief summary."
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt
                }
            ]
            }
        ],
        max_tokens=1700,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message.content

# groq call
def groq_summarizer(news, ticker):
    prompt = f'News of {ticker}: "{news}"\nIs {ticker} a buy at the moment?'
    completion = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a stock market analyser, Your job is to analyse the provided news of a particular stock and recommend if its a right or wrong purchase and also a brief summary."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stop=None,
    )
    return completion.choices[0].message.content

def openai_NERextractor(user_input):
    response = openai_client.chat.completions.create(
    model="gpt-4o",
    response_format={"type": "json_object"},
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "You are a NER extractor. Your job is only to extract two entities naming companies and time. Time has to be in format of years or months only in JSON format. \nOutput formating - \n{\n  \"Company\": \"Apple\",\n  \"time\": {\n    \"month\": 3,\n    \"year\": 2\n  }\n}"
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": user_input
            }
        ]
        }
    ],
    temperature=0.5,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].message.content

