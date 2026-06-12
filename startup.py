# startup.py

import subprocess
import sys

subprocess.run([
    sys.executable, "-m", "streamlit", "run", "app/main.py",
    "--server.port", "8000",
    "--server.address", "0.0.0.0"
])