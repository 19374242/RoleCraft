import json
import re
from tqdm import tqdm 

def read_file(path):
    with open(path, 'r', encoding='utf-8') as fp:
        return fp.read().strip()
    

def parse_json_file(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = []
    
    for obj in tqdm(content.splitlines(), desc="解析进度", unit="个对象"):
        obj = json.loads(obj)
        try:
            if obj.get('check_result') is True:
                question = obj.get('question', '')
                reply = obj.get('reply', '')
                query = obj.get('query', '')
                query = json.loads(query)
                score = query["score"]
                
                if float(score) > 0.7:
                    continue

                result.append({
                            'prompt': prompt + question,
                            'reply': reply,
                            'score': score
                })
            else:
                print(f"ID: {obj.get('id')} 的check_result不为True")
                
        except json.JSONDecodeError as e:
            print(f"解析JSON出错: {e}，内容: {obj}")
    

    for item in result:
        with open(output_file_path, 'a', encoding='utf-8') as fp:
            fp.write(json.dumps(item, ensure_ascii=False) + "\n")


    return result


# 使用示例
if __name__ == "__main__":
    file_path = ""
    output_file_path = ""
    parsed_data = parse_json_file(file_path, output_file_path)
    print(f"解析完成，共处理 {len(parsed_data)} 个有效对象")
    
