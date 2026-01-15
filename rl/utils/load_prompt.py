import json
import random, re

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


def load_prompt_score():
    questions = []
    random.seed(42)
    prompt_path = ""
    prompt = read_file(prompt_path)
    text_path = ""
    json_objects = read_answer(text_path)
    profile_path = ""
    persona_profile = read_file(profile_path)
    for text in json_objects:
        text = json.loads(text)
        questions.append({
            "prompt": prompt.format(text=text['reply'], persona_profile=persona_profile, character=""),
            "question": text['question'],
            "reply": text['reply'],
        })

    prompt_ds = []
    for idx, q in enumerate(questions):
        prompt_ds.append({
            'prompt': q["prompt"],
            'id': idx,
            "question": q["question"],
            "reply": q['reply'],
        })
    return prompt_ds

def load_prompt_dpo_data():
    questions = []
    random.seed(42)
    prompt_path = ""
    prompt = read_file(prompt_path)
    text_path = ""
    json_objects = read_answer(text_path)
    profile_path = ""
    persona_profile = read_file(profile_path)
    for text in json_objects:
        text = json.loads(text)
        questions.append({
            "prompt": prompt.format(text=text['reply'], persona_profile=persona_profile, character=""),
            "question": text['question'],
            "reply": text['reply'],
        })

    prompt_ds = []
    for idx, q in enumerate(questions):
        prompt_ds.append({
            'prompt': q["prompt"],
            'id': idx,
            "question": q["question"],
            "reply": q['reply'],
        })
    return prompt_ds


def write_to_file(obj, output_path):
    with open(output_path, 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(obj, ensure_ascii=False, indent=2))


