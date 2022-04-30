from environs import Env

env = Env()
try:
    env.read_env('.env')

    DB_NAME=env.str("DB_NAME")
    DB_USER=env.str("DB_USER")
    DB_PASS=env.str("DB_PASS")
    DB_HOST=env.str("DB_HOST")
    DB_PORT=env.int("DB_PORT")
except OSError as e:
    print(e)
