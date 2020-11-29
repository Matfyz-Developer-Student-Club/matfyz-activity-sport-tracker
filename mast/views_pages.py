import os
import datetime
import mast
from flask import redirect, request, render_template, url_for
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from mast.forms import LoginForm, RegisterForm, UpdateProfileForm, ChangePasswordForm, AddActivityForm
from mast.models import User, Competition, Sex, Age, Activity, ActivityType
from mast import bcr, queries, app, session
from mast.tools.sis_authentication import authenticate_via_sis
from mast.processor import GPXProcessor

UPLOAD_FILE_DIR = 'landing'
PROCESSOR = GPXProcessor()


def check_profile_verified(session_data: session.Session):
    if not current_user.is_completed():
        session_data.error('Your profile is not completed! Please, go to Settings and fill in your data.<br />' +
                           'Your activities will be considered only after your profile is verified.')
    elif not current_user.verified:
        session_data.warning('Your profile is not yet verified. ' +
                             'Let us know if you are sure you filled in correct data and it takes too long.<br />' +
                             'Your activities will be considered only after your profile is verified.')


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        form = LoginForm(request.form)
        if form.validate():
            user = User.query.filter_by(email=form.email.data.lower()).first()
            if user and bcr.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))
            else:
                form.email.errors.append(
                    'Specified pair of email and password is invalid!')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form = RegisterForm('register_form')
        return render_template('register.html', form=form)
    else:
        form = RegisterForm(request.form)
        if form.validate_on_submit():
            hashed_password = bcr.generate_password_hash(
                form.password.data.strip()).decode('UTF-8')
            user = User(email=form.email.data.lower().strip(),
                        password=hashed_password)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('register.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/personal_dashboard', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    session_data = mast.session.Session()
    db_query = mast.queries.Queries()
    add_activity_form = AddActivityForm()
    if add_activity_form.validate_on_submit():
        filename = secure_filename(add_activity_form.file.data.filename)
        path = os.path.join(__file__, os.pardir)
        add_activity_form.file.data.save(os.path.join(
            os.path.abspath(path), UPLOAD_FILE_DIR, filename))

        if add_activity_form.activity.data == ActivityType.Ride.name:
            a_type = ActivityType.Ride
        elif add_activity_form.activity.data == ActivityType.Run.name:
            a_type = ActivityType.Run
        else:
            a_type = ActivityType.Walk

        activity = PROCESSOR.process_input_data(filename)
        PROCESSOR.landing_cleanup(filename)
        distance = activity[0]
        seconds = activity[1].total_seconds()
        start_time = activity[2]

        if distance == 0:
            session_data.warning('Activity of zero distance ignored.')
        elif start_time is None:
            if a_type == ActivityType.Run:
                a_type = ActivityType.Walk
            start_time = datetime.datetime.now().replace(microsecond=0)
            full_time = datetime.time()
            avg_time = datetime.time()
            new_activity = Activity(datetime=start_time, distance=distance, duration=full_time,
                                    average_duration_per_km=avg_time, type=a_type)
            db_query.save_new_user_activities(current_user.id, new_activity)
            session_data.info(str(a_type) + ' activity of ' + str(distance) + ' km added.')
        else:
            avg_seconds = round(seconds / distance)
            full_time = (datetime.datetime(2000, 1, 1, 0) + datetime.timedelta(seconds=seconds)).time()
            avg_time = (datetime.datetime(2000, 1, 1, 0) + datetime.timedelta(seconds=avg_seconds)).time()
            new_activity = Activity(datetime=start_time, distance=distance, duration=full_time,
                                    average_duration_per_km=avg_time, type=a_type)
            db_query.save_new_user_activities(current_user.id, new_activity)
            session_data.info(str(a_type) + ' activity of ' + str(distance) + ' km added.')

        return redirect(url_for('home'))

    check_profile_verified(session_data)

    return render_template("personal_dashboard.html", title='Home', form=add_activity_form,
                           season=db_query.SEASON, session_data=session_data)


@app.route('/matfyz_challenges')
@login_required
def matfyz_challenges():
    session_data = mast.session.Session()
    check_profile_verified(session_data)
    db_query = mast.queries.Queries()
    checkpoints = db_query.get_challenge_parts_to_display()
    checkpoints_enriched = []
    order = 1
    for (dist, place) in checkpoints.items():
        checkpoints_enriched.append({'order': order, 'dist': dist, 'place': place})
        order = order + 1
    current_checkpoint = db_query.get_current_challenge_part()
    return render_template("matfyz_challenges.html", title='Matfyz Challenges',
                           checkpoints=checkpoints_enriched, current_checkpoint=current_checkpoint,
                           session_data=session_data)


@app.route('/running_5_km')
@login_required
def running_5_km():
    session_data = mast.session.Session()
    check_profile_verified(session_data)
    return render_template("running.html", title="Running-5", distance='5km',
                           session_data=session_data)


@app.route('/running_10_km')
@login_required
def running_10_km():
    session_data = mast.session.Session()
    check_profile_verified(session_data)
    return render_template("running.html", title="Running-10", distance='10km',
                           session_data=session_data)


@app.route('/running_walking')
@login_required
def running_walking():
    session_data = mast.session.Session()
    check_profile_verified(session_data)
    return render_template("running_walking.html", title="Jogging",
                           session_data=session_data)


@app.route('/user_settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    session_data = mast.session.Session()
    update_profile_form = UpdateProfileForm(name='up')
    display_update_profile_form = 'none'
    change_password_form = ChangePasswordForm(name='chp')
    display_change_password_form = 'none'
    if request.method == 'POST':
        if request.form['submit'] == 'Update profile':
            update_profile_form = UpdateProfileForm(request.form)
            if update_profile_form.validate():
                current_user.complete_profile(first_name=update_profile_form.first_name.data.strip(),
                                              last_name=update_profile_form.last_name.data.strip(),
                                              age=update_profile_form.age.data,
                                              sex=update_profile_form.sex.data,
                                              shirt_size=update_profile_form.shirt_size.data,
                                              user_type=update_profile_form.user_type.data,
                                              ukco=update_profile_form.ukco.data.strip(),
                                              display_name=update_profile_form.display_name.data.strip(),
                                              anonymous=update_profile_form.competing.data)

                if authenticate_via_sis(name=current_user.first_name, surname=current_user.last_name, login=None,
                                        ukco=current_user.uk_id, is_employee=current_user.type.value):
                    current_user.verify()
                    session_data.info('Your profile has been been verified.')
                    return redirect(url_for('user_settings'))
                else:
                    session_data.warning('Your profile has not been been verified.<br />' +
                                         'We will verify your profile in a few days if you are sure with your data.')

            else:
                # Keep the form visible if it contains errors
                display_update_profile_form = 'block'
        elif request.form['submit'] == 'Update password':
            change_password_form = ChangePasswordForm(request.form)
            if change_password_form.validate():
                hashed_password = bcr.generate_password_hash(
                    change_password_form.password.data).decode('UTF-8')
                current_user.change_password(hashed_password)
                session_data.info('Your password has been changed.')
                return redirect(url_for('user_settings'))
            else:
                # Keep the form visible if it contains errors
                display_change_password_form = 'block'

    # For GET and after POST method
    check_profile_verified(session_data)

    update_profile_form.first_name.data = current_user.first_name or ''
    update_profile_form.last_name.data = current_user.last_name or ''
    update_profile_form.display_name.data = current_user.display_name or ''
    update_profile_form.ukco.data = current_user.uk_id or ''
    update_profile_form.age.data = current_user.age.value if current_user.age else None
    update_profile_form.sex.data = current_user.sex.value if current_user.sex else None
    update_profile_form.shirt_size.data = current_user.shirt_size or None
    update_profile_form.user_type.data = current_user.type.value if current_user.type else None
    update_profile_form.competing.data = current_user.anonymous or None

    return render_template("user_settings.html", title='User Settings',
                           profile=current_user,
                           update_profile_form=update_profile_form,
                           display_update_profile_form=display_update_profile_form,
                           change_password_form=change_password_form,
                           display_change_password_form=display_change_password_form,
                           session_data=session_data)


@app.route('/cycling')
@login_required
def cycling():
    session_data = mast.session.Session()
    check_profile_verified(session_data)
    return render_template("cycling.html", title="Cycling",
                           session_data=session_data)


@app.route('/faq')
@login_required
def faq():
    session_data = mast.session.Session()
    check_profile_verified(session_data)
    return render_template("faq.html", title='Frequently Asked Questions', session_data=session_data)


@app.route('/about_competitions')
@login_required
def about_competitions():
    session_data = mast.session.Session()
    check_profile_verified(session_data)
    return render_template("about_competitions.html", title='About Competitions', session_data=session_data)


@app.route('/integrations')
@login_required
def integrations():
    session_data = mast.session.Session()
    check_profile_verified(session_data)
    return render_template("integrations.html", title='Integrations', session_data=session_data)


@app.route("/statistics")
def statistics():
    db_query = mast.queries.Queries()
    stats = db_query.get_stats()
    return render_template("statistics.html", stats=stats)
