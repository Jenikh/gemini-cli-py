import os
import platform
import sys

env = os.environ

def shouldAttemptBrowserLaunch() -> bool:
  browserBlockList = ['www-browser']
  browserEnv = env["BROWSER"]
  if browserEnv and browserBlockList.__contains__(browserEnv):
    return False
  if env['CI'] or env['DEBIAN_FRONTEND'] == 'noninteractive':
    return False
  isLinux = platform.system() == "Linux" or sys.platform.startswith('linux')
  isSSH = env['SHH_CONECTION']
  if isLinux:
    displayVariables = ['DISPLAY', 'WAYLAND_DISPLAY','MIR_SOCKET']
    has_display = any(bool(env.get(v)) for v in displayVariables)
    if not has_display:
      return False
  if isSSH and not isLinux:
    return False
  return True

