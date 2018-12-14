from django.views import View
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import PermissionRequiredMixin

class HomePageView(View):
    def get(self,request):
        form = FormHome()
        username = request.user
        pictures = FileUpload.objects.all()
        comments = Comment.objects.all().order_by("comment_date")
        return render(request,"kasztan/home.html",{"form":form,"username":username,"pictures":pictures,"comments":comments})

class FileUploadView(View):

    def get(self, request):
        form = UploadImagesForms()
        return render (request, "kasztan/upload_file.html", {"form":form})

    def post(self,request):
        form = UploadImagesForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/file_list')


class FileListView(View):

    def get(self,request):
        files = FileUpload.objects.all()

        return redirect("/home")

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'kasztan/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('login'),
                                password=form.cleaned_data.get('hasło'))
            if user is not None:
                login(request, user)
                return redirect('/home')
            else:
                return HttpResponse('Zły login lub hasło!')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/home')

class AddUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField()
    surname = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput)

    def clean(self):

        cleaned_data = super().clean()

        field1 = cleaned_data.get('password')
        field2 = cleaned_data.get('repeat_password')

        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self.add_error("username", "Ten użytkownik już jest w bazie!")

        if field1 != field2:
            self.add_error("repeat_password", "Password i repeat password muszą być takie same")

        return cleaned_data

class AddUserView(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, "kasztan/add_user.html", {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            email = form.cleaned_data.get('email')
            User.objects.create_user(username=username, password=password, email=email, first_name=name,
                                     last_name=surname)
            return redirect('/')
        return render(request, "kasztan/add_user.html", {'form': form})

class EditUserView(View):
    def get(self, request, id):
        u = User.objects.get(pk=id)
        form = UserForm(instance=u)
        return render(request, "kasztan/add_user.html", {'form': form})

    def post(self, request, id):
        u = User.objects.get(pk=id)
        form = UserForm(request.POST, instance=u)
        if form.is_valid():
            form.save()
            return redirect('/profile/{{id}}')
        return HttpResponse("Not valid")

class profileView(View):
    def get(self,request,id):
        user = User.objects.get(pk=id)
        return render(request,"kasztan/profile.html",{"user":user})
