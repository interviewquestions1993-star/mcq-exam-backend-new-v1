"""
MCQ API Client Examples
Shows how to use the MCQ API in different scenarios
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# ============================================================================
# EXAMPLE 1: Generate MCQ questions for a topic
# ============================================================================
def get_mcq_questions(topic: str, num_questions: int = 5, difficulty: str = None):
    """
    Generate MCQ questions for a given topic
    
    Args:
        topic: Topic name (e.g., "Angular", "React", "Python")
        num_questions: Number of questions to generate
        difficulty: "easy", "medium", "hard", or None for mixed
    
    Returns:
        List of questions or None if failed
    """
    try:
        response = requests.post(
            f"{BASE_URL}/api/mcq/generate",
            json={
                "topic": topic,
                "num_questions": num_questions,
                "difficulty": difficulty
            },
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json()['questions']
        else:
            print(f"Error: {response.json()}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None


# ============================================================================
# EXAMPLE 2: Display questions in a quiz format
# ============================================================================
def display_quiz(topic: str, num_questions: int = 3):
    """Display a quiz with questions from a topic"""
    print(f"\n{'=' * 70}")
    print(f"QUIZ: {topic.upper()}")
    print(f"{'=' * 70}\n")
    
    questions = get_mcq_questions(topic, num_questions)
    
    if not questions:
        print("Failed to generate questions")
        return
    
    user_answers = []
    
    for q in questions:
        print(f"Q{q['id']}: {q['question']}")
        for i, opt in enumerate(q['options'], 1):
            print(f"   {opt}")
        
        # Get user input
        while True:
            ans = input("Your answer (A/B/C/D): ").strip().upper()
            if ans in ['A', 'B', 'C', 'D']:
                user_answers.append({'q_id': q['id'], 'answer': ans})
                break
            print("Invalid input. Please enter A, B, C, or D")
        print()
    
    # Calculate score
    score = sum(1 for a in user_answers if a['answer'] == 
                next(q for q in questions if q['id'] == a['q_id'])['correct_answer'])
    
    print(f"{'=' * 70}")
    print(f"Your Score: {score}/{len(questions)}")
    print(f"{'=' * 70}\n")
    
    # Show explanations
    for i, q in enumerate(questions):
        user_ans = next(a['answer'] for a in user_answers if a['q_id'] == q['id'])
        correct = user_ans == q['correct_answer']
        
        print(f"Q{q['id']}: {q['question']}")
        print(f"  Your answer: {user_ans} {'✓' if correct else '✗'}")
        print(f"  Correct answer: {q['correct_answer']}")
        print(f"  Explanation: {q['explanation']}\n")


# ============================================================================
# EXAMPLE 3: Get questions by difficulty level
# ============================================================================
def get_practice_set(topic: str, difficulty: str = "easy"):
    """Get practice questions of specific difficulty"""
    questions = get_mcq_questions(topic, num_questions=3, difficulty=difficulty)
    
    if questions:
        print(f"\n{difficulty.upper()} level questions on {topic}:\n")
        for q in questions:
            print(f"Q{q['id']}: {q['question']}")
            print(f"Difficulty: {q['difficulty']}\n")
    
    return questions


# ============================================================================
# EXAMPLE 4: Get detailed question data for API response
# ============================================================================
def get_questions_with_details(topic: str, num_questions: int = 2):
    """Get questions with full details (for website display)"""
    response = requests.post(
        f"{BASE_URL}/api/mcq/generate",
        json={
            "topic": topic,
            "num_questions": num_questions
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"\nTopic: {data['topic']}")
        print(f"Total Questions: {data['num_questions']}")
        print(f"Status: {data['status']}\n")
        
        for q in data['questions']:
            print(f"ID: {q['id']}")
            print(f"Question: {q['question']}")
            print(f"Options: {q['options']}")
            print(f"Correct Answer: {q['correct_answer']}")
            print(f"Explanation: {q['explanation']}")
            print(f"Difficulty: {q['difficulty']}\n")
            print("-" * 70 + "\n")


# ============================================================================
# EXAMPLE 5: API Health Check
# ============================================================================
def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data['status']}")
            print(f"Message: {data['message']}")
            return True
        return False
    except:
        print("API is not running!")
        return False


# ============================================================================
# MAIN - Run examples
# ============================================================================
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("MCQ API CLIENT EXAMPLES")
    print("=" * 70)
    
    # Check API is running
    print("\n1. Checking API health...")
    if not check_api_health():
        print("Please start the backend: python main.py")
        exit(1)
    
    print("\n2. Generating questions...")
    get_questions_with_details("Angular", 2)
    
    print("\n3. Practice Set (Easy)...")
    get_practice_set("React", "easy")
    
    print("\nAll examples completed!")
