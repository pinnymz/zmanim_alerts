import json
import os
from datetime import datetime

from dateutil import tz
from slackclient import SlackClient
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar


def mishmar(event, context):
    zone = tz.gettz('America/New_York')
    time = datetime.now().astimezone(zone)

    cal = JewishCalendar(time.date())
    tomorrow = cal + 1
    sd = tomorrow.significant_day()

    slack_key = os.environ["SLACK_API_TOKEN"]
    sc = SlackClient(slack_key)

    if (time.hour == 21) and \
            (not tomorrow.is_assur_bemelacha()) and \
            (tomorrow.day_of_week == 6 or
             sd == 'erev_yom_kippur' or
             sd == 'erev_succos' or
             sd == 'purim_katan' or
             sd == 'pesach_sheni' or
             sd == 'tzom_gedalyah' or
             sd == 'tenth_of_teves' or
             sd == 'taanis_esther' or
             sd == 'seventeen_of_tammuz' or
             (tomorrow.jewish_month == 5 and tomorrow.jewish_day == 8) or
             sd == 'tu_beshvat' or
             (tomorrow.jewish_month == 9 and tomorrow.jewish_day == 25) or
             tomorrow.day_of_omer() == 33 or
             (tomorrow.jewish_month == 5 and tomorrow.jewish_day == 30)):

        modifier = None

        if tomorrow.jewish_month == 6 and tomorrow.jewish_day in range(22,29):
            modifier = 'Rosh Hashana is next week'
        elif sd == 'tzom_gedalyah':
            modifier = 'Tzom Gedalyah is tonight'
        elif sd == 'erev_yom_kippur':
            modifier = 'Yom Kippur is tomorrow'
        elif sd == 'erev_succos':
            modifier = 'Succos begins tomorrow'
        elif tomorrow.jewish_month == 9 and tomorrow.jewish_day == 25:
            modifier = "Chanukah began tonight"
        elif tomorrow.jewish_month == 9 and tomorrow.jewish_day == 24:
            modifier = 'Chanukah begins tomorrow'
        elif sd == 'tenth_of_teves':
            modifier = "Asara B'Teves is tonight"
        elif sd == 'tu_beshvat':
            modifier = "Tu B'Shvat is tonight"
        elif tomorrow.jewish_month == 11 and tomorrow.jewish_day == 14:
            modifier = "Tu B'Shvat is approaching"
        elif sd == 'purim_katan':
            modifier = "Purim Katan is tonight"
        elif sd == 'taanis_esther':
            modifier = 'Purim is approaching'
        elif tomorrow.jewish_month == 1 and tomorrow.jewish_day in range(7,14):
            modifier = 'Pesach begins next week'
        elif sd == 'pesach_sheni':
            modifier = 'Pesach Sheni is tonight'
        elif tomorrow.day_of_omer() == 33:
            modifier = "Lag B'Omer is tonight"
        elif tomorrow.day_of_omer() == 32:
            modifier = "Lag B'Omer is tomorrow"
        elif tomorrow.day_of_omer() in range(42,49):
            modifier = 'Shavuos begins next week'
        elif sd == 'seventeen_of_tammuz':
            modifier = 'Three weeks have begun'
        elif tomorrow.jewish_month == 5 and tomorrow.jewish_day == 8 and not tomorrow.day_of_week == 6:
             modifier = "Tisha B'Av is tomorrow"
        elif tomorrow.jewish_month == 5 and tomorrow.jewish_day in [7,8] and tomorrow.day_of_week == 6:
             modifier = "Tisha B'Av is approaching"
        elif tomorrow.jewish_month == 5 and tomorrow.jewish_day == 30:
            modifier = "Rosh Chodesh Elul is tonight"
        elif tomorrow.jewish_month == 5 and tomorrow.jewish_day == 29:
            modifier = "Rosh Chodesh Elul is approaching"

        result1 = sc.api_call('chat.postMessage',
                              channel='#general',
                              text=mishmarMessage('check out Mishmar in <#C3EP4TREX|torah>', modifier),
                              as_user=False,
                              username='slackbot',
                              icon_url='https://ca.slack-edge.com/T03DNU155-USLACKBOT-sv1444671949-72')

        result2 = sc.api_call('chat.postMessage',
                              channel='#torah',
                              text=mishmarMessage("it's Mishmar time!", modifier),
                              as_user=False,
                              username='slackbot',
                              icon_url='https://ca.slack-edge.com/T03DNU155-USLACKBOT-sv1444671949-72')

        body = {
            "message": "triggered",
            "input": event,
            "result": [result1, result2]
        }

    else:

        body = {
            "message": "not triggered",
            "input": event
        }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def mishmarMessage(text, modifier):
    if modifier is not None:
        text = modifier + ', ' + text
    return 'Reminder: ' + text
