from app import FlaskForm, StringField, HiddenField, SubmitField


class MainForm(FlaskForm):
    save_btn = SubmitField()
    del_btn = SubmitField()
    add_btn = SubmitField()
    add_root_btn = SubmitField()
    name_choice = StringField()
    element_id = HiddenField()

