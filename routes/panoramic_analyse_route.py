import sanic
import sanic.response
from sanic import Blueprint
from sanic.request import Request
from services.filters_service import get_region_consultations_filters

from controllers.panoramic_analyses_controller import get_atendimentos_genero

consultation_analyses_bp = Blueprint('consultations_bp')

@consultation_analyses_bp.route('/general_report/<regiao>', methods=['GET'])
async def general_analyse(request: Request, regiao: str):
    """
    Endpoint to calculate general datas based on the query parameters
    filter to calculate general datas to present in front-end.
    """
    regiao = "all" if regiao is None else regiao

    query_parts = await get_region_consultations_filters(regiao, request.args)

    # Falta criar o controller e aplicar ele sobre os dados
    
    return sanic.response.json(query_parts, status=200)