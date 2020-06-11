import json
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from math import ceil
import datetime,pytz
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Contact,Orders,OrderUpdate,ShopReview,Cart
from nursery.models import Plant
from accounts.models import Account
from shop.templatetags import my_filters,convertInt,extras
from django.conf import settings
from django.contrib.auth.decorators import login_required
from ast import literal_eval
from nursery.models import Nursery

#setting user to our customized user
User = settings.AUTH_USER_MODEL

@login_required(login_url='/')
def index(request):
    allProds = []
    catprod = Plant.objects.values('plantNursery','id')
    cats = {item['plantNursery'] for item in catprod}
    for cat in cats:
        prod = Plant.objects.filter(plantNursery=cat)
        n = len(prod)
        nSlides = (n // 4) + ceil((n / 4) - (n // 4))
        allProds.append([prod,range(1,nSlides),nSlides])
    if request.user.is_authenticated:
        user = request.user
        get_cart = Cart.objects.filter(user=user)[0]
        mn = "{}".format(get_cart.cart)
        params = {'allProds':allProds,'carty':mn}
    else:
        params = {'allProds':allProds}
    return render(request,'shop/index.html',params)

#search test one
def searchMatch1(query,item):
    if query in item.plantDesc.lower() or query in item.plantName.lower() or query in item.plantNursery.lower():
        return True
    else:
        return False

#search test two
def searchMatch2(query,item):
    if len(query.split())>1:
        for i in query.split():
            if i in item.plantDesc.lower() or i in item.plantName.lower() or i in item.plantNursery.lower():
                return True
    else:
        return False

@login_required(login_url='/')
def search(request):
    query =request.GET.get('search')
    allProds = []
    catprod = Plant.objects.values('plantNursery','id')
    cats = {item['plantNursery'] for item in catprod}
    for cat in cats:
        prodtemp = Plant.objects.filter(plantNursery=cat)
        prod = [item for item in prodtemp if searchMatch1(query.lower(),item)]
        if len(prod)<2:
            prod = prod + [item for item in prodtemp if searchMatch2(query.lower(), item)]
        n = len(prod)
        nSlides = (n // 4) + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod,range(1,nSlides),nSlides])
    
    #Sending he cart associated with the user
    user = request.user
    get_cart = Cart.objects.filter(user=user)[0]
    mn = "{}".format(get_cart.cart)
    params = {'allProds':allProds,'msg':"",'query':query,'carty':mn}
    if len(allProds)==0 or len(query)<2:
        params = {'msg': "Please enter relevant query!"}
    return render(request,'shop/search.html',params)

@login_required(login_url='/')
def about(request):
    return render(request,'shop/about.html')

@login_required(login_url='/')
def contact(request):
    if request.method=="POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html',{'thank':thank})
    return render(request, 'shop/contact.html')

@login_required(login_url='/')
def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId','')
        email = request.POST.get('email','')
        try:
            order = Orders.objects.filter(order_id = orderId,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'date':item.timestamp,"time":item.timestamp1})
                    response = json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception:
            return HttpResponse('{"status":"error"}')

    #orders that the user has placed
    orders = Orders.objects.filter(user=request.user)
    return render(request,'shop/tracker.html',{'orders':orders})

@login_required(login_url='/')
def productview(request,myid):
    #Fetch the product using id
    product = Plant.objects.filter(id=myid)[0]
    reviews = ShopReview.objects.filter(product=product,parent=None)
    replies = ShopReview.objects.filter(product=product).exclude(parent=None)
    repDict = {}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)
    product_all = Plant.objects.all()
    return render(request, 'shop/prodView.html',{'product':product,'product_all':product_all,'reviews':reviews,'replyDict':repDict})

@login_required(login_url='/')
def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('firstName','')+" "+request.POST.get('lastName','')
        amount = request.POST.get('amount','')
        email = request.POST.get('email','')
        address = request.POST.get('address1','')+" "+request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')
        nurseries = request.POST.get('nurseries','')
        x = list(map(str, nurseries.strip()[1:-1].split(',')))
        y = set(x)

        #save the order
        order = Orders(user=request.user,items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone,amount=amount)
        order.save()

        #add the nurseries associated with the order in m2m field
        for i in y:
            q = i[1:len(i)-1]
            order.nurseries.add(Nursery.objects.filter(name=q)[0])
            
        thank = True

        #get the current time
        now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        timex = now.strftime("%H:%M:%S")

        #pass the default update
        update = OrderUpdate(order_id=order.order_id,update_desc="The order has been placed",timestamp1=timex)
        update.save()

        id = order.order_id
        return render(request, 'shop/checkout.html',{'thank':thank,'id':id})
    return render(request, 'shop/checkout.html')

@login_required(login_url='/')
def cart(request):
    return render(request,'shop/cart.html')


def handleLogout(request):
    logout(request)
    messages.success(request,'Successfully logged out')
    return redirect('/')

@login_required(login_url='/')
def postReview(request):
    if request.method == "POST":
        review = request.POST.get("review")
        user = request.user
        productSno = request.POST.get("productSno")
        product = Plant.objects.filter(id=productSno)[0]
        parentSno = request.POST.get("parentSno")
        rating = request.POST.get("rating-value")
        #If it a review 
        if parentSno=="":
            review = ShopReview(review=review,user=user,product=product,rating=rating)
            review.save()
            messages.success(request,"Your comment has been posted successfully!")
        #if it is a reply
        else:
            parent = ShopReview.objects.filter(sno=parentSno)[0]
            comment = ShopReview(review=review,user=user,product=product,parent=parent)
            comment.save()
            messages.success(request,"Your Reply has been posted successfully!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    else:
        return HttpResponse('404 - Error Found')

@login_required(login_url='/')    
def update_cart(request):
    #dynamically updating the cart using ajax request
    user = request.user
    new_cart = request.GET.get('cart',None)
    get_cart = Cart.objects.filter(user=user)[0]
    get_cart.cart = new_cart
    get_cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))