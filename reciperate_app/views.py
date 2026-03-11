from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Reciperate Home Page")

def breakfast(request):
    return HttpResponse("Breakfast")

def lunch(request):
    return HttpResponse("Lunch")

def dinner(request):
    return HttpResponse("Dinner")

def add_recipe(request):
    return HttpResponse("Add Recipe")

def signup(request):
    return HttpResponse("Create Account")

def signin(request):
    return HttpResponse("Sign in")