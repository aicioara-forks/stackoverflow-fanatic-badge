import sendgrid
import os

def send_mail(subject, content):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

    data = {
        "personalizations": [{
            "to": [{
                "email": os.environ.get('NOTIFICATION_EMAIL'),
            }],
            "subject": subject,
        }],
        "from": {
            "email": "noreply@heroku.com",
            "name": "Stackoverflow",
        },
    }

    data['content'] = [{
        'type': 'text/plain',
        'value': content
    }]


    try:
        response = sg.client.mail.send.post(request_body=data)
        print(response.status_code)
        print(response.body)
    except Exception as e:
        print("ERROR sending emaik")
        print(e.body)


if __name__ == "__main__":
    send_mail("URGENT: StackOverflow login", "You did not login in a while")