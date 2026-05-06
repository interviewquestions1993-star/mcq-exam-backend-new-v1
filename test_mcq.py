import requests
import json

print('TESTING MCQ API ENDPOINT')
print('=' * 70)
print()

# Test MCQ generation
print('Testing POST /api/mcq/generate')
print('Topic: Angular, Questions: 3')
print()

try:
    response = requests.post('http://localhost:8000/api/mcq/generate',
        json={'topic': 'Angular', 'num_questions': 3},
        timeout=120
    )
    print('Status:', response.status_code)
    print()
    
    if response.status_code == 200:
        data = response.json()
        print('Generated', data['num_questions'], 'questions on', data['topic'])
        print()
        
        for q in data['questions']:
            q_text = q['question']
            if len(q_text) > 80:
                q_text = q_text[:80] + '...'
            print('Q' + str(q['id']) + ':', q_text)
            for opt in q['options']:
                print('   ' + opt)
            print('   Answer:', q['correct_answer'], '(' + q['difficulty'] + ')')
            expl = q['explanation']
            if len(expl) > 80:
                expl = expl[:80] + '...'
            print('   Explanation:', expl)
            print()
    else:
        error_data = response.json()
        print('Error:', error_data)
        
except Exception as e:
    print('Exception:', str(e))
    import traceback
    traceback.print_exc()
