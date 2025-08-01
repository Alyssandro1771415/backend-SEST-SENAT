import sanic
import sanic.response
from sanic import Blueprint
from sanic.request import Request

from services.filters_service import FiltersService
from controllers.lifestyle_quality_controller import LifestyleQualityController


lifestyle_quality_bp = Blueprint('lifestyle_quality_bp')

@lifestyle_quality_bp.route('/lifestyle_quality/<regiao>', methods=['GET'])
async def lifestyle_quality(request: Request, regiao: str):
    """
    Endpoint to calculate lifestyle quality based on the query parameters
    filters to get calculated data to present in front-end.
    """
    controller = LifestyleQualityController()
    filters = await FiltersService().get_region_and_filters_hearth_report(regiao, request.args)

    response = controller.get_lifestyle_quality(regiao, filters)

    return sanic.response.json(response, status=200)
