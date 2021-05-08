from django.utils.translation import ugettext as _
from django import forms
from jarrbo_theme.forms import JarrboFormHelper
from crispy_forms.layout import Submit

class ImportLedenForm(forms.Form):
    file = forms.FileField()
    def __init__(self, *args, **kwargs):
        super(ImportLedenForm, self).__init__(*args, **kwargs)
        self.helper = JarrboFormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('import', _('Import')))
