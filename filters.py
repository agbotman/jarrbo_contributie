from .models import Member, Payment, Activity, Contribution
from django.utils.translation import gettext as _
import django_filters

class MemberFilter(django_filters.FilterSet):
    class Meta:
        model = Member
        fields = {
            'relatiecode': ['exact'],
            'achternaam': ['icontains'],
            'roepnaam': ['icontains'],
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

class ContributionFilter(django_filters.FilterSet):
    voldaan = django_filters.BooleanFilter(
        method = 'voldaan_filter',
        label = _('Voldaan')
    )

    class Meta:
        model = Contribution
        fields = {
            'payment_method': ['exact'],
            'sponsored': ['exact'],
            'member__relatiecode': ['exact'],
            'member__roepnaam': ['icontains'],
            'member__achternaam': ['icontains'],
        }

    def voldaan_filter(self, queryset, name, value):
        return queryset.filter(voldaan=value)
