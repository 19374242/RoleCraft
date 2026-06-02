from openai import OpenAI

def get_output(res):
    out = res.message.content
    if res.finish_reason != 'stop':
        out += '<|NONSTOP|>'
    return out

def decoder_for_openai(model_name, input, max_tokens, temperature=0.7, top_p=0.95, apikey=None, n=1, stop=None, sys_prompt=None):
    frequency_penalty = 0
    presence_penalty = 0
    if sys_prompt:
        sys_prompt_content = sys_prompt
    else:
        sys_prompt_content = "You are a helpful assistant."
    
    client = OpenAI(api_key=apikey, base_url="https://api.apiyi.com/v1")

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

    if n == 1:
        return get_output(response.choices[0])
    print([get_output(res) for res in response.choices])
    return [get_output(res) for res in response.choices]