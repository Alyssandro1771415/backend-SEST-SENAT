import sanic
import sanic.response
import os
from dotenv import load_dotenv
from sanic_cors import CORS
from sanic_ext import Extend
from sanic.worker.manager import WorkerManager

from routes.health_report_route import health_bp
from routes.panoramic_analyse_route import consultation_analyses_bp

from controllers.health_report_controller import HealthReportController
from controllers.panoramic_analyses_controller import PanoramicAnalysesController

load_dotenv()

app = sanic.Sanic("app")
app.config.CORS_ORIGINS = os.getenv("FRONTEND_URL")
Extend(app)

CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND_URL")}}, automatic_options=True, supports_credentials=True)
WorkerManager.THRESHOLD = 10000

@app.route("/")
async def index(request):
    return sanic.response.text("Server starting up...")

# Blueprints of the application
app.blueprint(health_bp)
app.blueprint(consultation_analyses_bp)

@app.listener('before_server_start')
async def preload_controllers(app, loop):
    HealthReportController()
    PanoramicAnalysesController()

if __name__ == "__main__":
    port = int(os.getenv("PORT_SERVER"))
    host = os.getenv("HOST")
    fast = True
    workers = 1
    app.run(host=host, port=port, debug=True, access_log=True, workers=workers)
