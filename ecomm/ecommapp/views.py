from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from ecommapp.models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail
# from django import forms
# Create your views here.
def home(request):
    context={}
    context['name']="peter"
    context['age']=100
    context['x']=100
    context['y']=20
    context['l']=[10,20,30,40]
    context['products']=[
       {'id':1,'name':'samsung','cat':'mobile','price':20000},
       {'id':2,'name':'jeans','cat':'cloth','price':500},
       {'id':3,'name':'adidas shoes','cat':'shoes','price':3000},
       {'id':4,'name':'vivo','cat':'mobile','price':15000}
]
    if context['x'] >context['y']:
        #return HttpResponse("x is greater")
        context['res']="x is gretaer"
    else:
        #return HttpResponse("y is greater")
        context['res']="y is gretaer"
    #return HttpResponse("<i>This is home page</i>")
    return render(request,'hello.html',context)
def home2(request):
    # userid=request.user.id
    # print("id of logged in user:",userid)
    # print("result:",request.user.is_authenticated)
    context={}
    p=Product.objects.filter(is_active=True)
    print(p)
    print(p[0])
    print(p[0].price)
    print(p[0].cat)
    context['products']=p
    return render(request,'index.html',context)
def home3(request):
    context={}
    p=Product.objects.all()
    context['products']=p
    return render(request,'index.html',context)
def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1&q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)
def range(request):
    min=request.GET['min']
    max=request.GET['max']
    # print(min)
    # print(max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1&q2&q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)
def sort(request,sv):
    # print(type(sv))
    if sv=='0':
        col='price'
    else:
        col='-price'
    p=Product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)
def registration(request):
    context={}
    if request.method=='POST':
        uname=request.POST['uname'] 
        upass=request.POST['upass'] 
        ucpass=request.POST['ucpass'] 
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="field cannot be empty"
            return render(request,'registration.html',context)
        elif upass!=ucpass:
            context['errmsg']="password and confirm password did not match"
            return render(request,'registration.html',context)
        else:
            try:
                u=User.objects.create(username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="user created successfully"
                return render(request,'registration.html',context)
            except Exception:
                context['errmsg']="user with same username alerady exist"
                return render(request,'registration.html',context)
            #return HttpResponse("user created successfully")
    else:
        return render(request,'registration.html')
    #return render(request,'registration.html')
def dummyregistration(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
    return render(request,'dummyregistartion.html',{'form':form})
def login_user(request):
    context={}
    if request.method=='POST':
        uname=request.POST['uname'] 
        upass=request.POST['upass'] 
        if uname=="" or upass=="":
            context['errmsg']="field cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            # print(u)
            # print(u.email)
            # print(u.is_superuser)
            # return HttpResponse("in else part")
            if u is not None:
                login(request,u)#start session and store id of logged in user session
                return redirect('/home2')
            else:
                context['errmsg']="invalid username and password"
                return render(request,'login.html',context)
    return render(request,'login.html')
def user_logout(request):
    logout(request)
    # context={}
    # context['title1']="logout"
    #demo(request)
    #return render(request,'header.html',context)
    return redirect('/home2')
# def demo(request):
#     return redirect('/home2')
def product_detail(request,pid):
    context={}
    context['products']=Product.objects.filter(id=pid)
    return render(request,'product_detail.html',context)
def addtocart(request,pid):
    if request.user.is_authenticated:
        # print("user is logged")
        # return HttpResponse("user logged in")
        u=User.objects.filter(id=request.user.id)
        # print(u)
        # print(u[0])
        # print(u[0].username)
        # print(u[0].is_superuser)
        p=Product.objects.filter(id=pid)
        # print(p)#check product exist or not
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1&q2)
        print(c)
        n=len(c)
        print(n)
        context={}
        context['products']=p
        if n==1:
            context['msg']="product already exist!!"
        else:   
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="product added successfully to cart"
        return render(request,'product_detail.html',context)
    else:
        return redirect('/login')
def place_order(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    # print(c)
    oid=random.randrange(1000,9999)
    print("order id:",oid)
    for x in c:
        # print(x)
        # print(x.pid)
        # print(x.uid)
        # print(x.qty)
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    n=len(orders)
    for x in orders:
        s=s+x.pid.price*x.qty
    context={}
    context['products']=orders
    context['total']=s
    context['np']=n
    return render(request,'place_order.html',context)
def cart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    # print(c)
    # print(c[0])
    # print(c[1])
    # print(c[0].pid.name)
    # print(c[0].pid.price)
    n=len(c)
    s=0
    for x in c:
        #print(x)
        s=s+x.pid.price
    print(s)
    context={}
    context['np']=n
    context['total']=s
    context['products']=c
    return render(request,'cart.html',context)
def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')
def updateqty(request,qv,cid):
    # print(type(qv))
    # return HttpResponse("in update quantity")
    c=Cart.objects.filter(id=cid)
    s=0
    # print(c)
    # print(c[0].qty)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    for x in c:
        #print(x)
        s=s+x.pid.price*x.qty#s+800*5
    context={}
    # context['np']=n
    context['products']=c
    context['total']=s
    #return HttpResponse("in update quantity")
    #return redirect('/cart')
    return render(request,'cart.html',context)
def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_qPpA776V9DCblP", "TWcWQeLgGmHfG66yYcv7tzhJ"))
    data = { "amount": s*100, "currency": "MYR", "receipt": "oid" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    return render(request,'pay.html',context)
def sendusermail(request):
    uemail=request.user.email
    print(uemail)
    send_mail(
    "Ekart-Order placed successfuully",
    "Order details are:",
    "pooja.gada@itvedant.com",
    [uemail],
    fail_silently=False,
)
    return HttpResponse("mail is send successfully")
def about(request):
    #return HttpResponse("<h1>this is about page</h1>")
    return render(request,'about.html')
def contact(request):
    # return HttpResponse("this is contact page")
    return render(request,'contact.html')
def addition(request,a,b):
    print(type(a))
    res=int(a)+int(b)
    return HttpResponse(res)
#class based views
class SimpleView(View):
    def get(self,request):
        return HttpResponse("helo from simple view")