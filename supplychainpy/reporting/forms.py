# Copyright (c) 2015-2016, The Authors and Contributors
# <see AUTHORS file>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#import os
#
#from flask_uploads import UploadSet, DATA
#from wtforms import Form, SubmitField, StringField
#from flask_wtf.file import FileField, FileAllowed, FileRequired
#from wtforms import validators
#
#data = UploadSet('data', DATA)
#
#app_dir = os.path.dirname(__file__, )
#rel_path = '../uploads'
#abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))
#UPLOAD_FOLDER = abs_file_path
#
#
#class DataForm(Form):
#    orders = FileField('You data:',
#                       validators=[FileRequired(),
#                                   FileAllowed(data, 'data only!')])
#    submit = SubmitField("Send")
#
#
#def upload(request):
#    form = DataForm(request.POST)
#    if form.orders.data:
#        orders_data = request.FILES[form.orders.name].read()
#        open(os.path.join(UPLOAD_FOLDER, form.data.data), 'w').write(orders_data)
#
#
#class SettingsForm(Form):
#    first_name = StringField(u'First Name', validators=[validators.input_required()])
#    database_location = StringField(u'database location', validators=[validators.input_required()])
