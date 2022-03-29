class checker:
  accounts:list = []
  students:dict = {}
  def update(self):
    pass
  def has_study(self,name:str,stage:int=0)->bool:
    # update if doesn't contain
    return False
  def study_time(self,name:str,stage:int=0)->str:
    pass
  def add_account(self,name:str,passwd:str)->bool:
    return True
  def study_list(self,cls:str,stage:int=0)->list:
    if cls in self.students:
      return [f'{it["name"]},{it["startTimeStr"]}' for it in self.students[cls]]
    else:
      return []