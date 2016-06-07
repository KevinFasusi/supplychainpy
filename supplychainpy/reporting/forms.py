import os

from flask.ext.uploads import UploadSet, DATA
from wtforms import Form, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired

data = UploadSet('data', DATA)

app_dir = os.path.dirname(__file__, )
rel_path = '../uploads'
abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
UPLOAD_FOLDER = abs_file_path


class DataForm(Form):
    orders = FileField('You data:',
                       validators=[FileRequired(),
                                   FileAllowed(data, 'data only!')])
    submit = SubmitField("Send")


def upload(request):
    form = DataForm(request.POST)
    if form.orders.data:
        orders_data = request.FILES[form.orders.name].read()
        open(os.path.join(UPLOAD_FOLDER, form.data.data), 'w').write(orders_data)
