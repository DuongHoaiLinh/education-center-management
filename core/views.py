from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .forms import AbsenceRequestForm

# Create your views here.
def role_required(role):
    return user_passes_test(lambda u: u.is_authenticated and hasattr(u, 'student') if role == 'student' else hasattr(u, 'teacher') if role == 'teacher' else u.is_superuser)

@role_required('student')
def request_absence(request):
    if request.method == 'POST':
        form = AbsenceRequestForm(request.POST)
        if form.is_valid():
            absence = form.save(commit=False)
            absence.student = request.user.student
            absence.save()
            return redirect('home')
    else:
        form = AbsenceRequestForm()
    return render(request, 'request_absence.html', {'form': form})

@role_required('teacher')
def approve_absence(request, absence_id):
    absence = AbsenceRequest.objects.get(id=absence_id)
    if request.method == 'POST':
        absence.status = request.POST.get('status')
        absence.teacher = request.user.teacher
        absence.save()
        return redirect('home')
    return render(request, 'approve_absence.html', {'absence': absence})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'form': {}})
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')
