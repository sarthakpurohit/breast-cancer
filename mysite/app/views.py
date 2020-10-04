from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
# from .models import UserDetails,WorkerDetails
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
# EMAIL FROM SETTINGS
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from mysite.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError
# Create your views here.

#
# def loginworker(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#
#         user = auth.authenticate(username=username,password=password)
#         if user is not None:
#             auth.login(request,user)
#             return redirect('dashboardworker')
#         else:
#             # messages.error(request,"Invalid Credentials")
#             return redirect('loginworker')
#     else:
#         return render(request,'accounts/loginworker.html')
#






# Create your views here.
def index(request):
    # mail_subject = "[Activate Account] VE - Virtual Employee"
    # current_site = get_current_site(request)
    # message = render_to_string('app/email.html', {
    #     'user': role_user_email,
    #     'firstname': user_firstname,
    #     'lastname': user_lastname,
    #     'domain': current_site.domain,
    #     'pass': role_user_password,
    # })
    # email = EmailMessage(mail_subject, message, from_email=EMAIL_HOST_USER, to=[role_user_email])
    # email.send()
     return render(request,'app/index.html')

def userlogin(request):
    if request.method == 'POST':
        if 'create' in request.POST:
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            username=email

            if User.objects.filter(username=username).exists():
                # messages.error(request,'That username is already taken')
                return redirect('userlogin')
            else:
                user = User.objects.create_user(username=email,password=password,email=email,first_name=name,last_name=name)
                user.save()
                #
                # u_id = User.objects.get(username=email)
                # addusr = UserDetails(user_id=u_id,number=number,address=address)
                # addusr.save()

                # messages.success(request,'You are now registered and can log in')
                return redirect('userlogin')

        if 'login' in request.POST:
            username = request.POST['email']
            password = request.POST['password']

            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                print("Success")
                return redirect('/dashboard/')
            else:
                # messages.error(request,"Invalid Credentials")
                print("fail")
                return redirect('dashboard')
        else:
            return render(request,'app/userlogin.html')
    # print("outcfsdfs")
    return render(request,'app/login.html')



@login_required
def dashboard (request):
    return render(request,'app/dashboard.html')
