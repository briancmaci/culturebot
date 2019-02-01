from flask import Blueprint
from slackclient import SlackClient
import os


slackbot = Blueprint(
    'slackbot',
    __name__
)


from . import routes
