'''Run the app.'''
import os

from app import create_app
configure = os.getenv('APP_SETTINGS')
app = create_app(configure)

if __name__ == "__main__":
	app.run()