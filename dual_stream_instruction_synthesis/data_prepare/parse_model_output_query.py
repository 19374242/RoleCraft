import json
import re
from tqdm import tqdm  

def parse_json_file(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = []
    
    for obj in tqdm(content.splitlines(), desc="解析进度", unit="个对象"):
        obj = json.loads(obj)
        try:
            if obj.get('check_result') is True:
                completions = obj.get('answer', '')
                qa = re.findall(r'\{.*?\}', completions, re.DOTALL)
                for item in qa:
                    item_split = item.split(":")
                    if len(item_split) == 2:
                        result.append({
                            'q': item_split[1].strip(', ').replace('\"', ''),
                            'id': obj.get('id') 
                        })
            else:
                print(f"ID: {obj.get('id')} 的check_result不为True")
                
        except json.JSONDecodeError as e:
            print(f"解析JSON出错: {e}，内容: {obj}")
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result


# 使用示例
if __name__ == "__main__":
    file_path = ""
    output_file_path = ""
    parsed_data = parse_json_file(file_path, output_file_path)
    print(f"解析完成，共处理 {len(parsed_data)} 个有效对象")
    
