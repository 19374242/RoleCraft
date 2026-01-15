import json
import re
from tqdm import tqdm  # 导入进度条库

def parse_json_file(file_path, output_file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = []
    # 使用tqdm添加进度条，total参数指定总任务数
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
            # 每个元素单独转JSON并换行
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')  # 每行一条数据

    return result


# 使用示例
if __name__ == "__main__":
    file_path = ""
    output_file_path = ""
    parsed_data = parse_json_file(file_path, output_file_path)
    # print(parsed_data)
    print(f"解析完成，共处理 {len(parsed_data)} 个有效对象")
    
