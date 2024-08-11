from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import HeroForm, NovaPartyTestimonyForm, KibbutzStoryForm, TestimonialForm, AbducteeTestimonyForm
from .models import Hero, NovaPartyTestimony, KibbutzStory, Testimonial, AbducteeTestimony
from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.http import HttpResponseForbidden
from .models import AbducteeTestimony
from .forms import AbducteeTestimonyForm
from django.core.exceptions import PermissionDenied


User = get_user_model()

def home(request):
    heroes = Hero.objects.all()
    return render(request, 'home.html', {'heroes': heroes, 'user': request.user})


@login_required
def add_hero(request):
    if request.method == 'POST':
        form = HeroForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            hero = form.save(commit=False)
            hero.user = request.user
            hero.save()
            return redirect('home')
    else:
        form = HeroForm()
    return render(request, 'add_hero.html', {'form': form})


@login_required
def transition(request):
    return render(request, 'transition.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('join_form')  # Ensure 'join_form' URL name is correct
        else:
            messages.error(request, "Invalid credentials")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def forgot_password_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=True,
                email_template_name='reset_password_email.html'
            )
            return redirect('password_reset_done')
        else:
            return render(request, 'forgot_password.html', {'error': 'Invalid email address'})
    return render(request, 'forgot_password.html')


def forgot_password_submit(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        return redirect('forgot_password')
    return render(request, 'forgot_password.html')

def create_account_view(request):
    return render(request, 'create_account.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['new_password']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        messages.success(request, 'Account created successfully')
        return redirect('login')
    return render(request, 'register.html')

def join_form_view(request):
    return render(request, 'join_form.html')


def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next', '/')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def join_form(request):
    if request.method == 'POST':
        form = HeroForm(request.POST)
        if form.is_valid():
            hero = form.save(commit=False)
            hero.user = request.user
            hero.save()
            return redirect('home')
    else:
        form = HeroForm()
    return render(request, 'join_form.html', {'form': form})


def hall_of_fame(request):
    heroes = Hero.objects.all()
    return render(request, 'home.html', {'heroes': heroes})


def join_form_for_hero(request):
    if request.method == 'POST':
        print("Got form data")
        form = HeroForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            hero = form.save(commit=False)
            hero.user = request.user
            hero.save()
            return redirect('hall_of_fame')  # Redirect to the appropriate page
    else:
        form = HeroForm()
    return render(request, 'join_form_for_hero.html', {'form': form})


@login_required
def edit_hero(request, hero_id):
    hero = get_object_or_404(Hero, id=hero_id)
    # Check if the user is allowed to edit this hero
    if request.user != hero.user and not request.user.is_staff:
        return redirect('home')  # Redirect to home or show a permission error
    if request.method == 'POST':
        form = HeroForm(request.POST, instance=hero)
        if form.is_valid():
            form.save()
            return redirect('hero_detail', hero_id=hero.id)  # Redirect to the hero detail page after saving
    else:
        form = HeroForm(instance=hero)
    return render(request, 'edit_hero.html', {'form': form, 'hero': hero})


@login_required
def delete_hero(request, hero_id):
    hero = get_object_or_404(Hero, id=hero_id, user=request.user)
    if request.method == 'POST':
        hero.delete()
        return redirect('hall_of_fame')  # Redirect to the hall of fame or any other page
    return render(request, 'confirm_delete.html', {'hero': hero})


def hero_detail(request, hero_id):
    hero = get_object_or_404(Hero, id=hero_id)
    return render(request, 'hero_detail.html', {'hero': hero})


class HeroCreateView(LoginRequiredMixin, CreateView):
    model = Hero
    fields = ['first_name', 'last_name', 'age', 'hometown', 'country_of_birth', 'hero_story']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class HeroUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Hero
    fields = ['first_name', 'last_name', 'age', 'hometown', 'country_of_birth', 'hero_story']
    template_name = 'edit_hero.html'
    success_url = reverse_lazy('hall_of_fame')

    def test_func(self):
        hero = self.get_object()
        return self.request.user == hero.user or self.request.user.is_superuser

class HeroDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Hero
    template_name = 'delete_hero.html'
    success_url = reverse_lazy('hall_of_fame')

    def test_func(self):
        hero = self.get_object()
        return self.request.user == hero.user or self.request.user.is_superuser

def main_page(request):
    return render(request, 'home.html')

def transition(request):
    return render(request, 'transition.html')

class HeroListView(ListView):
    model = Hero
    template_name = 'hero_list.html'


def kibbutz_stories(request):
    stories = KibbutzStory.objects.all()
    return render(request, 'kibbutz_stories.html', {'kibbutz_stories': stories})

@login_required
def add_kibbutz_story(request):
    if request.method == 'POST':
        form = KibbutzStoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect('kibbutz_stories')
    else:
        form = KibbutzStoryForm()
    return render(request, 'add_kibbutz_story.html', {'form': form})


@login_required
def update_kibbutz_story(request, story_id):
    story = get_object_or_404(KibbutzStory, id=story_id)
    if request.user != story.author and not request.user.is_superuser:
        return redirect('kibbutz_stories')
    
    if request.method == 'POST':
        form = KibbutzStoryForm(request.POST, instance=story)
        if form.is_valid():
            form.save()
            return redirect('kibbutz_stories')
    else:
        form = KibbutzStoryForm(instance=story)
    
    return render(request, 'update_kibbutz_story.html', {'form': form})


@login_required
def delete_kibbutz_story(request, story_id):
    story = get_object_or_404(KibbutzStory, id=story_id)
    if request.user != story.author and not request.user.is_superuser:
        return redirect('kibbutz_stories')
    
    if request.method == 'POST':
        story.delete()
        return redirect('kibbutz_stories')
    
    return render(request, 'confirm_delete_story.html', {'story': story})


def nova_party_evidence(request):
    testimonies = NovaPartyTestimony.objects.all()
    return render(request, 'nova_party_evidence.html', {'testimonies': testimonies})


def add_nova_party_testimony(request):
    if request.method == 'POST':
        form = NovaPartyTestimonyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nova_party_evidence')  # Redirect to the testimonies page
    else:
        form = NovaPartyTestimonyForm()

    return render(request, 'add_nova_party_testimony.html', {'form': form})



@login_required
def update_testimonial(request, pk):
    testimonial = get_object_or_404(NovaPartyTestimony, id=pk)  # Changed to NovaPartyTestimony
    # Check if the user is the author or an admin
    if request.user != testimonial.author and not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to edit this testimonial.")
    if request.method == "POST":
        form = NovaPartyTestimonyForm(request.POST, instance=testimonial)  # Changed to NovaPartyTestimonyForm
        if form.is_valid():
            form.save()
            return redirect('nova_party_testimonies')
    else:
        form = NovaPartyTestimonyForm(instance=testimonial)  # Changed to NovaPartyTestimonyForm
    return render(request, 'update_testimonial.html', {'form': form})




@login_required
def delete_nova_party_testimony(request, testimony_id):
    testimony = get_object_or_404(NovaPartyTestimony, id=testimony_id)
    if request.user != testimony.author and not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to delete this testimonial.")
    if request.method == "GET" and request.GET.get('confirm') == 'yes':
        testimony.delete()
        return redirect('nova_party_testimonies')
    return render(request, 'confirm_delete_nova_party_testimony.html', {'testimony': testimony})


def zaka_people(request):
    # Add any context or data retrieval here if needed
    return render(request, 'zaka_people.html')


def testimonies_abductees(request):
    testimonies = AbducteeTestimony.objects.all()
    return render(request, 'testimonies_abductees.html', {'testimonies': testimonies})

@login_required
def add_abductee_testimony(request):
    if request.method == 'POST':
        form = AbducteeTestimonyForm(request.POST)
        if form.is_valid():
            AbducteeTestimony.objects.create(
                owner=form.cleaned_data['owner'],
                story=form.cleaned_data['story'],
                author=request.user,
                age=form.cleaned_data['age'],
                date_of_return=form.cleaned_data['date_of_return']
            )
            return redirect('testimonies-abductees')
    else:
        form = AbducteeTestimonyForm()
    return render(request, 'add_abductee_testimony.html', {'form': form})

@login_required
def update_abductee_testimony(request, testimony_id):
    testimony = get_object_or_404(AbducteeTestimony, pk=testimony_id)
    
    if request.method == 'POST':
        form = AbducteeTestimonyForm(request.POST, instance=testimony)
        if form.is_valid():
            form.save()
            return redirect('testimonies-abductees')
    else:
        form = AbducteeTestimonyForm(instance=testimony)

    return render(request, 'update_abductee_testimony.html', {'form': form})

@login_required
def delete_abductee_testimony(request, testimony_id):
    testimony = get_object_or_404(AbducteeTestimony, id=testimony_id)
    
    if request.user != testimony.author and not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == 'POST':
        testimony.delete()
        return redirect('testimonies-abductees')
    
    return render(request, 'confirm_deletion.html', {'testimony': testimony})