# from mast.models import Season, ChallengePart
from mast.models import Season, ChallengePart, User, Activity, ActivityType, CyclistsChallengePart, StudyField
# from datetime import date
from datetime import date, time, datetime
import logging
from mast import db, create_app


def init():
    """
    Creates all DB tables and fills Season and ChallengePart
    """
    logging.info("Creating DB")
    db.drop_all()
    db.create_all()

    # season = Season(title='ZS 2020/2021',
    #                 start_date=date(year=2020, month=11, day=12),
    #                 end_date=date(year=2020, month=12, day=20))
    season = Season(title='ZS 2020/2021',
                    start_date=date(year=2020, month=11, day=1),
                    end_date=date(year=2020, month=12, day=20))

    # season = Season(title='LS 2020/2021',
    #                 start_date=date(year=2021, month=3, day=29),
    #                 end_date=date(year=2021, month=6, day=30))
    db.session.add(season)
    db.session.flush()

    part = ChallengePart(season_id=season.id,
                         order=0,
                         target='Praha',
                         distance=0)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=1,
                         target='Mnichov',
                         distance=500)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=2,
                         target='Ulm',
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

    cyclo = CyclistsChallengePart(target="Torino",
                                  distance=0,
                                  altitude=239,
                                  cycle=0)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Corso San Maurizio",
                                  distance=7,
                                  altitude=237,
                                  cycle=0)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Lungo",
                                  distance=19,
                                  altitude=225,
                                  cycle=0)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Ingr. Parco del Val",
                                  distance=30,
                                  altitude=224,
                                  cycle=0)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Castello Del Valentino",
                                  distance=37,
                                  altitude=231,
                                  cycle=0)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Ponte Ballbis",
                                  distance=55,
                                  altitude=229,
                                  cycle=0)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Corso Moncalieri",
                                  distance=61,
                                  altitude=230,
                                  cycle=0)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Incr. Ponte Umberto",
                                  distance=83,
                                  altitude=230,
                                  cycle=0)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Torino",
                                  distance=90,
                                  altitude=222,
                                  cycle=0)

    db.session.add(cyclo)

    db.session.commit()


def test_data():
    logging.info("Inserting test data")

    user = User(email='a@b.cz', password='')
    user.complete_profile(first_name='Donald', last_name='Trump', sex='male',
                          shirt_size='L', user_type='student', ukco='', anonymous=False, study_field=StudyField.Mat)

    activity = Activity(datetime=datetime(2020, 11, 5, 15, 32, 15), distance=12.5, duration=time(0, 18, 45),
                        average_duration_per_km=time(0, 1, 30), type=ActivityType.Run, user_id=user.id, strava_id=1)
    db.session.add(activity)

    activity = Activity(datetime=datetime(2020, 11, 5, 18, 12, 15), distance=10, duration=time(0, 18, 40),

                        average_duration_per_km=time(0, 1, 52), type=ActivityType.Run, user_id=user.id, strava_id=1)
    db.session.add(activity)

    activity = Activity(datetime=datetime(2020, 11, 7, 18, 12, 15), distance=10, duration=time(0, 18, 40),
                        average_duration_per_km=time(0, 1, 52), type=ActivityType.Ride, user_id=user.id, strava_id=1)
    db.session.add(activity)

    activity = Activity(datetime=datetime(2020, 11, 7, 18, 12, 15), distance=10, duration=time(0, 18, 40),
                        average_duration_per_km=time(0, 1, 52), type=ActivityType.InlineSkate, user_id=user.id)
    db.session.add(activity)

    activity = Activity(datetime=datetime(2020, 11, 8, 18, 12, 15), distance=15, duration=time(0, 28, 0),
                        average_duration_per_km=time(0, 1, 52), type=ActivityType.Ride, user_id=user.id, strava_id=1)
    db.session.add(activity)

    activity = Activity(datetime=datetime(2020, 11, 8, 18, 12, 15), distance=17, duration=time(0, 28, 0),
                        average_duration_per_km=time(0, 1, 52), type=ActivityType.Run, user_id=user.id, strava_id=1)
    db.session.add(activity)

    user = User(email='a@b.com', password='')
    user.complete_profile(first_name='Joe', last_name='Biden', sex='male',
                          shirt_size='L', user_type='student', ukco='', anonymous=False, study_field=StudyField.Inf)

    activity = Activity(datetime=datetime(2020, 11, 5, 15, 32, 15), distance=10, duration=time(0, 20, 0),
                        average_duration_per_km=time(0, 2, 0), type=ActivityType.Run, user_id=user.id, strava_id=1)
    db.session.add(activity)

    activity = Activity(datetime=datetime(2020, 11, 5, 18, 12, 15), distance=8, duration=time(0, 8, 0),
                        average_duration_per_km=time(0, 1, 0), type=ActivityType.Run, user_id=user.id, strava_id=1)
    db.session.add(activity)

    activity = Activity(datetime=datetime(2020, 11, 7, 18, 12, 15), distance=5, duration=time(0, 18, 40),
                        average_duration_per_km=time(0, 1, 52), type=ActivityType.Ride, user_id=user.id, strava_id=1)

    db.session.add(activity)

    activity = Activity(datetime=datetime(2020, 11, 8, 18, 12, 15), distance=18, duration=time(0, 28, 0),
                        average_duration_per_km=time(0, 1, 52), type=ActivityType.Ride, user_id=user.id, strava_id=1)
    db.session.add(activity)

    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    init()
    test_data()
