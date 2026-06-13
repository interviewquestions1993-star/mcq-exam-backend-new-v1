import json
import traceback
from openai import OpenAI

client = OpenAI(base_url='http://127.0.0.1:11434/v1', api_key='ollama')
print('client created')
try:
    resp = client.chat.completions.create(
        model='phi4-mini',
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Return a JSON object with {"hello":"world"} only.'}
        ],
        temperature=0.1,
        max_tokens=120,
    )
    print('resp type', type(resp))
    print('has choices', hasattr(resp, 'choices'))
    print('choices len', len(resp.choices) if hasattr(resp, 'choices') else 'no')
    choice = resp.choices[0]
    print('choice type', type(choice))
    print('choice dir sample', [name for name in dir(choice) if name in ['message', 'text', 'content', 'index', 'finish_reason']])
    if hasattr(choice, 'message'):
        print('message type', type(choice.message))
        print('message attrs', [name for name in dir(choice.message) if name in ['content', 'role']])
        try:
            print('message.content repr', repr(choice.message.content))
        except Exception as e:
            print('message.content error', type(e), e)
    if hasattr(choice, 'content'):
        print('choice.content repr', repr(choice.content))
    if hasattr(choice, 'text'):
        print('choice.text repr', repr(choice.text))
    to_dict = resp.to_dict()
    print('resp to_dict keys', list(to_dict.keys()))
    print('resp json', json.dumps(to_dict, indent=2)[:2000])
except Exception:
    traceback.print_exc()
