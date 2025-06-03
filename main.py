
from channel_statuses import channels_data
from exceptions import ValidationException
from flask import Flask, request, jsonify, make_response

from menu_push_validators.glovo import validate_menu as validate_glovo
from menu_push_validators.uber_eats import validate_menu as validate_uber
from menu_push_validators.deliveroo import validate_menu as validate_deliveroo
from pos_data import POS_data

VALIDATOR_BY_CHANNEL = {
    "Glovo": validate_glovo,
    "UberEats": validate_uber,
    "Deliveroo": validate_deliveroo,
}


app = Flask(__name__)

@app.route("/")
def hi():
    return "<p>Hello, Yeva!</p>"


@app.route("/fetchProducts/<posId>", methods=['GET'])
def fetch_pos_data(posId: str):
    if posId not in POS_data:
        return make_response(jsonify({"error": f"POS with ID {posId} not found"}), 404)

    return make_response(jsonify(POS_data[posId]), 200)


@app.route("/activateChannel/<channelId>", methods=['POST'])
def activate_channel(channelId: str):
    if channelId not in channels_data:
        return make_response(jsonify({"error": f"Channel with ID {channelId} not found"}), 404)

    channels_data[channelId]["status"] = True if "deactivate" not in request.json else False

    return make_response(jsonify({channelId: channels_data[channelId]}), 200)


@app.route("/pushMenu/<channelId>", methods=['POST'])
def push_menu(channelId: str):
    if channelId not in channels_data:
        return make_response(jsonify({"error": f"Channel with ID {channelId} not found"}), 404)

    if not channels_data[channelId]["status"]:
        return make_response(
            jsonify({
                "error": f"Channel with ID {channelId} was not activated yet. "
                         f"Make sure to activate it on /activateChannel"
            }),
            400
        )

    channel_type = channels_data[channelId]["channel"]
    validator = VALIDATOR_BY_CHANNEL[channel_type]
    try:
        result = validator(request.json)
    except ValidationException as e:
        return make_response(jsonify({"error": f"{e}"}), 400)

    return make_response(jsonify({"success": result}), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)