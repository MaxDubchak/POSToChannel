import json
from typing import Type

import requests

from channelsAPIs.base import BaseAPI
from channelsAPIs.deliveroo import DeliverooAPI
from channelsAPIs.glovo import GlovoAPI
from channelsAPIs.uber_eats import UberEatsAPI
from db import channels_collection, menus_collection, pos_data_collection, orders_collection
from exceptions import ValidationException
from flask import Flask, request, jsonify, make_response


def get_channel_api(chanelType: str) -> Type[BaseAPI]:
    API_BY_CHANNEL = {
        "Glovo": GlovoAPI,
        "UberEats": UberEatsAPI,
        "Deliveroo": DeliverooAPI,
    }
    return API_BY_CHANNEL[chanelType]


app = Flask(__name__)

@app.route("/")
def hi():
    return "<p>Hello, Yeva!</p>"


@app.route("/fetchProducts/<posId>", methods=['GET'])
def fetch_pos_data(posId: str):
    if not (current_pos_data := pos_data_collection.find_one({"uid": posId})):
        return make_response(jsonify({"error": f"POS with ID {posId} not found"}), 404)

    return make_response(jsonify(current_pos_data["data"]), 200)


@app.route("/activateChannel/<channelId>", methods=['POST'])
def activate_channel(channelId: str):
    if not (channel := channels_collection.find_one({"uid": channelId}, projection={"_id": False})):
        return make_response(jsonify({"error": f"Channel with ID {channelId} not found"}), 404)

    if not channel.get("status"):
        channels_collection.update_one({"uid": channelId}, {"$set": {"status": True}})

    return make_response(jsonify({channelId: channel}), 200)


@app.route("/pushMenu/<channelId>", methods=['POST'])
def push_menu(channelId: str):
    if not (channel := channels_collection.find_one({"uid": channelId})):
        return make_response(jsonify({"error": f"Channel with ID {channelId} not found"}), 404)

    if not channel["status"]:
        return make_response(
            jsonify({
                "error": f"Channel with ID {channelId} was not activated yet. "
                         f"Make sure to activate it on /activateChannel"
            }),
            400
        )

    channel_type = channel["channel"]
    channel_api = get_channel_api(channel_type)
    try:
        result = channel_api.validate_menu(request.json)
    except ValidationException as e:
        return make_response(jsonify({"error": f"{e}"}), 400)
    else:
        if menus_collection.find_one({"channel_id": channelId}):
            menus_collection.update_one({"channel_id": channelId}, {"$set": request.json})
        else:
            menus_collection.insert_one({"channel_id": channelId, **request.json})

    return make_response(jsonify({"success": result}), 200)


@app.route("/menu/<channelId>", methods=["GET"])
def fetch_menu(channelId: str):
    if not channels_collection.find_one({"uid": channelId}):
        return make_response(jsonify({"error": f"Channel with ID {channelId} not found"}), 404)

    if not (menu := menus_collection.find_one({"channel_id": channelId}, projection={"_id": False})):
        return make_response(jsonify({"error": f"Menu for channel with ID {channelId} not found"}), 404)

    return make_response(jsonify(menu), 200)


@app.route("/receiveOrders/<channelId>", methods=['POST'])
def receive_orders(channelId: str):
    if not (channel := channels_collection.find_one({"uid": channelId})):
        return make_response(jsonify({"error": f"Channel with ID {channelId} not found"}), 404)

    if not (menu := menus_collection.find_one({"channel_id": channelId}, projection={"_id": False})):
        return make_response(jsonify({"error": f"Menu for channel with ID {channelId} not found"}), 404)

    request_data = request.json

    if not "url" in request_data:
        return make_response(jsonify({"error": f"Request data missing 'url' key"}), 400)

    url = request_data["url"]
    channel_api = get_channel_api(channel["channel"])
    order = channel_api.generate_order(menu)
    order = {"channel_id": channelId, "order": order}

    response = requests.post(url, json=order)
    if not response.ok:
        return make_response(
            jsonify({"error": f"Could not post order to url {url}, error: {response.text}"}), 400
        )

    return make_response({"success": True}, 200)


@app.route("/saveOrder", methods=['POST'])
def save_order():
    orders_collection.insert_one(request.json)
    return make_response({"success": True}, 200)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)