from llama_index.core.tools import FunctionTool
from langchain_community.tools import YouTubeSearchTool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import os

note_file = os.path.join('note.txt')
wrapper = DuckDuckGoSearchAPIWrapper(region="de-de", time="d", max_results=2)
search = DuckDuckGoSearchRun(api_wrapper=wrapper)
tool = YouTubeSearchTool()

def noteWriter(content:str) -> str:
    '''Writes a note to a file called note.txt'''
    with open(note_file, 'w') as f:
        f.write(content)

    return "Note saved to note.txt"

def search_youtube(query:str) -> str:
    '''Searches YouTube for a query'''
    results = tool.run(f"{query},5")
    return results

def search_web(query:str) -> str:
    '''Searches the web using DuckDuckGo'''
    results = search.run(query)
    return results

youtube_search_engine = FunctionTool.from_defaults(
    fn=search_youtube,
    name='YouTube_Search_Engine',
    description='This tool can be used to get the realtime search result from YouTube.',
)
note_engine = FunctionTool.from_defaults(
    fn=noteWriter,
    name='Note_saver',
    description='This tool can be used to save text data to a text file called note.txt in the local directory.',
)
web_search_engine = FunctionTool.from_defaults(
    fn=search_web,
    name='Web_Search_Engine',
    description='This tool can be used to get the realtime websearch result from the web using DuckDuckGo.',
)