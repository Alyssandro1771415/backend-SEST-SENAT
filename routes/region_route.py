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
    regiao = request.args.get('regiao')
    regiao = "all" if regiao is None else regiao
    
    datas = await get_region_datas(regiao = str(regiao))

    return sanic.response.json(datas, status=200)