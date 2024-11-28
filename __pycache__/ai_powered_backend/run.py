from flasgger import Swagger
from flask_mail import Mail, Message

from app import create_app, db

app = create_app()
swagger = Swagger(app)


@app.route('/swagger.yaml')
def get_yaml():
    from flasgger.utils import swag_from
    swag_from("swagger.yaml")
    return app.send_static_file('swagger.yaml')
# app.config.from_object('config.Config')
# mail = Mail(app)
#
# @app.route('/send_test_email')
# def send_test_email():
#     msg = Message(subject='Test Email',
#                   sender=app.config['MAIL_DEFAULT_SENDER'],
#                   recipients=['animaytiwari@outlook.com'],
#                   body='This is a test email')
#     mail.send(msg)
#     return 'Test email sent'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8080, debug=True)