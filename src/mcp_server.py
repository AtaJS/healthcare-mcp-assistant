"""
MCP Server that exposes healthcare data as tools.
The agent will connect to this server to access our 4 data sources.
"""

import asyncio
import json
from mcp.server import Server
from mcp.types import Tool, TextContent
from src.data import FAQ_DATA, APPOINTMENTS, LAB_RESULTS, DOCTORS


# Create MCP server instance
app = Server("healthcare-assistant")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Define the 4 tools available to the agent.
    Each tool corresponds to one data source.
    """
    return [
        Tool(
            name="check_faq",
            description="Search frequently asked questions about clinic hours, location, insurance, services, and policies. Use this for general information queries.",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question or topic to search for (e.g., 'hours', 'insurance', 'location')"
                    }
                },
                "required": ["question"]
            }
        ),
        Tool(
            name="lookup_appointment",
            description="Look up appointment details by appointment ID. Returns patient name, doctor, date, time, status, and reason for visit. Appointment IDs follow format APT-XXX.",
            inputSchema={
                "type": "object",
                "properties": {
                    "appointment_id": {
                        "type": "string",
                        "description": "The appointment ID (e.g., 'APT-101')"
                    }
                },
                "required": ["appointment_id"]
            }
        ),
        Tool(
            name="lookup_lab_result",
            description="Look up laboratory test results by lab ID. Returns test type, status, urgency, and result summary. Lab IDs follow format LAB-XXX.",
            inputSchema={
                "type": "object",
                "properties": {
                    "lab_id": {
                        "type": "string",
                        "description": "The lab result ID (e.g., 'LAB-201')"
                    }
                },
                "required": ["lab_id"]
            }
        ),
        Tool(
            name="find_doctor",
            description="Get information about a specific doctor including specialty, availability, languages spoken, and whether they're accepting new patients.",
            inputSchema={
                "type": "object",
                "properties": {
                    "doctor_name": {
                        "type": "string",
                        "description": "The doctor's name (e.g., 'Dr. Smith', 'Dr. Johnson', 'Dr. Lee')"
                    }
                },
                "required": ["doctor_name"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Execute the requested tool and return results.
    This is where the actual data lookup happens.
    """
    
    if name == "check_faq":
        question = arguments["question"].lower().strip()
        
        # Search for matching FAQ
        for key, answer in FAQ_DATA.items():
            if question in key or key in question:
                return [TextContent(
                    type="text",
                    text=f"FAQ Answer: {answer}"
                )]
        
        # No match found
        return [TextContent(
            type="text",
            text="I couldn't find an answer to that question in our FAQ. Please call us at 555-1234 for assistance."
        )]
    
    elif name == "lookup_appointment":
        apt_id = arguments["appointment_id"].upper()
        
        if apt_id in APPOINTMENTS:
            apt = APPOINTMENTS[apt_id]
            response = (
                f"Appointment {apt_id}:\n"
                f"Patient: {apt['patient']}\n"
                f"Doctor: {apt['doctor']}\n"
                f"Date: {apt['date']}\n"
                f"Time: {apt['time']}\n"
                f"Status: {apt['status']}\n"
                f"Reason: {apt['reason']}"
            )
            return [TextContent(type="text", text=response)]
        else:
            return [TextContent(
                type="text",
                text=f"Appointment {apt_id} not found. Please verify the appointment ID."
            )]
    
    elif name == "lookup_lab_result":
        lab_id = arguments["lab_id"].upper()
        
        if lab_id in LAB_RESULTS:
            lab = LAB_RESULTS[lab_id]
            urgency = "!!! URGENT !!!" if lab["urgent"] else "Normal priority"
            response = (
                f"Lab Result {lab_id}:\n"
                f"Patient: {lab['patient']}\n"
                f"Test: {lab['test_type']}\n"
                f"Ordered: {lab['ordered_date']}\n"
                f"Status: {lab['status']}\n"
                f"Priority: {urgency}\n"
                f"Summary: {lab['result_summary']}"
            )
            return [TextContent(type="text", text=response)]
        else:
            return [TextContent(
                type="text",
                text=f"Lab result {lab_id} not found. Please verify the lab ID."
            )]
    
    elif name == "find_doctor":
        doctor_name = arguments["doctor_name"]
        
        if doctor_name in DOCTORS:
            doc = DOCTORS[doctor_name]
            accepting = "Yes ✓" if doc["accepting_new_patients"] else "No (full schedule)"
            response = (
                f"{doc['full_name']}:\n"
                f"Specialty: {doc['specialty']}\n"
                f"Available: {', '.join(doc['available_days'])}\n"
                f"Accepting new patients: {accepting}\n"
                f"Languages: {', '.join(doc['languages'])}\n"
                f"Experience: {doc['years_experience']} years"
            )
            return [TextContent(type="text", text=response)]
        else:
            return [TextContent(
                type="text",
                text=f"Doctor {doctor_name} not found. Available doctors: Dr. Smith, Dr. Johnson, Dr. Lee"
            )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())