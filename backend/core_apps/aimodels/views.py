from django.shortcuts import render
from django.views import View
import requests
from typing import Tuple
import json
import re

DEEPINFRA_API_KEY = "pRGq69HjIJvZ4YVUd3pQ2UffuNuaDfbO"

def make_inference(system_prompt: str, user_text: str, max_retries: int = 3): # -> Tuple[str, dict]:

    headers = {
        "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    for attempt in range(max_retries):
        
        response = requests.post(
            url="https://api.deepinfra.com/v1/openai/chat/completions",
            headers=headers,
            json={
                "model": "Qwen/Qwen2.5-72B-Instruct",
                "stream": False,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": str(user_text)
                }
                ]
            }
        )
        # print(response.content)
        
        response.raise_for_status()

        try:
            return response.json()['choices'][0]['message']['content']
        except:
            return "ERROR: " + str(response.content)


def extract_and_parse_json(input_text):

    # First try to parse the entire input as JSON
    stripped_input = input_text.strip()
    if stripped_input.startswith('{') and stripped_input.endswith('}'):
        try:
            return json.loads(stripped_input)
        except json.JSONDecodeError:
            pass  # Continue to try other methods
        
    # Regular expression to match JSON objects or arrays within the text
    json_pattern = re.compile(r"json(.*?)|\[.*?\]|\{.*?\}", re.DOTALL)
    
    # Search for the JSON object or array
    match = json_pattern.search(input_text)
    if match:
        # Extract the JSON string
        json_string = match.group(1) if match.group(1) else match.group(0)
        
        # Clean the JSON string (remove leading/trailing whitespace and newlines)
        json_string = json_string.strip()
        # print(json_string)
        
        try:
            # Parse the extracted JSON
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON structure in the input text: {e}")
    else:
        raise ValueError("No JSON object found in the input text.")

class FeedbackFormView(View):
    template_name = 'aimodels/spelling/form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Get data from the form
        topic = request.POST.get('topic')
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        intended_meaning = request.POST.get('intended_meaning')

        system_prompt = """You are a teacher who is providing feedback on an elementary school student’s answer to a question.
        Please provide feedback on the answer (related to the topic provided) and spelling (just for the english answer) and suggest improvements. 
The first feedback should be solely on grammar and spelling (grammar and spelling corrections just for the answer in English), correcting mistakes according the join of what they provided and what they intended to say in Spanish (their native language) but.
The second feedback should provide a 50 word extra information. The feedback should be presented in English first and then the same feedback in Spanish.

As the answer provide a json object like the following example:

{
    "feedback": "Your answer is well structured, but there are some spelling mistakes. For example, 'recieve' should be 'receive'. Also, consider using more complex sentences to enhance your writing.",
    "feedback_spanish": "Tu respuesta está bien estructurada, pero hay algunos errores ortográficos. Por ejemplo, 'recieve' debería ser 'receive'. Además, considera usar oraciones más complejas para mejorar tu escritura.",
    "extra_info": "It's important to proofread your work before submitting it. This will help you catch any mistakes and improve the overall quality of your writing.",
    "extra_info_spanish": "Es importante revisar tu trabajo antes de enviarlo. Esto te ayudará a detectar cualquier error y mejorar la calidad general de tu escritura."
}

"""
        user_text = f"""Question: {question}
Answer: {answer}
The student is trying to convey the following meaning:in spanish {intended_meaning}.
"""
        inference = make_inference(system_prompt=system_prompt, user_text=user_text)

        # Display it for testing (Later we will send it to OpenAI)
        context = {
            'topic': topic,
            'question': question,
            'answer': answer,
            'intended_meaning': intended_meaning,
            'feedback': extract_and_parse_json(inference),
            'submitted': True
        }

        return render(request, self.template_name, context)