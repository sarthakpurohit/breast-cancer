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
from django.contrib.staticfiles.storage import staticfiles_storage
# Create your views here.
from .models import ImageUpload
from django.contrib import messages


from .inference import predict


# Create your views here.
def index(request):
    if request.method=="POST":
        print("Hello")
        if 'newsrequest' in request.POST:
            email=request.POST['email']
            name=request.POST['name']
            mail_subject = "[NewsLetter Subscription] Pink Ribbon - Digital Nerds"
            current_site = get_current_site(request)
            message = render_to_string('app/email.html', {
                'user': email,
                'firstname': name,
                'domain': current_site.domain,
                # 'pass': role_user_password,
            })
            email = EmailMessage(mail_subject, message, from_email=EMAIL_HOST_USER, to=[email])
            email.send()
            return redirect(request.path_info)

    return render(request,'app/index.html')

def userlogin(request):
    if request.method == 'POST':
        if 'create' in request.POST:
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            username=email

            if User.objects.filter(username=username).exists():
                messages.error(request,'That username is already taken')
                return redirect('userlogin')
            else:
                user = User.objects.create_user(username=email,password=password,email=email,first_name=name,last_name=name)
                user.save()
                #
                # u_id = User.objects.get(username=email)
                # addusr = UserDetails(user_id=u_id,number=number,address=address)
                # addusr.save()

                messages.success(request,'You are now registered and can log in')
                return redirect('userlogin')

        if 'login' in request.POST:
            username = request.POST['email']
            password = request.POST['password']

            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('/dashboard/')
            else:
                messages.error(request,"Invalid Credentials")
                print("fail")
                return redirect('dashboard')
        else:
            return render(request,'app/userlogin.html')
    return render(request,'app/login.html')








@login_required
def dashboard (request):
    prediction = {"class": "", "confidence": "", "display": "none"}
    if request.method=="POST":
        if 'upload' in request.POST:
            img_file=request.FILES['imgfile']
            count=ImageUpload.objects.count()
            count=count+1
            dis="img"+str(count)

            data=ImageUpload(img=img_file,img_id=dis)
            data.save()

            prediction = predict("media/testing_image/" + str(img_file))
            with open('media/predict.txt', 'w') as file:
                file.write(prediction[0] + "\n" + prediction[1])

            return redirect(request.path_info)
    if os.path.exists('media/predict.txt'):
        with open('media/predict.txt', 'r') as file:
            prediction = file.read().split('\n')
            prediction = {"class": prediction[0], "confidence": prediction[1]}
        os.remove('media/predict.txt')
    context = {
        'prediction': prediction
    }

    return render(request,'app/dashboard.html', context)