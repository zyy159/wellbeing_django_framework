import json
import threading
from email.mime.base import MIMEBase
import datetime as dt
import icalendar
import pytz
import uuid
from django.core.mail import EmailMultiAlternatives
from wellbeing_django_framework.settings import EMAIL_HOST_USER


def send_appointment(attendee_email, organiser_email, subj, body, location, start_time, end_time):
    # Timezone to use for our dates - change as needed
    tz = pytz.timezone("Asia/Shanghai")
    start = start_time
    # Build the event itself
    cal = icalendar.Calendar()
    cal.add('prodid', '-//My calendar application//example.com//')
    cal.add('version', '2.0')
    cal.add('method', "REQUEST")
    event = icalendar.Event()
    event.add('attendee', attendee_email)
    event.add('organizer', organiser_email)
    event.add('status', "confirmed")
    event.add('category', "Event")
    event.add('summary', subj)
    event.add('description', body)
    event.add('location', location)
    event.add('dtstart', start)
    event.add('dtend', end_time)
    event.add('dtstamp', tz.localize(dt.datetime.combine(dt.datetime.now(tz), dt.time(6, 0, 0))))
    event['uid'] = str(uuid.uuid4())  # Generate some unique ID
    event.add('priority', 5)
    event.add('sequence', 1)
    event.add('created', tz.localize(dt.datetime.now()))

    # Add a reminder
    alarm = icalendar.Alarm()
    alarm.add("action", "DISPLAY")
    alarm.add('description', "Reminder")
    # The only way to convince Outlook to do it correctly
    alarm.add("TRIGGER;RELATED=START", "-PT{0}H".format(0.25))
    event.add_component(alarm)
    cal.add_component(event)

    # Build the email message and attach the event to it
    msg = EmailMultiAlternatives(subj, body, organiser_email, [attendee_email])

    filename = "invite.ics"
    part = MIMEBase('text', "calendar", method="REQUEST", name=filename)
    part.set_payload(cal.to_ical())
    part.add_header('Content-Description', filename)
    part.add_header("Content-class", "urn:content-classes:calendarmessage")
    part.add_header("Filename", filename)
    part.add_header("Path", filename)
    msg.attach(part)

    # Send the email out
    msg.send()


class SendAppointmentsThread(threading.Thread):
    def __init__(self, schedule, attendee_email, location):
        threading.Thread.__init__(self)
        self.threadID = "Thread-Send-Appointments"
        self.schedule = schedule
        self.attendee_email = attendee_email
        self.location = location
        self.organiser_email = EMAIL_HOST_USER
        self.subj = 'Relex time'
        self.body = """It is time to relex yourself!

Click {} to start exercise!
                        """.format(self.location)

    def run(self):
        tz = pytz.timezone("Asia/Shanghai")
        schedules = json.loads(json.dumps(self.schedule))
        i = 1
        for s in schedules:
            print(f'start to send {i} message')
            start_time = s["start_time"]
            end_time = s["end_time"]
            start_time = dt.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
            end_time = dt.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ')
            start_time = tz.localize(start_time)
            end_time = tz.localize(end_time)
            # start_time = tz.localize(dt.datetime.now())
            # end_time = tz.localize(dt.datetime.combine(dt.datetime.now(tz), dt.time(start_time.hour + int((start_time.minute + 30)/60), (start_time.minute + 30) % 60, 0)))
            send_appointment(self.attendee_email, self.organiser_email, self.subj, self.body, self.location, start_time,
                             end_time)
            print(f'finish sending {i} message')
            i = i + 1
