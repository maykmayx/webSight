from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .smartAssFunctions import handle_uploaded_file


def http404(request):
    t = loader.get_template("404.html")
    return HttpResponseNotFound(
        t.render(RequestContext(request, {'request_path': request.path})))


def http500(request):
    t = loader.get_template("500.html")
    return HttpResponseServerError(
        t.render(RequestContext(request, {'request_path': request.path})))


def home(request):
    return render_to_response("index.html")

def post(request):
    if(request.method == "POST"):
        print("Posting!")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    return render_to_response("index.html")