import sanic
import sanic.response
import os
from dotenv import load_dotenv
from sanic_cors import CORS
from sanic_ext import Extend
from sanic.worker.manager import WorkerManager

from routes.general_personas import personas_bp
from routes.health_report_route import health_bp
from routes.lifestyle_quality import lifestyle_quality_bp
from routes.panoramic_analyse_route import consultation_analyses_bp

from controllers.general_personas_controller import GeneralPersonasController
from controllers.health_report_controller import HealthReportController
from controllers.lifestyle_quality_controller import LifestyleQualityController
from controllers.panoramic_analyses_controller import PanoramicAnalysesController

from services.cache_service import CacheService

load_dotenv()

app = sanic.Sanic("app")
app.config.CORS_ORIGINS = os.getenv("FRONTEND_URL")
app.config.KEEP_ALIVE_TIMEOUT = 30
Extend(app)

image_folder_path = os.path.join(os.getcwd(), "db", "PERSONAS")
app.static("/db/PERSONAS", image_folder_path)

CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND_URL")}}, automatic_options=True, supports_credentials=True)
WorkerManager.THRESHOLD = 10000

@app.route("/")
async def index(request):
    return sanic.response.text("Server starting up...")

# Blueprints of the application
app.blueprint(personas_bp)
app.blueprint(health_bp)
app.blueprint(lifestyle_quality_bp)
app.blueprint(consultation_analyses_bp)

@app.listener('before_server_start')
async def preload_controllers(app, loop):
    GeneralPersonasController()
    HealthReportController()
    LifestyleQualityController()
    PanoramicAnalysesController()

@app.listener('before_server_start')
async def setup_cache(app, loop):
    constroller_instance = PanoramicAnalysesController()
    cache_service = CacheService()
    cache_service.set_controller(constroller_instance)
    cache_service.starter_set()

if __name__ == "__main__":
    port = int(os.getenv("PORT_SERVER"))
    host = os.getenv("HOST")
    workers = 2
    app.run(host=host, port=port, debug=True, access_log=True, workers=workers)
