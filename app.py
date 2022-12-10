from flask import Flask
from flask_sqlalchemy import SQLAlchemy

driver="ODBC Driver 17 for SQL Server"
params = "%s:%s@%s/%s?driver=%s" % (
    'CanvasExtensionUser',
    'K6HfLD0pRc5q',
    'avenues-canvas-extension.database.windows.net:1433',
    'CanvasExtension',
	driver
)

# Create Flask app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI='mssql+pyodbc://%s' % params,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy()
db.init_app(app)