from macronizer_cores import create_app
from macronizer_cores import db

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()