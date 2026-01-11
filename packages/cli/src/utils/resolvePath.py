import os


def resolvePath(path: str) -> str:
  user_profile = os.path.expanduser("~")
  if not path:
    return ""
  expandedPath = path.replace("\\", "/")
  if path.lower().startswith("%userprofile%"):
    expandedPath = user_profile + expandedPath[13:]
  elif path == "~" or path.startswith("~/"):
    expandedPath = user_profile + expandedPath[2:]
  return expandedPath.strip()
