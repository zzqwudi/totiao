from flask import Blueprint
from flask_restful import Api

from utli.output import output_json
from . import channel

news_bp = Blueprint('news_bp', __name__)

news_api = Api(news_bp, catch_all_404s=True)
news_api.representation('application/json')(output_json)

news_api.add_resource(channel.ChannelView, '/app/v1_0/channels')
