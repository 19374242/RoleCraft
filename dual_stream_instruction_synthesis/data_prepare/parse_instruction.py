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
                obj["input"] = ""
                result.append(obj)
            else:
                print(f"ID: {obj.get('id')} 的check_result不为True")
                
        except json.JSONDecodeError as e:
            print(f"解析JSON出错: {e}，内容: {obj}")
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for item in result:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')  

    return result


# 使用示例
if __name__ == "__main__":
    file_path = ""
    output_file_path = ""
    parsed_data = parse_json_file(file_path, output_file_path)
    print(f"解析完成，共处理 {len(parsed_data)} 个有效对象")
    
