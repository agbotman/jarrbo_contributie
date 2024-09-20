from django.urls import re_path
from .views import ImportMemberView, ImportMemberDetail, \
                    ImportInschrijvingenView, ImportInschrijvingenDetail, \
                    ImportMachtigingenView, ImportMachtigingenDetail, MemberListView, \
                    MemberUpdateView, ContributionUpdateView, PaymentUpdateView, PaymentListView, ContributionListView, \
                    DashboardView, PaymentbatchListView, PaymentbatchSubmitView, PaymentbatchExecuteView, \
                    PaymentbatchCreateView, PaymentbatchPlanView, PaymentMovenextView, \
                    PaymentStatusupdateView, NoteCreateView, NoteUpdateView, PaymentMailView, \
                    MemberCreateView, FactuurView, FailedListView, ContributionExportView, \
                    PaymentExport, NotPayedExport

app_name = 'jarrbo_contributie'
urlpatterns = [
    re_path(r'^import/member/$', ImportMemberView.as_view(), name='importmember'),
    re_path(r'^import/member/success/(?P<pk>\d+)/$', ImportMemberDetail.as_view(),
                                                name='importmember_detail'),
    re_path(r'^import/inschrijvingen/$', ImportInschrijvingenView.as_view(), name='importinschrijvingen'),
    re_path(r'^import/inschrijvingen/success/$', ImportInschrijvingenDetail.as_view(),
                                                name='importinschrijvingen_detail'),
    re_path(r'^import/machtigingen/$', ImportMachtigingenView.as_view(), name='importmachtigingen'),
    re_path(r'^import/machtigingen/success/$', ImportMachtigingenDetail.as_view(),
                                                name='importmachtigingen_detail'),
    re_path(r'^members/$', MemberListView.as_view(), name='members'),
    re_path(r'^member/(?P<pk>\d+)/$', MemberUpdateView.as_view(), name='member_detail'),
    re_path(r'^contribution/(?P<pk>\d+)/$', ContributionUpdateView.as_view(), name='contribution_detail'),
    re_path(r'^contributions/$', ContributionListView.as_view(), name='contributions'),
    re_path(r'^payment/(?P<pk>\d+)/$', PaymentUpdateView.as_view(), name='payment_detail'),
    re_path(r'^payments/$', PaymentListView.as_view(), name='payments'),
    re_path(r'^$', DashboardView.as_view(), name='dashboard'),
    re_path(r'^incasso/$', PaymentbatchListView.as_view(), name='incasso'),
    re_path(r'^paymentbatch/submit/(?P<pk>\d+)/$', PaymentbatchSubmitView.as_view(), name='paymentbatch_submit'),
    re_path(r'^paymentbatch/execute/(?P<pk>\d+)/$', PaymentbatchExecuteView.as_view(), name='paymentbatch_execute'),
    re_path(r'^paymentbatch/create/(?P<pk>\d+)/$', PaymentbatchCreateView.as_view(), name='paymentbatch_create'),
    re_path(r'^paymentbatch/plan/(?P<pk>\d+)/$', PaymentbatchPlanView.as_view(), name='paymentbatch_plan'),
    re_path(r'^payment/movenext/(?P<pk>\d+)/$', PaymentMovenextView.as_view(), name='payment_movenext'),
    re_path(r'^payment/statusupdate/(?P<pk>\d+)/(?P<newstatuspk>\d+)$',
                        PaymentStatusupdateView.as_view(), name='payment_statusupdate'),
    re_path(r'^payment/statusupdate/(?P<pk>\d+)/(?P<newstatuspk>\d+)/(?P<statuscodepk>\d+)$',
                        PaymentStatusupdateView.as_view(), name='payment_statusupdate2'),
    re_path(r'^note/create/$', NoteCreateView.as_view(), name='note_create'),
    re_path(r'^note/update/(?P<pk>\d+)/$', NoteUpdateView.as_view(), name='note_update'),
    re_path(r'^payment/mail/(?P<pk>\d+)/$', PaymentMailView.as_view(), name='mail'),
    re_path(r'^member/create/$', MemberCreateView.as_view(), name='member_create'),
    re_path(r'^payments/export/$', PaymentExport, name='payment_export'),
    re_path(r'^notpayed/$', NotPayedExport, name='notpayed_export'),
    re_path(r'^factuur/(?P<pk>\d+)/$', FactuurView.as_view(), name='factuur'),
    re_path(r'^failed/(?P<pk>\d+)/$', FailedListView.as_view(), name='failed'),
    re_path(r'^contributions/export$', ContributionExportView.as_view(), name='contribution_export'),
]
