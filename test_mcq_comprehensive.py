import requests
import json

print('COMPREHENSIVE MCQ API TEST')
print('=' * 70)
print()

# Test with different topics
topics = [
    {'topic': 'React', 'num': 2},
    {'topic': 'Python', 'num': 2},
    {'topic': 'JavaScript', 'num': 2},
]

for test in topics:
    print('Testing:', test['topic'], '(' + str(test['num']) + ' questions)')
    try:
        resp = requests.post('http://localhost:8000/api/mcq/generate',
            json={'topic': test['topic'], 'num_questions': test['num']},
            timeout=120
        )
        if resp.status_code == 200:
            data = resp.json()
            print('  Status: SUCCESS')
            print('  Generated:', len(data['questions']), 'questions')
            for q in data['questions']:
                q_text = q['question']
                if len(q_text) > 60:
                    q_text = q_text[:60] + '...'
                print('    Q' + str(q['id']) + ':', q_text)
            print()
        else:
            print('  Error:', resp.json())
            print()
    except Exception as e:
        print('  Exception:', str(e))
        print()

print('=' * 70)
print('MCQ API TEST COMPLETE!')
