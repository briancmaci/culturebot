from typing import List

from . import slackbot
from slackclient import SlackClient
from flask import Response, jsonify, render_template, flash
from ..models import db, Post, AdditionalFact, TagButton

import os

slack_message_text = "*BLAF* :blue_heart: Aaptiv"

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

    message_text = slack_message_text
    message_attachments = [fact.slack_serialize(get_color(fact_id), additional_facts_list, tag_buttons_list)]
    slack_bot_token = os.environ["SLACK_API_TOKEN"]
    slack_channel = "#culturebot-test"
    slack_client = SlackClient(slack_bot_token)

    response = jsonify(message_attachments)
    response.status_code = 200

    slack_client.api_call("chat.postMessage", channel=slack_channel, text=message_text, attachments=message_attachments)
    return 'OK'


@slackbot.route('/send-next-fact', methods=['GET'])
def send_next_fact():
    fact = Post.query.filter_by(shown=False).first()

    if fact is None:
        errorResponse = Response(
            response="All facts have been sent! :(",
            status=404,
            mimetype='application/json'
        )
        return errorResponse

    shown_index = len(Post.query.filter_by(shown=False).all())
    additional_facts_list = AdditionalFact.query.filter_by(post_id=fact.id).all()
    tag_buttons_list = TagButton.query.filter_by(post_id=fact.id).all()

    message_text = slack_message_text
    message_attachments = [fact.slack_serialize(get_color(shown_index), additional_facts_list, tag_buttons_list)]
    slack_bot_token = os.environ["SLACK_API_TOKEN"]
    slack_channel = os.environ["SLACK_CHANNEL"]
    slack_client = SlackClient(slack_bot_token)

    response = jsonify(message_attachments)
    response.status_code = 200

    slack_client.api_call("chat.postMessage", channel=slack_channel, text=message_text, attachments=message_attachments)

    fact.shown = True
    db.session.commit()
    return 'OK'


def get_color(offset):
    return '#72a633'
    # colors: List[str] = ['#72a633']
    # color_index = int(offset) % len(colors) - 1
    # return colors[color_index]


