from requests import Session
import json
import ua

# region urls
url_login = "http://dxx.scyol.com/backend/adminUser/login"
url_login_info = "http://dxx.scyol.com/backend/adminUser/loginInfo"
url_stage_url = "http://dxx.scyol.com/backend/stages/list"
url_stu_list  = "http://dxx.scyol.com/backend/study/student/list"
# endregion

# region headers
header_common = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Host": "dxx.scyol.com",
    "Origin": "http://dxx.scyol.com",
    "Referer": "http://dxx.scyol.com/dxxBackend/"
}

def get_login_header()->dict:
    return {
        **header_common,
        "Cookie":"sidebarStatus=0",
        "User-Agent":ua.chrome
    }
def get_stage_header(token:str)->dict:
    """for stage and list
    """
    return {
        **get_login_header(),
        "token":token
    }
# endregion
# region payload
def get_login_payload(user:str,passwd:str)->dict:
    return {
        "username": user,
        "password": passwd
    }
def get_list_payload(stage:int,org:int)->dict:
    return {
        "stagesId": stage,
        "orgId": org,
        "name": "",
        "tel": "",
        "pageNo": 1,
        "pageSize": 40
    }
# endregion
# {"data":{ "token": "", "orgId": 0 } }
def user_login(sess:Session,user:str,passwd:str)->dict:
    """login to backend
    @return {"token":token,"orgId":orgId}
    """
    resp = sess.post(url_login, headers=get_login_header(),
        data=json.dumps(get_login_payload(user,passwd)).encode("utf-8"))
    response = resp.json()
    if response["code"] != 200:
        raise RuntimeError(response["msg"])
    return {
        "token": response["data"]["token"],
        "orgId": response["data"]["orgId"]
    }

# { "data": [{"id": 5,},], }
def get_stage_info(sess:Session,token:str)->int:
    # url = f"{url_login_info}?token={token}" # seems no need
    payload = { "pageNo": 1, "pageSize": 500 }
    resp = sess.post(url_stage_url,data=json.dumps(payload),
        headers=get_stage_header(token))
    data = json.loads(resp.text)["data"]
    return 0 if len(data) == 0 else data[0]["id"]

# "data": [{
    # "name": "",
    # "startTime": 1648460438,
    # "startTimeStr": "2022-03-28 17:40:38",
# }]
def get_study_list(sess:Session,token:str,stage:int,orgId:int)->list:
    resp = sess.post(url_stu_list,headers=get_stage_header(token),
        data=json.dumps(get_list_payload(stage,orgId)).encode("utf-8"))
    Json = resp.json()
    if Json["code"] != 200:
        print(Json["msg"])
        return []
    else:
        return Json["data"]


def login_for_list(user:str,passwd:str,stage:int=0)->list:
    session = Session()
    data = user_login(session,user,passwd)
    token = data["token"]
    orgId = data["orgId"]
    maxStage = get_stage_info(session,token)
    results = [] if stage > maxStage else get_study_list(session,token,maxStage if stage == 0 else stage,orgId)
    session.close()
    return results

# [print(it["name"],it["startTimeStr"]) for it in login_for_list("2019级计算机第六团支部","123456")]