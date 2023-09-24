from django.shortcuts import render


from django.http import HttpResponse


def home(request):

    people  = [
        {"name":"Rishabh Sharma", "age":26},
        {"name":"Ankit Gupta", "age":35},
        {"name":"Munna Teli", "age":12},
        {"name":"Ravi Singh", "age":45},

    ]

    text = "dwfdsf wefndwjfn fodjnfodnodsnfods fdsojfndsof fdsjfdsjf jds fjdsf dsj fjdsf dsojfnjdsgbhgbojs aja "

    return render(request, "index.html", context= {"page": "Home","people" :people, "text": text})



def success_page(request):
    return HttpResponse("<h1> Success Page! </h1>")


def about(request):
    context = {"page" : "About"}

    return render(request, "about.html", context)




def contact(request):
    context = {"page" : "Contact"}


    return render(request, "contact.html", context)