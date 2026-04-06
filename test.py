import asyncio
from vanna_setup import agent
from vanna.core.user import RequestContext




async def test():
    response = await agent.run(
        input="How many patients?",
        request_context=RequestContext()
    )
    print(response)

asyncio.run(test())