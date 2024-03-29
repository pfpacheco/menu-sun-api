# settings.py
from pathlib import Path  # python3 only
from dotenv import load_dotenv

load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)
