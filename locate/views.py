from django.shortcuts import render,render_to_response,redirect,HttpResponseRedirect
from .forms import *
import urllib2
import json
import warnings
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext



# Create your views here.


@login_required
def home(request):
    return render(request,'locate/home.html',{})

@login_required
def locateMobile(request):
    print "checking"
    if request.method=="POST":
        form=detailsForm(request.POST)
        if form.is_valid():
            phoneNumber=request.POST.get('phoneNumber')
            phoneNumber_arr=phoneNumber.split(",")

            for i in range(len(phoneNumber_arr)):
                if phoneNumber_arr[i][0]=="+":
                    temp=phoneNumber_arr[i]
                    phoneNumber_arr[i]=temp[1:]
                else:
                    temp=phoneNumber_arr[i]
                    phoneNumber_arr[i]="91"+temp

            temp_address=""
            for i in phoneNumber_arr:
                temp_address=temp_address+"address=tel%3A%2B"+i+"&"
            url="https://partner.vodafone.in/services2/locationsandbox/2_0/location/queries/location?"+temp_address+"requestedAccuracy=100"

            username = 'f22cc3003769f2b964f8c6f594afe4a0'
            password='y2{Br*{H'
            #auth_encoded = base64.encodestring('%s:%s' % (username, password))[:-1]
            p = urllib2.HTTPPasswordMgrWithDefaultRealm()
            p.add_password(None, url, username, password)
            handler = urllib2.HTTPBasicAuthHandler(p)
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)
            page = urllib2.urlopen(url).read()
            data = json.loads(page)
            temp_data=data["terminalLocationList"]["terminalLocation"]
            locations={}
            context={}
            not_found=[]
            print temp_data,type(temp_data)
            for i in range(len(temp_data)):
                if temp_data[i]["locationRetrievalStatus"]=="Retrieved":
                    tempLoc=[]
                    tempLoc.append(temp_data[i]["currentLocation"]["latitude"])
                    tempLoc.append(temp_data[i]["currentLocation"]["longitude"])
                    locations[temp_data[i]["address"]]=tempLoc
                else:
                    print "Error"
            context['locations']=locations
            context['not_found']=not_found
            request.session['_context']=context
            return redirect('info_page')
        else:
            print "error in form"
    else:
        form=detailsForm()

    return render(request,'locate/mainPage.html',{'form':form})

@login_required
def infoPage(request):
    context=request.session['_context']
    myCenter=[]
    if context['locations']:
        myCenter=context['locations'].itervalues().next()
    context['myCenter']=myCenter
    print "in info page"
    print context
    print json.dumps(context['locations'])
    return render(request,'locate/infoPage.html',context)


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })

    return render_to_response(
    'registration/register.html',
    variables,
    )