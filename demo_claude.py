"""
Healthcare assistant using Claude (Anthropic) API with MCP-style tool calling.
Demonstrates handling multiple tool calls in a single conversation turn.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic
from src.data import FAQ_DATA, APPOINTMENTS, LAB_RESULTS, DOCTORS


# Load API key
load_dotenv()
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# Define tools
def check_faq(question: str) -> str:
    """Search frequently asked questions"""
    question = question.lower().strip()
    for key, answer in FAQ_DATA.items():
        if question in key or key in question:
            return f"FAQ Answer: {answer}"
    return "I couldn't find an answer to that question. Please call 555-1234."


def lookup_appointment(appointment_id: str) -> str:
    """Look up appointment details"""
    apt_id = appointment_id.upper()
    if apt_id in APPOINTMENTS:
        apt = APPOINTMENTS[apt_id]
        return (
            f"Appointment {apt_id}:\n"
            f"Patient: {apt['patient']}\n"
            f"Doctor: {apt['doctor']}\n"
            f"Date: {apt['date']}\n"
            f"Time: {apt['time']}\n"
            f"Status: {apt['status']}\n"
            f"Reason: {apt['reason']}"
        )
    return f"Appointment {apt_id} not found."


def lookup_lab_result(lab_id: str) -> str:
    """Look up lab results"""
    lab_id = lab_id.upper()
    if lab_id in LAB_RESULTS:
        lab = LAB_RESULTS[lab_id]
        urgency = "🚨 URGENT" if lab["urgent"] else "Normal priority"
        return (
            f"Lab Result {lab_id}:\n"
            f"Patient: {lab['patient']}\n"
            f"Test: {lab['test_type']}\n"
            f"Status: {lab['status']}\n"
            f"Priority: {urgency}\n"
            f"Summary: {lab['result_summary']}"
        )
    return f"Lab result {lab_id} not found."


def find_doctor(doctor_name: str) -> str:
    """Get doctor information"""
    if doctor_name in DOCTORS:
        doc = DOCTORS[doctor_name]
        accepting = "Yes ✓" if doc["accepting_new_patients"] else "No (full schedule)"
        return (
            f"{doc['full_name']}:\n"
            f"Specialty: {doc['specialty']}\n"
            f"Available: {', '.join(doc['available_days'])}\n"
            f"Accepting new patients: {accepting}\n"
            f"Languages: {', '.join(doc['languages'])}\n"
            f"Experience: {doc['years_experience']} years"
        )
    return "Doctor not found. Available: Dr. Smith, Dr. Johnson, Dr. Lee"


# Map functions
FUNCTION_MAP = {
    "check_faq": check_faq,
    "lookup_appointment": lookup_appointment,
    "lookup_lab_result": lookup_lab_result,
    "find_doctor": find_doctor
}


# Define tools for Claude
TOOLS = [
    {
        "name": "check_faq",
        "description": "Search frequently asked questions about clinic hours, location, insurance, services, and policies. Use this for general information queries.",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question or topic to search for (e.g., 'hours', 'insurance', 'location')"
                }
            },
            "required": ["question"]
        }
    },
    {
        "name": "lookup_appointment",
        "description": "Look up appointment details by appointment ID. Returns patient name, doctor, date, time, status, and reason. Appointment IDs follow format APT-XXX.",
        "input_schema": {
            "type": "object",
            "properties": {
                "appointment_id": {
                    "type": "string",
                    "description": "The appointment ID (e.g., 'APT-101')"
                }
            },
            "required": ["appointment_id"]
        }
    },
    {
        "name": "lookup_lab_result",
        "description": "Look up laboratory test results by lab ID. Returns test type, status, urgency, and result summary. Lab IDs follow format LAB-XXX.",
        "input_schema": {
            "type": "object",
            "properties": {
                "lab_id": {
                    "type": "string",
                    "description": "The lab result ID (e.g., 'LAB-201')"
                }
            },
            "required": ["lab_id"]
        }
    },
    {
        "name": "find_doctor",
        "description": "Get information about a specific doctor including specialty, availability, languages spoken, and whether they're accepting new patients.",
        "input_schema": {
            "type": "object",
            "properties": {
                "doctor_name": {
                    "type": "string",
                    "description": "The doctor's name (e.g., 'Dr. Smith', 'Dr. Johnson', 'Dr. Lee')"
                }
            },
            "required": ["doctor_name"]
        }
    }
]


def print_separator():
    print("\n" + "="*70 + "\n")


def run_agent(query: str):
    """Run Claude agent with tool calling"""
    
    messages = [{"role": "user", "content": query}]
    
    # Initial API call
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=TOOLS,
        messages=messages
    )
    
    # Handle tool calls in a loop
    while response.stop_reason == "tool_use":
        # Extract tool calls from response
        tool_uses = [block for block in response.content if block.type == "tool_use"]
        
        # Add assistant's response to messages
        messages.append({"role": "assistant", "content": response.content})
        
        # Execute each tool and collect results
        tool_results = []
        for tool_use in tool_uses:
            function_name = tool_use.name
            function_args = tool_use.input
            
            # Execute the function
            result = FUNCTION_MAP[function_name](**function_args)
            
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": result
            })
        
        # Add tool results to messages
        messages.append({"role": "user", "content": tool_results})
        
        # Get next response
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )
    
    # Extract final text response
    text_blocks = [block.text for block in response.content if hasattr(block, "text")]
    return " ".join(text_blocks)


def main():
    print("Healthcare Assistant Demo (Claude API)")
    print_separator()
    
    queries = [
        "What are your hours?",
        "Is APT-101 confirmed?",
        "What's the status of LAB-202?",
        "Tell me about Dr. Smith",
        "Is APT-101 confirmed and what are your office hours?",
        "I have APT-102 scheduled. What doctor will I see and are they accepting new patients?",
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"Query {i}: {query}")
        print("-" * 70)
        try:
            response = run_agent(query)
            print(f"Claude: {response}")
        except Exception as e:
            print(f" Error: {e}")
            import traceback
            traceback.print_exc()
        print_separator()
    
    print(" Demo complete!")


if __name__ == "__main__":
    main()