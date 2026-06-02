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

def batch_generator(lst, batch_size=1000):
    it = iter(lst)
    while True:
        batch = list(islice(it, batch_size))
        if not batch:
            break
        yield batch

def parse_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    core_values = []
    communication_style = []
    emotional_tone = []
    speech_patterns = []
    political_positions = []
    signature_expressions = []
    

    for obj in tqdm(content.splitlines(), desc="解析进度", unit="个对象"):
        obj = json.loads(obj)
        try:
            if obj.get('check_result') is True:
                completions = obj.get('answer', '')
                completions = json.loads(completions)
                if "core_values" in completions:
                    core_values.extend(completions["core_values"])
                if "communication_style" in completions:
                    communication_style.extend(completions["communication_style"])
                if "emotional_tone" in completions:
                    emotional_tone.extend(completions["emotional_tone"])
                if "speech_patterns" in completions:
                    speech_patterns.extend(completions["speech_patterns"])
                if "political_positions" in completions:
                    political_positions.extend(completions["political_positions"])
                if "signature_expressions" in completions:
                    signature_expressions.extend(completions["signature_expressions"])
            else:
                print(f"ID: {obj.get('id')} 的check_result不为True")
                
        except json.JSONDecodeError as e:
            print(f"解析JSON出错: {e}，内容: {obj}")
    
    core_values_path = ""
    communication_style_path = ""
    emotional_tone_path = ""
    speech_patterns_path = ""
    political_positions_path = ""
    signature_expressions_path = ""

    print("core_values start...")
    request_cluster_model(core_values, core_values_path)
    print("communication_style start...")
    request_cluster_model(communication_style, communication_style_path)
    print("emotional_tone start...")
    request_cluster_model(emotional_tone, emotional_tone_path)
    print("speech_patterns start...")
    request_cluster_model(speech_patterns, speech_patterns_path)
    print("political_positions start...")
    request_cluster_model(political_positions, political_positions_path)
    print("signature_expressions start...")
    request_cluster_model(signature_expressions, signature_expressions_path)


    
def request_cluster_model(array, output_file_path):
    print(array)
    print("原数组", len(array))
    array_embeddings = []
    client = OpenAI(api_key=apikey_list[0], base_url="")
    for i, batch in enumerate(batch_generator(array)):
        print(f"正在处理第{i+1}批数据")
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=batch,  
            dimensions=1024  
        )
        print("输出向量：", len(response.data))
        embeddings = np.array([d.embedding for d in response.data])
        array_embeddings.extend(embeddings)
    print("embeddings length:", len(array_embeddings))
    kmeans = KMeans(n_clusters=10, random_state=42)
    labels = kmeans.fit_predict(array_embeddings)  
    print(labels)  
    clusters = {}
    for label, phrase in zip(labels, array):
        python_label = int(label)
        clusters.setdefault(python_label, []).append(phrase)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(clusters, f, ensure_ascii=False, indent=2)

# 使用示例
if __name__ == "__main__":
    file_path = ""
    parse_json_file(file_path)
    
