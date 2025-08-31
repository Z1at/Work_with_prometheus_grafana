from service.endpoints.get_all_data import api_router as get_all_data
from service.endpoints.get_data_by_id import api_router as get_data_by_id
from service.endpoints.delete_data_by_id import api_router as delete_data_by_id
from service.endpoints.insert_data import api_router as insert_data
from service.endpoints.run_query import api_router as run_query


list_of_routes = [
    get_all_data,
    get_data_by_id,
    delete_data_by_id,
    insert_data,
    run_query
]

__all__ = [
    "list_of_routes"
]
