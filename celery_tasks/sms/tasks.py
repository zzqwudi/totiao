import json

from ronglian_sms_sdk import SmsSDK

from celery_tasks.main import celery_app

accId = '8aaf0708802d0d8501804495ffb30537'
accToken = '4f3346359d6c459abec923da5e408254'
appId = '8aaf0708802d0d8501804ad81f55077c'


@celery_app.task(name='send_message')
def send_message(mobile, code, exc_time):
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    datas = (code, exc_time)
    resp = sdk.sendMessage(tid, mobile, datas)
    resp_info = json.loads(resp).get('statusCode')
    return True if resp_info == '000000' else False
