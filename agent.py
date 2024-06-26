from llama_index.retrievers.pathway import PathwayRetriever
from llama_index.core import PromptTemplate
from llama_index.core.tools import QueryEngineTool,ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.core import settings
from tools import note_engine,youtube_search_engine,web_search_engine
import nest_asyncio
import chainlit as cl
import time

nest_asyncio.apply()

retriever = PathwayRetriever(host="127.0.0.1", port=8754)
# results = retriever.retrieve("what is javascript")
# print(results)

from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.ollama import Ollama

llm = Ollama(model="phi3:latest",request_timeout=1600)


query_engine = RetrieverQueryEngine.from_args(
    retriever,
    llm=llm,
)

tools = [
    QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="Google_Drive_Query_Engine",
            description="This tool give the similarity search results from Google Drive documents.",
        ),
    ),
    note_engine,
    youtube_search_engine,
    web_search_engine,
]

context = """Purpoes: The primary purpose of this agent is to assist user by using the tools for analyazing documents ,search web and provide accurate results."""

agent =ReActAgent.from_tools(tools=tools,llm=llm,verbose=True,context=context)

# while (question := input("Ask me something: "))!='q':
#     response = agent.chat(question)
#     print(response)

@cl.on_chat_start
async def on_chat_start():
    # await cl.Message(content="Hello! I am your assistant. How can I help you?").send()
    cl.user_session.set("agent", agent)

@cl.on_message
async def on_message(message:cl.Message):
    agent = cl.user_session.get("agent")
    msg = cl.Message(content="")
    try:
        response = agent.chat(message.content,tool_choice='auto')
        await cl.Message(content=str(response)).send()
    except Exception as e:
        time.sleep(15)
        response = agent.chat(message.content,tool_choice='auto')
        await cl.Message(content=str(response)).send()
    # res = await cl.make_async(agent.chat)(message.content)
    # for token in res.response_gen:
    #     await msg.stream_token(token)
    # await msg.send()
