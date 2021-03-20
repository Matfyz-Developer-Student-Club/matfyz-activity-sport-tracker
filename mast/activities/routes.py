from flask import render_template, Blueprint
from flask_login import current_user, login_required
from mast.queries import Queries
from mast.session import Session
from mast.activities.utils import ordinal
from mast.tools.utils import check_profile_verified

activities = Blueprint('activities', __name__)


@activities.route('/matfyz_challenges_combined')
def matfyz_challenges_combined():
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
        return render_template("matfyz_challenges_combined.html", title='Matfyz Challenges - Combined',
                               checkpoints=checkpoints_enriched, current_checkpoint=current_checkpoint,
                               session_data=session_data)
    else:
        return render_template("matfyz_challenges_combined_public.html", title='Matfyz Challenges - Combined',
                               checkpoints=checkpoints_enriched, current_checkpoint=current_checkpoint,
                               route='activities.matfyz_challenges_cyclist', default=True)


@activities.route('/matfyz_challenges_cyclist')
def matfyz_challenges_cyclist():
    db_query = Queries()
    checkpoints, current_dist = db_query.get_cyclists_challenge_parts_to_display()
    checkpoints_enriched = []
    order = 1
    for (dist, place) in checkpoints.items():
        checkpoints_enriched.append({'order': order, 'dist': dist, 'place': place['target'], 'altitude': place['alt']})
        order = order + 1
    current_checkpoint = db_query.get_current_challenge_part()

    if current_user.is_authenticated:
        session_data = Session()
        check_profile_verified(session_data)
        # TODO: Rename template
        return render_template("matfyz_challenges_cyclist.html", title='Matfyz Challenges - Cyclists',
                               checkpoints=checkpoints_enriched, current_checkpoint=current_checkpoint,
                               session_data=session_data, current_dist=current_dist)
    else:
        return render_template("matfyz_challenges_combined_public.html", title='Matfyz Challenges - Cyclists',
                               checkpoints=checkpoints_enriched, current_checkpoint=current_checkpoint,
                               current_dist=current_dist, route='activities.matfyz_challenges_combined', default=False)


@activities.route('/competitions')
def competitions():
    return render_template("competitions_public.html", title="Competitions")


@activities.route('/running')
@login_required
def running():
    session_data = Session()
    check_profile_verified(session_data)
    db_query = Queries()
<<<<<<< HEAD
<<<<<<< HEAD
    position = db_query.get_score_position_for_run(current_user.id)
    total_score = db_query.get_total_score_by_user_for_run(current_user.id)
    return render_template("running.html", title="Running",
                           position=ordinal(position), session_data=session_data, total_score=total_score)
=======
    position = db_query.get_position_best_run(current_user.id)
    return render_template("running.html", title="Running",
                           position=ordinal(position), session_data=session_data)
>>>>>>> Adding inline view and route. Adjustment of data model.
=======
    position = db_query.get_score_position_for_run(current_user.id)
    total_score = db_query.get_total_score_by_user_for_run(current_user.id)
    return render_template("running.html", title="Running",
                           position=ordinal(position), session_data=session_data, total_score=total_score)
>>>>>>> Finalizing views and contest logic for the Release.


@activities.route('/walking')
@login_required
def walking():
    session_data = Session()
    check_profile_verified(session_data)
    db_query = Queries()
<<<<<<< HEAD
<<<<<<< HEAD
    total_score = db_query.get_total_score_by_user_for_walk(current_user.id)
    position = db_query.get_score_position_for_walk(current_user.id)
    return render_template("walking.html", title="Walking",
                           total_score=total_score, position=ordinal(position),
=======
    total_distance = db_query.get_total_distance_by_user_on_foot(current_user.id)
    position = db_query.get_position_total_distance_on_foot(current_user.id)
    return render_template("walking.html", title="Walking",
                           total_distance=total_distance, position=ordinal(position),
>>>>>>> Adding inline view and route. Adjustment of data model.
=======
    total_score = db_query.get_total_score_by_user_for_walk(current_user.id)
    position = db_query.get_score_position_for_walk(current_user.id)
    return render_template("walking.html", title="Walking",
                           total_score=total_score, position=ordinal(position),
>>>>>>> Finalizing views and contest logic for the Release.
                           session_data=session_data)


@activities.route('/inline')
@login_required
def inline():
    session_data = Session()
    check_profile_verified(session_data)
    db_query = Queries()
<<<<<<< HEAD
<<<<<<< HEAD
    position = db_query.get_score_position_for_inline(current_user.id)
    total_score = db_query.get_total_score_by_user_for_inline(current_user.id)
    return render_template("inline.html", title="Inline", position=ordinal(position),
                           session_data=session_data, total_score=total_score)
=======
    position = db_query.get_position_total_distance_on_foot(current_user.id)
    return render_template("inline.html", title="Inline", position=ordinal(position),
                           session_data=session_data)
>>>>>>> Adding inline view and route. Adjustment of data model.
=======
    position = db_query.get_score_position_for_inline(current_user.id)
    total_score = db_query.get_total_score_by_user_for_inline(current_user.id)
    return render_template("inline.html", title="Inline", position=ordinal(position),
                           session_data=session_data, total_score=total_score)
>>>>>>> Finalizing views and contest logic for the Release.


@activities.route('/cycling')
@login_required
def cycling():
    session_data = Session()
    check_profile_verified(session_data)
    db_query = Queries()
    total_score = db_query.get_total_score_by_user_for_ride(current_user.id)
    position = db_query.get_score_position_for_ride(current_user.id)
    return render_template("cycling.html", title="Cycling",
                           total_score=total_score, position=ordinal(position),
                           session_data=session_data)
