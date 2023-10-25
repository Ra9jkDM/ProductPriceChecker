import json
from os import environ

NAME = ".env_json"
ENV = ".env"

settings = {
    "flask": {
        "SECRET_KEY": "",
        "prefix": "",
    },
    "api": {
        "url": "http://127.0.0.1:3000",
    },
    "database": {
        "dialect": "postgresql+psycopg2",
        "username": "postgres",
        "password": "",
        "host": "localhost",
        "port": "5432",
        "name": "get_price"
    },
    "s3": {
        "host": "localhost",
        "port": "9000", 
        "bucket": "get-price",
        "access_key": "",
        "secret_key": "",
        "secure": "0",
    }
}

def create_settings_template():
    with open(NAME, 'w') as f:
        data = json.dumps(settings, indent=4)
        f.write(data)

def create_env_file():
    env = None
    with open(NAME) as f:
        data = f.read()
        env = json.loads(data)

    with open(ENV, "w") as f:
        for key, value in env.items():
            for key1, value1 in value.items():
                if key1.isupper(): 
                    # environ[key1] = value1
                    f.write(f"{key1}={value1}\n")
                else:
                    # environ[f"{key}_{key1}"] = value1
                    f.write(f"{key}_{key1}={value1}\n")


def show_env():
    print("Enviroment variables:")
    for name, value in environ.items():
        print(f"\t{name}: {value}")

if __name__ == "__main__":
    # create_settings_template()
    create_env_file()
    show_env()