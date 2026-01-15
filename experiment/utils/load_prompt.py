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


def load_prompt_test_question():
    questions = []
    random.seed(42)
    prompt_path = "/root/gy/role-play/speech_method/prompt/gen_test_question.txt"
    prompt = read_file(prompt_path)
    # text_path = "/root/gy/role-play/speech_method/data/test.txt"
    text_path = "/root/gy/role-play/trainable-agents/data/seed_data/profiles/wiki_Donald J. Trump.txt"
    agent_name, agent_profile = read_profile(text_path)
    for text in agent_profile:
        questions.append(prompt.format(text=text))
    prompt_ds = []
    for idx, q in enumerate(questions):
        prompt_ds.append({
            'prompt': q,
            'id': idx,
        })
    return prompt_ds



def load_prompt_llm_evaluate_single_interview():
    questions = []
    random.seed(42)
    prompt_path = ""
    prompt = read_file(prompt_path)
    text_path = ""
    profile_path = ""
    agent_name, agent_profile = read_profile(profile_path)

    with open(text_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = json.loads(content)
    print(len(content))
    prompt_ds = []
    character = ""
    for i in range(len(content)):
        id = content[i]['topic_id']
        question = content[i]['question'].strip()
        answer = content[i]['reply'].strip()
        if answer == "":
            answer = "empty"
        file = agent_profile[id]
        prompt_ds.append({
            'prompt': prompt.format(text=file, question=question, answer=answer, character=character),
            'id': id,
        })
    return prompt_ds


def load_prompt_llm_evaluate_multi_interview():
    questions = []
    random.seed(42)
    prompt_path = ""
    prompt = read_file(prompt_path)
    text_path = ''
    profile_path = ""
    persona_profile = read_file(profile_path)

    with open(text_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = json.loads(content)
    print(len(content))
    prompt_ds = []
    character = "Trump"
    for i in range(len(content)):
        id = content[i][0]['topic_id']
        prompt_ds.append({
            'prompt': prompt.format(conversation=content[i], persona_profile=persona_profile),
            'id': id,
        })
    return prompt_ds


def load_prompt_llm_evaluate_challenge_interview():
    questions = []
    random.seed(42)
    prompt_path = ""
    prompt = read_file(prompt_path)
    text_path = ''
    profile_path = ""
    persona_profile = read_file(profile_path)

    with open(text_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = json.loads(content)
    print(len(content))
    prompt_ds = []
    character = ""
    for i in range(len(content)):
        id = content[i]['topic_id']
        question = content[i]['question'].strip()
        answer = content[i]['reply'].strip()
        prompt_ds.append({
            'prompt': prompt.format(character=character, question=question, answer=answer, persona_profile=persona_profile),
            'id': id,
        })
    return prompt_ds


