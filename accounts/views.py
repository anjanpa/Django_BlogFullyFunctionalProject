from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

from .forms import (
    UserRegistrationForm,
    UserProfileUpdateForm,
    ProfilePictureUpdateForm
)


from .decorators import (
    not_logged_in_required
)

from .models import CustomUser,Follow

@never_cache
@not_logged_in_required
def register_user(request):
    form=UserRegistrationForm()

    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request,"Registration success")
            return redirect('login')
    context={
        "form":form
    }
    return render(request,'registration.html',context)


@login_required(login_url='login')
def profile(request):
    account=get_object_or_404(CustomUser,pk=request.user.pk)
    form=UserProfileUpdateForm(instance=account)

    if request.method == "POST":
        if request.user.pk != account.pk:
            return redirect('home')
        
        form = UserProfileUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated sucessfully")
            return redirect('profile')
        else:
            print(form.errors)

    context = {
        "account": account,
        "form": form
    }
    return render(request, 'profile.html', context)


@login_required
def change_profile_picture(request):
    if request.method == "POST":
        
        form = ProfilePictureUpdateForm(request.POST, request.FILES)
        
        if form.is_valid():
            image = request.FILES['profile_image']
            user = get_object_or_404(CustomUser, pk=request.user.pk)
            
            if request.user.pk != user.pk:
                return redirect('home')

            user.profile_image = image
            user.save()
            messages.success(request, "Profile image updated successfully")

        else:
            print(form.errors)

    return redirect('profile')


def view_user_information(request,username):
    account=get_object_or_404(CustomUser,username=username)
    following=False

    if request.user.is_authenticated:
        if request.user.id ==account.id:
            return redirect("profile")
            
        followers=account.followers.filter(
        followed_by_id=request.user.id)
        if followers.exists():
            following=True
    context={
        "account":account,
        "following":following,
    }
    return render(request,"user_information.html",context)


@login_required(login_url = "login")
def follow_or_unfollow_user(request, user_id):
    followed = get_object_or_404(CustomUser, id=user_id)
    followed_by = get_object_or_404(CustomUser, id=request.user.id)

    follow, created = Follow.objects.get_or_create(
        followed=followed,
        followed_by=followed_by
    )

    if created:
        followed.followers.add(follow)

    else:
        followed.followers.remove(follow)
        follow.delete()

    return redirect("view_user_information", username=followed.username)