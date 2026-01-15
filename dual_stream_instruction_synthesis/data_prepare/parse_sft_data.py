import json
import re
from tqdm import tqdm  # 导入进度条库

def read_file(path):
    with open(path, 'r', encoding='utf-8') as fp:
        return fp.read().strip()

def parse_json_file_three_dimension(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = json.loads(content)
    result = []
    profile_path = ""
    persona_profile = read_file(profile_path)
    prompt_path = ""
    prompt = read_file(prompt_path)
    prompt = prompt.format(character="", persona_profile=persona_profile)
    
    # 使用tqdm添加进度条，total参数指定总任务数
    for obj in tqdm(content, desc="解析进度", unit="个对象"):
        try:
            q = obj.get('q', '')
            a = obj.get('a', '')
            id = obj.get('id', '')
            q = prompt + q
            # if len(a) < 50:
            #     continue
            result.append({
                'instruction': q,
                'input': "",
                'output': a,
                'data_from': "1",
                'id': id
            })
                
        except json.JSONDecodeError as e:
            print(f"解析JSON出错: {e}，内容: {obj}")
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for item in result:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    return result


def parse_json_file_profile(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    result = []
    profile_path = ""
    persona_profile = read_file(profile_path)
    prompt_path = ""
    prompt = read_file(prompt_path)
    prompt = prompt.format(character="", persona_profile=persona_profile)
    
    for obj in tqdm(content.splitlines(), desc="解析进度", unit="个对象"):
        obj = json.loads(obj)
        try:
            q = obj.get('question', '')
            a = obj.get('answer', '')
            id = obj.get('id', '')
            q = prompt + q
            # if len(a) < 50:
            #     continue
            result.append({
                'instruction': q,
                'input': "",
                'output': a,
                'data_from': "2",
                'id': id
            })
                
        except json.JSONDecodeError as e:
            print(f"解析JSON出错: {e}，内容: {obj}")
    
    with open(output_file_path, 'a', encoding='utf-8') as f:
        for item in result:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    return result


def parse_json_file_profile_alpaca(file_path, output_file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    result = []

    # 使用tqdm添加进度条，total参数指定总任务数
    for obj in tqdm(content.splitlines(), desc="解析进度", unit="个对象"):
        obj = json.loads(obj)
        try:
            q = obj.get('instruction', '')
            a = obj.get('output', '')
            id = obj.get('id', '')

            result.append({
                'instruction': q,
                'input': "",
                'output': a,
                'data_from': "2",
                'id': id
            })
                
        except json.JSONDecodeError as e:
            print(f"解析JSON出错: {e}，内容: {obj}")
    
    with open(output_file_path, 'a', encoding='utf-8') as f:
        for item in result:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    return result
-

def parse_json_file_profile_alpaca_modify_instruction(file_path, output_file_path):
    profile_path = ""
    persona_profile = read_file(profile_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    result = []

    for obj in tqdm(content.splitlines(), desc="解析进度", unit="个对象"):
        obj = json.loads(obj)
        try:
            q = obj.get('instruction', '')
            a = obj.get('output', '')
            id = obj.get('id', '')

            pattern = r'(?<=Persona Description:).*?(?=Example output:)'
            q= re.sub(pattern, "\n" + persona_profile + "\n\n", q, flags=re.DOTALL)



            result.append({
                'instruction': q,
                'input': "",
                'output': a,
                'data_from': "2",
                'id': id
            })
                
        except json.JSONDecodeError as e:
            print(f"解析JSON出错: {e}，内容: {obj}")
    
    result = result[:10619]
    with open(output_file_path, 'a', encoding='utf-8') as f:
        for item in result:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    return result


# 使用示例
if __name__ == "__main__":
    file_path = ""
    output_file_path = ""
    parsed_data1 = parse_json_file_three_dimension(file_path, output_file_path)
    print(f"解析完成，共处理 {len(parsed_data1)} 个有效对象")
    file_path_profile = "/root/gy/role-play/opencharacter/opencharacter_sft_data_no_empty.jsonl"
    parsed_data2 = parse_json_file_profile_alpaca_modify_instruction(file_path_profile, output_file_path)
    print(f"解析完成，共处理 {len(parsed_data2)} 个有效对象")
    print(f"解析完成，共处理 {len(parsed_data1 + parsed_data2)} 个有效对象")

    
