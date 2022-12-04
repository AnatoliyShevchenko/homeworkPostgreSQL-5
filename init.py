from dotenv import load_dotenv
import os


load_dotenv()
def get_env(key: str):
    data: str = os.environ.get(key)
    if not data:
        raise KeyError('ERROR Key {} is not found'.format(key))

    return data