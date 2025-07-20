import sanic
import sanic.response
import os
from dotenv import load_dotenv
from db.mongo import init_db
from sanic_cors import CORS
from sanic_ext import Extend

from routes.health_report_route import state_bp

load_dotenv()

app = sanic.Sanic("app")
app.config.CORS_ORIGINS = os.getenv("FRONTEND_URL")
Extend(app)

CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND_URL")}}, automatic_options=True, supports_credentials=True)

@app.listener("before_server_start")
async def setup_db(app, loop):
    await init_db()

@app.route("/")
async def index(request):
    return sanic.response.text("Server starting up...")

# Blueprints da aplicação
app.blueprint(state_bp)

if __name__ == "__main__":
    port = int(os.getenv("PORT_SERVER"))
    host = os.getenv("HOST")
    app.run(host=host, port=port, debug=True, access_log=True)
