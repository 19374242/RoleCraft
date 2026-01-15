import json
import random

def shuffle_jsonl_file(input_file: str, output_file: str = None):
    if output_file is None:
        output_file = input_file
    
    data_list = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:  
                continue
            try:
                data = json.loads(line)
                data_list.append(data)
            except json.JSONDecodeError as e:
                print(f"警告：第 {line_num} 行 JSON 格式错误，已跳过 → {e}")
    
    random.shuffle(data_list)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for data in data_list:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    print(f"✅ 完成！共处理 {len(data_list)} 条数据，已打乱并写入 {output_file}")

if __name__ == "__main__":
    input_path = ""
    output_path = ""
    shuffle_jsonl_file(input_path, output_path)