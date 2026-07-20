from django.contrib import admin
from .models import loanApplication
from .models import loanModel
from .models import paymentModel, EMI

admin.site.register(loanApplication)
admin.site.register(loanModel)
admin.site.register(paymentModel)
admin.site.register(EMI)