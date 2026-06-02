
from openai import OpenAI
from tqdm import tqdm
from datetime import datetime
import json
def read_file(path):
    with open(path, 'r', encoding='utf-8') as fp:
        return fp.read().strip()

question_path = ''
prompt_path = ""
prompt_origin = read_file(prompt_path)
profile_path = ""
persona_profile = read_file(profile_path)

prompt_question_path = ""
prompt_question_origin = read_file(prompt_question_path)


model_name_or_path = ""
output_path = ""
outputs = []
threads = []
with open(question_path, 'rb') as fp:
    questions = json.load(fp)
questions = questions
print(len(questions))
client = OpenAI(api_key="0",base_url="http://127.0.0.1:8133/v1")
api_key = ""
client_openai = OpenAI(
    api_key=api_key,  
    base_url="https://api.apiyi.com/v1"
)
epoch = 3
for i in tqdm(range(len(questions)), desc="处理进度", unit="个问题"):
    conversation = []
    for j in range(epoch):
        prompt = prompt_origin.format(character="", persona_profile=persona_profile, conversation=conversation)
        model_prompt = prompt + " " + questions[i]["question"]
        response1 = client.chat.completions.create(
            model = model_name_or_path,
            messages=[
                {"role": "user", "content": model_prompt},  
            ], 
            max_tokens=2048,
            temperature=0.2,
            top_p=0.95,
            n=1,
        )
        # response1 = client_openai.chat.completions.create(
        #     model = "gpt-3.5-turbo",
        #     messages=[
        #         {"role": "user", "content": model_prompt},  
        #     ], 
        #     max_tokens=2048,
        #     temperature=0.2,
        #     top_p=0.95,
        #     n=1,
        # )

        output = {
            'topic_id': questions[i]['topic_id'],
            'question': questions[i]["question"],
            'reply': response1.choices[0].message.content, 
        }

        conversation.append(output)

        if j == epoch - 1:
            break
            

        prompt_question = prompt_question_origin.format(character="", conversation=conversation)
        # print(prompt_question)

        response2 = client_openai.chat.completions.create(
            model = "gpt-4o",
            messages=[
                {"role": "user", "content": prompt_question},  
            ], 
            max_tokens=2048,
            temperature=0.2,
            top_p=0.95,
            n=1,
        )
        # print("-------------------------")
        # print(response2.choices[0].message.content)
        # print("-------------------------")
        questions[i]["question"] = response2.choices[0].message.content
    
    outputs.append(conversation)

        
with open(output_path, 'w', encoding='utf-8') as fp:
    json.dump(outputs, fp, ensure_ascii=False, indent=2)
    
