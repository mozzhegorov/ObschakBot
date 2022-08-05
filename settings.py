import configparser

config = configparser.ConfigParser()
config.read('/home/.env')

general_env = config["General"]

DATABASE = general_env['DATABASE']
API_TOKEN = general_env['API_TOKEN']
