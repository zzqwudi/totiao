import re


# 验证手机号正则
def mobile(mobile_code):
    if re.match(r"^1[3-9]\d{9}$", mobile_code):
        return mobile_code
    else:
        raise ValueError(f"{mobile_code}手机号码格式错误")


def code(code_str):
    if re.match(r"^\d{6}$", code_str):
        return code_str
    else:
        raise ValueError(f"{code_str}验证码格式错误")
