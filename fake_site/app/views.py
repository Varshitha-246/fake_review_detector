# fake_site/app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from pathlib import Path
from .forms import ContactForm 
from .models import ContactMessage
import numpy as np
import joblib                           
import os                               
from django.conf import settings        


# Load Review Origin Model (AI / BOT / HUMAN)
ORIGIN_MODEL_PATH = os.path.join(settings.BASE_DIR, "ml_models", "review_origin_pipeline.joblib")
origin_model = joblib.load(ORIGIN_MODEL_PATH)

# --------------------------
# AUTHENTICATION VIEWS
# --------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """Handle login authentication."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            pass
            #messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def home_view(request):
    unread_count = ContactMessage.objects.filter(
        email=request.user.email, is_replied=True, is_read=False
    ).count()

    return render(request, 'home.html', {
        'user': request.user,
        'unread_count': unread_count
    })


def logout_view(request):
    """Logout and redirect to login."""
    logout(request)
    return redirect('login')

@login_required
def predict_review(request):
    unread_count = ContactMessage.objects.filter(
        email=request.user.email, is_replied=True, is_read=False
    ).count()

    if request.method == "POST":
        review_text = request.POST.get("review", "").strip()
        if not review_text:
            return render(request, "predict.html", {
                "error": "Please enter a review.",
                "unread_count": unread_count
            })

        # Run Single Model (HUMAN / AI / BOT)
        probs = origin_model.predict_proba([review_text])[0]
        classes = origin_model.classes_
        origin_prediction = classes[probs.argmax()]

        # Convert to Fake/Genuine Logic
        if origin_prediction == "HUMAN":
            label = "GENUINE"
            review_type = "Human-Generated Review"
            reason = "Natural language flow, realistic detail and thought variation indicate genuine human writing."
        elif origin_prediction == "AI":
            label = "FAKE"
            review_type = "AI-Generated Review"
            reason = "Detected structured patterns, formal tone and artificial flow typical of AI-generated writing."
        else:  # BOT
            label = "FAKE"
            review_type = "BOT-Generated Review"
            reason = "Detected repetitive template-style phrases and promotional spam consistent with automated bots."

        confidence = round(max(probs) * 100, 2)

        return render(request, "result.html", {
            "review": review_text,
            "label": label,
            "confidence": confidence,
            "review_type": review_type,
            "reason": reason,
            "unread_count": unread_count
        })

    return render(request, "predict.html", {"unread_count": unread_count})


@login_required
def about_view(request):
    unread_count = ContactMessage.objects.filter(
        email=request.user.email, is_replied=True, is_read=False
    ).count()

    return render(request, "about.html", {"unread_count": unread_count})


@login_required
def contact_view(request):
    unread_count = ContactMessage.objects.filter(
        email=request.user.email, is_replied=True, is_read=False
    ).count()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form, "unread_count": unread_count})


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_messages(request):
    messages = ContactMessage.objects.all().order_by("-created_at")
    return render(request, "admin_messages.html", {"messages": messages})

from django.shortcuts import get_object_or_404

@staff_member_required
def send_reply(request, msg_id):
    if request.method == "POST":
        reply_text = request.POST.get("reply")
        msg = get_object_or_404(ContactMessage, id=msg_id)
        msg.reply = reply_text
        msg.is_replied = True
        msg.save()
        return redirect('admin_messages')

@login_required
def notifications(request):
    # Fetch unread count for notification badge
    unread_count = ContactMessage.objects.filter(
        email=request.user.email, is_replied=True, is_read=False
    ).count()

    # Fetch all user messages (replied ones)
    user_messages = ContactMessage.objects.filter(email=request.user.email, is_replied=True)

    return render(request, "notifications.html", {
        "messages": user_messages,
        "unread_count": unread_count
    })

from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def mark_as_read(request, msg_id):
    msg = get_object_or_404(ContactMessage, id=msg_id, email=request.user.email)
    msg.is_read = True
    msg.save()
    return HttpResponseRedirect(reverse('notifications'))

@login_required
def mark_read(request):
    ContactMessage.objects.filter(
        email=request.user.email, is_replied=True, is_read=False
    ).update(is_read=True)

    return redirect('notifications')

from django.contrib.auth.decorators import user_passes_test
def admin_check(user):
    return user.is_superuser


@user_passes_test(admin_check)
def admin_messages(request):
    # Show all messages ordered newest first
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, "admin_messages.html", {"messages": messages})

@user_passes_test(admin_check)
def reply_message(request, message_id):
    message = ContactMessage.objects.get(id=message_id)

    if request.method == "POST":
        reply_text = request.POST.get("reply")
        message.reply = reply_text
        message.is_replied = True
        message.save()
        return redirect('admin_messages')

    return render(request, "reply_message.html", {"message": message})
