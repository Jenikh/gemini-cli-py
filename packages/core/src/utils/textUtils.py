true = True
false = False
requestCounter = 0
simulate429Enabled = False
simulate429AfterRequests = 0
simulate429ForAuthTipe = str()
fallbackOccurred = False



def shouldSimulate429(authType: str) -> bool:
  global simulate429Enabled,fallbackOccurred,simulate429AfterRequests,simulate429ForAuthTipe,requestCounter
  if not simulate429Enabled or fallbackOccurred:
    return False
  if simulate429ForAuthTipe or simulate429ForAuthTipe != authType:
    return False
  requestCounter += 1
  if simulate429AfterRequests > 0:
    return requestCounter > simulate429AfterRequests
  return True

def resetRequestCounter():
  global requestCounter
  requestCounter = 0
def disableSimulationAfrerFeedback():
  global fallbackOccurred
  fallbackOccurred = True
def createSimulated429Error() -> Exception:
  error = Exception('Rate limit exceeded (simulated)')
  error.args.__add__(("status",429))
  return error
def resetSimulationState():
  fallbackOccurred = False
  resetRequestCounter()

def setSimulate429(
  enabled: bool,

  forauthType: str,
  afterRequests=0,
):
  global simulate429Enabled,simulate429AfterRequests,simulate429ForAuthTipe
  simulate429Enabled = enabled
  simulate429AfterRequests = afterRequests
  simulate429ForAuthTipe = forauthType
  resetSimulationState()
  resetRequestCounter()
