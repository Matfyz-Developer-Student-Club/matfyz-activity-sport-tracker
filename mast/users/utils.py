from flask import url_for, current_app
from mast import mail
from flask_mail import Message
from mast.queries import Queries


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])

    msg.body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email. No changes required here.
    '''
    mail.send(msg)


def send_registration_email(user):
    msg = Message('Welcome to Mathletics',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email])

    msg.body = f'''Hi, 
        welcome to Mathletics.
      
        You can now participate in our current competitions. 

        Good luck,
        Matfyz Developer Student Club



        If you did not register, please contact us at matfyz.dsc@gmail.com.

        '''
    mail.send(msg)


def send_mass_email():
    emails = Queries().get_all_users_emails()
    msg = Message('NoReply - Mathletics',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=emails)

    msg.body = f'''Dear users, 
        due to the technical problem several of you cannot see your activities from STRAVA.
        The problem was partially solved, and if you want to see your data, please visit 
        your STRAVA https://www.strava.com/athlete/training and re-upload your activities.
        
        If the activity cannot be re-uploaded (Delete + Upload) then please stay tuned. 
        We are currently working on the solution and we will provide update when resolved. 

        We are sorry for an inconvenience,
        yours Matfyz Developer Student Club

        '''
    mail.send(msg)
