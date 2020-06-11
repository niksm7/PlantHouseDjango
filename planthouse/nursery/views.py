from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from nursery.forms import ProductForm
from .models import Plant
from django.contrib.auth.decorators import login_required
from shop.models import Orders,OrderUpdate
from .models import Nursery
import json
import datetime,pytz
from django.contrib import messages

@login_required(login_url='/')
def index(request):
    if not(request.user.is_nurseryManager):
        return redirect('/shop')
    thisNursery = Plant.objects.filter(plantNursery=request.user.nursery_name)
    params = {'plants':thisNursery}
    return render(request,'nursery/index.html',params)

@login_required(login_url='/')
def addItem(request):
    if not(request.user.is_nurseryManager):
        return redirect('/shop')
    form = ProductForm()
    return render(request,'nursery/addItem.html',{'form':form})

@login_required(login_url='/')
def saveItem(request):
    if not(request.user.is_nurseryManager):
        return redirect('/shop')

    if request.method == "POST": 
        form = ProductForm(request.POST, request.FILES) 
        if form.is_valid(): 
            name = form.cleaned_data.get("plantName") 
            price = form.cleaned_data.get("plantPrice")
            img = form.cleaned_data.get("plantImage") 
            desc = form.cleaned_data.get("plantDesc")
            nurseryname = request.user.nursery_name
            obj = Plant.objects.create(plantName=name,plantPrice=price,plantImage=img,plantDesc=desc,plantNursery=nurseryname) 
            obj.save()
            messages.success(request,"YOUR PRODUCT HAS BEEN ADDED")
        else: 
            raise Http404
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@login_required(login_url='/')
def manageOrders(request):
    if not(request.user.is_nurseryManager):
        return redirect('/shop')
    
    #filter orders belonging to the nursery
    allOrders = Orders.objects.filter(nurseries=Nursery.objects.filter(name=request.user.nursery_name)[0])

    lst = []
    
    #Filter the products of the orders belonging to the nursery because an order can contain products of multiple nurseries.

    for order in allOrders:
        x = json.loads(order.items_json)
        for key,value in x.items():
            if value[-1] == request.user.nursery_name:
                lst.append([order.order_id,order.address,order.phone]+value+[value[0]*int(value[2])])
    return render(request,'nursery/manageOrders.html',{'allOrders':lst})

@login_required(login_url='/')
def saveUpdate(request,id):
    if not(request.user.is_nurseryManager):
        return redirect('/shop')
    if request.method == "POST":
        update = str(request.user.nursery_name)+" : "+str(request.POST.get("update"))
        now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        timex = now.strftime("%H:%M:%S")
        updated = OrderUpdate(order_id=id,update_desc=update,timestamp1=timex)
        updated.save()
        messages.success(request,"UPDATE PUSHED")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

