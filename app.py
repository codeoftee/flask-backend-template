from dotenv import load_dotenv
from os.path import join, dirname

from server import create_app

env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)

app = create_app()
