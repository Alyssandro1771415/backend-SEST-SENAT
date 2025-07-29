import sanic
import sanic.response
from sanic import Blueprint
from sanic.request import Request

from controllers.general_personas_controller import GeneralPersonasController

personas_bp = Blueprint('personas_bp')

@personas_bp.route('/general_personas/<regiao>', methods=['GET'])
async def general_personas(request: Request, regiao: str):
    """
    Endpoint to calculate analises of health and revel standards of utilization,
    efetivitie of especialities e oportunities os otimization
    """
    regiao = "all" if regiao is None else regiao

    if regiao == "all":
        data = GeneralPersonasController().get_datas_personas_nacional()
    else:
        data = GeneralPersonasController().get_datas_personas_regional(regiao)

    return sanic.response.json(data, status=200)
