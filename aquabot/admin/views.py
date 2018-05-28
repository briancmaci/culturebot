from flask import render_template, request, flash, redirect, url_for
from . import admin
from .forms import LoginForm, RegistrationForm, PostFactForm, ImportCSVFileForm
from ..models import db, User, Post, AdditionalFact, TagButton
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
import csv
import io
import giphy_client
from giphy_client.rest import ApiException
import requests


def find_additional_fact_index(original_fact=AdditionalFact, updated_facts=[AdditionalFact]):
    found_fact_index = -1
    for i, uf in enumerate(updated_facts):
        if uf["id"] == original_fact.id:
            found_fact_index = i
    return found_fact_index

def find_tag_button_index(original_button=TagButton, updated_buttons=[TagButton]):
    found_button_index = -1
    for i, ub in enumerate(updated_buttons):
        if ub["id"] == original_button.id:
            found_button_index = i
    return found_button_index


@admin.route('/')
@admin.route('/index')
@login_required
def index():
    default_image_url = "https://vignette.wikia.nocookie.net/justdance/images/8/8b/Alyssa_edwards_BYF_judging.gif"
    image_url = default_image_url

    api_instance = giphy_client.DefaultApi()
    api_key = 'dc6zaTOxFJmzC'
    tag = 'lgbtq'

    try:
        api_response = api_instance.gifs_random_get(api_key, tag=tag)
        image_url = api_response.data.image_url
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_random_get: %s\n" % e)

    return render_template('index.html', image_url=image_url)


@admin.route('/fact/<fact_id>')
@login_required
def preview_fact(fact_id):
    fact = Post.query.filter_by(id=fact_id).first()
    if fact is None:
        flash('Fact not found')
    return render_template('fact.html', fact=fact)


@admin.route('/fact/delete/<fact_id>')
@login_required
def delete_fact(fact_id):
    fact = Post.query.filter_by(id=fact_id).first()
    if fact is None:
        flash('Fact not found')
    db.session.delete(fact)
    db.session.commit()
    return redirect(url_for('.facts'))


@admin.route('/fact/edit/<fact_id>', methods=['GET', 'POST'])
@login_required
def edit_fact(fact_id):
    fact = Post.query.filter_by(id=fact_id).first()
    if fact is None:
        flash('Fact not found')

    form = PostFactForm(obj=fact)
    form.submit.label.text = "Save changes"

    if form.validate_on_submit():
        fact.header = form.header.data
        fact.title = form.title.data
        fact.title_url = form.title_url.data
        fact.image_url = form.image_url.data
        fact.body = form.body.data

        original_additional_facts = AdditionalFact.query.filter_by(post_id=fact.id).all()
        updated_additional_facts = form.additional_facts.data

        # Remove/update old additional facts
        for of in original_additional_facts:
            db.session.delete(of)

        # Add new additional facts
        for af in updated_additional_facts:
            additionalFact = AdditionalFact(post_id=fact.id, title=af['title'], text=af['text'], is_long=af['is_long'])
            db.session.add(additionalFact)

        original_tag_buttons = TagButton.query.filter_by(post_id=fact.id).all()
        updated_tag_buttons = form.tag_buttons.data

        # Remove/update old tag buttons
        for ob in original_tag_buttons:
            db.session.delete(ob)

        # Add new tag buttons
        for tag in updated_tag_buttons:
            tagButton = TagButton(post_id=fact.id, title=tag['title'], url=tag['url'])
            db.session.add(tagButton)

        db.session.commit()
        return redirect(url_for('.preview_fact', fact_id=fact.id))

    else:
        flash(form.errors)

    return render_template('post_fact.html', title='Post an LGBTQ Fact', form=form)


@admin.route('/fact/reset/<fact_id>')
@login_required
def reset_fact(fact_id):
    fact = Post.query.filter_by(id=fact_id).first()
    if fact is None:
        flash('Fact not found')

    fact.shown = False
    db.session.commit()
    return redirect(url_for('.facts'))


@admin.route('/facts')
@login_required
def facts():
    facts = Post.query.all()
    return render_template('facts.html', title="🌈 aquabot | LGBTQ Pride Facts", facts=facts)


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@admin.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('.login'))
    return render_template('register.html', title='Register', form=form)


@admin.route('/post_fact', methods=['GET', 'POST'])
@login_required
def post_fact():
    form = PostFactForm()

    if form.validate_on_submit():
        post = Post(user_id=current_user.id,
                    header=form.header.data,
                    title=form.title.data,
                    title_url=form.title_url.data,
                    image_url=form.image_url.data,
                    body=form.body.data)
        db.session.add(post)
        db.session.flush()

        for fact in form.additional_facts.data:
            additionalFact = AdditionalFact(post_id=post.id,
                                            title=fact['title'],
                                            text=fact['text'],
                                            is_long=fact['is_long'])
            db.session.add(additionalFact)

        for tag in form.tag_buttons.data:
            tagButton = TagButton(post_id=post.id, title=tag['title'], url=tag['url'])
            db.session.add(tagButton)


        db.session.commit()
        return redirect(url_for('.facts'))

    else:
        flash(form.errors)

    return render_template('post_fact.html', title='Post an LGBTQ Fact', form=form)


@admin.route('/import_csv', methods=['GET', 'POST'])
@login_required
def import_csv():
    form = ImportCSVFileForm()

    if form.validate_on_submit():
        additional_fact_count = 3
        tag_button_count = 3

        file = request.files[form.csv_file.name]
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)

        for row in csv_input:
            if row['completed'] == 'TRUE':
                post = Post(user_id=current_user.id,
                            header=row['header'],
                            title=row['title'],
                            title_url=row['title_url'],
                            image_url=row['image_url'],
                            body=row['body'])
                db.session.add(post)
                db.session.flush()

                for index in range(1, additional_fact_count + 1):
                    if row['fact_title_' + str(index)] != None:
                        additionalFact = AdditionalFact(post_id=post.id,
                                                        title=row['fact_title_' + str(index)],
                                                        text=row['fact_text_' + str(index)])
                        db.session.add(additionalFact)

                for index in range(1, tag_button_count + 1):
                    if row['button_title_' + str(index)] != None:
                        tagButton = TagButton(post_id=post.id,
                                              title=row['button_title_' + str(index)],
                                              url=row['button_url_' + str(index)])
                        db.session.add(tagButton)

                db.session.commit()

        return redirect(url_for('.facts'))

    else:
        flash(form.errors)

    return render_template('import_csv.html', title='aquabot | CSV Import', form=form)

@admin.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.index'))
