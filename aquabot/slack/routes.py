from . import slack
from slackclient import SlackClient


@slack.route('/postfact', methods=['GET'])
def get_fact(fact_id):
    slack_token = os.environ["SLACK_API_TOKEN"]
    sc = SlackClient(slack_token)

    sc.api_call(
      "chat.postMessage",
      channel="C0XXXXXX",
      text="Hello from Python! :tada:"
    )