from WebAutomator import webautomator
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("URL")
user = os.getenv("USER")
password = os.getenv("PASSWORD")

web = webautomator(url, user, password).WebRobot()