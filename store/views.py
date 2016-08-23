from django.shortcuts import render,HttpResponse
import json
import warnings
from django.contrib.auth.decorators import login_required
from django.db import connection
# Create your views here.



@login_required
def redrawArea(request):
    temp=request.GET
    not_found=1
    context={}
    cursor = connection.cursor()
    current_user=request.user
    if len(temp)==0:
        print "first tym"
        cursor.execute("SELECT area_name FROM test_vodafone.area_geoJson where user_name=%s",[current_user])
        area_list_temp=cursor.fetchall()
        area_list=[]
        for i in area_list_temp:
            area_list.append(i[0])
        context["area_list"]=area_list

    else:
        area_name=temp.getlist("area_name")[0]
        print area_name

        if(cursor.execute("SELECT area_name,geoJson_data FROM test_vodafone.area_geoJson where area_name=%s and user_name=%s",[area_name,current_user])):
            not_found=0
            data=cursor.fetchone()
            context["area_name"]=data[0]
            context["Geo_Json"]=data[1]
            context["not_found"]=not_found
            return HttpResponse(json.dumps(context),content_type="application/json")
        else:
            not_found=1
            context["not_found"]=not_found
            print context
            return HttpResponse(json.dumps(context),content_type="application/json")

    return render(request,'store/drawmap.html',context)

@login_required
def storeArea(request):
    temp=request.GET
    if(len(temp)==0):
        print "First tym"

    else:
        data= temp.getlist("GeoJson_data")[0]
        addr=temp.getlist("area_name")[0]
        current_user=request.user
        cursor = connection.cursor()
        cursor.execute("insert into area_geoJson values(%s,%s,%s)",[addr,data,current_user])


    return render(request,'store/index.html',{})
