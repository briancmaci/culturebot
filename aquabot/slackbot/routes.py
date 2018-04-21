from . import slackbot
from slackclient import SlackClient
from flask import Response, jsonify
from ..models import Post, AdditionalFact, TagButton

import os


@slackbot.route('/sendfact/<fact_id>', methods=['GET'])
def send_fact(fact_id):
    fact = Post.query.filter_by(id=fact_id).first()

    if fact is None:
        errorResponse = Response(
            response="Fact could not be found",
            status=404,
            mimetype='application/json'
        )
        return errorResponse

    additional_facts_list = AdditionalFact.query.filter_by(post_id=fact.id).all()
    tag_buttons_list = TagButton.query.filter_by(post_id=fact.id).all()

    message_text = ":rainbow:AQuA :heart: Aaptiv"
    message_attachments = [fact.slack_serialize(additional_facts_list, tag_buttons_list)]
    # slack_token = os.environ["SLACK_API_TOKEN"]
    slack_bot_token = "xoxb-347026176099-eIL17IqSh79utThfAQJ4oIe0"
    slack_client = SlackClient(slack_bot_token)

    response = jsonify(message_attachments)
    response.status_code = 200

    slack_client.api_call("chat.postMessage", channel="#aaptiv-pride", text=message_text, attachments=message_attachments)

    return response

