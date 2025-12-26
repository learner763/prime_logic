from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from random import *
from .models import *
from django.conf import settings
import os, time

def index(request):
    return redirect('prime_view')
def prime_add(request):
    return render(request,'prime_add.html')
def prime_edit(request):
    return render(request,'prime_edit.html')
def prime_view(request):
    return render(request,'prime_view.html')
@api_view(['POST'])
def add_contractor(request):
    if(request.data['edit'])==False:
        if(len(list(personal_info.objects.filter(email=request.data['email']))))>0:
            return Response({'success':False,'message':'Contractor with this email already exists'})
        elif len(list(personal_info.objects.filter(fullname=request.data['fullname'])))>0:
            return Response({'success':False,'message':'Contractor with this name already exists'})
        else:
            person=personal_info.objects.create(status=request.data['status'],email=request.data['email'],fullname=request.data['fullname'],phone=request.data['phone'],businessname=request.data['businessname'],password=request.data['password'],date=request.data['date'])
            person=location.objects.create(city=request.data['city'],area=request.data['area'],email=request.data['email'])
            person=services.objects.create(email=request.data['email'],services=request.data['services'])
            person=preferences.objects.create(email=request.data['email'],preferences=request.data['preferences'])
            return Response({'success':True})
    else:
        person=personal_info.objects.get(email=request.data['email'])
        person.fullname=request.data['fullname']
        person.phone=request.data['phone']
        person.businessname=request.data['businessname']
        person.password=request.data['password']
        person.status=request.data['status']
        person.save()
        person=location.objects.get(email=request.data['email'])
        person.city=request.data['city']
        person.area=request.data['area']
        person.save()
        person=services.objects.get(email=request.data['email'])
        person.services=request.data['services']
        person.save()
        person=preferences.objects.get(email=request.data['email'])
        person.preferences=request.data['preferences']
        person.save()
        return Response({'success':True})
    
@api_view(['GET'])
def all_contractors(request):
    overall_data=[]
    emails=list(personal_info.objects.values_list('email',flat=True))
    for email in emails:
        user_data={}
        person=personal_info.objects.get(email=email)
        user_data['email']=person.email
        user_data['fullname']=person.fullname
        user_data['phone']=person.phone
        user_data['businessname']=person.businessname
        user_data['date']=person.date
        user_data['password']=person.password
        user_data['img_liability']=person.img_liability
        user_data['img_tax']=person.img_tax
        user_data['img_workman']=person.img_workman
        user_data['status']=person.status
        person=location.objects.get(email=email)
        user_data['city']=person.city
        user_data['area']=person.area
        person=services.objects.get(email=email)
        user_data['services']=person.services
        person=preferences.objects.get(email=email)
        user_data['preferences']=person.preferences
        
        overall_data.append(user_data)
    return Response({'user_data':overall_data})
@api_view(['POST'])
def get_user(request):
    try:
        person=personal_info.objects.get(email=request.data['email'])
        person1=location.objects.get(email=request.data['email'])
        person2=services.objects.get(email=request.data['email'])
        person3=preferences.objects.get(email=request.data['email'])
        return Response({'success':True,'status':person.status,'email':person.email,'fullname':person.fullname,'phone':person.phone,'businessname':person.businessname,'date':person.date,'password':person.password,
                    'services':person2.services,'preferences':person3.preferences,'city':person1.city,'area':person1.area,
                    'img_tax':person.img_tax,'img_liability':person.img_liability,'img_workman':person.img_workman})
    except personal_info.DoesNotExist:
        return Response({'success':False})
    
@api_view(['POST'])
def delete_user(request):
    personal_info.objects.filter(email=request.data['email']).delete()
    location.objects.filter(email=request.data['email']).delete()
    preferences.objects.filter(email=request.data['email']).delete()
    services.objects.filter(email=request.data['email']).delete()
    return Response({'success':True})
@csrf_exempt
def upload_img(request):
    if request.method == 'POST' :
        image_workman = request.FILES['image_workman']
        image_tax = request.FILES['image_tax']
        image_liability=request.FILES['image_liability']
        image_array=[image_workman,image_tax,image_liability]

        # Optional: add timestamp to avoid duplicate names
        filename1 = f"{int(time.time())}_{image_workman.name}"
        filename2 = f"{int(time.time())}_{image_tax.name}"
        filename3 = f"{int(time.time())}_{image_liability.name}"
        filename_array=[filename1,filename2,filename3]
        for i in range(3):
        # Path in main/static
            save_path = os.path.join(settings.BASE_DIR, 'main', 'static', filename_array[i])

        # Save file
            with open(save_path, 'wb+') as f:
                for chunk in image_array[i].chunks():
                    f.write(chunk)

        # Return URL
        #url = f'/static/{filename}'
        person=personal_info.objects.get(email=request.POST['email'])
        person.img_liability=f"/static/{filename3}"
        person.img_tax=f"/static/{filename2}"
        person.img_workman=f"/static/{filename1}"
        person.save()
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'No image uploaded'}, status=400)
