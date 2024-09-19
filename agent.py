from llama_index.retrievers.pathway import PathwayRetriever
from llama_index.core import PromptTemplate
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from tools import note_engine, youtube_search_engine, web_search_engine
import nest_asyncio
import chainlit as cl
import time
import os
from llama_index.core.tools import FunctionTool

nest_asyncio.apply()

retriever = PathwayRetriever(host="127.0.0.1", port=8754)
# results = retriever.retrieve("what is javascript")
# print(results)

from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.ollama import Ollama
from llama_index.multi_modal_llms.ollama import OllamaMultiModal
from llama_index.core import SimpleDirectoryReader
from PIL import Image

llm = Ollama(model="phi3:latest", request_timeout=1600)
m_llm = OllamaMultiModal(model="llava:latest", request_timeout=1600)

# test_file_path = os.path.join(os.getcwd(), ".files")
# test_img_doc = SimpleDirectoryReader('./files').load_data(show_progress=True)


def get_image_data(question: str) -> str:
    """This function is used to get the image data from the image that user has given and it takes question as the argument."""
    file_path = os.path.join(os.getcwd(), "images")
    img_doc = SimpleDirectoryReader(file_path).load_data(show_progress=True)
    print("image loaded")
    image_data = m_llm.complete(prompt=question, image_documents=img_doc)
    return image_data


image_data_engine = FunctionTool.from_defaults(
    fn=get_image_data,
    name="image_data_engine",
    description="This tool can be used to get the image data from the image that user has given and it takes question as the argument.",
)


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
    image_data_engine,
    note_engine,
    youtube_search_engine,
    web_search_engine,
]
print("tools loaded")

context = """Purpoes: The primary purpose of this agent is to assist user by using the tools for analyazing documents ,search web,provide the information with the image data and provide accurate results."""

agent = ReActAgent.from_tools(tools=tools, llm=llm, verbose=True, context=context)
prev_img = None


@cl.on_chat_start
async def on_chat_start():
    # await cl.Message(content="Hello! I am your assistant. How can I help you?").send()
    cl.user_session.set("agent", agent)


@cl.on_message
async def on_message(message: cl.Message):
    global prev_img
    agent = cl.user_session.get("agent")
    msg = cl.Message(content="")
    images = [file for file in message.elements if "image" in file.mime]
    save_path = os.path.join(os.getcwd(), "images")
    if images != []:
        if prev_img is not None:
            os.remove(prev_img)
        with open(images[0].path, "rb") as f:
            image_data = Image.open(f)
            image_path = os.path.join(save_path, images[0].name)
            image_data.save(image_path)
            prev_img = image_path
    try:
        response = agent.chat(message.content, tool_choice="auto")
        print(response)
        await cl.Message(content=str(response)).send()
    except Exception as e:
        time.sleep(15)
        response = agent.chat(message.content, tool_choice="auto")
        print(response)
        await cl.Message(content=str(response)).send()


@cl.on_chat_end
def end():
    global prev_img
    if prev_img is not None:
        os.remove(prev_img)
    print("program ended")
