from src import app, db
from src.models import User, History
if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=80)
