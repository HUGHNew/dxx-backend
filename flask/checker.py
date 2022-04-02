import json
import crawler
class checker:
  accounts:list = []
  """
  {
    "username":"",
    "password":""
  }
  """
  students:dict = {}
  """
  {
    "cls":[
      {
        "name":"",
        "startTimeStr":""
      }
    ]
  }
  """
  last_err:str = ""
  def __init__(self,file:str) -> None:
    with open(file) as fd:
      users = json.loads(fd.read())
    for item in users:
      self.add_account(item["username"],item["password"])
  def get_study_time(self,name:str)->tuple:
    time = ""
    cls = ""
    for k,v in self.students.items():
      for i in v:
        if i["name"] == name:
          cls = k
          time = i["startTimeStr"]
    return cls,time
  def update(self,cls:str):
    for i in self.accounts:
      if cls == i["username"]:
        self.students[cls] = crawler.login_for_list(cls,i["password"])
  def update_all(self):
    for i in self.accounts:
      self.students[i["username"]] = crawler.login_for_list(i["username"],i["password"])
  def study_count(self,cls:str)->int:
    return len(self.students[cls]) if cls in self.students else -1
  def has_study(self,name:str,stage:int=0)->bool:
    return self.study_time(name,stage) != ""
  def study_time(self,name:str,stage:int=0)->str:
    cls,time = self.get_study_time(name)
    if time == "":
      self.update(cls)
    cls,time = self.get_study_time(name)
    return time
  def add_account(self,name:str,passwd:str)->bool:
    account = {
      "username":name,
      "password":passwd
    }
    if account in self.accounts:
      return True
    else:
      self.accounts.append(account)
      try:
        self.update(name)
      except RuntimeError as re:
        self.last_err = re.args[0]
        return False
      return True
  def study_list(self,cls:str,stage:int=0)->list:
    if cls in self.students:
      return [f'{it["name"]},{it["startTimeStr"]}' for it in self.students[cls]]
    else:
      return []
  def get_err_msg(self)->str:
    return self.last_err