# from mast.models import Season, ChallengePart
from mast.models import Role, Season, ChallengePart, User, Activity, ActivityType, CyclistsChallengePart, StudyField
# from datetime import date
from datetime import date, time, datetime
import logging
from mast import db, create_app, bcr
import os


def init():
    """
    Creates all DB tables and fills Season and ChallengePart
    """
    logging.info(db)
    logging.info("Creating DB")
    db.drop_all()
    db.create_all()

    season = Season(title='LS 2020/2021',
                    start_date=date(year=2021, month=3, day=29),
                    end_date=date(year=2021, month=6, day=30))
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
                         distance=470)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=2,
                         target='Ulm',
                         distance=233)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=3,
                         target='Weil der Stadt',
                         distance=125)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=4,
                         target='Frankfurt',
                         distance=207)

    part = ChallengePart(season_id=season.id,
                         order=5,
                         target='Brussel',
                         distance=457)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=6,
                         target='London',
                         distance=475)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=7,
                         target='Colchester',
                         distance=127)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=8,
                         target='Oxford',
                         distance=231)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=9,
                         target='Cambridge',
                         distance=175)

    part = ChallengePart(season_id=season.id,
                         order=10,
                         target='Kirkcudbrightshire',
                         distance=736)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=11,
                         target='Lurgan',
                         distance=300)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=12,
                         target='Glasgow',
                         distance=332)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=13,
                         target='Edinburgh',
                         distance=96)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=14,
                         target='Newcastle',
                         distance=288)

    part = ChallengePart(season_id=season.id,
                         order=15,
                         target='Woolsthorpe by Coisterworth',
                         distance=469)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=16,
                         target='Cambridge',
                         distance=144)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=17,
                         target='London',
                         distance=116)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=19,
                         target='Briston',
                         distance=266)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=21,
                         target='Den Helder',
                         distance=0)

    part = ChallengePart(season_id=season.id,
                         order=21,
                         target='Utrecht',
                         distance=138)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=22,
                         target='Lennep',
                         distance=267)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=23,
                         target='Kodaň',
                         distance=1032)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=24,
                         target='Berlín',
                         distance=659)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=25,
                         target='Varšava',
                         distance=772)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=26,
                         target='Praha',
                         distance=912)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=27,
                         target='Mnichov',
                         distance=470)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=28,
                         target='Corych',
                         distance=385)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=29,
                         target='Smiljan',
                         distance=1018)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=30,
                         target='Bělehrad',
                         distance=726)
    db.session.add(part)

    part = ChallengePart(season_id=season.id,
                         order=31,
                         target='Titel',
                         distance=62)
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

    cyclo = CyclistsChallengePart(target="Stupinigi",
                                  distance=0,
                                  altitude=240,
                                  cycle=1)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Carignano",
                                  distance=88,
                                  altitude=232,
                                  cycle=1)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Casalgrasso",
                                  distance=199,
                                  altitude=240,
                                  cycle=1)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Racconigi",
                                  distance=280,
                                  altitude=260,
                                  cycle=1)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Carmagnola",
                                  distance=389,
                                  altitude=240,
                                  cycle=1)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Santena",
                                  distance=523,
                                  altitude=237,
                                  cycle=1)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Andezeno",
                                  distance=664,
                                  altitude=277,
                                  cycle=1)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Gallareto",
                                  distance=812,
                                  altitude=222,
                                  cycle=1)
    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Villadeati",
                                  distance=1048,
                                  altitude=330,
                                  cycle=1)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Bv. Tricerro",
                                  distance=1375,
                                  altitude=132,
                                  cycle=1)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Novara",
                                  distance=1730,
                                  altitude=160,
                                  cycle=1)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Biella",
                                  distance=0,
                                  altitude=341,
                                  cycle=2)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Cavaglia",
                                  distance=124,
                                  altitude=272,
                                  cycle=2)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Cigliano",
                                  distance=258,
                                  altitude=237,
                                  cycle=2)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Crescentino",
                                  distance=414,
                                  altitude=155,
                                  cycle=2)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Cavallo Grigio",
                                  distance=566,
                                  altitude=251,
                                  cycle=2)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Asti",
                                  distance=864,
                                  altitude=125,
                                  cycle=2)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Bric Delle Forche",
                                  distance=1224,
                                  altitude=522,
                                  cycle=2)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Castino",
                                  distance=1447,
                                  altitude=540,
                                  cycle=2)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Manera",
                                  distance=1539,
                                  altitude=625,
                                  cycle=2)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Guarene",
                                  distance=1753,
                                  altitude=360,
                                  cycle=2)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Canale",
                                  distance=1870,
                                  altitude=193,
                                  cycle=2)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Piacenza",
                                  distance=0,
                                  altitude=54,
                                  cycle=3)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Fidenza",
                                  distance=302,
                                  altitude=76,
                                  cycle=3)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Parma",
                                  distance=534,
                                  altitude=55,
                                  cycle=3)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Canossa",
                                  distance=869,
                                  altitude=508,
                                  cycle=3)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Castello di Carpineti",
                                  distance=1107,
                                  altitude=780,
                                  cycle=3)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Ponte Secchia",
                                  distance=1236,
                                  altitude=287,
                                  cycle=3)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Montemolino",
                                  distance=1423,
                                  altitude=933,
                                  cycle=3)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Ponte di Strettara",
                                  distance=1627,
                                  altitude=548,
                                  cycle=3)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Sestola",
                                  distance=1860,
                                  altitude=1020,
                                  cycle=3)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Modena",
                                  distance=0,
                                  altitude=34,
                                  cycle=4)
    d
    b.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Bologna",
                                  distance=353,
                                  altitude=74,
                                  cycle=4)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Toscanella di Dozza",
                                  distance=628,
                                  altitude=68,
                                  cycle=4)

    cyclo = CyclistsChallengePart(target="Forli",
                                  distance=997,
                                  altitude=30,
                                  cycle=4)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Budrio",
                                  distance=1297,
                                  altitude=34,
                                  cycle=4)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Cattolica",
                                  distance=1710,
                                  altitude=9,
                                  cycle=4)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Grotte di Frasassi",
                                  distance=0,
                                  altitude=225,
                                  cycle=5)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Castelraimondo",
                                  distance=216,
                                  altitude=313,
                                  cycle=5)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Maddalena",
                                  distance=406,
                                  altitude=428,
                                  cycle=5)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Visso",
                                  distance=604,
                                  altitude=602,
                                  cycle=5)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Forca di Gualdo",
                                  distance=781,
                                  altitude=1496,
                                  cycle=5)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Forca di Presta",
                                  distance=905,
                                  altitude=1536,
                                  cycle=5)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Quintodecimo",
                                  distance=1118,
                                  altitude=407,
                                  cycle=5)

    cyclo = CyclistsChallengePart(target="Ascoli Piceno",
                                  distance=1331,
                                  altitude=153,
                                  cycle=5)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Ascoli Piceno (S.Giacomo)",
                                  distance=1500,
                                  altitude=1090,
                                  cycle=5)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Notaresco",
                                  distance=0,
                                  altitude=62,
                                  cycle=6)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Montesilviano",
                                  distance=277,
                                  altitude=4,
                                  cycle=6)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Chieti",
                                  distance=599,
                                  altitude=330,
                                  cycle=6)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Crecchio",
                                  distance=908,
                                  altitude=202,
                                  cycle=6)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Marina di San Vito",
                                  distance=1127,
                                  altitude=14,
                                  cycle=6)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Marina di Vasto",
                                  distance=1511,
                                  altitude=15,
                                  cycle=6)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Termoli",
                                  distance=1780,
                                  altitude=39,
                                  cycle=6)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Foggia",
                                  distance=0,
                                  altitude=78,
                                  cycle=7)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Svinc. di Volturara Appula",
                                  distance=434,
                                  altitude=347,
                                  cycle=7)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Campobasso",
                                  distance=835,
                                  altitude=710,
                                  cycle=7)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Bocca della Selva",
                                  distance=1196,
                                  altitude=1393,
                                  cycle=7)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Cerreto Sannita",
                                  distance=1485,
                                  altitude=287,
                                  cycle=7)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Guardia Sanframondi",
                                  distance=1730,
                                  altitude=445,
                                  cycle=7)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Castel di Sangro",
                                  distance=0,
                                  altitude=820,
                                  cycle=8)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Passo Godi",
                                  distance=363,
                                  altitude=1556,
                                  cycle=8)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Anversa degli Abruzzi",
                                  distance=658,
                                  altitude=556,
                                  cycle=8)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Forca Caruso",
                                  distance=1028,
                                  altitude=1107,
                                  cycle=8)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Ovindoli",
                                  distance=1337,
                                  altitude=1378,
                                  cycle=8)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Campo Felice",
                                  distance=1600,
                                  altitude=1655,
                                  cycle=8)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="L'Aquila",
                                  distance=0,
                                  altitude=637,
                                  cycle=9)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Terme id Cotilia",
                                  distance=386,
                                  altitude=409,
                                  cycle=9)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Piediluco",
                                  distance=743,
                                  altitude=381,
                                  cycle=9)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Valico della Somma",
                                  distance=1008,
                                  altitude=655,
                                  cycle=9)

    db.session.add(cyclo)

    cyclo = CyclistsChallengePart(target="Foligno",
                                  distance=1400,
                                  altitude=226,
                                  cycle=9)

    db.session.add(cyclo)

    db.session.commit()


def test_data():
    logging.info("Inserting test data")

    user = User(email='a@b.cz', password='')
    user.complete_profile(first_name='Donald', last_name='Trump', sex='male',
                          shirt_size='L', user_type='student', ukco='', anonymous=False, study_field=StudyField.Mat,
                          competing=True)

    activity = Activity(datetime=datetime(2020, 11, 5, 15, 32, 15), distance=12.5, duration=time(0, 18, 45),
                        average_duration_per_km=time(0, 1, 30), type=ActivityType.Run, user_id=user.id, strava_id=1)
    db.session.add(activity)

    activity = Activity(datetime=datetime(2020, 11, 5, 18, 12, 15), distance=10, duration=time(0, 18, 40),

                        average_duration_per_km=time(0, 1, 52), type=ActivityType.Run, user_id=user.id, strava_id=1)
    db.session.add(activity)

    activity = Activity(datetime=datetime(2020, 11, 7, 18, 12, 15), distance=10, duration=time(0, 18, 40),
                        average_duration_per_km=time(0, 1, 52), type=ActivityType.Ride, user_id=user.id, strava_id=1)
    db.session.add(activity)

    activity = Activity(datetime=datetime(2020, 11, 8, 18, 12, 15), distance=15, duration=time(0, 28, 0),
                        average_duration_per_km=time(0, 1, 52), type=ActivityType.Ride, user_id=user.id, strava_id=1)
    db.session.add(activity)

    activity = Activity(datetime=datetime(2020, 11, 8, 18, 12, 15), distance=17, duration=time(0, 28, 0),
                        average_duration_per_km=time(0, 1, 52), type=ActivityType.Run, user_id=user.id, strava_id=1)
    db.session.add(activity)

    user = User(email='a@b.com', password='')
    user.complete_profile(first_name='Joe', last_name='Biden', sex='male',
                          shirt_size='L', user_type='student', ukco='', anonymous=False, study_field=StudyField.Inf,
                          competing=True)

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
    # test_data()
