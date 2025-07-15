import sanic
import sanic.response
from sanic import Blueprint
from sanic.request import Request
from controllers.health_report_controller import get_region_datas, get_region_datas_with_filters


state_bp = Blueprint('region_filter')

@state_bp.route('/health_report/<regiao>', methods=['GET'])
async def filter_regions(request: Request, regiao: str):
    """
    Endpoint to filter regions based on a query parameter.
    """
    regiao = "all" if regiao is None else regiao

    if not request.args:
        datas = await get_region_datas(regiao = str(regiao))
    else:
        datas = await get_region_datas_with_filters(regiao = str(regiao), filters = request.args)
    return sanic.response.json(datas, status=200)