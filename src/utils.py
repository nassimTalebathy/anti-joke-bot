import openai


PROMPT_TEXT = '\n\n###\n\n'
END_TEXT = '###'
FINE_TUNED_MODEL_NAME = 'davinci:ft-naked-2023-01-10-10-44-16'


def prep_question(q: str):
    if isinstance(q, str):
        q = q.strip()
    else:
        q = q.str.strip()
    return q + PROMPT_TEXT


def prep_answer(ans):
    if isinstance(ans, str):
        ans = ans.strip()
    else:
        ans = ans.str.strip()
    return ' ' + ans + END_TEXT


def process_answer(a: str):
    return a.strip()


def validate_input(prompt: str, api_key: str, temperature: float, max_tokens: int, mode: str):
    assert isinstance(prompt, str), "Prompt must be a str"
    assert prompt.strip() not in [' ', ''], "prompt.strip() not in [' ', '']"
    assert 4 <= len(prompt) <= 100, "4 <= len(prompt) <= 100"
    assert isinstance(api_key, str), "api_key must be a str"
    assert api_key.strip() not in [' ', ''], "api_key.strip() not in [' ', '']"
    assert 30 <= len(api_key) <= 100, "30 <= len(api_key) <= 100"
    assert 0 <= temperature <= 1, '0 <= temperature <= 1'
    assert 1 <= max_tokens <= 50, '1 <= max_tokens <= 50'
    assert mode in ['dev','prod'], "mode in ['dev','prod']"
    return


def get_punchline(
    prompt: str, api_key: str, 
    temperature: float=0.6, max_tokens:int=16, mode:str='dev',
    **kwargs
):
    # Validate input
    validate_input(prompt=prompt, api_key=api_key, temperature=temperature, max_tokens=max_tokens, mode=mode)
    kwargs = {**kwargs, 'temperature':temperature, 'max_tokens':max_tokens}
    kwargs['max_tokens'] = min(50, kwargs['max_tokens']) # cap at 50
    # set API key
    openai.api_key = api_key
    # Response
    if mode != 'prod' or mode == 'dev':
        text = 'A generic response'
    else:
        response = openai.Completion.create(
            model=FINE_TUNED_MODEL_NAME,
            prompt=prep_question(prompt),
            stop='###',
            n=1, # only 1 choice
            **kwargs,
        )
        # Process
        text = response['choices'][0]['text']
    text = process_answer(text)
    return text