from src.llm.schemas import LLMItem

def predict_llm(request, engine):
    '''
    Returns LLM reply

        Params:
                request (DataInItem): request query
                engine (RetrieverQueryEngine): LLm engine

        Returns: final_query (LLMItem): request query with response
    '''
    response = engine.query(request.query)
    final_obj = LLMItem(query=response.response)

    return final_obj