from typing import Optional
from django import template
from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse, response
from django.template import loader
import io


# Create your views here.


def accept(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        degree = request.POST.get("degree", "")
        summary = request.POST.get("summary", "")
        school = request.POST.get("school", "")

        skills = request.POST.get("skills", "")
        previous_work = request.POST.get("previous_work", "")

        profile = Profile(name=name, email=email, phone=phone, degree=degree, summary=summary,
                          school=school, skills=skills,  previous_work=previous_work)
        profile.save()

    return render(request, 'pdf/accept.html')


def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({'user_profile': user_profile})
    Options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, Options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename = "resume.pdf"
    return response


def list(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf/list.html', {'profiles': profiles})
