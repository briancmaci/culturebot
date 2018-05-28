from typing import List

from . import slackbot
from slackclient import SlackClient
from flask import Response, jsonify, render_template, flash
from ..models import Post, AdditionalFact, TagButton

import os


colors: List[str] = ['#e70000', '#ff8c00', '#ffef00', '#00811f', '#0044ff', '#760089']

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

    message_text = "Aqua :trans_heart: Aaptiv"
    message_attachments = [fact.slack_serialize(get_color(fact_id), additional_facts_list, tag_buttons_list)]
    slack_bot_token = os.environ["SLACK_API_TOKEN"]
    slack_channel = os.environ["SLACK_CHANNEL"]
    slack_client = SlackClient(slack_bot_token)

    response = jsonify(message_attachments)
    response.status_code = 200

    slack_client.api_call("chat.postMessage", channel=slack_channel, text=message_text, attachments=message_attachments)
    return 'OK'

def get_color(offset):
    return colors[offset % len(colors)]


