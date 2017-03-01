from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Document
from .forms import DocumentForm


def list(request):
    #This allows the user to handle
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            #Redirect to the list once it is complete
            return HttpResponseRedirect(reverse('list'))
        else:
            form = DocumentForm()
        #Load list page
        documents = Document.objects.all()

        return render(
        request, 'list.html', {'documents': documents, 'form':form})
