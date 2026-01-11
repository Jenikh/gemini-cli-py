def assumeExhaustive(value): return {}
def checkExhaustive(value,msg="unexpected value ${value}!"):
  msg = msg.replace("${value}",str(value))
  raise Exception(msg)
