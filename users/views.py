from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
# import webbrowser
from django.contrib.auth.decorators import login_required
from .models import Profile, Incident
from datetime import datetime


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = str(form.cleaned_data.get('email'))
            password1 = str(form.cleaned_data.get('password1'))
            password2 = str(form.cleaned_data.get('password2'))
            username = str(form.cleaned_data.get('username'))
            print(username)
            first_name = str(form.cleaned_data.get('first_name'))
            print(first_name)
            last_name = str(form.cleaned_data.get('last_name'))
            print(last_name)
            print(email)
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.warning("username already taken")
                elif User.objects.filter(email=email).exists():
                    messages.warning("email is already taken")

            form.save()
            # user=User(username=username,first_name=first_name,last_name=last_name,email=email,password1=password1,password2=password2)
            # filter_Student = Student.objects.filter(StudentUserName=username, StudentFirstName=first_name, StudentLastName=last_name, StudentEmail=email)
            # print(filter_Student[0])

            userObj = User.objects.filter(username=username)
            # print(user.BirthDate)
            profile = Profile(user=userObj[0], Username=username,
                              UserFirstName=first_name, UserLastName=last_name, UserEmail=email)
            print(profile)
            profile.save()
            usr = User.objects.get(username=username)
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            messages.success(request, 'Your form is not valid register again')
            form = UserRegisterForm()
            return render(request, 'app/signup.html', {'form': form})

    else:
        form = UserRegisterForm()
        return render(request, 'app/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,
                            password=password)  # None
        if user is not None:
            messages.warning(request, 'Success: you are now logged in.')
            login(request, user)
            print("success")
            return redirect('home')
        elif User.objects.filter(username=username).exists():
            if password != User.objects.filter(password=password).exists():
                print('enter')
                messages.warning(request, f'Please enter a correct password.')
                return render(request, 'app/login.html', {'msg': 'Please enter a correct username and password. Note that both fields may be case-sensitive.'})
        elif not User.objects.filter(username=username).exists():
            messages.warning(request, 'User does not exist')
            return render(request, 'app/login.html', {'msg': 'User does not exist'})
        else:
            messages.info(request, 'invalid credentials')
            return render(request, 'app/login.html', {'msg': 'invalid credentials'})
    else:
        return render(request, 'app/login.html', {'msg': ''})


@login_required
def reportIncident(request):
    if request.method == "POST":
        username = request.user
        print(username)
        userObj = User.objects.filter(username=username)
        location = request.POST['Location']
        print(location)
        if location == "CH":
            location = "CH"
        if location == "OD":
            location = "OD"
        if location == "WS":
            location = "WS"
        if location == "MD":
            location = "MD"

        incidentDescription = request.POST['IncidentDescription']
        dateOfIncident = request.POST['DateOfIncident']
        print(dateOfIncident)
        f = "%Y-%m-%d"
        incident_date = datetime.strptime(dateOfIncident, f)
        print(incident_date)
        print(type(incident_date))
        timeOfIncident = request.POST['TimeOfIncident']
        timeOfIncident1 = timeOfIncident+':00'
        f = "%H:%M:%S"
        incident_time = datetime.strptime(timeOfIncident1, f)
        print(incident_time)
        print(type(incident_time))
        dateTimeOfIncident = dateOfIncident+'T'+timeOfIncident+':00.000Z'
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        out = datetime.strptime(dateTimeOfIncident, f)
        #my_date = datetime.strptime(dateTimeOfIncident, "%Y-%m-%d")
        print(out)
        print(type(out))
        # print(out.year)
        # print(out.hour)
        # print(out.minute)
        incidentLocation = request.POST['IncidentLocation']
        initialSeverity = request.POST['InitialSeverity']
        suspectedCause = request.POST['SuspectedCause']
        immediateActionsTaken = request.POST['ImmediateActionsTaken']
        subIncidentTypes = request.POST.get('SubIncidentTypes')
        print(subIncidentTypes)
        types = subIncidentTypes.split(',')
        print(len(types))
        type_env = False
        type_injury = False
        type_property = False
        type_vehicle = False

        if types[0] == 'EnvironmentalIncident' or types[1] == 'EnvironmentalIncident' or types[2] == 'EnvironmentalIncident' or types[3] == 'EnvironmentalIncident':
            type_env = True
        if types[0] == 'Injury/illness' or types[1] == 'Injury/illness' or types[2] == 'Injury/illness' or types[3] == 'Injury/illness':
            type_injury = True
        if types[0] == 'PropertyDamage' or types[1] == 'PropertyDamage' or types[2] == 'PropertyDamage' or types[3] == 'PropertyDamage':
            type_property = True
        if types[0] == 'Vehicle' or types[1] == 'Vehicle' or types[2] == 'Vehicle' or types[3] == 'Vehicle':
            type_vehicle = True

        reportedBy = request.POST['ReportedBy']
        incident = Incident(location=location, description=incidentDescription, incident_date=out, incident_time=timeOfIncident, incident_location=incidentLocation, severity=initialSeverity,
                            cause=suspectedCause, actions=immediateActionsTaken, type_env=type_env, type_injury=type_injury, type_property=type_property, type_vehicle=type_vehicle, submitted=False, reported_by=userObj[0])
        incident.save()
        messages.info(request, 'your Incident successfully saved')

    return render(request, 'app/reportIncident.html')


@login_required
def savedIncidents(request):
    if request.method=="POST":
        username = request.user
        print(username)
        userObj = User.objects.filter(username=username)
        incidents = Incident.objects.filter(submitted=False,reported_by_id=userObj[0])
        for incident in incidents:
            print(incident)
            incident.submitted=True
            #incid=Incident(location=incident.location,description=incident.description,incident_time=incident.incident_time,incident_date=incident.incident_date,incident_location=incident.incident_location,severity=incident.severity,cause=incident.cause,actions=incident.actions,type_env=incident.type_env,type_injury=incident.type_injury,type_property=incident.type_property,type_vehicle=incident.type_vehicle,submitted=True,reported_by_id=userObj[0])
            incident.save()
        return redirect('home')
    else:
        username = request.user
        print(username)
        userObj = User.objects.filter(username=username)
        incidents = Incident.objects.filter(reported_by_id=userObj[0], submitted=False)
        if (len(incidents)>0):
            print(incidents[len(incidents)-1].incident_date)
            print(type(incidents[len(incidents)-1].incident_date))
            print(incidents[len(incidents)-1].incident_time)
            print(type(incidents[len(incidents)-1].incident_time))
            months = []
            years = []
            days = []
            for incident in incidents:
                incident.year = str(incident.incident_date).split('-')[0]
                years.append(str(incident.incident_date).split('-')[0])
                incident.month = str(incident.incident_date).split('-')[1]
                months.append(str(incident.incident_date).split('-')[1])
                incident.day = str(incident.incident_date).split('-')[2]
                days.append(str(incident.incident_date).split('-')[2])
                print(str(incident.incident_date).split('-')[2])
                print(str(incident.incident_date).split('-')[1])
                print(str(incident.incident_date).split('-')[0])
                return render(request, 'app/savedIncidents.html', {'incidents': incidents, 'days': days, 'months': months, 'years': years})
        messages.info(request,'you do not have any saved incident.')
        return render(request, 'app/savedIncidents.html')


@login_required
def submitIncident(request):
    pass

@login_required
def sentIncidents(request):
    username = request.user
    print(username)
    userObj = User.objects.filter(username=username)
    incidents = Incident.objects.filter(reported_by_id=userObj[0], submitted=True)
    if (len(incidents)>0):
        print(incidents[len(incidents)-1].incident_date)
        print(type(incidents[len(incidents)-1].incident_date))
        print(incidents[len(incidents)-1].incident_time)
        print(type(incidents[len(incidents)-1].incident_time))
        months = []
        years = []
        days = []
        for incident in incidents:
            incident.year = str(incident.incident_date).split('-')[0]
            years.append(str(incident.incident_date).split('-')[0])
            incident.month = str(incident.incident_date).split('-')[1]
            months.append(str(incident.incident_date).split('-')[1])
            incident.day = str(incident.incident_date).split('-')[2]
            days.append(str(incident.incident_date).split('-')[2])
            print(str(incident.incident_date).split('-')[2])
            print(str(incident.incident_date).split('-')[1])
            print(str(incident.incident_date).split('-')[0])
        return render(request, 'app/sentIncidents.html', {'incidents': incidents, 'days': days, 'months': months, 'years': years})
    messages.info(request,'you do not have any saved incident.')
    return render(request, 'app/sentIncidents.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        # which is uploaded bu user from his/her p.c.'s location
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        Cuser = request.user

        context = {
            'u_form': u_form,
            'p_form': p_form,
        }
        return render(request, 'app/profile.html', context)
