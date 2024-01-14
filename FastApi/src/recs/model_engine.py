

from llama_index import get_response_synthesizer, ServiceContext
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.postprocessor import SimilarityPostprocessor
from llama_index import StorageContext, load_index_from_storage


DATA_PATH = "./data/film_summaries_index_dump"
TOP_N = 10


def get_engine():
    '''
    Returns model query engine (RetrieverQueryEngine).

        Params:

        Returns: query_engine (RetrieverQueryEngine): model engine
    '''
    # build index
    service_context = ServiceContext.from_defaults(llm=None, embed_model="local:BAAI/bge-large-en-v1.5")
    storage_context = StorageContext.from_defaults(persist_dir=DATA_PATH)
    # load index
    index = load_index_from_storage(
        storage_context,
        service_context=service_context,
        show_progress=True
    )
    # configure retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=TOP_N,
    )
    # configure response synthesizer
    response_synthesizer = get_response_synthesizer(
        service_context=service_context,
        response_mode="compact"
    )
    # assemble query engine
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.5)],
    )

    return query_engine
