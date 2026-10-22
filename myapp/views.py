from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,decorators,authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from holidays import country_holidays
from .forms import *
from .models import *
# Create your views here.

# resister view
def register(request):
    
    if request.method == "POST":
        email=request.POST.get("email")
        existUser=User.objects.filter(email=email)
        
        if existUser.exists():
            messages.error(request, "User already exists!")
            return redirect("/register/")
        
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user_id=user,
                phone=request.POST.get("phone"),
                profile_image=request.FILES.get("profile_image"),
                age=request.POST.get("age"),
                gender=request.POST.get("gender"),
                
            )
            # Send welcome email
            send_mail(
                subject="Welcome to Game Booking!",
                message=f"""
                    Hi {user.username},

                    Welcome to our Game Booking website!

                    Your registration was successful.
                    Now you can explore games and book your favourite activities.

                    Thank you for joining us!

                    Regards,
                    Game Booking Team
                                    """,
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False
            )
            
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})


# login view
def login_view(request):
    if request.method=="POST":
        
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("/dashboard/")
        else:
            messages.error(request, "Invalid username or password!")
        
    return render(request, "login.html", )

# layout view
def layout_view(request):
    user=request.user
    
    profile=Profile.objects.filter(user_id=user).first()
    

    context = {
            "user": user,
            "profile": profile,
        }
    return render(request,"layout.html",context)

# dashboard view
@decorators.login_required(login_url="login")
def dashboard_view(request):
    
    # Currently logged-in user
    user = request.user
    
    # print(user)
    
    profile = Profile.objects.filter(user_id=user).first()
    
    context = {
        "user": user,
        "profile": profile,
    }

    return render(request, "dashboard.html", context)


@decorators.login_required(login_url="login")
@require_GET
def dashboard_holidays(request):
    year_value = request.GET.get("year", "")
    try:
        year = int(year_value)
    except ValueError:
        return JsonResponse({"error": "A valid calendar year is required."}, status=400)

    if not 2001 <= year <= 2035:
        return JsonResponse(
            {"error": "Festival data is available for years 2001 through 2035."},
            status=400,
        )

    holidays = country_holidays("IN", years=[year])
    return JsonResponse({
        "year": year,
        "holidays": {
            holiday_date.isoformat(): name
            for holiday_date, name in sorted(holidays.items())
            if holiday_date.year == year
        },
    })

