from django.views.generic import FormView, DetailView, TemplateView, ListView, View
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.db.models import F
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.template.loader import get_template

from extra_views import ModelFormSetView

from .forms import *
from .models import MemberImport, Member, Contribution, Activity, Paymentbatch, Note, CoronaRestitution
from .filters import MemberFilter, PaymentFilter
from .importers import *
from .tools import send_contributiemail

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'jarrbo_contributie/dashboard.html'
    title = 'Dashboard'
    
    def generictotals(self):
        generictotals = Contribution.objects.all().aggregate(
                                basiscontributie=Sum('bc'), 
                                kledingfonds=Sum('kf'),
                                toeslagen=Sum(F('ak') + F('aanmaningskosten')),
                                kortingen=Sum(F('kd') + F('kortingopadres') + F('ks')),
                                totalcontribution=Sum('tc')
                                )
        generictotals['betaald'] = Payment.objects.filter(status__status='Betaald').aggregate(
                                tot=Sum('amount'))['tot']
        return generictotals

    def activitytotals(self):
        totals = Contribution.objects.order_by('activity').values('activity__description').annotate(
                                basiscontributie=Sum('bc'), 
                                kledingfonds=Sum('kf'),
                                administratiekosten=Sum('ak'),
                                aanmaningskosten=Sum('aanmaningskosten'),
                                kortingopdatum = Sum('kd'),
                                gezinskorting = Sum('kortingopadres'),
                                kortingspeciaal = Sum('ks'),
                                totalcontribution=Sum('tc')
                                )
        for d in totals:
            d['toeslagen'] = d['administratiekosten'] + d['aanmaningskosten']
            d['kortingen'] = d['kortingopdatum'] + d['gezinskorting'] + d['kortingspeciaal']
            d['betaald'] = Payment.objects.filter(
                            contribution__activity__description=d['activity__description'],
                            status__status='Betaald').aggregate(
                                tot=Sum('amount'))['tot']
        return totals

    def categorytotals(self):
        totals = Contribution.objects.order_by('member__lc').values('member__lc__description').annotate(
                                basiscontributie=Sum('bc'), 
                                kledingfonds=Sum('kf'),
                                administratiekosten=Sum('ak'),
                                aanmaningskosten=Sum('aanmaningskosten'),
                                kortingopdatum = Sum('kd'),
                                gezinskorting = Sum('kortingopadres'),
                                kortingspeciaal = Sum('ks'),
                                totalcontribution=Sum('tc')
                                )
        for d in totals:
            d['toeslagen'] = d['administratiekosten'] + d['aanmaningskosten']
            d['kortingen'] = d['kortingopdatum'] + d['gezinskorting'] + d['kortingspeciaal']
            d['betaald'] = Payment.objects.filter(
                            contribution__member__lc__description=d['member__lc__description'],
                            status__status='Betaald').aggregate(
                                tot=Sum('amount'))['tot']
        return totals

class ImportMemberView(LoginRequiredMixin, FormView):
    form_class = ImportMemberForm
    template_name = 'jarrbo_contributie/import_members.html'
    
    def get_success_url(self):
        return reverse_lazy('jarrbo_contributie:importmember_detail',
                            kwargs={'pk': self.pk})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                self.pk = import_Memberfile(request.FILES['file'])
            except (MissingHeaderException, InvalidFileFormatException) as e:
                form.add_error('file', e)
                return self.form_invalid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
class ImportMemberDetail(LoginRequiredMixin, DetailView):
    model = MemberImport
    template_name = 'jarrbo_contributie/import_member_detail.html'

class ImportRddataView(LoginRequiredMixin, FormView):
    form_class = ImportRddataForm
    template_name = 'jarrbo_contributie/import_rddata.html'
    
    def get_success_url(self):
        return reverse_lazy('jarrbo_contributie:importrddata_detail')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            import_Rddatafile(request.FILES['file'])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
class ImportRddataDetail(LoginRequiredMixin, TemplateView):
    template_name = 'jarrbo_contributie/import_rddata_detail.html'

class ImportInschrijvingenView(LoginRequiredMixin, FormView):
    form_class = ImportInschrijvingenForm
    template_name = 'jarrbo_contributie/import_inschrijvingen.html'
    
    def get_success_url(self):
        return reverse_lazy('jarrbo_contributie:importinschrijvingen_detail')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            import_Inschrijvingenfile(request.FILES['file'])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
class ImportInschrijvingenDetail(LoginRequiredMixin, TemplateView):
    template_name = 'jarrbo_contributie/import_inschrijvingen_detail.html'

class ImportMachtigingenView(LoginRequiredMixin, FormView):
    form_class = ImportMachtigingenForm
    template_name = 'jarrbo_contributie/import_machtigingen.html'
    
    def get_success_url(self):
        return reverse_lazy('jarrbo_contributie:importmachtigingen_detail')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            import_Machtigingenfile(request.FILES['file'])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
class ImportMachtigingenDetail(LoginRequiredMixin, TemplateView):
    template_name = 'jarrbo_contributie/import_machtigingen_detail.html'
    
class MemberListView(LoginRequiredMixin, FilterView):
    model = Member
    paginate_by = 18
    filterset_class = MemberFilter
    
class PaymentListView(LoginRequiredMixin, FilterView):
    model = Payment
    paginate_by = 18
    filterset_class = PaymentFilter

    # A Queryset containing all paymentstatus is needed in payment_filter.html
    def paymentstatus(self):
        return Paymentstatus.objects.all()
    
class PaymentbatchListView(LoginRequiredMixin, ListView):
    model = Paymentbatch

class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    form_class = UpdateMemberForm

    def get_success_url(self):
        return reverse_lazy('jarrbo_contributie:member_detail',
                            kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        redirect_url = super(MemberUpdateView,self).form_valid(form)
        if form.has_changed():
            for c in self.object.contributions.all():
                c.update_memberdata()
        return redirect_url

class ContributionUpdateView(LoginRequiredMixin, UpdateView):
    model = Contribution
    form_class = UpdateContributionForm

    def get_success_url(self):
        return reverse_lazy('jarrbo_contributie:contribution_detail',
                            kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        redirect_url = super(ContributionUpdateView,self).form_valid(form)
        if form.has_changed():
            self.object.recreate_payments()
        return redirect_url

class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = UpdatePaymentForm

    def get_success_url(self):
        return reverse_lazy('jarrbo_contributie:payment_detail',
                            kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        redirect_url = super(PaymentUpdateView,self).form_valid(form)
        if form.has_changed():
            if 'amount' in form.changed_data:
                fromdate = self.object.paymentdate
                self.object.contribution.recreate_payments(fromdate)
        return redirect_url

                            
class PaymentbatchSubmitView(LoginRequiredMixin, View):
    http_method_names = ['post'] 
    
    def post(self, request, pk):
        batchgepland = PaymentbatchStatus.objects.get(status='Gepland')
        batchverzonden = PaymentbatchStatus.objects.get(status='Verzonden')
        paymentgepland = Paymentstatus.objects.get(status='Gepland')
        paymentverzonden = Paymentstatus.objects.get(status='Verzonden')
        try:
            paymentbatch = Paymentbatch.objects.get(pk=pk)
            paymentbatch.status = batchverzonden
            paymentbatch.save()
            Payment.objects.filter(paymentbatch=paymentbatch,
                                   status=paymentgepland).update(status=paymentverzonden)
        except:
            pass
        redirect_url = reverse('jarrbo_contributie:incasso')
        return redirect(redirect_url)
                            
class PaymentbatchCreateView(LoginRequiredMixin, View):
    http_method_names = ['get'] 
    
    def get(self, request, pk):
        paymentbatch = Paymentbatch.objects.get(pk=pk)
        wb = paymentbatch.createIncassobatch()
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")
        filename=("Incassobatch_%s_%s.xlsx" % (paymentbatch, dt_string))
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        wb.save(response)
        return response

                            
class PaymentbatchExecuteView(LoginRequiredMixin, View):
    http_method_names = ['post'] 
    
    def post(self, request, pk):
        batchverzonden = PaymentbatchStatus.objects.get(status='Verzonden')
        batchuitgevoerd = PaymentbatchStatus.objects.get(status='Uitgevoerd')
        paymentverzonden = Paymentstatus.objects.get(status='Verzonden')
        paymentbetaald = Paymentstatus.objects.get(status='Betaald')
        paymentbatch = Paymentbatch.objects.get(pk=pk)
        paymentbatch.status = batchuitgevoerd
        paymentbatch.save()
        Payment.objects.filter(paymentbatch=paymentbatch,
                               status=paymentverzonden).update(status=paymentbetaald)
        redirect_url = reverse('jarrbo_contributie:incasso')
        return redirect(redirect_url)
                            
class PaymentbatchPlanView(LoginRequiredMixin, View):
    http_method_names = ['post'] 
    
    def post(self, request, pk):
        batchuitgevoerd = PaymentbatchStatus.objects.get(status='Uitgevoerd')
        batchgepland = PaymentbatchStatus.objects.get(status='Gepland')
        paymentbetaald = Paymentstatus.objects.get(status='Betaald')
        paymentgepland = Paymentstatus.objects.get(status='Gepland')
        paymentbatch = Paymentbatch.objects.get(pk=pk)
        paymentbatch.status = batchgepland
        paymentbatch.save()
        Payment.objects.filter(paymentbatch=paymentbatch,
                               status=paymentbetaald).update(status=paymentgepland)
        redirect_url = reverse('jarrbo_contributie:incasso')
        return redirect(redirect_url)
        
class PaymentMovenextView(LoginRequiredMixin, View):
    http_method_names = ['post']
    
    def post(self, request, pk):
        payment = Payment.objects.get(pk=pk)
        paymentgepland = Paymentstatus.objects.get(status='Gepland')
        batchgepland = PaymentbatchStatus.objects.get(status='Gepland')
        incasso = Paymentmethod.objects.get(description='Incasso')
        if payment.status == paymentgepland and payment.method == incasso:
            batchlist = list(Paymentbatch.objects.filter(status=batchgepland))
            currentpos = batchlist.index(payment.paymentbatch)
            if currentpos < len(batchlist) - 1:
                nextbatch = batchlist[currentpos + 1]
                payment.paymentbatch = nextbatch
                payment.save()
        redirect_url = request.META.get('HTTP_REFERER')
        return redirect(redirect_url)

class PaymentStatusupdateView(LoginRequiredMixin, View):
    http_method_names = ['post']
    
    def post(self, request, pk, newstatuspk):
        payment = Payment.objects.get(pk=pk)
        currentstatus = payment.status
        newstatus = Paymentstatus.objects.get(pk=newstatuspk)
        method = payment.method
        valid = True
        try:
            PaymentstatusChange.objects.get(paymenttype=method.type,
                                            statusbefore=currentstatus,
                                            statusafter=newstatus)
        except PaymentstatusChange.DoesNotExist:
            valid = False
        if valid:
            payment.status = newstatus
            payment.save()
        if currentstatus.regular and not newstatus.regular:
            if payment.method == Paymentmethod.objects.get(description='Incasso'):
                st = PaymentbatchStatus.objects.get(status='Gepland')
                nextbatch = Paymentbatch.objects.filter(seizoen=payment.seizoen,status=st)[0]
                newpayment = Payment()
                newpayment.seizoen = payment.seizoen
                newpayment.contribution = payment.contribution
                newpayment.paymentbatch = nextbatch
                newpayment.method = payment.method
                newpayment.amount = payment.amount
                newpayment.status =Paymentstatus.objects.get(status='Gepland')
                newpayment.createdate = date.today()
                newpayment.save()
        redirect_url = request.META.get('HTTP_REFERER')
        return redirect(redirect_url)

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = CreateNoteForm

    def get_initial(self, *args, **kwargs):
        initial = super(NoteCreateView, self).get_initial(**kwargs)
        relatiecode = self.request.GET['relatiecode']
        initial['member'] = Member.objects.get(relatiecode=relatiecode)
        return initial      

    def get_success_url(self):
        return self.request.GET.get('next') or \
                reverse_lazy('jarrbo_contributie:member_detail',
                            kwargs={'pk': self.object.member.pk})

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = CreateNoteForm

    def get_success_url(self):
        return self.request.GET.get('next') or \
                reverse_lazy('jarrbo_contributie:member_detail',
                            kwargs={'pk': self.object.member.pk})

class PaymentMailView(LoginRequiredMixin, View):
    http_method_names = ['post']
    
    def post(self, request, pk):
        payment = Payment.objects.get(pk=pk)
        if payment.status.status == 'Teruggeboekt' or payment.status.status == 'Geensaldo':
            if not payment.withdrawnmaildate:
                template = get_template('jarrbo_contributie/stornering-1.txt')
                
                ctx = {'payment': payment,
                       'nextbatch': Paymentbatch.objects.nextbatch(),
                      }
                subject = ("Incasso contributie %s niet geslaagd" % (payment.contribution.member.fullname,))
                body = template.render(ctx)
                to_mail = payment.contribution.member.email
                send_contributiemail(subject, body, to_mail)
                payment.withdrawnmaildate = date.today()
                payment.save()
        if payment.method.description == 'Huygenspas' and not payment.huygensmaildate:
            template = get_template('jarrbo_contributie/huygens.txt')
            
            ctx = {'payment': payment,
                  }
            subject = "Betalen contributie SVW'27 met Huygenspas"
            body = template.render(ctx)
            to_mail = payment.contribution.member.email
            send_contributiemail(subject, body, to_mail)
            payment.huygensmaildate = date.today()
            payment.save()
        redirect_url = request.META.get('HTTP_REFERER')
        return redirect(redirect_url)
        

class MemberCreateView(LoginRequiredMixin, CreateView):
    model = Member
    form_class = MemberCreateForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        redirect_url = super(MemberCreateView,self).form_valid(form)
        self.object.naam_machtiging = self.object.fullname
        self.object.adres_machtiging = self.object.shortaddress
        self.object.postcode_machtiging = self.object.postcode
        self.object.plaats_machtiging = self.object.plaats
        method = Paymentmethod.objects.get(description='Factuur')
        donateur = Activity.objects.get(description='Donateur')
        if donateur in self.object.activities.all():
            self.object.paymentmethod = Paymentmethod.objects.get(description='Factuur')
        self.object.save()
        for activity in self.object.activities.all():
            c = Contribution.objects.create_contribution(member=self.object, 
                                                seizoen=config.seizoen, activity=activity)
            c.recreate_payments()
        return redirect_url
        
def PaymentExport(request):
    import csv
    # set nl language code so that decimal point will be comma
    import locale
    locale.setlocale(locale.LC_ALL,'nl_NL.utf8')

    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")
    filename=("Payments_%s.xlsx" % (dt_string,))
    response = HttpResponse(
        content_type='text/csv',
    )
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    
    # Create a csv witer that writes to the response object
    writer = csv.writer(response, delimiter=";")
    # Write a first row with header information
    writer.writerow(['naam', 'activiteit', 'categorie',
                     'betaalmethode', 'bedrag', 'status'])
    
    for p in Payment.objects.all().select_related('contribution__member',
                                                    'contribution__activity'):
        writer.writerow([p.contribution.member, p.contribution.activity,
                         p.contribution.member.lc, p.method, '{0:n}'.format(p.amount),
                         p.status])
    return response
        
class FactuurView(View):
    http_method_names = ['post']
    
    def post(self, request, pk):
        from mailmerge import MailMerge
        from django.conf import settings
        import locale
        locale.setlocale(locale.LC_ALL,'nl_NL.utf8')
        
        payment = Payment.objects.get(pk=pk)
        c = payment.contribution
        m = payment.contribution.member
        a = payment.contribution.activity
        if payment.method.description == 'Jeugdsportfonds':
            if not payment.factuurnummer:
                config = Configuration.objects.get()
                payment.factuurnummer = config.last_factuurnummer + 1
                config.last_factuurnummer = payment.factuurnummer
                payment.save()
                config.save()
        if a.description == 'Donateur':
            betreft="Bijdrage donateur SVW'27"
        else:
            betreft="Contributie SVW'27"
        datum = date.today()
        machtigingdatum = datum + timedelta(weeks=2)
        betaaldatum = datum + timedelta(weeks=4)
        if c.total_korting == 0:
            kortingregel = ''
            korting = ''
        else:
            kortingregel='Korting'
            korting = ("€    %s" % ('{0:n}'.format(c.total_korting),))
        extra = ''
        if m.leeftijdscategorie.description == 'Senioren':
            extra = ("%s %s %s %s %s %s %s %s" % (
                'Seniorenleden zijn vorig seizoen extra getroffen door de Coronamaatregelen.', 
                'Daarom hebben zij recht op een teruggave van € 70,-.', 
                'Op korte termijn kunnen zij hiervoor een verzoek indienen via', 
                'een webformulier op de site.',
                'Voorwaarde is dat van de seizoenen 2019-2020 en 2020-2021',
                'de contributie volledig betaald is.',
                'Vanwege administratieve redenen kan dit niet gecombineerd',
                'worden met de betaling van de contributie.',))
        merge_dict = {
                      'fullname': m.naam_machtiging,
                      'geboortedatum': m.geboortedatum.strftime('%d-%m-%Y'),
                      'adres': m.adres_machtiging,
                      'postcode': m.postcode_machtiging,
                      'plaats': m.plaats_machtiging,
                      'relatiecode': m.relatiecode,
                      'factuurdatum': datum.strftime('%d %B %Y'),
                      'seizoen': str(c.seizoen),
                      'basiscontributie': '{0:n}'.format(c.base_contribution),
                      'betreft': betreft,
                      'lidnaam': m.fullname,
                      'kosten': '{0:n}'.format(c.total_cost),
                      'totaalcontributie': '{0:n}'.format(c.total_contribution),
                      'factuurbedrag': '{0:n}'.format(payment.amount),
                      'machtigingdatum': machtigingdatum.strftime('%d %B %Y'),
                      'betaaldatum': betaaldatum.strftime('%d %B %Y'),
                      'kortingregel': kortingregel,
                      'korting': korting,
                      'extra': extra,
                      'aanvraagnummer': payment.aanvraagnummer,
                      'factuurnummer': 'C' + str(payment.factuurnummer),
        }
        if payment.method.description == 'Jeugdsportfonds':
            path = '/'.join((settings.MEDIA_ROOT,'jarrbo_contributie','factuur_template_jeugdsportfonds_v1.0.docx'))
        elif a.description == 'Donateur':
            path = '/'.join((settings.MEDIA_ROOT,'jarrbo_contributie','factuur_template_donateur.docx'))
        else:
            path = '/'.join((settings.MEDIA_ROOT,'jarrbo_contributie','factuur_template_spelend.docx'))
        document = MailMerge(path)
        document.merge(**merge_dict)
            
        filename = ("factuur_%s.docx" % (m.relatiecode,))

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        )
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        document.write(response)
        
        return response

class RestitutionFormSet(ModelFormSetView):
    model = CoronaRestitution
    fields = ['s_2021', 'applied', 'amount', 'payed']
    template_name = 'jarrbo_contributie/coronarestitution_formset.html'
    factory_kwargs = {'extra': 0, }
    paginate_by = 18
    
    # For instantiation of the formset we use the page_object iso of the full model query
    def get_formset_kwargs(self):
        from django.core.paginator import Paginator
        kwargs = super().get_formset_kwargs()
        qs = kwargs["queryset"]
        paginator = Paginator(qs, self.paginate_by)
        page_kwarg = self.page_kwarg
        page_number = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        page_object = paginator.get_page(page_number)
        page_object.ordered = True
        kwargs["queryset"] = page_object
        return kwargs
        
        