import sanic
import sanic.response
from sanic import Blueprint
from sanic.request import Request
from controllers.health_report_controller import calc_all_average
from services.filters_service import get_region_health_datas_filters


health_bp = Blueprint('health_bp')

@health_bp.route('/health_report/<regiao>', methods=['GET'])
async def health_report(request: Request, regiao: str):
    """
    Endpoint to calculate datas based on the query parameters
    filters to get calculated datas to present in front-end.
    """
    regiao = "all" if regiao is None else regiao

    datas = await get_region_health_datas_filters(regiao, request.args)

    datas = calc_all_average(datas)
    
    return sanic.response.json(datas, status=200)