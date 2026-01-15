from threading import Thread, Lock
import sys
sys.path.append("../")
from utils import decoder_for_openai, load_prompt_profile
from tqdm import tqdm
import json
from functools import partial
from apikeys import apikey_list

threads = []
# n_workers = 16
n_workers = 16
progress_lock = Lock()
file_lock = Lock()
current_idx = 0

def check_result(text):
    return len(text) > 0

def api_worker(dataset, progress_bar, lock, write_fn, apikey):
    global current_idx
    cur_task_done_retry = 0
    while True:
        if cur_task_done_retry <= 0:
            with lock:
                idx = current_idx
                current_idx += 1
            if idx >= len(dataset):
                break
        obj = dataset[idx]
        prompt = obj['prompt']
        completion = ''
        try:
            completion = decoder_for_openai("gpt-4o", prompt, max_tokens=None, temperature=0.7, n=1, sys_prompt=None, apikey=apikey)
        except Exception as e:
            print(repr(e))
            cur_task_done_retry = 100
        assert isinstance(completion, str), type(completion)
        obj['answer'] = completion
        res = check_result(completion)
        obj['check_result'] = res
        obj.pop('prompt', None)
        
        if not res:
            cur_task_done_retry += 1
            if cur_task_done_retry > 3:  # 3
                obj['retry_time'] = cur_task_done_retry
                write_fn(obj)
                print(f'failed for index {idx}')
                with lock:
                    progress_bar.update()
                cur_task_done_retry = 0
            continue
        else:
            obj['retry_time'] = cur_task_done_retry + 1
            cur_task_done_retry = 0
            write_fn(obj)
            with lock:
                progress_bar.update()

def write_to_file(obj, output_path, lock):
    with lock:
        with open(output_path, 'a', encoding='utf-8') as fp:
            fp.write(json.dumps(obj, ensure_ascii=False) + "\n")

prompt_ds = load_prompt_profile()
progress_bar = tqdm(prompt_ds)
output_path = ""
write_fn = partial(write_to_file, output_path=output_path, lock=file_lock)  # 冻结两个参数不变
for i in range(n_workers):
    api_idx = i % len(apikey_list)
    t = Thread(target=api_worker, args=(prompt_ds, progress_bar, progress_lock, write_fn, apikey_list[api_idx]))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()



# 样例：

# 输出短语
# {
#   "core_values / 核心价值观": [
#     "America First / 美国优先",
#     "Sovereignty / 国家主权",
#     "Security / 安全保障",
#     "Justice / 正义公平",
#     "Prosperity / 繁荣发展",
#     "Freedom / 自由权利",
#     "Patriotism / 爱国主义",
#     "National Success / 国家成功",
#     "Unity / 团结统一",
#     "Liberty / 自由自主",
#     "Competence / 胜任能力",
#     "Loyalty / 忠诚守信",
#     "Fairness / 公平公正",
#     "Law and Order / 法律与秩序"
#   ],
#   "communication_style / 沟通风格": [
#     "Confident / 自信果断",
#     "Optimistic / 乐观积极",
#     "Assertive / 坚定有力",
#     "Repetitive / 重复强调",
#     "Inspiring / 鼓舞人心",
#     "Authoritative / 权威主导",
#     "Emphatic / 语气强烈",
#     "Nationalistic / 民族主义"
#   ],
#   "emotional_tone / 情感基调": [
#     "Hopeful / 充满希望",
#     "Determined / 意志坚定",
#     "Proud / 自豪骄傲",
#     "Passionate / 饱含热情",
#     "Resolute / 坚定不移",
#     "Grateful / 心怀感激",
#     "Compassionate / 富有同情心"
#   ],
#   "speech_patterns / 言语模式": [
#     "Rhetorical questions / 反问修辞",
#     "Repetition for emphasis / 重复强调",
#     "Patriotic references / 爱国相关表述",
#     "Historical references / 历史相关引用",
#     "Bold promises / 大胆承诺",
#     "Challenges to the status quo / 挑战现状",
#     "Strong declarations of intent / 明确意图宣告",
#     "Acknowledgment of supporters / 致谢支持者",
#     "Declaring victories / 宣告胜利",
#     "Visual imagery / 视觉意象描绘"
#   ],
#   "political_positions / 政治立场": [
#     "Tough on immigration / 强硬对待移民",
#     "Anti-corruption / 反对腐败",
#     "America-centric policies / 以美国为中心的政策",
#     "Economic protectionism / 经济保护主义",
#     "Energy independence / 能源独立",
#     "Military strength / 军事力量强化",
#     "Opposition to censorship / 反对审查制度",
#     "Traditional values / 传统价值观",
#     "Law enforcement support / 支持执法部门",
#     "Anti-globalism / 反全球化"
#   ],
#   "signature_expressions / 标志性表达": [
#     "Make America Great Again / 让美国再次伟大",
#     "Drill, baby, drill / 钻吧，宝贝，钻吧（支持能源开采）",
#     "America First / 美国优先",
#     "Common sense / 常识判断",
#     "Law and order / 法律与秩序",
#     "Free speech / 言论自由",
#     "Proud American / 自豪的美国人",
#     "Unity under God / 上帝之下的团结",
#     "Liberation Day / 解放日",
#     "Golden Age of America / 美国黄金时代"
#   ]
# }

# 对输出无要求
# {
#   "core_values / 核心价值观": [
#     "America First / 美国优先",
#     "Sovereignty / 国家主权",
#     "Safety / 安全保障",
#     "Prosperity / 繁荣发展",
#     "Freedom / 自由权利",
#     "National Success / 国家成功",
#     "Honesty / 诚实守信",
#     "Challenges / 勇于挑战",
#     "Patriotism / 爱国主义",
#     "Faith / 信念信仰",
#     "Unity / 团结统一",
#     "Excellence / 追求卓越",
#     "Success / 成功成就",
#     "Courage / 勇气胆识",
#     "Vigor / 活力干劲",
#     "Compassion / 同情心"
#   ],
#   "communication_style / 沟通风格": [
#     "Confident / 自信果断",
#     "Optimistic / 乐观积极",
#     "Assertive / 坚定有力",
#     "Patriotic / 爱国热忱",
#     "Inspirational / 鼓舞人心",
#     "Authoritative / 权威主导",
#     "Emphatic / 语气强烈",
#     "Repetitive / 重复强调",
#     "Direct / 直截了当",
#     "Persuasive / 富有说服力"
#   ],
#   "emotional_tone / 情感基调": [
#     "Hopeful / 充满希望",
#     "Determined / 意志坚定",
#     "Proud / 自豪骄傲",
#     "Grateful / 心怀感激",
#     "Passionate / 饱含热情",
#     "Resolute / 坚定不移",
#     "Optimistic / 乐观向上",
#     "Resilient / 坚韧不拔",
#     "Energetic / 精力充沛",
#     "Defiant / 桀骜不驯"
#   ],
#   "speech_patterns / 言语模式": [
#     "Rhetorical questions / 反问修辞",
#     "Lists of accomplishments / 罗列成就",
#     "Promise of rapid change / 承诺快速变革",
#     "Promising a better future / 承诺美好未来",
#     "Condemnation of past failures / 谴责过往失误",
#     "Vivid descriptions / 生动描述",
#     "Historical references / 历史引用",
#     "Appeal to patriotism / 诉诸爱国情怀",
#     "Challenging the status quo / 挑战现状",
#     "Reiteration of key messages / 重申核心信息"
#   ],
#   "political_positions / 政治立场": [
#     "Tough stance on immigration / 强硬的移民立场",
#     "National security focus / 聚焦国家安全",
#     "Economic protectionism / 经济保护主义",
#     "Anti-globalist policies / 反全球化政策",
#     "Law and order emphasis / 强调法律与秩序",
#     "Energy independence / 能源独立",
#     "Education reform / 教育改革",
#     "Military strength and focus / 重视军事力量",
#     "Anti-censorship / 反对审查制度",
#     "Traditional gender views / 传统性别观念"
#   ],
#   "signature_expressions / 标志性表达": [
#     "Make America Great Again / 让美国再次伟大",
#     "Drill, baby, drill / 钻吧，宝贝，钻吧（支持能源开采）",
#     "America First / 美国优先",
#     "We will win like never before / 我们将赢得前所未有的胜利",
#     "Thank you, God bless America / 谢谢大家，上帝保佑美国",
#     "Freedom, sovereignty, independence / 自由、主权、独立",
#     "The impossible is what we do best / 我们最擅长做不可能的事",
#     "From this day on / 从今天起",
#     "God bless America / 上帝保佑美国",
#     "Our golden age has just begun / 我们的黄金时代才刚刚开始"
#   ]
# }