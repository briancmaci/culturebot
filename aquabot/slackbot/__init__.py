from flask import Blueprint
from slackclient import SlackClient
import os


slackbot = Blueprint(
    'slackbot',
    __name__
)


def send_fact():
    #slack_token = os.environ["SLACK_API_TOKEN"]
    slack_bot_token = "xoxb-347026176099-eIL17IqSh79utThfAQJ4oIe0"
    slack_verification_token = "Qhw48BMuKNF7P96r6a0WA4ES"
    slack_client = SlackClient(slack_bot_token)

    slack_client.api_call("auth.test")

    message = "Haaaayyy aaptiv! I am aquabot :tada: You can see me!"
    slack_client.api_call("chat.postMessage", channel="#aaptiv-pride", text=message)


from . import routes