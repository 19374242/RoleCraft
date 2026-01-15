import json
import re
from tqdm import tqdm  # 导入进度条库
import textwrap

def parse_json_file(file_path, output_file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    

    content = json.loads(content)
    if content.get('check_result') is True:
        # 获取completions字段并处理
        completions = content.get('answer', '')
        completions = json.loads(completions)
        Character_Overview = completions["Character_Overview"]
        Personality_Summary = completions["Personality_Summary"]
        Core_Values = completions["Core_Values"]
        Communication_Style = completions["Communication_Style"]
        Emotional_Tone = completions["Emotional_Tone"]
        Common_Topics = completions["Common_Topics"]
        Signature_Expressions = completions["Signature_Expressions"]
        Roleplay_Guidelines = completions["Roleplay_Guidelines"]
        
    else:
        print(f"ID: {content.get('id')} 的check_result不为True")

    # textwrap保证每行顶格写
    profile = textwrap.dedent(f"""
        === Donald Trump Persona Profile ===

        Character Overview:
        {Character_Overview.strip()}

        Personality Summary:
        {Personality_Summary.strip()}

        Core Values:
        {Core_Values.strip()}

        Communication Style:
        {Communication_Style.strip()}

        Emotional Tone:
        {Emotional_Tone.strip()}

        Common Topics:
        {Common_Topics.strip()}

        Signature Expressions:
        {Signature_Expressions.strip()}

        Roleplay Guidelines:
        {Roleplay_Guidelines.strip()}
    """).strip()

                
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(profile)



# 使用示例
if __name__ == "__main__":
    file_path = "/root/gy/role-play/user_profile/result/assemble_final_user_profile_model_output.jsonl"
    output_file_path = "/root/gy/role-play/user_profile/profile/profile.txt"
    parse_json_file(file_path, output_file_path)

    
