from flask.cli import FlaskGroup
from os import getenv
from mast import create_app, db, bcr
from mast.models import User

app = create_app()

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    hashed_password = bcr.generate_password_hash(getenv('ADMIN_PASSWD')).decode('UTF-8')

    db.session.add(
        User(email="matfyz.sdc@gmail.com", password=hashed_password)
    )
    db.session.commit()


if __name__ == "__main__":
    cli()
