import requests
import json
from .config import SOME_ENV_VAR

def get_user_info(user_id=None):
    """识别用户身份"""
    if user_id is None:
        user_id = SOME_ENV_VAR
    # url = f"http://some-site-url/user/query"
    # params = {"user": user_id}
    # resp = requests.get(url, params=params)
    # resp.raise_for_status()
    # data = resp.json().get("data", {})
    # return {
    #     "userCode": data.get("userCode"),
    #     "userName": data.get("userName"),
    #     "deptName": data.get("deptName"),
    #     "email": data.get("email")
    # }
    return {
        "userCode": user_id,
        "userName": "demo_user_name",
        "deptName": "demo_dept_name",
        "email": ""
    }

def query_resources(criteria=None, user_id=None):
    """根据筛选条件查询特定资源数据"""
    if user_id is None:
        user_id = SOME_ENV_VAR
    result = []
    result.append({
        "id": 1,
        "title": "示例资源标题",
        "createdBy": "示例创建人",
        "createdTime": "2025-07-02 15:04:05",
        "updatedBy": "示例更新人",
        "updatedTime": "2025-07-03 15:04:05",
    })
    return result
