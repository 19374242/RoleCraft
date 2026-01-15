from threading import Thread, Lock
import sys
sys.path.append("../")
from utils import decoder_for_openai, load_prompt_gen_response
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

def load_existing_ids(output_path):
    """读取已存在的id，避免重复处理"""
    existing = set()
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                if 'id' in obj:
                    existing.add(obj['id'])
    except FileNotFoundError:
        # 若文件不存在，返回空集合
        pass
    except Exception as e:
        print(f"读取已有id失败: {e}")
    return existing

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
        if obj['id'] in existing_ids:
            with lock:
                progress_bar.update()
            continue

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

prompt_ds = load_prompt_gen_response()
output_path = ""
existing_ids = load_existing_ids(output_path)
print(f"已处理的id数量: {len(existing_ids)}")

progress_bar = tqdm(prompt_ds)

write_fn = partial(write_to_file, output_path=output_path, lock=file_lock)  # 冻结两个参数不变
for i in range(n_workers):
    api_idx = i % len(apikey_list)
    t = Thread(target=api_worker, args=(prompt_ds, progress_bar, progress_lock, write_fn, apikey_list[api_idx]))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()