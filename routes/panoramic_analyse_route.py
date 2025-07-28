import asyncio
from concurrent.futures import ThreadPoolExecutor

import sanic
import sanic.response
from sanic import Blueprint
from sanic.request import Request

from controllers.panoramic_analyses_controller import PanoramicAnalysesController
from services.filters_service import FiltersService

# Using ThreadPoolExecutor to handle blocking I/O operations in a non-blocking way
# This is useful for operations that are CPU-bound or involve blocking I/O, such as database
executor = ThreadPoolExecutor(max_workers=4)
consultation_analyses_bp = Blueprint('consultations_bp')

@consultation_analyses_bp.route('/general_report/<regiao>', methods=['GET'])
async def general_analyse(request: Request, regiao: str):
    """
    Endpoint to calculate general datas based on the query parameters
    filter to calculate general datas to present in front-end.
    """
    regiao = "all" if regiao is None else regiao

    filters = await FiltersService().get_region_and_filters_panoramic_analyse(regiao, request.args)

    controller = PanoramicAnalysesController()
    loop = asyncio.get_event_loop()

    response_results = await loop.run_in_executor(
        executor, 
        controller.painel_atendimentos, 
        filters
    )
    
    return sanic.response.json(response_results, status=200)
