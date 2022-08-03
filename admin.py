from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import *

admin.site.register(Configuration, SingletonModelAdmin)
admin.site.register(MemberImport)
admin.site.register(ContributionTable)
admin.site.register(Seizoen)
admin.site.register(Activity)
admin.site.register(Leeftijdscategory)
admin.site.register(Longcategory)
admin.site.register(Paymentstatus)
admin.site.register(Paymentmethod)
admin.site.register(Paymentbatch)
admin.site.register(PaymentbatchStatus)
admin.site.register(Payment)
admin.site.register(Memberstatus)
admin.site.register(Member)
admin.site.register(Contribution)
admin.site.register(Rddata)
admin.site.register(PaymentstatusChange)
admin.site.register(PaymentType)
admin.site.register(PaymentStatusCode)