from django.shortcuts import render, HttpResponse, redirect
from .models import User, Poke
from django.contrib import messages
import bcrypt


def index(request):
    if request.method == 'POST':
        errors = User.objects.validate_registration(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/main')
        else:
            found_users = User.objects.filter(email=request.POST['email'])
            if found_users.count() > 0:
                messages.error(request, "Sorry, this email had previously registered.", extra_tags="email")
                return redirect('/main')
            else:
                hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                created_user = User.objects.create(firstName=request.POST['firstName'], lastName=request.POST['lastName'], username=request.POST['username'], email=request.POST['email'], password=hashed_pw)
                request.session['user_id'] = created_user.id
                request.session['user_name'] = created_user.firstName
                return redirect('/pokes')
    return render(request, "pokes/index.html")
    
def login(request):
    if request.method == 'POST':
        found_users = User.objects.filter(email=request.POST['email'])
        if found_users.count > 0:
            found_user = found_users.first()
            if bcrypt.checkpw(request.POST['password'].encode(), found_user.password.encode()) == True:
                request.session['user_id'] = found_user.id
                request.session['user_name'] = found_user.firstName
                return redirect('/pokes')
            else:
                messages.error(request, "Login Failed, incorrect password", extra_tags="password")
                return redirect('/')
        else:
            messages.error(request, "Login Failed, email is not registered", extra_tags="email")
            return redirect('/')
    return render(request, "pokes/login.html")

def logout(request):
    request.session['user_id'] = 0
    request.session['user_name'] = ""
    return redirect('/login')

def dashboard(request):
    people = User.objects.exclude(id=request.session['user_id'])
    pokes = Poke.objects.filter(pokee_id=request.session['user_id']).order_by('-pokeCount')     # "-" infront of pokeCount is descending order

    '''Build list that contain user object and total pokes'''
    pokeHistory = []
    for user in people:
        totalPokes = 0
        for y in range(user.pokers.count()):
            totalPokes += user.pokers.all()[y].pokeCount
        pokeHistory.append([user, totalPokes])
    
    context = {
        "people": pokeHistory,
        "pokes": pokes
    }
    return render(request, "pokes/pokes.html", context)

def poked(request, user_id):
    poker = User.objects.get(id=request.session['user_id'])
    pokee = User.objects.get(id=user_id)
    existingPokes = Poke.objects.filter(poker_id=poker.id).filter(pokee_id=pokee.id)
    if existingPokes.count() > 0:
        p = existingPokes.first()
        p.pokeCount += 1
        p.save()
    else:
        Poke.objects.create(poker=poker, pokee=pokee, pokeCount=1)
    return redirect('/pokes')





