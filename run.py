'''Run the app.'''
import os

from app import create_app
configuration = os.getenv('APP_SETTINGS')
app = create_app()
port = os.getenv("PORT", 5000)
if _name_ == "_main_":
	app.run(host='0.0.0.0', port=port)