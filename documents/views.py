
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DocumentUploadForm
from .models import Document

@login_required
def upload_document_view(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.save()
            return redirect('document_list')
    else:
        form = DocumentUploadForm()
    return render(request, 'documents/upload.html', {'form': form})

@login_required
def document_list_view(request):
    documents = Document.objects.filter(owner=request.user)
    return render(request, 'documents/list.html', {'documents': documents})


