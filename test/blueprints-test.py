from sanic.response import json
from sanic import Blueprint
from sanic import Sanic

bp = Blueprint("my_blueprint")


@bp.route("/")
async def bp_root(request):
    return json({"my": "blueprint"})


app = Sanic(__name__)
app.blueprint(bp)
if __name__ == '__main__':
    app.run()
    # app.run(host="0.0.0.0", port=8000)

# 访问：http://127.0.0.1:8000 显示：{"my":"blueprint"}
