import sanic
import sanic.response
from sanic import Blueprint
from sanic.request import Request
from controllers.health_report_controller import HealthReportController
from services.filters_service import get_region_and_filters


health_bp = Blueprint('health_bp')

@health_bp.route('/health_report/<regiao>', methods=['GET'])
async def health_report(request: Request, regiao: str):
    """
    Endpoint to calculate datas based on the query parameters
    filters to get calculated datas to present in front-end.
    """

    controller = HealthReportController()

    regiao = "all" if regiao is None else regiao

    filters = await get_region_and_filters(regiao, request.args)

    datas = controller.get_datas_by_filters(filters)

    print(datas)

    finel_datas_result = controller.calc_all_average(datas)
    
    return sanic.response.json(finel_datas_result, status=200)