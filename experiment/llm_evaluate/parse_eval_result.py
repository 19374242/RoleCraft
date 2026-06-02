import json
import re
from tqdm import tqdm  

def parse_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    num = 0
    value_total = tone_total = hallucination_total = 0
    for obj in tqdm(content.splitlines(), desc="解析进度", unit="个对象"):
        obj = json.loads(obj)
        try:
            completions = obj.get('answer', '')
            qa = re.findall(r'\{.*?\}', completions, re.DOTALL)
            value = tone = hallucination = -1
            for item in qa:
                item = item.strip('{}').strip()
                item_split = item.split("\n")
                if len(item_split) == 2:
                    q = item_split[0].split(":")
                    q[0] = q[0].strip()
                    if len(q) == 2:
                        if q[0] == "Values score":
                            value = q[1].strip().replace(',', '')
                        if q[0] == "Tone score":
                            tone = q[1].strip().replace(',', '')
                        if q[0] == "Fact score":
                            hallucination = q[1].strip().replace(',', '')
                    else:
                        print("q len error:", q)
                else:
                    print("item_split len error:", item)
            if value != -1 and tone != -1 and hallucination != -1:
                print("id:", obj.get('id', ''), "value:", value, "tone:", tone, "hallucination:", hallucination)
                num += 1
                value_total += int(value)
                tone_total += int(tone)
                hallucination_total += int(hallucination)
        except json.JSONDecodeError as e:
            print(f"解析JSON出错: {e}，内容: {obj}")

    print("value:", value_total/num, "tone:", tone_total/num, "hallucination:", hallucination_total/num)



# 使用示例
if __name__ == "__main__":
    file_path = ""
    parsed_data = parse_json_file(file_path)

