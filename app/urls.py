from django.urls import path
from .views import about, index,apply,business,contact,emi,faq,loan,login,personal,privacy,signup,terms,track, logout,profile,edit_profile, pay_emi

urlpatterns = [
    path('', index, name='home'),

    path('about/', about,name="about"),

    path('apply/', apply,name="apply"),

    path('business/', business,name="base"),

    path('contact/', contact,name="contact"),

    path('emi/', emi,name="emi"),

    path('faq/', faq,name="faq"),

    path('loan/', loan,name="loan"),

    path('personal/', personal,name="personal"),

    path('privacy/', privacy,name="privacy"),

    path('signup/', signup,name="signup"),

    path('terms/', terms,name="terms"),

    path('track/', track,name="track"),

    path('login/', login,name="login"),

    path('logout/', logout,name="logout"),

    path('profile/', profile,name="profile"),

    path('edit-profile/', edit_profile, name='edit_profile'),
    
    path('pay-emi/<int:emi_id>/', pay_emi, name='pay_emi'),
]

