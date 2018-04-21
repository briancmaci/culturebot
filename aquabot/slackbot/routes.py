from . import slackbot
from slackclient import SlackClient
import os


@slackbot.route('/sendfact', methods=['GET'])
def send_fact():
    # slack_token = os.environ["SLACK_API_TOKEN"]
    slack_token = "Qhw48BMuKNF7P96r6a0WA4ES"
    slack_client = SlackClient(slack_token)

    if slack_client.rtm_connect():
        message = "Haaaayyy aaptiv! I am aquabot :tada:"
        slack_client.api_call("chat.postMessage", channel="#aaptiv-pride", text=message)
        return 'OK'

    else:
        print("Connection Failed, invalid token?")
        return 'Error'