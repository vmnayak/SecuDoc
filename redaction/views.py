# redaction/views.py
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import RedactionTask, RedactionRegion
from .forms import RedactionTaskForm, RedactionRegionForm
from .utils import redact_pdf

@login_required
def create_task(request):
    if request.method == 'POST':
        form = RedactionTaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save()
            return redirect('redaction:task_detail', task.id)
    else:
        form = RedactionTaskForm()
    return render(request, 'redaction/create_task.html', {'form': form})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(RedactionTask, id=task_id)
    region_form = RedactionRegionForm()
    return render(request, 'redaction/task_detail.html', {
        'task': task,
        'region_form': region_form,
    })

@login_required
def add_region(request, task_id):
    task = get_object_or_404(RedactionTask, id=task_id)
    if request.method == 'POST':
        form = RedactionRegionForm(request.POST)
        if form.is_valid():
            region = form.save(commit=False)
            region.task = task
            region.save()
    return redirect('redaction:task_detail', task.id)

@login_required
def process_task(request, task_id):
    task = get_object_or_404(RedactionTask, id=task_id)
    try:
        # gather regions
        regions = []
        for r in task.regions.all():
            regions.append({
                'page_number': r.page_number,
                'x': r.x,
                'y': r.y,
                'width': r.width,
                'height': r.height,
            })
        # paths
        input_path = task.original_file.path
        # create output filename
        base = os.path.basename(input_path)
        out_path = os.path.join(settings.MEDIA_ROOT, 'redaction', 'processed', f'redacted_{base}')
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        # perform redaction
        redact_pdf(input_path, out_path, regions)

        # save to model (use FileField relative path)
        # set redacted_file to relative path under MEDIA_ROOT
        from django.core.files import File
        with open(out_path, 'rb') as f:
            task.redacted_file.save(f'redacted_{base}', File(f), save=True)

        task.processed = True
        task.processed_at = timezone.now()
        task.error_msg = ''
        task.save()
    except Exception as e:
        task.error_msg = str(e)
        task.save()
    return redirect('redaction:task_detail', task.id)
