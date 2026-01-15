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


def load_prompt_profile():
    questions = []
    random.seed(42)
    prompt_path = ""
    prompt = read_file(prompt_path)
    text_path = ""
    agent_name, agent_profile = read_profile(text_path)
    for text in agent_profile:
        questions.append(prompt.format(text=text))
    prompt_ds = []
    for idx, q in enumerate(questions):
        prompt_ds.append({
            'prompt': q,
            'id': idx,
        })
        # break
    return prompt_ds

def load_prompt_assemble_profile():
    questions = []
    random.seed(42)
    prompt_path = ""
    prompt = read_file(prompt_path)

    core_values_set_path = ""
    communication_style_set_path = ""
    emotional_tone_set_path = ""
    speech_patterns_set_path = ""
    stance_orientation_set_path = ""
    signature_expressions_set_path = ""
    core_values = read_file(core_values_set_path)
    communication_style = read_file(communication_style_set_path)
    emotional_tone = read_file(emotional_tone_set_path)
    speech_patterns = read_file(speech_patterns_set_path)
    stance_orientation = read_file(stance_orientation_set_path)
    signature_expressions = read_file(signature_expressions_set_path)

    questions.append(prompt.format(core_values=core_values, communication_style=communication_style, emotional_tone=emotional_tone, speech_patterns=speech_patterns, stance_orientation=stance_orientation, signature_expressions=signature_expressions))
    prompt_ds = []
    for idx, q in enumerate(questions):
        prompt_ds.append({
            'prompt': q,
            'id': idx,
        })
    return prompt_ds


def write_to_file(obj, output_path):
    with open(output_path, 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(obj, ensure_ascii=False, indent=2))



