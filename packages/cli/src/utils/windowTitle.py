import os
import re
def computeWindowTitle(folderName: str) -> str:
  """Computes the window title for the Gemini CLI application.

  Args:
      folderName: The name of the current folder/workspace to display in the title.

  Returns:
      The computed window title, either from the CLI_TITLE environment variable or the default Gemini title.
  """
  title = os.environ.get("CLI_TITLE") or f"Gemini - {folderName}"
  return re.sub(r'[\x00-\x1F\x7F]', '', title)
