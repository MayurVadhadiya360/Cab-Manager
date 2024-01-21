import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import UserRegistrationForm, UserLoginForm, RideBookingForm, DriverSignupForm
from .models import User, Driver, Ride, Feedback

admin_email = "" # Your admin mail
# Create your views here.
user_profile = {
    'user_logged_in': False,
    'driver_logged_in': False,
}


def index(request):
    return render(request, 'index.html')

def DriverLogin(request):
    return render(request, 'driver_login_signup.html')

def UserLogin(request):
    return render(request, 'user_login_signup.html')

def register_user(request):
    # if request.method == 'POST':
    #     form = UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('login_user')
    # else:
    #     form = UserRegistrationForm()
    # return render(request, 'register_user.html', {'form': form})
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        User.objects.create(username=username, email=email, password=password)
        send_mail(
            subject="Registration Done!",
            message="Congratulations for completing registration and joining as User!",
            from_email=admin_email,
            recipient_list=[email],
            fail_silently=True
        )
        try:
            user = User.objects.get(email=email, password=password)
        except Exception as e:
            print(e)
            user = False
        if user:
            user_profile['user_logged_in'] = True
            request.session['user'] = user.email
            return redirect('user_dashboard')
    return render(request, 'user_login_signup.html')


def login_user(request):
    # if request.method == 'POST':
    #     form = UserLoginForm(request.POST)
    #     if form.is_valid():
    #         # Implement user login logic (authenticate and login user)
    #         return redirect('dashboard')  # Replace 'dashboard' with your actual dashboard URL
    # else:
    #     form = UserLoginForm()
    # return render(request, 'login_user.html', {'form': form})
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try: 
            user = User.objects.get(email=email, password=password)
        except Exception as e:
            print(e)
            user = False
        if user:
            user_profile['user_logged_in'] = True
            request.session['user'] = user.email
            return redirect('user_dashboard')
    return render(request, 'user_login_signup.html')

def register_driver(request):
    # if request.method == 'POST':
    #     form = DriverSignupForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('driver_dashboard')  # Replace 'driver_dashboard' with your actual driver dashboard URL
    # else:
    #     form = DriverSignupForm()
    # return render(request, 'signup_driver.html', {'form': form})
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        license_number = request.POST.get('license_number')
        vehicle_model = request.POST.get('vehicle_model')

        Driver.objects.create(username=username, email=email, password=password, vehicle_model=vehicle_model, license_number=license_number)
        send_mail(
            subject="Registration Done!",
            message="Congratulations for completing registration and joining as Driver!",
            from_email=admin_email,
            recipient_list=[email],
            fail_silently=True
        )
        try:
            driver = Driver.objects.get(email=email, password=password)
        except Exception as e:
            print(e)
            driver = False
        if driver:
            user_profile['driver_logged_in'] = True
            request.session['driver'] = driver.email
            return redirect('driver_dashboard')
    return render(request, 'driver_login_signup.html')

def login_driver(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            driver = Driver.objects.get(email=email, password=password)
            driver.availability = True
            driver.save()
        except Exception as e:
            print(e)
            driver = False
        if driver:
            user_profile['driver_logged_in'] = True
            request.session['driver'] = driver.email
            return redirect('driver_dashboard')
    return render(request, 'driver_login_signup.html')

def driver_dashboard(request):
    # Implement logic to retrieve and display driver dashboard information
    if user_profile['driver_logged_in']:
        driveremail = request.session['driver']
        try:
            driver = Driver.objects.get(email=driveremail)
        except Exception as e:
            print(e)
            driver = False
        if driver:
            profile = {
                'username': driver.username,
                'email': driver.email,
                'rating': driver.overall_rating
            }
            if not driver.availability:
                try:
                    # ride = Ride.objects.filter(driver=driver, completed=False)
                    # ride.delete()
                    ride = Ride.objects.get(driver=driver, completed=False)

                    ride_detail = {
                        'pk': ride.pk,
                        'user': ride.user.username,
                        'driver': ride.driver.username,
                        'pickup_point': ride.pickup_point,
                        'dropoff_point': ride.dropoff_point,
                    }
                except Exception as e:
                    print(e)
                    ride_detail = {
                        "no_detail": True
                    }
            else:
                ride_detail = {
                    "no_detail": True
                }
            print(ride_detail)
            print(driver.availability)
            # available_cabs = Driver.objects.filter(availability=True)


            return render(request, 'driver_dashboard.html', {'profile':profile, 'ride_detail':ride_detail})
    return redirect('DriverLogin')

def user_dashboard(request):
    # Implement logic for admin dashboard
    # Ensure that only admin users have access to this view
    if user_profile['user_logged_in']:
        useremail = request.session['user']
        print(useremail)
        try:
            user = User.objects.get(email=useremail)
        except Exception as e:
            print(e)
            user = False
        if user:
            profile = {
                'username': user.username,
                'email': user.email
            }
            available_cabs = Driver.objects.filter(availability=True)

            return render(request, 'user_dashboard.html', {'profile':profile, 'available_cabs':available_cabs})
    return redirect('UserLogin')

def book_ride(request):
    # if request.method == 'POST':
    #     form = RideBookingForm(request.POST)
    #     if form.is_valid():
    #         # Implement ride booking logic
    #         return redirect('ride_history')  # Replace 'ride_history' with your actual ride history URL
    # else:
    #     form = RideBookingForm()
    # return render(request, 'book_ride.html', {'form': form})
    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        driver_ = request.POST.get('driver')
        license_number = request.POST.get('license_number')
        price = request.POST.get('price')
        print(license_number)

        if user_profile['user_logged_in']:
            usermail = request.session['user']
            user = User.objects.get(email=usermail)
            driver = Driver.objects.get(license_number=license_number)
            Ride.objects.create(
                user=user,
                driver=driver,
                pickup_point=source,
                dropoff_point=destination,
                price=price
            )
            driver.availability = False
            driver.save()

            send_mail(
                subject="Booking Done!",
                message=f"Ride Detail:\n Driver: {driver.username}\n pickup_point: {source}\n dropoff_point:{destination}\n Price:{price}",
                from_email=admin_email,
                recipient_list=[user.email],
                fail_silently=True
            )

            send_mail(
                subject="Your Ride is booked",
                message=f"{user.username} has booked your cab, Please check!",
                from_email=admin_email,
                recipient_list=[driver.email],
                fail_silently=True
            )
            return redirect('history')
        return redirect('user_dashboard')

def user_history(request):
    if user_profile['user_logged_in']:
        usermail = request.session['user']
        user = User.objects.get(email=usermail)
        rides = Ride.objects.filter(user=user)
        rids = []
        for ride in rides:
            temp = {
                'ride': ride
            }
            try:
                fdbk = Feedback.objects.get(ride=ride)
                fdbk = fdbk.rating
            except Feedback.DoesNotExist:
                fdbk = False
            # if fdbk is not None:
            temp['feedback'] = fdbk
            rids.append(temp)
        return render(request, 'user_history.html', {'rides': rids})
    return redirect('UserLogin')

def rate_ride(request):
    if request.method == "POST":
        try:
            pk = request.POST.get('pk')
            comment = request.POST.get('Comment')
            rating = int(request.POST.get('rating'))
            ride = Ride.objects.get(pk=pk)
            print("pk", pk)
            print("ride")
            Feedback.objects.create(
                ride = ride,
                rating = rating,
                comment = comment
            )
            ride.driver.total_feedbacks += 1
            ride.driver.overall_rating = (ride.driver.overall_rating * (ride.driver.total_feedbacks - 1) + rating) / ride.driver.total_feedbacks
            ride.driver.save()

        except Exception as e:
            print(e)
        return redirect('history')
        
def complete_ride(request):
    if request.method == 'POST':
        data = {
            'success': False
        }
        try:
            load_data = json.loads(request.body)
            pk = load_data['pk']
            ride = Ride.objects.get(pk=pk)
            ride.completed = True
            driver = Driver.objects.get(email=ride.driver.email)
            driver.availability = True
            send_mail(
                subject="Ride Completed!",
                message=f"Your ride from {ride.pickup_point} to {ride.dropoff_point} is Completed.\nPlease give feedback!",
                from_email=admin_email,
                recipient_list=[ride.user.email],
                fail_silently=True
            )
            ride.save()
            driver.save()
            data['success'] = True
        except Exception as e:
            print(e)
            data['success'] = False
        return JsonResponse(data)

def user_logout(request):
    if user_profile['user_logged_in']:
        user_profile['user_logged_in'] = False
        del request.session['user']
    return redirect('index')

def driver_logout(request):
    if user_profile['driver_logged_in']:
        user_profile['driver_logged_in'] = False
        driver = Driver.objects.get(email = request.session['driver'])
        driver.availability = False
        driver.save()
        del request.session['driver']
    return redirect('index')