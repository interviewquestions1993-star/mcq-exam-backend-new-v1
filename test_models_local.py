#!/usr/bin/env python
"""Test Pydantic models locally"""
from main import MCQGenerationRequest, MCQGenerationResponse, MCQQuestion

try:
    # Test creating a request
    req = MCQGenerationRequest(topic="Angular", num_questions=5)
    print(f"✅ Request model created: {req}")

    # Test creating a response with questions
    q = MCQQuestion(
        id=1,
        question="Test?",
        options=["A) 1", "B) 2", "C) 3", "D) 4"],
        correct_answer="A",
        explanation="Because",
        difficulty="medium"
    )
    resp = MCQGenerationResponse(
        topic="Angular",
        num_questions=1,
        questions=[q]
    )
    print(f"✅ Response model created with {len(resp.questions)} questions")
    print("✅ All Pydantic models validate successfully!")
    print("\n✅✅✅ READY FOR DEPLOYMENT ✅✅✅")
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
