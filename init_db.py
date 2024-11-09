from sqlalchemy import create_engine
from models import Base
import populate_db

# Create an engine and initialize the database
engine = create_engine('sqlite:///risk_dashboard.db')
Base.metadata.create_all(engine)

# Populate the database with sample data
populate_db.main() 