import pathway as pw

import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.WARN, force=True)


data_sources = []
# data_sources.append(
#     pw.io.fs.read(
#         "./data",
#         format="binary",
#         # format="plaintext",
#         mode="static",
#         with_metadata=True,
#     )  # This creates a `pathway` connector that tracks
#     # all the files in the ./data directory
# )


data_sources.append(
    pw.io.gdrive.read(
        object_id='',#your object id
        service_user_credentials_file="credentials.json",
        # refresh_interval=1,
        with_metadata=True,   
    )  # This creates a `pathway` connector that tracks
    # all the files in the ./data directory
)

from pathway.xpacks.llm.vector_store import VectorStoreServer
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import TokenTextSplitter
from pathway.xpacks.llm.parsers import ParseUnstructured,ParseUtf8

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text:latest",
    base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
)

transformations_example = [
    TokenTextSplitter(
        chunk_size=150,
        chunk_overlap=10,
        separator=" ",
    ),
    embed_model,
]

processing_pipeline = VectorStoreServer.from_llamaindex_components(
    *data_sources,
    transformations=transformations_example,
    parser=ParseUnstructured(),
    # parser=ParseUtf8(),
)

# Define the Host and port that Pathway will be on
PATHWAY_HOST = "127.0.0.1"
PATHWAY_PORT = 8754

# `threaded` runs pathway in detached mode, we have to set it to False when running from terminal or container
# for more information on `with_cache` check out https://pathway.com/developers/api-docs/persistence-api
processing_pipeline.run_server(
    host=PATHWAY_HOST, port=PATHWAY_PORT, with_cache=True, threaded=False
)