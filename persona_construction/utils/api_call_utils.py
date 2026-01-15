from openai import OpenAI

def get_output(res):
    out = res.message.content
    if res.finish_reason != 'stop':
        # print(res.finish_reason)
        out += '<|NONSTOP|>'
    return out

# @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_never)
def decoder_for_openai(model_name, input, max_tokens, temperature=0.7, top_p=0.95, apikey=None, n=1, stop=None, sys_prompt=None):
    frequency_penalty = 0
    presence_penalty = 0
    if sys_prompt:
        sys_prompt_content = sys_prompt
    else:
        sys_prompt_content = "You are a helpful assistant."
    
    # 初始化OpenAI客户端
    client = OpenAI(api_key=apikey, base_url="https://api.apiyi.com/v1")
    # client = OpenAI(api_key=apikey, base_url="http://192.168.10.131:8000/v1")
    # client = OpenAI(api_key=apikey, base_url="https://openrouter.ai/api/v1")

    # 调用最新版聊天接口
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": sys_prompt_content},
            {"role": "user", "content": input},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        n=n,
        stop=stop,
    )

    # 处理响应结果（注意新版响应是对象属性访问，而非字典键访问）
    if n == 1:
        return get_output(response.choices[0])
    print([get_output(res) for res in response.choices])
    return [get_output(res) for res in response.choices]

def get_output_with_logits(res):
    out = res.message.content
    token_logprobs = []
    # res.logprobs.content 是一个 token 对象列表，每个对象包含 token, logprob, top_logprobs 等
    if hasattr(res, "logprobs") and res.logprobs and hasattr(res.logprobs, "content"):
        for t in res.logprobs.content:
            # 转换成可序列化字典
            item = {
                "token": getattr(t, "token", None),
                "logprob": getattr(t, "logprob", None),
                "top_logprobs": None
            }
            # top_logprobs 也是一组 token-logprob 对，应转化成普通字典
            if hasattr(t, "top_logprobs") and t.top_logprobs is not None:
                if isinstance(t.top_logprobs, list):
                    item["top_logprobs"] = [
                        {"token": getattr(x, "token", None), "logprob": getattr(x, "logprob", None)}
                        for x in t.top_logprobs
                    ]
                elif isinstance(t.top_logprobs, dict):
                    item["top_logprobs"] = {
                        k: v for k, v in t.top_logprobs.items()
                    }
            token_logprobs.append(item)
    if res.finish_reason != 'stop':
        # print(res.finish_reason)
        out += '<|NONSTOP|>'
    return out, token_logprobs

# @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_never)
def decoder_for_openai_with_logits(model_name, input, max_tokens, temperature=0.7, top_p=0.95, apikey=None, n=1, stop=None, sys_prompt=None):
    frequency_penalty = 0
    presence_penalty = 0
    if sys_prompt:
        sys_prompt_content = sys_prompt
    else:
        sys_prompt_content = "You are a helpful assistant."
    
    # 初始化OpenAI客户端
    client = OpenAI(api_key=apikey, base_url="https://api.apiyi.com/v1")
    # client = OpenAI(api_key=apikey, base_url="http://192.168.10.131:8000/v1")
    # client = OpenAI(api_key=apikey, base_url="https://openrouter.ai/api/v1")

    # 调用最新版聊天接口
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": sys_prompt_content},
            {"role": "user", "content": input},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        n=n,
        stop=stop,
        logprobs=True,
        top_logprobs=5
    )

    # 处理响应结果（注意新版响应是对象属性访问，而非字典键访问）
    if n == 1:
        return get_output_with_logits(response.choices[0])
    return "", []