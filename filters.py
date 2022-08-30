from .models import Member, Payment, Activity
from django.utils.translation import ugettext as _
import django_filters

class MemberFilter(django_filters.FilterSet):
    class Meta:
        model = Member
        fields = {
            'relatiecode': ['exact'],
            'achternaam': ['icontains'],
            'lc': ['exact'],
            'status': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super(MemberFilter, self).__init__(*args, **kwargs)
        self.filters['achternaam__icontains'].label=_('Family name contains')
        self.filters['lc'].label=_('Age category')
        

class PaymentFilter(django_filters.FilterSet):
    activiteit = django_filters.ModelChoiceFilter(
        queryset = Activity.objects.all(),
        method = 'activity_filter',
        label = _('Activity')
        )

    class Meta:
        model = Payment
        fields = {
            'method': ['exact'],
            'paymentbatch': ['exact'],
            'status': ['exact'],
            'paymentstatuscode': ['exact'],
            'contribution__member__relatiecode': ['exact'],
        }

    def activity_filter(self, queryset, name, value):
        return queryset.filter(contribution__activity__description=value.description)

    def __init__(self, *args, **kwargs):
        super(PaymentFilter, self).__init__(*args, **kwargs)
        self.filters['contribution__member__relatiecode'].label=_('Relation code')
