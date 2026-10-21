from dotenv import load_dotenv
load_dotenv()  # lê o .env e injeta as variáveis em os.environ

import os
print(os.environ["RESEND_API_KEY"])
print(os.environ["FLASK_SECRET_KEY"])