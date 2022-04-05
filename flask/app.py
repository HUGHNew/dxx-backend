from checker import checker
from threading import Thread
from flask import Flask, Response, make_response, request
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={r"/*": {"origins": "*"}})
Checker = checker("account.json")

def wrapper(content:dict)->Response:
  """wrapper of response for charset
  """
  resp = make_response(content)
  resp.mimetype = "application/json; charset=utf-8"
  return resp
# add default accounts
@app.route("/user/add",methods=["POST"])
def add_admin():
  account = request.get_json()
  if ("username" in account and "password" in account and
    Checker.add_account(account["username"],account["password"])):
    return {
      "code":200,
      "msg": "add account successfully"
    }
  else:
    msg = Checker.get_err_msg()
    return wrapper({
      "code":400,
      "msg":msg if msg != "" else "invalid username or password"
    })

@app.route("/user/check/<string:name>")
def check_user(name):
  if len(name)>4:
    return {
      "code":401,
      "msg": "name is to long"
    }
  return {
    "code":200,
    "status": Checker.has_study(name)
  }

@app.route("/user/time/<string:name>")
def check_user_time(name):
  if len(name)>4:
    return wrapper({
      "code":401,
      "msg": "name is to long"
    })
  return wrapper({
    "code":200,
    "time": Checker.get_study_time(name)[1]
  })

@app.route("/count/<string:cls>")
def counts_user(cls):
  return wrapper({
    "code": 200,
    "count": Checker.study_count(cls)
  })

@app.route("/list/<string:cls>")
def list_all(cls):
  return wrapper({
    "code": 200,
    "data": Checker.study_list(cls)
  })
@app.route("/update")
def force_update():
  Thread(target=Checker.update_all()).start()
  return {
    "code": 200,
    "status": "updating"
  }
@app.route("/")
def hello():
  return "<h1>Hello, this is the backend of dxx</h1>"
if __name__=="__main__":
  app.run(host="127.0.0.1",port=5000)