import json
import random, re
from tqdm import tqdm 

def read_file(path):
    with open(path, 'r', encoding='utf-8') as fp:
        return fp.read().strip()

def read_profile(path):
    with open(path, 'r', encoding='utf-8') as fp:
        text = fp.read().strip()
    parts = text.split('\n\n')
    assert parts[0].startswith('# '), parts[0]
    agent_name = parts[0].replace('#', '').strip()
    agent_profile = []
    for p in parts[1:]:
        agent_profile.append(p.strip())
    return agent_name, agent_profile

def read_answer(path):
    with open(path, 'r', encoding='utf-8') as fp:
        content = fp.read()
    json_objects = re.findall(r'\{.*?\}', content, re.DOTALL)
    return json_objects


def load_data():
    questions = []
    random.seed(42)
    prompt_path = ""
    prompt = read_file(prompt_path)
    text_path = 'alpaca_train.jsonl'

    with open(text_path, 'r', encoding='utf-8') as f:
        content = f.read()

    prompt_ds = []
    for obj in tqdm(content.splitlines(), desc="解析进度", unit="个对象"):
        obj = json.loads(obj)
        id = obj['id']
        instruction = obj['instruction'].strip()
        output = obj['output'].strip()
        prompt_ds.append({
            'prompt': prompt.format(question=instruction, answer=output),
            'id': id,
            'instruction': instruction
        })
    print(len(prompt_ds))
    return prompt_ds

def load_prompt_gen_query():
    questions = []
    random.seed(42)
    prompt_path = ""
    prompt = read_file(prompt_path)
    profile_path = ""
    persona_profile = read_file(profile_path)
    text_path = ""
    agent_name, agent_profile = read_profile(text_path)
    for text in agent_profile:
        questions.append(prompt.format(segment=text, character=""))
    prompt_ds = []
    for idx, q in enumerate(questions):
        prompt_ds.append({
            'prompt': q,
            'id': idx,
        })
    return prompt_ds


def load_prompt_gen_response():
    questions = []
    random.seed(42)
    prompt_path = ""
    prompt = read_file(prompt_path)
    profile_path = ""
    persona_profile = read_file(profile_path)
    text_path = ""
    q = ""
    qs = read_file(q)
    agent_name, agent_profile = read_profile(text_path)
    for text in agent_profile:
        questions.append(prompt.format(segment=text, persona_profile=persona_profile, character="", questions=qs))
    prompt_ds = []
    for idx, q in enumerate(questions):
        prompt_ds.append({
            'prompt': q,
            'id': idx,
        })
    return prompt_ds


