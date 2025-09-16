from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

fast_check_api = os.getenv("FAST_CHECK_API_KEY")

def get_factcheck_service():
    service = build("factchecktools", "v1alpha1", developerKey=fast_check_api)
    return service