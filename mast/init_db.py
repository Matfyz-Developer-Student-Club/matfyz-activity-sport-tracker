from mast import db
from mast.models import Season, ChallengePart
from datetime import date

from mast.models import User, Activity, UserType, Sex, Age, ActivityType
from datetime import datetime, time


def init():
    """
    Creates all DB tables and fills Season and ChallengePart
    """
    db.create_all()

    # season = Season(title='ZS 2020/2021',
    #                 start_date=date(year=2020, month=11, day=12),
    #                 end_date=date(year=2020, month=12, day=20))
    season = Season(title='ZS 2020/2021',
                    start_date=date(year=2020, month=11, day=1),
                    end_date=date(year=2020, month=12, day=20))
    db.session.add(season)
    db.session.flush()

    part = ChallengePart(season_id=season.id,
                         order=0,
                         target='MFF, Ke Karlovu 3',
                         distance=0)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=1,
                         target='Hrčava (nejvýchodnější bod ČR)',
                         distance=500)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=2,
                         target='Nová Sedlica (nejvýchodnější bod SR)',
                         distance=388)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=3,
                         target='Oravská Polhora (nejsevernější bod SR)',
                         distance=324)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=4,
                         target='Varšava',
                         distance=518)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=5,
                         target='Gdaňsk',
                         distance=446)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=6,
                         target='Berlín',
                         distance=685)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=7,
                         target='Brémy',
                         distance=472)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=8,
                         target='Bremenhaven',
                         distance=94)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=9,
                         target='Amsterdam',
                         distance=461)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=10,
                         target='Brussel',
                         distance=260)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=11,
                         target='Lucemburk',
                         distance=269)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=12,
                         target='Paříž',
                         distance=352)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=13,
                         target='Bern',
                         distance=724)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=14,
                         target='Monako',
                         distance=650)
    db.session.add(part)

    db.session.commit()


# def test_data():
#     user = User(email='a@b.cz', password='', name='Donald', surname='Trump',
#                 sex=Sex.Male, age=Age.Over35, type=UserType.Student)
#     db.session.add(user)
#     db.session.flush()
#
#     activity = Activity(datetime=datetime(2020, 11, 5, 15, 32, 15), distance=12.5, duration=time(0, 18, 45),
#                         average_duration_per_km=time(0, 1, 30), type=ActivityType.Run, user_id=user.id)
#     db.session.add(activity)
#
#     activity = Activity(datetime=datetime(2020, 11, 5, 18, 12, 15), distance=10, duration=time(0, 18, 40),
#                         average_duration_per_km=time(0, 1, 52), type=ActivityType.Run, user_id=user.id)
#     db.session.add(activity)
#
#     activity = Activity(datetime=datetime(2020, 11, 7, 18, 12, 15), distance=10, duration=time(0, 18, 40),
#                         average_duration_per_km=time(0, 1, 52), type=ActivityType.Ride, user_id=user.id)
#     db.session.add(activity)
#
#     activity = Activity(datetime=datetime(2020, 11, 8, 18, 12, 15), distance=15, duration=time(0, 28, 0),
#                         average_duration_per_km=time(0, 1, 52), type=ActivityType.Ride, user_id=user.id)
#     db.session.add(activity)
#
#     user = User(email='a@b.com', password='', name='Joe', surname='Biden',
#                 sex=Sex.Male, age=Age.Over35, type=UserType.Student)
#     db.session.add(user)
#     db.session.flush()
#
#     activity = Activity(datetime=datetime(2020, 11, 5, 15, 32, 15), distance=10, duration=time(0, 20, 0),
#                         average_duration_per_km=time(0, 2, 0), type=ActivityType.Run, user_id=user.id)
#     db.session.add(activity)
#
#     activity = Activity(datetime=datetime(2020, 11, 5, 18, 12, 15), distance=8, duration=time(0, 8, 0),
#                         average_duration_per_km=time(0, 1, 0), type=ActivityType.Run, user_id=user.id)
#     db.session.add(activity)
#
#     activity = Activity(datetime=datetime(2020, 11, 7, 18, 12, 15), distance=5, duration=time(0, 18, 40),
#                         average_duration_per_km=time(0, 1, 52), type=ActivityType.Ride, user_id=user.id)
#     db.session.add(activity)
#
#     activity = Activity(datetime=datetime(2020, 11, 8, 18, 12, 15), distance=18, duration=time(0, 28, 0),
#                         average_duration_per_km=time(0, 1, 52), type=ActivityType.Ride, user_id=user.id)
#     db.session.add(activity)
#
#     db.session.commit()


if __name__ == '__main__':
    init()
    test_data()
