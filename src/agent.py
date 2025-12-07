"""
MCP Agent that connects to the healthcare MCP server.
This agent can dynamically discover and use all 4 tools.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
import os


def create_healthcare_agent():
    """
    Create and return a healthcare agent connected to MCP server.
    """
    
    # Configure connection to MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.mcp_server"],
        env=None
    )
    
    # Create connection params
    connection_params = StdioConnectionParams(server_params=server_params)
    
    # Create MCP toolset
    mcp_tools = McpToolset(connection_params=connection_params)
    
    # Create agent with MCP tools
    agent = LlmAgent(
        name="healthcare_assistant",
        model=Gemini(model_name="gemini-2.0-flash-exp"),
        tools=[mcp_tools],
        instruction="""You are a helpful healthcare assistant.

You have access to 4 tools:
1. check_faq - For general questions about hours, location, insurance, services
2. lookup_appointment - For appointment details using appointment ID (APT-XXX)
3. lookup_lab_result - For lab results using lab ID (LAB-XXX)
4. find_doctor - For doctor information

When users ask questions:
- Use the appropriate tool(s) to find information
- If a query requires multiple pieces of information, use multiple tools
- Be friendly and professional
- If you can't find information, politely suggest they call 555-1234

Always provide complete, helpful answers based on the tool results."""
    )
    
    return agent


if __name__ == "__main__":
    # Quick test
    agent = create_healthcare_agent()
    print("Healthcare MCP Agent initialized successfully!")