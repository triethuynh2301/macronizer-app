from macronizer_cores import create_app
from config import ProductionConfig, DevelopmentConfig, FLASK_ENV

# determine the environment to run the app (development by default)
app_config = DevelopmentConfig
if FLASK_ENV == 'production':
    app_config = ProductionConfig


app = create_app(app_config)


if __name__ == '__main__':
    app.run()