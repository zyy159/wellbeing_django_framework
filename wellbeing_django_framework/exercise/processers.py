from email.mime.base import MIMEBase
import datetime as dt
import icalendar
import pytz
import email
import uuid

from django.core.mail import EmailMultiAlternatives


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
  event['uid'] = str(uuid.uuid4()) # Generate some unique ID
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
  part.set_payload( cal.to_ical() )
  part.add_header('Content-Description', filename)
  part.add_header("Content-class", "urn:content-classes:calendarmessage")
  part.add_header("Filename", filename)
  part.add_header("Path", filename)
  msg.attach(part)

  # Send the email out
  msg.send()

