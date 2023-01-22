from django.utils.translation import ugettext as _
from django import forms
from .models import Member, Contribution, Payment, Paymentmethod, Paymentstatus, \
                    Paymentbatch, Note
from django.db.models import Sum
from .tools import valid_iban, clean_iban, valid_postcode, clean_postcode
from jarrbo_theme.forms import JarrboFormHelper
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Row, Column
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
import datetime

class ImportMemberForm(forms.Form):
    filedate = forms.DateField(initial=datetime.date.today,
                widget=forms.TextInput(attrs={'type': 'date'}))
    file = forms.FileField()
    def __init__(self, *args, **kwargs):
        super(ImportMemberForm, self).__init__(*args, **kwargs)
        self.helper = JarrboFormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('import', _('Import')))

class ImportRddataForm(forms.Form):
    file = forms.FileField()
    def __init__(self, *args, **kwargs):
        super(ImportRddataForm, self).__init__(*args, **kwargs)
        self.helper = JarrboFormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('import', _('Import')))

class ImportInschrijvingenForm(forms.Form):
    file = forms.FileField()
    def __init__(self, *args, **kwargs):
        super(ImportInschrijvingenForm, self).__init__(*args, **kwargs)
        self.helper = JarrboFormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('import', _('Import')))

class ImportMachtigingenForm(forms.Form):
    file = forms.FileField()
    def __init__(self, *args, **kwargs):
        super(ImportMachtigingenForm, self).__init__(*args, **kwargs)
        self.helper = JarrboFormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('import', _('Import')))

class UpdateMemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = [
                  'machtiging', 'huygenspas', 'iban', 'kortingpercentage', 
                  'machtiging_withdrawn', 'naam_machtiging', 'adres_machtiging', 
                  'postcode_machtiging', 'plaats_machtiging', 'email_machtiging',
                  'status', 'payment_method', 
                  'machtigingsdatum', 'aanmeldingsdatum', 'kenmerk_machtiging',
                  ]
        labels = {
                  'machtiging': _('Authority'),
                  'kortingpercentage': _('Discount'),
                  'naam_machtiging': _('Authority ascription'),
                  'adres_machtiging': _('Authority addresss'),
                  'postcode_machtiging': _('Postal code'),
                  'plaats_machtiging': _('Authority city'),
                  'email_machtiging': _('Authority e-mail'),
                  'machtiging_withdrawn': _('Withdrawn'),
                  'payment_method': _('Payment method'),
                  'status': _('state'),
                  'machtigingsdatum': _('Authority date'),
                  'aanmeldingsdatum': _('Sign up date'),
                  'kenmerk_machtiging': _('Authority feature'),
                 }

    def clean_iban(self):
        iban = self.cleaned_data['iban']
        if iban:
            iban = clean_iban(iban)
            if not valid_iban(iban):
                raise forms.ValidationError(_('Invalid IBAN number'))
        return iban

    def clean_postcode_machtiging(self):
        postcode_machtiging = self.cleaned_data['postcode_machtiging']
        if postcode_machtiging:
            postcode_machtiging = clean_postcode(postcode_machtiging)
            if not valid_postcode(postcode_machtiging):
                raise forms.ValidationError(_('Invalid postal code'))
        return postcode_machtiging

    def __init__(self, *args, **kwargs):
        super(UpdateMemberForm, self).__init__(*args, **kwargs)
        self.fields['machtigingsdatum'].widget = forms.TextInput(attrs={'type': 'date'})
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
                Row(
                    Column('payment_method', css_class='form-group col-lg-2 mb-0'),
                    Column('iban', css_class='form-group col-lg-3 mb-0'),
                    Column(AppendedText('kortingpercentage', '%'), css_class='form-group col-lg-2 mb-0'),
                    Column('status', css_class='form-group col-lg-2 mb-0'),
                    Column('huygenspas', css_class='form-group col-lg-2 pt-4'),
                    css_class='form-row'
                ),
                Row(
                    Column('naam_machtiging', css_class='form-group col-lg-4 mb-0'),
                    Column('email_machtiging', css_class='form-group col-lg-4 mb-0'),
                    Column('machtiging', css_class='form-group col-lg-2 pt-4'),
                    Column('machtiging_withdrawn', css_class='form-group col-lg-2 pt-4'),
                    css_class='form-row'
                ),
                Row(
                    Column('adres_machtiging', css_class='form-group col-lg-6 mb-0'),
                    Column('postcode_machtiging', css_class='form-group col-lg-2 mb-0'),
                    Column('plaats_machtiging', css_class='form-group col-lg-4 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('kenmerk_machtiging', css_class='form-group col-lg-4 mb-0'),
                    Column('machtigingsdatum', css_class='form-group col-lg-4 mb-0'),
                    Column('aanmeldingsdatum', css_class='form-group col-lg-4 mb-0'),
                    css_class='form-row'
                ),
                )
        self.helper.add_input(Submit('update', _('Update')))

class UpdateContributionForm(forms.ModelForm):

    class Meta:
        model = Contribution
        queryset = Contribution.seizoen_objects.all()
        fields = [
                  'kortingpercentage', 'kortingvast', 'termijnen', 'kortingopadres', 
                  'payment_method', 'iban', 'factuur_naam', 'factuur_adres', 
                  'factuur_postcode', 'factuur_plaats', 'factuur_email', 'sponsored', 
                  ]
        labels = {
                  'kortingpercentage': _('Discount percentage'),
                  'kortingvast': _('Fixed discount'),
                  'termijnen': _('Terms'),
                  'kortingopadres': _('Family discount'),
                  'payment_method': _('Payment method'),
                  'iban': _('IBAN number'),
                  'factuur_naam': _('Invoice name'),
                  'factuur_adres': _('Invoice address'),
                  'factuur_postcode': _('Invoice postal code'),
                  'factuur_plaats': _('Invoice city'),
                  'factuur_email': _('Invoice e-mail address'),
                  'sponsored': _('Sponsored'),
                 } 

    def clean_iban(self):
        iban = self.cleaned_data['iban']
        if iban:
            iban = clean_iban(iban)
            if not valid_iban(iban):
                raise forms.ValidationError(_('Invalid IBAN number'))
        return iban

    def clean_postcode(self):
        postcode = self.cleaned_data['postcode']
        if postcode:
            postcode = clean_postcode(postcode)
            if not valid_postcode(postcode):
                raise forms.ValidationError(_('Invalid postal code'))
        return postcode

    def __init__(self, *args, **kwargs):
        super(UpdateContributionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
                Row(
                    Column('kortingpercentage', css_class='form-group col-lg-3 mb-0'),
                    Column('kortingvast', css_class='form-group col-lg-3 mb-0'),
                    Column('kortingopadres', css_class='form-group col-lg-3 mb-0'),
                    Column('termijnen', css_class='form-group col-lg-3 mb-0'),
                ),
                Row(
                    Column('payment_method', css_class='form-group col-lg-4 mb-0'),
                    Column('iban', css_class='form-group col-lg-4 mb-0'),
                    Column('sponsored', css_class='form-group col-lg-4 mb-0'),
                ),
                Row(
                    Column('factuur_naam', css_class='form-group col-lg-6 mb-0'),
                    Column('factuur_email', css_class='form-group col-lg-6 mb-0'),
                ),
                Row(
                    Column('factuur_adres', css_class='form-group col-lg-6 mb-0'),
                    Column('factuur_postcode', css_class='form-group col-lg-2 mb-0'),
                    Column('factuur_plaats', css_class='form-group col-lg-4 mb-0'),
                ),
                )
        self.helper.add_input(Submit('update', _('Update')))

class UpdatePaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        queryset = Payment.seizoen_objects.all()
        fields = ['amount', 'paymentbatch', 'method',  'paymentdate',
                  'aanvraagnummer', 'status',
                 ]
        labels = {
                  'amount': _('Amount'),
                  'paymentbatch': _('Paymentbatch'),
                  'method': _('Payment method'),
                  'paymentdate': _('Payment date'),
                  'aanvraagnummer': _('Request number'),
                  'status': _('Status'),
                 }
        
    def batchfilter(self):
        if self.instance.method != Paymentmethod.objects.get(description='Incasso'):
            return None
        if self.instance.status == Paymentstatus.objects.get(status='Gepland'):
            return Paymentbatch.seizoen_objects.filter(status__status='Gepland')
        else:
            return None

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        betaaldverzonden = Payment.seizoen_objects.filter(contribution__member=self.instance.contribution.member,
                                         status__include=True).exclude(id=self.instance.id).\
                                         aggregate(Sum('amount'))['amount__sum'] or 0
        toplan = self.instance.contribution.tc - betaaldverzonden
        if amount > toplan:
            raise forms.ValidationError(_('Amount too high'))
        return amount

    def __init__(self, *args, **kwargs):
        super(UpdatePaymentForm, self).__init__(*args, **kwargs)
        batchqs = self.batchfilter()
        if batchqs:
            self.fields['paymentbatch'].queryset = batchqs
        else:
            self.fields['paymentbatch'].disabled = True
        self.fields['paymentdate'].widget = forms.TextInput(attrs={'type': 'date'})
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
                Row(
                    Column('paymentbatch', css_class='form-group col-lg-6 mb-0'),
                    Column('method', css_class='form-group col-lg-6 mb-0'),
                ),
                Row(
                    Column(PrependedText('amount', '€'), css_class='form-group col-lg-6 mb-0'),
                    Column('paymentdate', css_class='form-group col-lg-6 mb-0'),
                ),
                Row(
                    Column('aanvraagnummer', css_class='form-group col-lg-6 mb-0'),
                    Column('status', css_class='form-group col-lg-6 mb-0'),
                ),
                )
        self.helper.add_input(Submit('update', _('Update')))

class CreateNoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['member', 'description', 'note',   
                 ]
        labels = {
                  'member': _('Member'),
                  'description': _('Description'),
                  'note': _('Note'),
                 }

    def __init__(self, *args, **kwargs):
        super(CreateNoteForm, self).__init__(*args, **kwargs)
        self.fields['member'].disabled = True
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('update', _('Update')))

class MemberCreateForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ['relatiecode', 'roepnaam', 'voorletters', 'tussenvoegsels', 
                  'achternaam', 'straatnaam' , 'huisnummer',
                  'toevoeging', 'postcode', 'plaats', 'activities',
                 ]
        labels = {
                  'relatiecode': _('Relationcode'),
                  'roepnaam': _('First name'),
                  'voorletters': _('Initials'),
                  'tussenvoegsels': _('Infixes'),
                  'achternaam': _('Family name'),
                  'straatnaam': _('Street'),
                  'huisnummer': _('House number'),
                  'toevoeging': _('Addition'),
                  'postcode': _('Postal code'),
                  'plaats': _('City'),
                  'activities': _('Activities'),
                 }

    def clean_postcode(self):
        postcode = self.cleaned_data['postcode']
        if postcode:
            postcode = clean_postcode(postcode)
            if not valid_postcode(postcode):
                raise forms.ValidationError(_('Invalid postal code'))
        return postcode

    def __init__(self, *args, **kwargs):
        super(MemberCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
                Row(
                    Column('relatiecode', css_class='form-group col-lg-3 mb-0'),
                ),
                Row(
                    Column('roepnaam', css_class='form-group col-lg-3 mb-0'),
                    Column('voorletters', css_class='form-group col-lg-1 mb-0'),
                    Column('tussenvoegsels', css_class='form-group col-lg-2 mb-0'),
                    Column('achternaam', css_class='form-group col-lg-6 mb-0'),
                ),
                Row(
                    Column('straatnaam', css_class='form-group col-lg-8 mb-0'),
                    Column('huisnummer', css_class='form-group col-lg-2 mb-0'),
                    Column('toevoeging', css_class='form-group col-lg-2 mb-0'),
                ),
                Row(
                    Column('postcode', css_class='form-group col-lg-2 mb-0'),
                    Column('plaats', css_class='form-group col-lg-7 mb-0'),
                    Column('activities', css_class='form-group col-lg-3 mb-0'),
                ),
                )
        self.helper.add_input(Submit('update', _('Update')))
