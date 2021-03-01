import os

PRODUCTION = False

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # this is the project root

RESOURCES = os.path.join(ROOT_DIR, "resources")

API_BASE_URL = "/api/v1"
