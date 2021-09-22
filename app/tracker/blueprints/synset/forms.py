from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, TextField


class SynsetHistoryForm(FlaskForm):
    date_from = DateField("date from", format="%d-%m-%Y")
    date_to = DateField("date to", format="%d-%m-%Y")
    synset_id = TextField()
    user = TextField("user")


class SynsetAttributesHistoryForm(FlaskForm):
    date_from = DateField("date from", format="%d-%m-%Y")
    date_to = DateField("date to", format="%d-%m-%Y")
    synset_id = TextField()
    user = TextField("user")


class SynsetRelationsHistoryForm(FlaskForm):
    date_from = DateField("date from", format="%d-%m-%Y")
    date_to = DateField("date to", format="%d-%m-%Y")
    synset_id = TextField()
    user = TextField("user")
    relation_type = TextField("relation_type")
