# Import necessary modules
import os  # for interacting with the operating system
from dotenv import load_dotenv  # for loading environment variables from a .env file

# Load environment variables from a .env file
load_dotenv()

# Configuration class to store various settings and environment variables
class Config:
    # URI for connecting to the database, fetched from the environment variable "DATABASE_URL"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    
    # Disable tracking modifications of objects and their changes in the database to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret key for securely signing sessions and cookies, fetched from the environment variable "SECRET_KEY"
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    # Type of session management to use (e.g., 'filesystem', 'redis', etc.), fetched from the environment variable "SESSION_TYPE"
    SESSION_TYPE = os.getenv("SESSION_TYPE")
    
    # Hugging Face Token for accessing Hugging Face APIs or models, fetched from the environment variable "HUGGINGFACE_TOKEN"
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN") 
    
    # Address 
    ADDRESS = "Bhopal, Madhya Pradesh"
    
    # Contact information for my website
    CONTACT_INFO = (
        "You can contact at sneha280904@gmail.com or call +91-6266258679."
    )

    # File paths for various dataset files
    DATASET_FILE = "D:/Coding/Python-Projects/QuickBot-Chat/dataset/dataset.json"


