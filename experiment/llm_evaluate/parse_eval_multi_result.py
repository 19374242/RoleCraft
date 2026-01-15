import json
import re
from tqdm import tqdm  # 导入进度条库

def parse_json_file(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    num = 0
    Persona_Consistency_Across_Turns_Score_total = 0
    # 使用tqdm添加进度条，total参数指定总任务数
    for obj in tqdm(content.splitlines(), desc="解析进度", unit="个对象"):
        obj = json.loads(obj)
        try:
            # 获取completions字段并处理
            completions = obj.get('answer', '')
            qa = re.findall(r'\{.*?\}', completions, re.DOTALL)
            Persona_Consistency_Across_Turns_Score = -1
            for item in qa:
                item = item.strip('{}').strip()
                item_split = item.split("\n")
                if len(item_split) == 2:
                    q = item_split[0].split(":")
                    q[0] = q[0].strip()
                    if len(q) == 2:
                        if q[0] == "Persona Consistency Across Turns Score":
                            Persona_Consistency_Across_Turns_Score = q[1].strip().replace(',', '')
                    else:
                        print("q len error:", q)
                else:
                    print("item_split len error:", item)
            if Persona_Consistency_Across_Turns_Score != -1:
                print("id:", obj.get('id', ''), "Persona Consistency Across Turns Score:", Persona_Consistency_Across_Turns_Score)
                num += 1
                Persona_Consistency_Across_Turns_Score_total += int(Persona_Consistency_Across_Turns_Score)
        except json.JSONDecodeError as e:
            print(f"解析JSON出错: {e}，内容: {obj}")

    print("Persona_Consistency_Across_Turns_Score:", Persona_Consistency_Across_Turns_Score_total/num, "nums", num)



# 使用示例
if __name__ == "__main__":
    file_path = ""
    parsed_data = parse_json_file(file_path)

