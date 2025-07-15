import sanic
import sanic.response
from sanic import Blueprint
from sanic.request import Request
from controllers.region_controller import get_region_datas


state_bp = Blueprint('region_filter')

@state_bp.route('/region', methods=['GET'])
async def filter_regions(request: Request):
    """
    Endpoint to filter regions based on a query parameter.
    """

    estado = request.args.get('estado')
    estado = "all" if estado is None else estado
    
    datas = await get_region_datas(estado = str(estado))

    return sanic.response.json(datas, status=200)