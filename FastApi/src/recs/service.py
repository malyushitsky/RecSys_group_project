

from src.recs.schemas import DataOut, QueryResponseItem
from src.recs.utils import preprocess_response


def get_top_n_predictions(requests, engine):
    '''
    Returns top n movie recommendations for all request queries.

        Params:
                requests (DataIn): request queries
                engine (RetrieverQueryEngine): model engine

        Returns: final_obj (DataOut): request queries with responses
    '''
    final_lst = []
    for obj in requests.objects:
        response = engine.retrieve(obj.query)
        cur_lst = []
        for node in response[:obj.n_recs]:
            cur_lst.append(preprocess_response(node.metadata, node.text))
        new_obj = QueryResponseItem(n_recs=obj.n_recs, query=obj.query, response=cur_lst)
        final_lst.append(new_obj)
    final_obj = DataOut(objects=final_lst)

    return final_obj


def get_top_n_prediction(request, engine):
    '''
    Returns top n movie recommendations for a single request query.

        Params:
                request (DataInItem): request query
                engine (RetrieverQueryEngine): model engine

        Returns: final_query (QueryResponseItem): request query with response
    '''
    response = engine.retrieve(request.query)
    cur_lst = []
    for node in response[:request.n_recs]:
        cur_lst.append(preprocess_response(node.metadata, node.text))
    final_obj = QueryResponseItem(n_recs=request.n_recs, query=request.query, response=cur_lst)

    return final_obj
