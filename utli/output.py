from json import dumps

from flask import make_response, current_app, request
from flask_restful.utils import PY3


def output_json(data, code, headers=None):  # 没有覆盖
    """Makes a Flask response with a JSON encoded body"""
    if str(code) == '400': # 如果是400，则返回错误信息
        current_app.logger.warn(request.headers) # 记录日志
        current_app.logger.warn(request.data) # 记录日志
        current_app.logger.warn(str(data)) # 记录日志

    if 'message' not in data: # 如果没有message，则添加message
        data = {
            'message': 'OK',
            'data': data
        }

    settings = current_app.config.get('RESTFUL_JSON', {}) # 获取配置

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.  We also set the "sort_keys" value.
    if current_app.debug: # 如果是debug模式
        settings.setdefault('indent', 4) # 设置缩进
        settings.setdefault('sort_keys', not PY3) # 设置排序

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = dumps(data, **settings) + "\n" # 序列化

    resp = make_response(dumped, code) # 创建响应
    resp.headers.extend(headers or {}) # 添加头部
    return resp
