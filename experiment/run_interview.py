import json
import os
from threading import Thread
from datetime import datetime
from tqdm import tqdm
import copy, re
from tenacity import (
    retry,
    stop_after_attempt,
)
from openai import OpenAI



# API_PORT=8121 CUDA_VISIBLE_DEVICES=3 llamafactory-cli api path
from tqdm import tqdm
from datetime import datetime
import json
def read_file(path):
    with open(path, 'r', encoding='utf-8') as fp:
        return fp.read().strip()

question_path = ''
prompt_path = ""
prompt = read_file(prompt_path)
profile_path = ""
persona_profile = read_file(profile_path)
prompt = prompt.format(character="", persona_profile=persona_profile)
model_name_ot_path = ""
output_path = ""
outputs = []
threads = []
with open(question_path, 'rb') as fp:
    questions = json.load(fp)
questions = questions
print(len(questions))
client = OpenAI(api_key="0",base_url="")
# api_key = ""
# client = OpenAI(
#     api_key=api_key,  
#     base_url=""
# )
for i in tqdm(range(len(questions)), desc="处理进度", unit="个问题"):
    model_prompt = prompt + " " + questions[i]["question"]
    # print(model_prompt)
    response = client.chat.completions.create(
        model = model_name_ot_path,
        messages=[
            {"role": "user", "content": model_prompt},  
        ], 
        max_tokens=2048,
        temperature=0.2,
        top_p=0.95,
        n=1,
    )
    # response = client.chat.completions.create(
    #     model = "gpt-4o",
    #     messages=[
    #         {"role": "user", "content": model_prompt},  
    #     ], 
    #     max_tokens=2048,
    #     temperature=0.2,
    #     top_p=0.95,
    #     n=1,
    # )
    # print("-------------------------")
    # print(response.choices[0].message.content)
    output = {
        'topic_id': questions[i]['topic_id'],
        'question': questions[i]["question"],
        'reply': response.choices[0].message.content, 
    }
    outputs.append(output)
with open(output_path, 'w', encoding='utf-8') as fp:
    json.dump(outputs, fp, ensure_ascii=False, indent=2)
    
