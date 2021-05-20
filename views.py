from django.shortcuts import render
import json
from decimal import Decimal
from django import forms
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.urls.conf import include
from django.views.decorators.csrf import csrf_exempt
from .models import User, Code, Language, Color, Item, Price, MemberPrice, Bill, Billlist, Head, Channel, Order, Orderlist

@csrf_exempt
@login_required
def page(request):

    data = json.loads(request.body)
    searchword = data.get("searchword", "")
    searchby = data.get("searchby", "")
    page = data.get("page", "")

    if searchby == "Code":
        allcode = Code.objects.all()
        codelist = [c.code for c in allcode]
        result = [s for s in codelist if searchword.casefold() in s.casefold()]
        thiscode = Code.objects.filter(code__in=result)
        aitems = Item.objects.filter(code__in=thiscode).order_by('code','color')

    elif searchby == "Name":
        allname = Code.objects.all()
        namelisten = [c.nameen for c in allname]
        namelistth = [c.nameth for c in allname]
        namelist = namelisten + namelistth
        print(namelist)
        result = [s for s in namelist if searchword.casefold() in s.casefold()]
        thiscode = Code.objects.filter(nameen__in=result) | Code.objects.filter(nameth__in=result)
        aitems = Item.objects.filter(code__in=thiscode).order_by('code','color')

    else:
        aitems = Item.objects.all().order_by('code','color')


    try:
        paginator = Paginator(aitems, 10)
        totalpages = int(paginator.num_pages)
        page_number = page

        context = {
            'pagenum': page_number,
            'plen': totalpages
        }
    except User.DoesNotExist:
        return render(request, "network/login.html", {
                "message": "Log in required."
            })
    return JsonResponse(context, status=201)


# done
def index(request):
    if request.user.is_authenticated:
        return render(request, "en/index.html")

    else:
        return render(request, "en/login.html")



# done
@csrf_exempt
@login_required
def add(request):
    return render(request, "en/add.html")

# done
@csrf_exempt
@login_required
def addproduct(request):

    if request.method != "POST":
        return JsonResponse({"error": "PUT request required."}, status=400)

    try:

        data = json.loads(request.body)
        print(data)
        acode = data.get("acode","")
        anameth = data.get("anameth","")
        anameen = data.get("anameen","")
        anote = data.get("anote","")
        aurl = data.get("aurl","")
        izero = int("0")
        goldshop = data.get("agoldshop",izero)
        agoldshop = goldshop if goldshop else izero
        goldfactory = data.get("agoldfactory",izero)
        agoldfactory = goldfactory if goldfactory else izero
        blackshop = data.get("ablackshop",izero)
        ablackshop = blackshop if blackshop else izero
        blackfactory = data.get("ablackfactory",izero)
        ablackfactory = blackfactory if blackfactory else izero
        greenshop = data.get("agreenshop",izero)
        agreenshop = greenshop if greenshop else izero
        greenfactory = data.get("agreenfactory",izero)
        agreenfactory = greenfactory if greenfactory else izero
        othershop = data.get("aothershop",izero)
        aothershop = othershop if othershop else izero
        otherfactory = data.get("aotherfactory",izero)
        aotherfactory = otherfactory if otherfactory else izero
        dzero = Decimal(0)
        sizew = data.get("asizew", dzero)
        asizew = sizew if sizew else dzero
        sizel = data.get("asizel", dzero)
        asizel = sizel if sizel else dzero
        sizeh = data.get("asizeh", dzero)
        asizeh = sizeh if sizeh else dzero
        weight = data.get("aweight", dzero)
        aweight = weight if weight else dzero

        createcode = Code(code=acode, nameth=anameth, nameen=anameen, 
            sizew=asizew, sizel=asizel, sizeh=asizeh, weight=aweight, note=anote, url=aurl )
        createcode.save() 

        colorgold = Color.objects.get(colorid='1')
        creategold = Item(code=createcode, color=colorgold, shop=agoldshop, factory=agoldfactory)
        creategold.save()

        colorblack = Color.objects.get(colorid='2')
        createblack = Item(code=createcode, color=colorblack, shop=ablackshop, factory=ablackfactory)
        createblack.save()

        colorgreen = Color.objects.get(colorid='3')
        creategreen = Item(code=createcode, color=colorgreen, shop=agreenshop, factory=agreenfactory)
        creategreen.save()

        colorother = Color.objects.get(colorid='4')
        createother = Item(code=createcode, color=colorother, shop=aothershop, factory=aotherfactory)
        createother.save()

        return JsonResponse({"message": "add successfully."}, status=201)
    
    except:
        return JsonResponse({"error": "Not successful, please try again or contact admin"}, status=201)



# done
def product(request, askcode):
    thiscode = Code.objects.filter(code=askcode)
    if thiscode :
        pitem = Item.objects.filter(code__in=thiscode).first
        items = Item.objects.filter(code__in=thiscode).order_by('code','color')
        return render(request, "en/product/CODE.html", {           
            "title": "found",
            "items": items,
            "pitem": pitem

        })
    else:
        return render(request, "en/product/CODE.html", {
            "title": "Not found",
            })


@csrf_exempt
@login_required
def stock(request):

    if request.method == "POST":

        data = json.loads(request.body)
        print(data)
        searchword = data['searchword']
        searchby = data['searchby']
        thiscode = Code.objects.filter(code=searchword)
        items = Item.objects.filter(code__in=thiscode).order_by('code','color')
    
    else:

        items = Item.objects.all().order_by('code','color')

    paginator = Paginator(items, 10)
    
    totalpages = int(paginator.num_pages)
    page_number = request.GET.get('page', 1)
    page = int(page_number)
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.page(1)

    context = {'items': page_obj,
        'page': page,
        'loops': range(1, totalpages + 1)
    }

    return render(request, "en/stock.html", context)


@csrf_exempt
def stockkey(request):

    try:
        data = json.loads(request.body)
        searchword = data.get("searchword", "")
        searchby = data.get("searchby", "")
        page = data.get("page", "")

        if searchby == "Code":
            allcode = Code.objects.all()
            codelist = [c.code for c in allcode]
            result = [s for s in codelist if searchword.casefold() in s.casefold()]
            thiscode = Code.objects.filter(code__in=result)
            aitems = Item.objects.filter(code__in=thiscode).order_by('code','color')

        elif searchby == "Name":
            allname = Code.objects.all()
            namelisten = [c.nameen for c in allname]
            namelistth = [c.nameth for c in allname]
            namelist = namelisten + namelistth
            print(namelist)
            result = [s for s in namelist if searchword.casefold() in s.casefold()]
            thiscode = Code.objects.filter(nameen__in=result) | Code.objects.filter(nameth__in=result)
            aitems = Item.objects.filter(code__in=thiscode).order_by('code','color')

        else:
            aitems = Item.objects.all().order_by('code','color')

        pcount = len(aitems)
        paginator = Paginator(aitems, 10)
        totalpages = int(paginator.num_pages)
        page_number = page
        try:
            items = paginator.get_page(page_number)
        except EmptyPage:
            items = paginator.page(1)
        return JsonResponse([item.serialize() for item in items], safe=False)

    except:
        return JsonResponse({"error": "Could not find the product, please try again."}, status=201)





def index2(request, langs):
    if langs == "en":
        return render(request, "en/index.html")
    
    if langs == "th":
        return render(request, "th/index.html")

    else:
        return render(request, "en/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "en/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "en/login.html")


def logout_view(request):
    logout(request)
    return render(request, "en/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "en/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "en/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "en/register.html")
