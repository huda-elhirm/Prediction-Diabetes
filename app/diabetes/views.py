import pickle
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html')


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


@csrf_exempt
def diabetes_pre(request):
    template = loader.get_template('result.html')  # Utilise le modèle result.html
    pregnancies = request.POST.get("Pregnancies")
    glucose = request.POST.get("Glucose")
    bloodpressure = request.POST.get("BloodPressure")
    skinthickness = request.POST.get("SkinThickness")
    insulin = request.POST.get("Insulin")
    BMI = request.POST.get("BMI")
    DiabetesPedigreeFunction = request.POST.get("DiabetesPedigreeFunction")
    age = request.POST.get("Age")

    diabetes_data = [
        [pregnancies, glucose, bloodpressure, skinthickness, insulin, BMI, DiabetesPedigreeFunction, age]]
    diabetes_model = pickle.load(open('diabetes_model.pickle', 'rb'))
    prediction = diabetes_model.predict(
        [[pregnancies, glucose, bloodpressure, skinthickness, insulin, BMI, DiabetesPedigreeFunction, age]])
    outcome = prediction

    if outcome == 1:
        result = "Vous êtes diabétique, veuillez consulter votre médecin"
    elif outcome == 0:
        result = "Vous n'êtes pas diabétique"

    return redirect('result', result=result)  # Redirige vers la vue result avec le résultat comme paramètre


def result(request, result):
    template = loader.get_template('result.html')
    return HttpResponse(template.render({'result': result}))
