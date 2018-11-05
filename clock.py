import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

import sendgrid_helper
import stack_exchange_api
import stack_overflow_page

schedule = BlockingScheduler()


@schedule.scheduled_job('interval', hours=3)
def access_stack_overflow_page():
    stack_overflow_page.login()

@schedule.scheduled_job('interval', minutes=30)
def heartbeat():
    print("HB {}".format(datetime.datetime.now()))


@schedule.scheduled_job('interval', hours=3)
def access_stack_overflow_api():
    delta_hours = 12
    if stack_exchange_api.have_logged_in(12) is False:
        message = "You haven't logged in for at least " + str(delta_hours) + " hours! \n " + \
                  "Access stackoverflow.com to save your login streak"
        print("ERROR!\n" + message)
        sendgrid_helper.send_mail("Login overdue alert!", message)


@schedule.scheduled_job('interval', days=7)
def email_heartbeat():
    sendgrid_helper.send_mail("All good", "All systems operational")


print("Testing all systems")
try:
    access_stack_overflow_page()
    heartbeat()
    access_stack_overflow_api()
    email_heartbeat()
except Exception as e:
    sendgrid_helper.send_mail("Got an error when starting", "Please check")
    print("Actually got an error, but ignoring...\n", e)
except:
    print("Actually got an error. Ignoring...")


print("Process Started {}".format(datetime.datetime.now()))
schedule.start()

