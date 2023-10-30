# app/services/db/clean_db.py

# app/db/clean_db.py

from sqlalchemy.orm import Session
from app.db.session import engine
from app.db.base import Base
import click

@click.command()
def clean_db():
    """
    Borrar todos los datos de la base de datos.
    """
    with Session(engine) as session:
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()

if __name__ == "__main__":
    clean_db()
