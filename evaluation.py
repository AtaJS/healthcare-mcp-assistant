"""
Simple DeepEval evaluation for healthcare assistant.
Focuses on response quality without complex MCP tracking.
"""

import os
from dotenv import load_dotenv
from deepeval import evaluate
from deepeval.metrics import GEval, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.models import AnthropicModel
from demo_claude import run_agent

load_dotenv()


def main():
    print("="*70)
    print("HEALTHCARE ASSISTANT EVALUATION (DeepEval)")
    print("="*70)
    print("\nRunning queries and evaluating responses...\n")
    
    # Use Claude as the evaluation judge
    eval_model = AnthropicModel(model="claude-sonnet-4-20250514")
    
    # Create test cases
    queries = [
        ("What are your hours?", "Monday-Friday 8AM-6PM, Saturday 9AM-2PM"),
        ("Is APT-101 confirmed?", "Confirmed for John Doe with Dr. Smith on December 10"),
        ("What's the status of LAB-202?", "Ready, urgent, chest X-ray with abnormal findings"),
        ("Tell me about Dr. Smith", "Dr. Sarah Smith, Family Medicine, 15 years experience"),
        ("Is APT-101 confirmed and what are your hours?", "APT-101 confirmed, hours Mon-Fri 8AM-6PM"),
    ]
    
    test_cases = []
    for i, (query, expected) in enumerate(queries, 1):
        print(f"{i}. Processing: {query}")
        actual = run_agent(query)
        test_cases.append(LLMTestCase(
            input=query,
            actual_output=actual,
            expected_output=expected
        ))
    
    print("\n" + "="*70)
    print("RUNNING EVALUATION")
    print("="*70 + "\n")
    
    # Define metrics
    correctness = GEval(
        name="Correctness",
        criteria="Is the actual output factually correct based on expected output?",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
        model=eval_model,
        threshold=0.7
    )
    
    completeness = GEval(
        name="Completeness", 
        criteria="Does the actual output fully answer all parts of the user's question?",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        model=eval_model,
        threshold=0.7
    )
    
    # Run evaluation (removed print_results parameter)
    results = evaluate(
        test_cases=test_cases,
        metrics=[correctness, completeness]
    )
    
    print("\n" + "="*70)
    print("EVALUATION COMPLETE")
    print("="*70)
    print(f"\nResults: {results}")


if __name__ == "__main__":
    main()