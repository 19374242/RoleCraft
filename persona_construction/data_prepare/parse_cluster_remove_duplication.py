import json
import re
from tqdm import tqdm  
from sklearn.cluster import KMeans
import sys
sys.path.append("../")
from openai import OpenAI
from apikeys import apikey_list
import numpy as np
from itertools import islice


core_values_path = ""
communication_style_path = ""
emotional_tone_path = ""
speech_patterns_path = ""
stance_orientation_path = ""
signature_expressions_path = ""

core_values_set_path = ""
communication_style_set_path = ""
emotional_tone_set_path = ""
speech_patterns_set_path = ""
stance_orientation_set_path = ""
signature_expressions_set_path = ""


def parse_json_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = json.loads(content)
    
    result = {}
    for key in content:
        if isinstance(content[key], list):
            count_dict = {}
            for item in content[key]:
                if item in count_dict:
                    count_dict[item] += 1
                else:
                    count_dict[item] = 1
                    
            total_count = sum(count_dict.values())
            if total_count < 50:
                print(f"聚类 {key} 样本总数 {total_count} < 50，整体剔除")
                continue
            filtered_dict = {item: count for item, count in count_dict.items() if count >= 10}
            if not filtered_dict:
                print(f"聚类 {key} 过滤后无属性，跳过")
                continue
            result[key] = filtered_dict
    
    result_json = json.dumps(result, ensure_ascii=False, indent=2)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result_json)

parse_json_file(core_values_path, core_values_set_path)
parse_json_file(communication_style_path, communication_style_set_path)
parse_json_file(emotional_tone_path, emotional_tone_set_path)
parse_json_file(speech_patterns_path, speech_patterns_set_path)
parse_json_file(stance_orientation_path, stance_orientation_set_path)
parse_json_file(signature_expressions_path, signature_expressions_set_path)