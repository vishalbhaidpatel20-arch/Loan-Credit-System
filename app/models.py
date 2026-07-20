from django.db import models
from django.contrib.auth.models import User

class loanApplication(models.Model):

    LOAN_STATUS = (
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending')
    )

    LOAN_TYPE = (
        ('personal', 'Personal Loan'),
        ('business', 'Business Loan'),
        ('home', 'Home Loan'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=30)
    email = models.EmailField()
    number = models.CharField(max_length=10)
    address = models.TextField()
    PanNumber = models.CharField(max_length=13)
    employeStatus = models.CharField(max_length=30)

    loan_type = models.CharField(max_length=20, choices=LOAN_TYPE, default="")
    loan_amount = models.IntegerField()
    loan_duration = models.IntegerField(max_length=12, default=12)  # months
    income = models.IntegerField()
    city = models.TextField()

    status = models.CharField(max_length=20, choices=LOAN_STATUS, default="pending")
    interest_rate = models.FloatField(default=10)

    def __str__(self):
        return f"{self.name} - {self.loan_type}"


class loanModel(models.Model):
    application = models.ForeignKey(loanApplication, on_delete=models.CASCADE)

    approved_amount = models.IntegerField()
    interest_rate = models.FloatField()

    loan_start_date = models.DateField()
    loan_end_date = models.DateField()

    status = models.BooleanField(default=False)  # True = active

    # EMI Calculation
    def emi(self):
        P = self.approved_amount
        R = self.interest_rate / 100 / 12
        N = self.application.loan_duration

        if R == 0:
            return P / N

        emi = (P * R * (1 + R)**N) / ((1 + R)**N - 1)
        return round(emi, 2)

    def __str__(self):
        return f"Loan for {self.application.name}"


class paymentModel(models.Model):
    loan = models.ForeignKey(loanModel, on_delete=models.CASCADE)  # ✅ FIXED

    amount = models.IntegerField()
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=30)

    STATUS = (
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('failed', 'Failed')
    )

    status = models.CharField(max_length=20, choices=STATUS)

    def __str__(self):
        return f"{self.amount} paid"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_pic = models.ImageField(upload_to='profile/', default='profile/default.png')
    mobile_no = models.CharField(max_length=10)
    address = models.TextField()


class EMI(models.Model):
    loan = models.ForeignKey(loanApplication, on_delete=models.CASCADE)
    installment_number = models.IntegerField()
    amount = models.FloatField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=(('paid', 'Paid'), ('pending', 'Pending')),
        default='pending'
    )

    def __str__(self):
        return f"{self.loan.name} - EMI {self.installment_number}"