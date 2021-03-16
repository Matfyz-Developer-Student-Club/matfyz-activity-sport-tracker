from flask import render_template, Blueprint
from flask_login import current_user, login_required
from mast.queries import Queries
from mast.session import Session
from mast.activities.utils import ordinal
from mast.tools.utils import check_profile_verified

activities = Blueprint('activities', __name__)


@activities.route('/matfyz_challenges')
def matfyz_challenges():
    db_query = Queries()
    checkpoints = db_query.get_challenge_parts_to_display()
    checkpoints_enriched = []
    order = 1
    for (dist, place) in checkpoints.items():
        checkpoints_enriched.append({'order': order, 'dist': dist, 'place': place})
        order = order + 1
    current_checkpoint = db_query.get_current_challenge_part()

    if current_user.is_authenticated:
        session_data = Session()
        check_profile_verified(session_data)
        return render_template("matfyz_challenges.html", title='Matfyz Challenges',
                               checkpoints=checkpoints_enriched, current_checkpoint=current_checkpoint,
                               session_data=session_data)
    else:
        return render_template("matfyz_challenges_public.html", title='Matfyz Challenges',
                               checkpoints=checkpoints_enriched, current_checkpoint=current_checkpoint)


@activities.route('/competitions')
def competitions():
    return render_template("competitions_public.html", title="Competitions")


@activities.route('/running')
@login_required
def running():
    session_data = Session()
    check_profile_verified(session_data)
    db_query = Queries()
    position = db_query.get_position_best_run(current_user.id)
    return render_template("running.html", title="Running",
                           position=ordinal(position), session_data=session_data)


@activities.route('/walking')
@login_required
def walking():
    session_data = Session()
    check_profile_verified(session_data)
    db_query = Queries()
    total_distance = db_query.get_total_distance_by_user_on_foot(current_user.id)
    position = db_query.get_position_total_distance_on_foot(current_user.id)
    return render_template("walking.html", title="Walking",
                           total_distance=total_distance, position=ordinal(position),
                           session_data=session_data)


@activities.route('/inline')
@login_required
def inline():
    session_data = Session()
    check_profile_verified(session_data)
    db_query = Queries()
    position = db_query.get_position_total_distance_on_foot(current_user.id)
    return render_template("inline.html", title="Inline", position=ordinal(position),
                           session_data=session_data)


@activities.route('/cycling')
@login_required
def cycling():
    session_data = Session()
    check_profile_verified(session_data)
    db_query = Queries()
    total_distance = db_query.get_total_distance_by_user_on_bike(current_user.id)
    position = db_query.get_position_total_distance_on_bike(current_user.id)
    return render_template("cycling.html", title="Cycling",
                           total_distance=total_distance, position=ordinal(position),
                           session_data=session_data)
