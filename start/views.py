from contextlib import nullcontext
from datetime import date, datetime
from functools import reduce
from logging.config import valid_ident
from multiprocessing import context
from time import time
from django.shortcuts import redirect, render,HttpResponse
import razorpay
from yoga import settings
from django.views.decorators.csrf import csrf_exempt 
from start.models import studentpaymentremaining,studentpaymentsdone
from django.contrib import messages
import re
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa




# Create your views here.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



def index(request):

        
        
    
    

    return render(request,'index.html')

def register(request):
    
  
    if request.method == "POST":
        name = request.POST.get('name')
        city = request.POST.get('city')
        number = request.POST.get('number')
        request.session['name'] = name
        request.session['city'] = city
        request.session['number'] = number
        
        
        
        if(name == ""):
            messages.add_message(request, messages.INFO, 'Plz Fill The Name Field')
        elif(city == ""):
            messages.add_message(request, messages.INFO, 'Plz Fill The City Field')
        elif(number == ""):
            messages.add_message(request, messages.INFO, 'Plz Fill The Number Field')
        elif(number):
            check10 = str(number)
            m = re.match(r'^\d{10}$', check10)
            if m:
                checkmob = studentpaymentsdone.objects.all()
                for checking in checkmob:
                    if(checking.number == number):
                        messages.add_message(request, messages.INFO, 'Number Already Exist Use Another One')
                        break
                else:
                    
                    info = studentpaymentremaining(name = name , city = city , number = number ,date = datetime.today())
                    info.save()
                    return redirect("/billing")
            else:
                messages.add_message(request, messages.INFO, "Number Must Be 10 digits")
       


           
            
            
            
        
    
    return render(request,'register.html')



def billing(request):

       

       
       
        
    
        currency = 'INR'
        amount = 100000  # Rs. 200

        name = request.session['name']
         
         

        city = request.session['city']
         
        number = request.session['number']
        paymentchecking = studentpaymentsdone.objects.all()
        for paymentcheck in paymentchecking:
                if(number == paymentcheck.number):
                    messages.add_message(request, messages.INFO, "Payment is Done")
                    return redirect("alreadydone") 
        else:

         


        
         
         

         
       
       
 
    # Create a Razorpay Order
         razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='1'))
 
    # order id of newly created order.
         razorpay_order_id = razorpay_order['id']
         context = {}
         context['razorpay_order_id'] = razorpay_order_id
         context['resname'] = name
         context['rescity'] = city
         context['resnumber'] = number
         return render(request, 'billing.html',context=context)


@csrf_exempt
def sucess(request):
    if request.method == "POST":
            
           
            # get the required parameters from post request.
            
            name = request.session['name']
         
         

            city = request.session['city']
         
            number = request.session['number']
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")


            


         
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            request.session['payid'] = payment_id
            request.session['orderid'] = razorpay_order_id
            request.session['signatureid'] = signature

            context = {
                'title' : 'Trasaction details',
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
                'resoname' : name,
                'resocity' : city,
                'resonumber' : number
            }
           
                                                                            


            
            paymentinfo = studentpaymentsdone(name = name ,city = city ,number = number , paymentstatus = "Online",paymentid = payment_id,orderid = razorpay_order_id,signature = signature,date = datetime.today(),time = current_time)
            paymentinfo.save()
            numberchecking = studentpaymentremaining.objects.all()
            for numbercheck in numberchecking:
                if(number == numbercheck.number):
                    numberchecking.delete()
            

            return render(request,'sucess.html',context)


def alreadydone(request):
    name = request.session['name']

         
         

    city = request.session['city']
         
    number = request.session['number']
    
    paymentcheckingg = studentpaymentsdone.objects.get(number = number)
    orderid = paymentcheckingg.orderid
    paymentid = paymentcheckingg.paymentid
    
   


    context  = {
        'resoiname':  name,
        'resoicity' : city,
        'resoinumber' : number,
        'razoorpay_order_id': orderid,
        'razoorpay_payment_id': paymentid

    }


    return render(request,'alreadydone.html',context=context)
            
def login_view(request):
         if request.method == "POST":
  
            username = request.POST['aduser']
            password = request.POST['adpass']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("admindashboard")
        # Redirect to a success page.
      
            else:
        # Return an 'invalid login' error message.
                return redirect("login_view")
        
         return render(request,'login_view.html')

def admindashboard(request):
    if request.user.is_anonymous:
        return redirect("login_view")
    
    sinfo = studentpaymentsdone.objects.all()
    return render(request,'admindashboard.html',{'sinf' : sinfo})

def logoutuser(request):
    logout(request)
    return redirect("/")
         

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def billtemplate(request):
      name = request.session['name']

         
         

      city = request.session['city']
         
      number = request.session['number']
    
      paymentcheckingg = studentpaymentsdone.objects.get(number = number)
      orderid = paymentcheckingg.orderid
      paymentid = paymentcheckingg.paymentid
      date = paymentcheckingg.date
      time = paymentcheckingg.time
      signature = paymentcheckingg.signature
      mode = paymentcheckingg.paymentstatus
    
   


      context  = {
        'resoiname':  name,
        'resoicity' : city,
        'resoinumber' : number,
        'razoorpay_order_id': orderid,
        'razoorpay_payment_id': paymentid,
        'date' : date,
        'time' : time,
        'signature' : signature,
        'mode' :mode

        }
      pdf = render_to_pdf('billtemplate.html',context)
      if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(context['razoorpay_order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
      return HttpResponse("Not found")

      