from django.shortcuts import render, redirect
from .models import * # it imports models
from django.http import HttpResponse
import math

from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout # used because password was encrypted and login for session

from django.contrib.auth.decorators import login_required  #for making the recipe page open only when login is done.

from django.core.paginator import Paginator # for page number at the end of the page and limited data according to page.

from django.db.models import Q
# Create your views here.

@login_required(login_url="/login")
def recipes(request):
    if request.method == "POST":
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')


        # print(recipe_name)
        # print(recipe_description)
        # print(recipe_image)

        Recipe.objects.create(
            recipe_name = recipe_name,
            recipe_description = recipe_description,
            recipe_image = recipe_image
                              )
        return redirect('/recipes/')
    
    queryset = Recipe.objects.all()

    if request.GET.get('search_re'):
        queryset = queryset.filter(recipe_name__icontains = request.GET.get('search_re') )
    

    context = {'recipes':queryset}

    return render(request, "recipes.html", context=context)





def update_recipe(request, id):
    queryset = Recipe.objects.get(id = id)

    if request.method == "POST":
        data = request.POST

        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description

        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()

        return redirect("/recipes/")

    context = {"recipe":queryset}


    return render(request, "update_recipe.html", context = context)





def delete_recipe(request, id):
    queryset = Recipe.objects.get(id = id)
    queryset.delete()

    return redirect('/recipes/')


def login_page(request):
    # for login we only need email and password, here email is taken as username for simpilicity of code.
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username = username)
        if not user.exists():

            messages.error(request, "Invalid Email!")
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, "Incorrect Password!")
            return redirect("/login/")
        
        else:
            login(request, user)
            return redirect("/recipes")


    return render(request, "login.html")

# for registration
def register(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")


        user = User.objects.filter(username = username)

        if user.exists():
            messages.error(request, "You already have an account!")
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )

        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfuly!")


        return redirect('/register/')



    return render(request, "register.html")




def logout_page(request):
    logout(request)

    return redirect("/login/")



def get_students(request):

    if request.GET.get('optionFilter'):
        optionFilter = request.GET.get('optionFilter')
        print(optionFilter)

    queryset = Student.objects.all()
    search = ''

    if request.GET.get('search'):
        search = request.GET.get('search')
        lookup = {f"{optionFilter}__startswith": search}
        query = Q(**lookup)
        print(query)
        queryset = queryset.filter(query)  



    paginator = Paginator(queryset, 10)  # Show 10 contacts per page.
    a = math.ceil(len(queryset)/10)
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)  


    return render(request, "report/student.html", {'queryset' : page_obj, "range": range(a), "search" : search})
