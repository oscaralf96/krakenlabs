from django.shortcuts import render
from django.views import View
import requests
from typing import Tuple

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
        

class FeedbackFormView(View):
    template_name = 'aimodels/spelling/form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Get data from the form
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        intended_meaning = request.POST.get('intended_meaning')

        system_prompt = """You are a teacher who is providing feedback on a student's of elementary school answer to a question.
        Please provide feedback on the answer and spelling and suggest improvements. Provide a 50 word extra information. Provide the feedback in English and Spanish."""
        user_text = f"""Question: {question}
Answer: {answer}
The student is trying to convey the following meaning:in spanish {intended_meaning}.
"""
        inference = make_inference(system_prompt=system_prompt, user_text=user_text)

        # Display it for testing (Later we will send it to OpenAI)
        context = {
            'question': question,
            'answer': answer,
            'intended_meaning': intended_meaning,
            'feedback': inference,
            'submitted': True
        }

        return render(request, self.template_name, context)