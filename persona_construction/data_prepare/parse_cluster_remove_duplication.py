import json
import re
from tqdm import tqdm  # 导入进度条库
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
            # 统计次数
            for item in content[key]:
                if item in count_dict:
                    count_dict[item] += 1
                else:
                    count_dict[item] = 1
                    
            # 2. 过滤掉次数为1的元素
            filtered_dict = {item: count for item, count in count_dict.items() if count > 1}
            result[key] = filtered_dict  # 只保留次数>1的元素
    
    # 转换为JSON格式字符串（便于查看或存储）
    result_json = json.dumps(result, ensure_ascii=False, indent=2)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result_json)

parse_json_file(core_values_path, core_values_set_path)
parse_json_file(communication_style_path, communication_style_set_path)
parse_json_file(emotional_tone_path, emotional_tone_set_path)
parse_json_file(speech_patterns_path, speech_patterns_set_path)
parse_json_file(stance_orientation_path, stance_orientation_set_path)
parse_json_file(signature_expressions_path, signature_expressions_set_path)