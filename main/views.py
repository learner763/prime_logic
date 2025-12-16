from django.shortcuts import render
from .forms import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from random import *
from .models import *
import secrets,string
def creator_studio_login(request):
    return render(request, "creator_studio_login.html")
def view_admin(request):
    return render(request, "view_admin.html")
def add_admin(request):
    return render(request, "add_admin.html")

def edit_admin(request):
    return render(request, "edit_admin.html")
@api_view(['POST'])
def delete_user(request):
    print(request.data['email'])
    app_users.objects.filter(email=request.data['email']).delete()
    return Response({"success": True})
@api_view(['POST'])
def all_users(request):
    person=app_users.objects.get(email=request.data['email'])
    people=''
    status=''
    name=''
    edited=''
    if request.data['edit']==False:
        if person.parent==request.data['email']:
            status='Admin'
            name=person.fullname
            people=list(app_users.objects.filter(parent=request.data['email']).exclude(email=request.data['email']).values())
        else:
            admin=app_users.objects.get(email=person.parent)
            if admin.parent==admin.email:
                status='User'
                name=person.fullname
                people=list(app_users.objects.filter(parent=request.data['email']).exclude(email=request.data['email']).values())
            else:
                status='SubUser'
                admin=app_users.objects.get(email=person.parent)
                name=admin.fullname
                people=list(app_users.objects.filter(parent=admin.email).exclude(email=admin.email).values())
        return Response({"success": False,'status':status,'people':people,'name':name,'edited':edited})

    if request.data['edit']:
        name=person.fullname
        edited=list(app_users.objects.filter(email=request.data['edit']).values())
        return Response({"success": len(edited)>0 and edited[0]['parent']==request.data['email'],'status':status,'people':people,'name':name,'edited':edited})

@api_view(['POST'])
def add_user(request):
    if(request.data['edit']==False):
        try:
            person=app_users.objects.get(email=request.data['email'])
            return Response({"success": False,"message":"User with this email already exists."})
        except app_users.DoesNotExist:
            person=app_users.objects.create(email=request.data['email'],password=request.data['password'],subscription=request.data['subscription'],
                                            fullname=request.data['fullname'],residence=request.data['residence'],source=request.data['source'],parent=request.data['parent'],
                                            displayname=request.data['fullname'],account=request.data['account'])
            return Response({"success": True})
    else:
        try:
            person=app_users.objects.get(email=request.data['email'])
            person.fullname=request.data['fullname']
            person.subscription=request.data['subscription']
            person.residence=request.data['residence']
            person.source=request.data['source']
            person.account=request.data['account']
            person.password=request.data['password']
            person.fullname=request.data['fullname']
            person.displayname=request.data['fullname']
            person.save()
            return Response({"success": True})
        except app_users.DoesNotExist:
            return Response({"success": False,"message":"User with this email does not exist."})
@api_view(['POST'])
def register(request):
    if(request.data['logging_in']==True):
        try:
            person=app_users.objects.get(email=request.data['email'],password=request.data['password'],account='Active')
            person.last_login=request.data['last_login']
            person.save()
            return Response({"success": True,"email":person.email})
        except app_users.DoesNotExist:
            return Response({"success": False,"message":"Invalid Credentials/You are not an active user!"})

    elif (request.data['logging_in']==False):
        if(len(list(app_users.objects.filter(email=request.data['email'])))==0):
            person=app_users.objects.create(email=request.data['email'],password=request.data['password'],fullname=request.data['fullname'],displayname=request.data['displayname'],residence=request.data['residence'],source=request.data['source'],parent=request.data['email'],account='Active',subscription='Active')
            return Response({"success": True,"email":person.email})
        else:
            return Response({"success": False,"message":"User with this email exists already.Choose another!"})
    else:
        try:
            person=app_users.objects.get(email=request.data['email'])
            return Response({"success": True,"message":f"Your Password is {person.password}"})
        except app_users.DoesNotExist:
            return Response({"success": False,"message":"User with this email does not exist!"})
'''
def pr(request):
    return render(request, "pr.html")

from .models import *
def login_admin(request):
    return render(request, "login_admin.html")
@api_view(['POST'])
def login(request):
    try:
        person=admin_person.objects.get(email=request.data['email'],password=request.data['password'],mode='Admin')
        print(person.group)
        print(person.email)
        return Response({"success": True,'group':person.group,'email':person.email})
    except admin_person.DoesNotExist:
        return Response({"success": False,"message":"Invalid Credentials/Someone removed you from being the admin."})


@api_view(['POST'])
def signup(request):
    if len(list(admin_person.objects.filter(email=request.data['email'])))==0:
        person=admin_person.objects.create(first_name=request.data['first_name'],last_name=request.data['last_name'],email=request.data['email'],password=request.data['password'],phone=str(request.data['phone']),mode='Admin',group=request.data['email'])
        return Response({"success": True})
    else:
        return Response({"success": False,"message":"Admin with this email exists already.Choose another!"})
def dashboard_admin(request):
    return render(request, "dashboard_admin.html")
@api_view(['POST'])
def forgot_password(request):
    try:
        person=admin_person.objects.get(email=request.data['email'],mode='Admin')
        return Response({"success": True,"password":person.password})
    except admin_person.DoesNotExist:
        return Response({"success": False,"message":"Admin with this email does not exist!"})
@api_view(['POST'])
def subusers_data(request):
    person=list(admin_person.objects.filter(group=request.data['group'],mode='Employee').values())
    return Response({"data":person})
@api_view(['POST'])
def personal_data(request):
    person=list(admin_person.objects.filter(group=request.data['group'],mode='Admin').values())
    return Response({"data":person})
@api_view(['POST'])
def update_personal_data(request):
    person=admin_person.objects.first()
    person.first_name=request.data['first_name']
    person.last_name=request.data['last_name']
    person.email=request.data['email']
    person.phone=str(request.data['phone'])
    person.password=request.data['password']
    person.save()
    return Response({"success": True})
@api_view(['POST'])
def delete_subuser(request):
    try:
        person=admin_person.objects.get(id=request.data['id'])
        if person.mode=='Admin':
            return Response({"success": False,"message":"You cant delete an admin!"})
        else:
            admin_person.objects.filter(id=request.data['id']).delete()
            return Response({"success": True,'id':request.data['id']})
    except admin_person.DoesNotExist:
        return Response({"success": False,"message":"Subuser not found!"})
@api_view(['POST'])
def update_subuser(request):
    try:
        person=admin_person.objects.get(id=request.data['id'])
        if person.mode=='Admin' and request.data['email']!=person.email and request.data['field']!='mode':
            print(request.data['field'])
            return Response({"success": False,"message":"You cant update other admin!"})
        if person.mode=='Admin' and request.data['email']==person.email and request.data['field']=='mode':
            return Response({"success": False,"message":"You cant change status of you being admin!"})
        if request.data['field']=='email':            
            return Response({"success": False,"message":"You cant update email."})
        else:
            setattr(person,request.data['field'],str(request.data['value']))
            person.save()
            return Response({'success':True,'value':request.data['value'],'id':request.data['id'],'field':request.data['field']})
    except admin_person.DoesNotExist:
        return Response({"success": False,"message":"Subuser not found"})
    
        
@api_view(['POST'])
def add_subuser(request):
    print(request.data)
    if(len(list(admin_person.objects.filter(email=request.data['email']))))==0:
        person=admin_person.objects.create(first_name=request.data['first_name'],last_name=request.data['last_name'],email=request.data['email'],password=request.data['password'],phone=str(request.data['phone']),mode=request.data['mode'],group=request.data['group'])
        return Response({"success": True,"id":person.id,"first_name":person.first_name,"last_name":person.last_name,"email":person.email,"phone":person.phone,"mode":person.mode,"password":person.password})
    else:
        return Response({"success": False,"message":"Subuser with this email already exists."})


def email_page(request):
    return render(request, "email_page.html")

@api_view(['POST'])
def verify_otp(request):
    try:
        person=emails.objects.get(email=request.data['email'])
        if(person.Otp==request.data['otp']):
            return Response({"success": True})
    except emails.DoesNotExist:
        return Response({"success": False,"message":f"Invalid OTP.Go to {request.data['email']} and paste correct one or may be ensure that your email address actually exists!"})
@api_view(['POST'])
def send_email(request):
    code=randint(100000,999999)
    try:
        send_mail(
            subject='OTP',
            message=str(code),
            from_email="uaftab1010@gmail.com",
            recipient_list=[request.data['recipient']],
            fail_silently=False
        )
        emails.objects.create(email=request.data['recipient'],Otp=code)
        return Response({"success": True,'OTP':code,'email':request.data['recipient']})
    except Exception as e:
        return Response({"error": f"{request.data['recipient']} is not a valid email address!"})

def upload_page(request):
    # This serves the HTML page
    return render(request, 'upload.html')

@api_view(['POST'])
def upload_profile(request):
    form = FileUploadForm(request.POST, request.FILES)

    if form.is_valid():
        image = form.cleaned_data['image']
        # Optional: save file
        return Response({"uploaded": True, "filename": image.name})

    return Response({"error": form.errors}, status=400)
def notes(request):
    return render(request, "notes.html")
def profile_page(request):
    return render(request, "profile.html")
@api_view(['POST'])
def profile_upload(request):
    form=file_upload(request.data)
    if form.is_valid():
        return Response({"responce":'File is valid'})
    else:
        return Response({"responce":form.errors.get_json_data()})
@api_view(['POST'])
def update_record(request):
    if(request.data['field']=='name'):
        if(len(request.data['new_value'])<=20):
            print('valid name')
            try:
                person=Students.objects.get(id=request.data['id'])
            except Students.DoesNotExist:
                return Response({"error": "Record not found"})
            if(len(list(Students.objects.filter(name=request.data['new_value']))))==0 or person.name==request.data['new_value']:
                person.name=request.data['new_value']
                person.save()
                return Response({"updated":True,"id":person.id,"name":person.name})
            else:
                return Response({"error": f"{request.data['new_value']} already exists"})
        else:
            return Response({"error": "Name length exceeds 20 characters"})
    elif(request.data['field']=='age'):
        if(request.data['new_value']>=20 and request.data['new_value']<=25):
            try:
                person=Students.objects.get(id=request.data['id'])
            except Students.DoesNotExist:
                return Response({"error": "Record not found"})            
            person.age=request.data['new_value']
            person.save()
            return Response({"updated":True,"id":person.id,"age":person.age})
        else:
            return Response({"error": "Age Range : 20:25"})
    elif(request.data['field']=='cgpa'):
        if(request.data['new_value']>=0.0 and request.data['new_value']<=4.0):
            try:
                person=Students.objects.get(id=request.data['id'])
            except Students.DoesNotExist:
                return Response({"error": "Record not found"})
            person.cgpa=request.data['new_value']
            person.save()
            return Response({"updated":True,"id":person.id,"cgpa":person.cgpa})
        else:
            return Response({"error": "CGPA Range : 0.0:4.0"})
@api_view(['POST'])
def delete_record(request):
    id=request.data['id']
    Students.objects.filter(id=id).delete()
    return Response({"deleted":True,"id":id})

@api_view(['POST'])
def add_note(request):
    form=StudentsForm(request.data)
    if form.is_valid():
        print('valid')
        if(len(list(Students.objects.filter(name=form.cleaned_data['name']))))==0:
            person=Students.objects.create(name=form.cleaned_data['name'],age=form.cleaned_data['age'],cgpa=form.cleaned_data['cgpa'])
            return Response({"created":True,"id":person.id,"name":person.name,"age":person.age,"cgpa":person.cgpa})
        else:
            return Response({"error": f"{request.data['name']} already exists","type":'exists'})
    else:
        print(request.data)
        return Response({"error": form.errors.get_json_data(),"type":'form'})
@api_view(['GET'])
def get_notes(request):
    all_notes=Students.objects.all().values()
    print(all_notes)
    return Response({'responce':list(all_notes)})


'''
def index(request):
    return render(request, "index.html")
@csrf_exempt
@api_view(['POST'])
def event_registration(request):
    try:
        person=techfest_participants.objects.get(token=request.data['token'])
        if request.data['operation']=='add':
            person.events.append(request.data['event_title'])
        else:
            person.events.remove(request.data['event_title'])
        person.save()
        return Response({'success':True,'code':request.data['code']})
    except techfest_participants.DoesNotExist:
        return Response({'success':False,'message':'Your token inside browser was changed/removed.Now Please log in to access your account'})

@csrf_exempt
@api_view(['POST'])
def handle_registration(request):
    need_auth=False
    if(request.data['action']==True):
        try:
            person=techfest_participants.objects.get(token=request.data['token'])
            if(person.email==request.data['email'] and person.password==request.data['password']):
                return Response({'success':True,'verified':True,'token':person.token})
            else:
                need_auth=True
        except techfest_participants.DoesNotExist:
            need_auth=True
        if(need_auth):
            try:
                person=techfest_participants.objects.get(email=request.data['email'],password=request.data['password'])
                code=randint(100000,999999)
                chars = string.ascii_letters + string.digits
                try:
                    send_mail(
                        subject='OTP',
                        message=f"Your techfest account OTP is {code}",
                        from_email="uaftab1010@gmail.com",
                        recipient_list=[request.data['email']],
                        fail_silently=False
                    )
                    person.otp=code
                    person.save()
                    return Response({'success':True,'message':f"An OTP has been sent to {request.data['email']}",'email':request.data['email']})
                except Exception:
                    return Response({'success':False,"message": f"{request.data['email']} is not a valid email address!"})
            except techfest_participants.DoesNotExist:
                return Response({'success':False,'message':'Invalid Credentials'})
        
    else:
        print(list(techfest_participants.objects.filter(email=request.data['email'])))
        if(len(list(techfest_participants.objects.filter(email=request.data['email']))))!=0:
            return Response({"success": False,'message':'Email already taken.Choose Another!'})
        elif(len(list(techfest_participants.objects.filter(fullname=request.data['fullname']))))!=0:
            return Response({"success": False,'message':'Name already taken.Choose Another!'})
        else:
            code=randint(100000,999999)
            chars = string.ascii_letters + string.digits
            text=''
            for i in range(20):
                text+=secrets.choice(chars)
            try:
                send_mail(
                    subject='OTP',
                    message=f"Your techfest account OTP is {code}",
                    from_email="uaftab1010@gmail.com",
                    recipient_list=[request.data['email']],
                    fail_silently=False
                )
                person=techfest_participants.objects.create(email=request.data['email'],password=request.data['password'],fullname=request.data['fullname'],otp=code,token=text)
                return Response({'success':True,'message':f"An OTP has been sent to {request.data['email']}",'email':person.email})
            except Exception as e:
                return Response({'success':False,"message": f"{request.data['email']} is not a valid email address!"})
@csrf_exempt
@api_view(['POST'])
def verify_otp(request):
    try:
        print(request.data)
        person=techfest_participants.objects.get(email=request.data['email'])
        if(person.otp==request.data['otp']):
            return Response({"success": True,'token':person.token})
        else:
            return Response({"success": False,'message':"Invalid OTP/Ensure email address provided is valid"})
    except techfest_participants.DoesNotExist:
        return Response({"success": False,'InvalidToken':'Your email inside browser was changed/removed.Now Please log in to access your account'})
    
@csrf_exempt
@api_view(['POST'])
def my_registered_events(request):
    try:
        person=techfest_participants.objects.get(token=request.data['token'])
        print(person)
        return Response({'success':True,'events':person.events,'name':person.fullname})
    except techfest_participants.DoesNotExist:
        return Response({'success':False,'message':'Your token inside browser was changed/removed.Now Please log in to access your account'})

@csrf_exempt
@api_view(['POST'])
def remember_me(request):
    person=''
    through=''
    found=False
    try:
        person=techfest_participants.objects.get(email=request.data['email'])
        found=True
        through='email'
    except techfest_participants.DoesNotExist:
        try:
            person=techfest_participants.objects.get(token=request.data['token'])
            found=True
            through='token'
        except:
            pass
    if(found):
        return Response({'success':True,'email':person.email,'password':person.password,'message':f"An OTP has been sent to {person.email}",'through':through})
    else:
        return Response({'success':False,'message':'Your email/token inside browser was changed/removed.Now Please log in to access your account'})
def elara(request):
    return render(request, "elara.html")
def elara_info(request):
    return render(request, "elara_info.html")
@csrf_exempt
@api_view(['POST'])
def forgot_password(request):
    print(request)
    found=False
    need_auth=False
    try:
        person=techfest_participants.objects.get(token=request.data['token'])
        found=True
    except techfest_participants.DoesNotExist:
        try:
            person=techfest_participants.objects.get(email=request.data['email'])
            found=True
        except techfest_participants.DoesNotExist:
            pass
    if(found):
        if person.email==request.data['account_email']:
            need_auth=False
            return Response({'success':True,'password':person.password,'verified':True})
        else:
            try:
                person=techfest_participants.objects.get(email=request.data['account_email'])
                need_auth=True
            except techfest_participants.DoesNotExist:
                need_auth=True
    if(need_auth):
        try:
            person=techfest_participants.objects.get(email=request.data['account_email'])
            try:
                send_mail(
                    subject='OTP',
                    message=f"Your techfest account password is {person.password}",
                    from_email="uaftab1010@gmail.com",
                    recipient_list=[request.data['account_email']],
                    fail_silently=False
                )
                return Response({'success':True,'message':f"Account Password has been sent to {request.data['account_email']}"})
            except Exception:
                return Response({'success':False,"message": f"No account exists with {request.data['account_email']}"})
        except techfest_participants.DoesNotExist:
            return Response({'success':False,'message':f'No account exists with {request.data['account_email']}'})