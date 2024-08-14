from django.shortcuts import render
from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import status
from django.http import HttpResponseForbidden

# Helper function
def is_admin(user):
    return user.is_superuser

# View for listing all students
def StudentView(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def StudentFormView(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
    context = {"form":form}
    return render(request,"form.html",context)



# Views for admins only
  # To create students
def StudentCreateView(request):
    if not is_admin(request.user):
        return HttpResponseForbidden("You do not have permission to access this page.")
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'form.html', {'form': form})


# To update students
def StudentUpdateView(request, pk):
    if not is_admin(request.user):
        return HttpResponseForbidden("You do not have permission to access this page.")
    
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'form.html', {'form': form})

# deleting students
def StudentDeleteView(request, pk):
    if not is_admin(request.user):
        return HttpResponseForbidden("You do not have permission to access this page.")
    
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'student_delete.html', {'student': student})



#APis views

class StudentListView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()  
    serializer_class = StudentSerializer

# Api Views only for admins
class CreateApiView(APIView):
    @permission_classes([IsAdminUser])
    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)   

class UpdateApiView(APIView):
    @permission_classes([IsAdminUser])
    def put(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)   

class DeleteApiView(APIView):
    @permission_classes([IsAdminUser])
    def delete(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        return redirect('student_list')      