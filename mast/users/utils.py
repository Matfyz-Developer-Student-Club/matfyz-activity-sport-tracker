from flask import url_for, current_app
from mast import mail
from flask_mail import Message


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
                  sender='noreply@mathletics.mff.cuni.cz',
                  recipients=[user.email])

    msg.body = f'''Hi, 
        welcome to Mathletics.
      
        You can now participate in our current competitions. 

        Good luck,
        Matfyz Developer Student Club



        If you did not register, please contact us at matfyz.sdc@gmail.com.

        '''
    mail.send(msg)
