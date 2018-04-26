from flask import Response, json, jsonify
from . import api

from ..models import Post, AdditionalFact, TagButton


# @api.route('/facts', methods=['GET'])
# def get_facts():

@api.route('/fact/<fact_id>', methods=['GET'])
def get_fact(fact_id):
    fact = Post.query.filter_by(id=fact_id).first()
    additional_facts_list = AdditionalFact.query.filter_by(post_id=fact.id).all()
    tag_buttons_list = TagButton.query.filter_by(post_id=fact.id).all()

    if fact is None:
        errorResponse = Response(
            response="Fact could not be found",
            status=404,
            mimetype='application/json'
        )
        return errorResponse

    fact_json = jsonify(
        id = fact.id,
        header = fact.header,
        title = fact.title,
        title_url = fact.title_url,
        image_url = fact.image_url,
        body = fact.body,
        additional_facts = [af.serialize() for af in additional_facts_list],
        tag_buttons = [tb.serialize() for tb in tag_buttons_list]
    )
    response = fact_json
    response.status_code = 200
    return response

@api.route('/fact/<fact_id>/slack', methods=['GET'])
def get_fact_slack(fact_id):
    fact = Post.query.filter_by(id=fact_id).first()
    additional_facts_list = AdditionalFact.query.filter_by(post_id=fact.id).all()
    tag_buttons_list = TagButton.query.filter_by(post_id=fact.id).all()

    if fact is None:
        errorResponse = Response(
            response="Fact could not be found",
            status=404,
            mimetype='application/json'
        )
        return errorResponse

    fact_slack_json = jsonify(
        text = ":rainbow:AQuA :heart: Aaptiv",
        attachments = fact.slack_serialize(additional_facts_list, tag_buttons_list)
    )
    response = fact_slack_json
    response.status_code = 200
    return response
