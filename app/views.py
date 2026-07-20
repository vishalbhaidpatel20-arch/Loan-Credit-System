from django.shortcuts import render , redirect, get_object_or_404
from .models import loanApplication      #"  import the all models in urls and in path add the models"
#from .models import loanModel                 " like :-  "
#from .models import paymentModel
  #                                          def about(request):         
  #                                          xyz = loanModel.objects.all()     "xyz is the store the all objects of loanmodel"
  #                                          return render(request, 'about.html', {"hello" : xyz})    " hello is the keyvalue store the all values of xyz"
from .models import loanApplication, loanModel, UserProfile, paymentModel, EMI
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date
from django.contrib import messages




# Create your views here.
def  index(request):
    return render(request, 'index.html')

def about(request):
    return render(request,'about.html')

@login_required
def apply(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        address = request.POST.get('address')
        PanNumber = request.POST.get('PanNumber')
        employeStatus = request.POST.get('employeStatus')
        loan_duration = request.POST.get('loan_duration')
        loan_amount = request.POST.get('loan_amount')
        income = request.POST.get('income')
        city = request.POST.get('city')
        loan_type = request.POST.get('loan_type', "")
        loanApplication.objects.create(name=name ,email=email ,number=number,address=address,PanNumber=PanNumber,employeStatus=employeStatus,loan_amount=loan_amount,loan_duration=loan_duration,income=income,city=city,loan_type=loan_type, user=request.user)
        return redirect('home')
    return render(request,'apply.html')

def business(request):
    return render(request,'business-loan.html')

def contact(request):
    return render(request,'contact.html')

def emi(request):
    return render(request,'emi-calculator.html')

def faq(request):
    return render(request,'faq.html')

def loan(request):
    return render(request,'loans.html')

def login(request):
    if request.method == "POST":
        username= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home')
        return render(request,'login.html', {'error_msg' : "Please Enter valid details"})
    return render(request,'login.html')

def personal(request):
    return render(request,'personal-loan.html')

def privacy(request):
    return render(request,'privacy.html')

def signup(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        email= request.POST.get('email')
        password= request.POST.get('password')
        if User.objects.filter(username=username).exists():
             return render(request,'signup.html', {'error_msg': 'Username already exists'})
        User.objects.create_user(username=username,email=email,password=password)
        return redirect('login')
    return render(request,'signup.html')

def logout(request):
    auth_logout(request)
    return redirect('login')


def terms(request):
    return render(request,'terms.html')

def track(request):
    return render(request,'track.html')

from datetime import timedelta, date
from .models import EMI

@login_required
def profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    applications = loanApplication.objects.filter(user=user)

    approved = applications.filter(status="approved").count()
    pending = applications.filter(status="pending").count()
    rejected = applications.filter(status="rejected").count()

    
    # EMI creation logic
    for app in applications.filter(status="approved"):

        if not EMI.objects.filter(loan=app).exists():

            months = int(app.loan_duration)
            monthly_rate = app.interest_rate / 100 / 12

            if monthly_rate == 0:
                emi_amount = app.loan_amount / months
            else:
                emi_amount = (
                    app.loan_amount * monthly_rate * (1 + monthly_rate)**months
                ) / ((1 + monthly_rate)**months - 1)

            for i in range(1, months + 1):
                EMI.objects.create(
                    loan=app,
                    installment_number=i,
                    amount=round(emi_amount, 2),
                    due_date=date.today() + timedelta(days=30 * i)
                )
    emis = EMI.objects.filter(loan__user=request.user)

    return render(request, 'profile.html', {
        'profile': profile,
        'applications': applications,
        'approved': approved,
        'pending': pending,
        'rejected': rejected,
        'emis': emis
    })




@login_required
def pay_emi(request, emi_id):
    emi = get_object_or_404(EMI, id=emi_id)
    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        emi.status = "paid"
        emi.save()
        print(emi.status)

        messages.success(request, "Payment Successful!")

        return redirect('profile')

    return render(request, 'payment.html', {'emi': emi})

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.mobile_no = request.POST.get('mobile_no')
        profile.address = request.POST.get('address')

        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES.get('profile_pic')

        profile.save()
        return redirect('profile')

    return render(request, 'edit_profile.html', {'profile': profile})
