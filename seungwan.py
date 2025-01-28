from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    print("Hello langchain")
    print(os.environ['OPEN_API_KEY'])