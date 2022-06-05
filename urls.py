from django.conf.urls import url
from django_filters.views import FilterView
from .filters import MemberFilter, PaymentFilter
from .views import *

app_name = 'jarrbo_contributie'
urlpatterns = [
    url(r'^import/member/$', ImportMemberView.as_view(), name='importmember'),
    url(r'^import/member/success/(?P<pk>\d+)/$', ImportMemberDetail.as_view(),
                                                name='importmember_detail'),
    url(r'^import/rddata/$', ImportRddataView.as_view(), name='importrddata'),
    url(r'^import/rddata/success/$', ImportRddataDetail.as_view(),
                                                name='importrddata_detail'),
    url(r'^import/inschrijvingen/$', ImportInschrijvingenView.as_view(), name='importinschrijvingen'),
    url(r'^import/inschrijvingen/success/$', ImportInschrijvingenDetail.as_view(),
                                                name='importinschrijvingen_detail'),
    url(r'^import/machtigingen/$', ImportMachtigingenView.as_view(), name='importmachtigingen'),
    url(r'^import/machtigingen/success/$', ImportMachtigingenDetail.as_view(),
                                                name='importmachtigingen_detail'),
    url(r'^members/$', MemberListView.as_view(), name='members'),
    url(r'^member/(?P<pk>\d+)/$', MemberUpdateView.as_view(), name='member_detail'),
    url(r'^contribution/(?P<pk>\d+)/$', ContributionUpdateView.as_view(), name='contribution_detail'),
    url(r'^payment/(?P<pk>\d+)/$', PaymentUpdateView.as_view(), name='payment_detail'),
    url(r'^payments/$', PaymentListView.as_view(), name='payments'),
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^incasso/$', PaymentbatchListView.as_view(), name='incasso'),
    url(r'^paymentbatch/submit/(?P<pk>\d+)/$', PaymentbatchSubmitView.as_view(), name='paymentbatch_submit'),
    url(r'^paymentbatch/execute/(?P<pk>\d+)/$', PaymentbatchExecuteView.as_view(), name='paymentbatch_execute'),
    url(r'^paymentbatch/create/(?P<pk>\d+)/$', PaymentbatchCreateView.as_view(), name='paymentbatch_create'),
    url(r'^paymentbatch/plan/(?P<pk>\d+)/$', PaymentbatchPlanView.as_view(), name='paymentbatch_plan'),
    url(r'^payment/movenext/(?P<pk>\d+)/$', PaymentMovenextView.as_view(), name='payment_movenext'),
    url(r'^payment/statusupdate/(?P<pk>\d+)/(?P<newstatuspk>\d+)$',
                        PaymentStatusupdateView.as_view(), name='payment_statusupdate'),
    url(r'^note/create/$', NoteCreateView.as_view(), name='note_create'),
    url(r'^note/update/(?P<pk>\d+)/$', NoteUpdateView.as_view(), name='note_update'),
    url(r'^payment/mail/(?P<pk>\d+)/$', PaymentMailView.as_view(), name='mail'),
    url(r'^member/create/$', MemberCreateView.as_view(), name='member_create'),
    url(r'^payments/export/$', PaymentExport, name='payment_export'),
    url(r'^notpayed/$', NotPayedExport, name='notpayed_export'),
    url(r'^factuur/(?P<pk>\d+)/$', FactuurView.as_view(), name='factuur'),
    url(r'^restitutions/$', RestitutionFormSet.as_view(), name='restitutions'),
    url(r'^failed/(?P<pk>\d+)/$', FailedListView.as_view(), name='failed'),
]
