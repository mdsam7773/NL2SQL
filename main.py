

import os

import os

from vanna import Agent
from vanna.core.registry import ToolRegistry
 
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool, SaveTextMemoryTool
from vanna.servers.fastapi import VannaFastAPIServer
from vanna.integrations.ollama import OllamaLlmService
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.core.user import RequestContext
from vanna.integrations.openai import OpenAILlmService


from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext
from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import SaveQuestionToolArgsTool, SearchSavedCorrectToolUsesTool
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory

#for gemini
from vanna.integrations.google import GeminiLlmService
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

'''
# ✅ LLM (gemini)
llm = GeminiLlmService(
    model="gemini-2.5-flash",
    api_key="AIzaSyBAeGVwBaWBMDds-72K1Pvs_FsU_S3zD0I"  # Or use os.getenv("GOOGLE_API_KEY")

)'''

api_key = os.getenv('GROQ_API_KEY')

llm = OpenAILlmService(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
    model="llama-3.1-8b-instant"
)



# ✅ Database
db_tool = RunSqlTool(
    sql_runner=SqliteRunner("clinic.db")
)

# ✅ Memory
agent_memory = DemoAgentMemory(max_items=1000)

class SimpleUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        user_email = request_context.get_cookie('vanna_email') or 'guest@example.com'
        group = 'admin' if user_email == 'admin@example.com' else 'user'
        return User(id=user_email, email=user_email, group_memberships=[group])

user_resolver = SimpleUserResolver()

# ✅ Tools
tools = ToolRegistry()

tools.register_local_tool(db_tool, access_groups=["admin", "user"])
tools.register_local_tool(SaveQuestionToolArgsTool(), access_groups=["admin"])
tools.register_local_tool(SearchSavedCorrectToolUsesTool(), access_groups=["admin", "user"])
tools.register_local_tool(SaveTextMemoryTool(), access_groups=["admin", "user"])
tools.register_local_tool(VisualizeDataTool(), access_groups=["admin", "user"])

# ✅ Agent
agent = Agent(
    llm_service=llm,
    tool_registry=tools,
    user_resolver=user_resolver,
    
    agent_memory=agent_memory
)



# ✅ FastAPI Server
server = VannaFastAPIServer(agent)


if __name__ == "__main__":
    server.run()
