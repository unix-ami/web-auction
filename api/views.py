"""
Views for handling auction listings, bidding, user profiles,
and rendering the main single-page application (SPA).
"""

import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import redirect, render
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomRegistrationForm, CustomLoginForm
from .models import Item, User, Bid, Question
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.utils import timezone
from decimal import Decimal

@ensure_csrf_cookie
#@require_http_methods(["GET"])
@login_required
def set_csrf_token(request):
   return JsonResponse({'message': 'CSRF token set'})

# @never_cache
@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    """Renders the main single-page application (SPA) HTML template."""
    return render(request, 'api/spa/index.html', {})

@login_required
def api_email_view(request: HttpRequest) -> JsonResponse:
    """Returns the authenticated user's email address as JSON."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    return JsonResponse({'email': request.user.email})

def auth_redirect(request: HttpRequest) -> HttpResponse:
    """Redirects users based on authentication status."""
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')

def register_view(request: HttpRequest) -> HttpResponse:
    """Handles user registration."""
    #if request.user.is_authenticated:
    #    return redirect('home')
    
    if request.method == 'POST':
        # request.FILES to handle image uploads
        form = CustomRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect('login')
        else:
            print(form.errors)  # For debugging
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomRegistrationForm()

    return render(request, 'api/auth/register.html', {'form': form})

@login_required
def vue_app(request):
    """Renders the Vue.js application."""
    return render(request, 'vue_app.html')

def login_view(request):
    """Handles user login."""
    #if request.user.is_authenticated:
    #    return redirect('home')
    if request.user.is_authenticated:
        # return redirect(settings.FRONTEND_URL)
        return redirect('/home/')
    form = CustomLoginForm(data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # Use form.cleaned_data to get the username and password
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in!")
                # return redirect(settings.FRONTEND_URL)
                return redirect('/home/')
            else:
                messages.error(request, "Invalid login credentials. Please try again.")

    return render(request, 'api/auth/login.html', {'form': form})

def logout_view(request):
    """Logs out the user and redirects to the login page."""
    logout(request)
    return redirect('login')

# @csrf_exempt - for testing purposes only
def items_view(request: HttpRequest) -> JsonResponse:
    """Renders the main page with a list of items and their details."""
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
        
    elif request.method == "GET":
        items = Item.objects.all()

        data = [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "starting_price": str(item.starting_price),
                # Return absolute image URL
                'image': request.build_absolute_uri(item.image.url) if item.image else None,
                "auction_end": item.auction_end.isoformat(),
                "is_owner": item.user.id == request.user.id, 
            }
            for item in items
        ]

        return JsonResponse(data, safe=False)
    
def item_detail(request: HttpRequest, item_id: int) -> JsonResponse:
    """GET single item by ID"""

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    if request.method == "GET":
        item = get_object_or_404(Item, id=item_id)
        
        data = {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "starting_price": str(item.starting_price),
            "image": request.build_absolute_uri(item.image.url) if item.image else "",
            "auction_end": item.auction_end.isoformat(),
            "seller": item.user.username,
            "created_at": item.created_at.isoformat(),
            "is_owner": item.user.id == request.user.id,
        }
        
        return JsonResponse(data)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def auth_view(request):
    """Handles user authentication via login form."""
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # target URL after login
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Invalid input')

    return render(request, 'api/auth/login.html', {'form': form})

@login_required
def profile_view(request):
    """Updates user profile information."""
    
    user = request.user
    
    if request.method == "GET":
        data = {
            'email': user.email,
            'dob': user.dob.isoformat() if user.dob else None,
        }
        return JsonResponse(data)
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        user.email = data.get('email', user.email)
        user.dob = data.get('dob', user.dob)
        user.save()
        return JsonResponse({'message': 'Profile updated successfully'}, status=200)
    
def logout_user(request):
    """Logs out the user and redirects to the login page."""
    logout(request)  # Clear Django session
    return redirect('/login/')  # Redirect to Django login page

@login_required
def api_profile(request):
    """Returns the authenticated user's profile information as JSON."""
    profile_image_url = ''
    if request.user.profile_image:
        # Build absolute URL with domain and port
        profile_image_url = f"{request.user.profile_image.url}"
    
    return JsonResponse({
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'dob': request.user.dob.strftime('%Y-%m-%d') if request.user.dob else '',
        'profile_image': profile_image_url,
    })

@login_required
def update_profile(request):
    """Updates the authenticated user's profile information."""
    if request.method == 'POST':
        user = request.user
        
        # Handle FormData
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.username = request.POST.get('username', user.username)  

        if request.POST.get('dob'):
            user.dob = datetime.strptime(request.POST['dob'], '%Y-%m-%d').date()
        
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        
        user.save()
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def create_item(request: HttpRequest) -> JsonResponse:
    """Creates a new auction item."""
    if request.method == "POST":
        user: User = request.user
        
        item = Item.objects.create(
            user=user,
            title=request.POST.get("title", ""),
            description=request.POST.get("description", ""),
            starting_price=request.POST.get("starting_price", 0),
            auction_end=request.POST.get("auction_end"), 
        )
        
        if "image" in request.FILES:
            item.image = request.FILES["image"]
            item.save()
        
        return JsonResponse({"success": True, "id": item.id})
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

@login_required
def place_bid(request: HttpRequest, item_id: int) -> JsonResponse:
    """Places a bid on an auction item."""
    item = get_object_or_404(Item, id=item_id)
    
    # Check auction active
    if item.auction_end < timezone.now():
        return JsonResponse({'error': 'Auction has ended'}, status=400)
    
    # Check not owner
    if item.user == request.user:
        return JsonResponse({'error': 'Cannot bid on your own item'}, status=400)
    
    data = json.loads(request.body)
    amount = Decimal(data['amount'])
    
    # Get highest bid
    highest_bid = item.bids.order_by('-amount').first()
    min_amount = highest_bid.amount if highest_bid else item.starting_price
    
    if amount < min_amount:
        return JsonResponse({'error': f'Bid must be higher than £{min_amount}'}, status=400)
    
    # Update previous highest bid status to OUTBID
    if highest_bid:
        highest_bid.status = 'OUTBID'
        highest_bid.save()
    
    # Create new bid with PENDING status
    bid = Bid.objects.create(
        item=item, 
        user=request.user, 
        amount=amount,
        status='PENDING'
    )
    
    return JsonResponse({
        'success': True,
        'bid': {
            'id': bid.id,
            'amount': str(bid.amount),
            'user': bid.user.username,
            'created_at': bid.created_at.isoformat(),
            'status': bid.status,
        }
    })

@login_required
def item_bids(request: HttpRequest, item_id: int) -> JsonResponse:
    """GET all bids for an item"""
    item = get_object_or_404(Item, id=item_id)
    bids = item.bids.order_by('-amount')
    
    data = [
        {
            'id': bid.id,
            'amount': str(bid.amount),
            'user': bid.user.username,
            'created_at': bid.created_at.isoformat(),
        }
        for bid in bids
    ]
    
    return JsonResponse(data, safe=False)

@login_required
def user_bids(request: HttpRequest) -> JsonResponse:
    """GET all bids placed by the authenticated user"""

    # Order by time
    bids = Bid.objects.filter(user=request.user).select_related('item').order_by('-created_at')
    
    data = [
        {
            'id': bid.id,
            'amount': str(bid.amount),
            'status': bid.status,
            'created_at': bid.created_at.isoformat(),
            'item_id': bid.item.id,
            'item_title': bid.item.title,
            'item_image': request.build_absolute_uri(bid.item.image.url) if bid.item.image else None,
            'auction_end': bid.item.auction_end.isoformat(),
        }
        for bid in bids
    ]
    
    return JsonResponse(data, safe=False)

@login_required
def item_questions(request: HttpRequest, item_id: int) -> JsonResponse:
    """GET all questions for an item"""
    item = get_object_or_404(Item, id=item_id)
    questions = item.questions.select_related('user').all()
    
    data = [
        {
            'id': q.id,
            'text': q.text,
            'answer': q.answer,
            'created_at': q.created_at.isoformat(),
            'answered_at': q.answered_at.isoformat() if q.answered_at else None,
            'user': {
                'id': q.user.id,
                'username': q.user.username,
                'profile_image': request.build_absolute_uri(q.user.profile_image.url) if q.user.profile_image else None,
            }
        }
        for q in questions
    ]
    
    return JsonResponse(data, safe=False)

@login_required
def ask_question(request: HttpRequest, item_id: int) -> JsonResponse:
    """POST a new question"""
    item = get_object_or_404(Item, id=item_id)
    data = json.loads(request.body)
    
    question = Question.objects.create(
        item=item,
        user=request.user,
        text=data['text']
    )
    
    return JsonResponse({
        'success': True,
        'question': {
            'id': question.id,
            'text': question.text,
            'created_at': question.created_at.isoformat(),
            'user': {
                'username': request.user.username,
                'profile_image': request.build_absolute_uri(request.user.profile_image.url) if request.user.profile_image else None,
            }
        }
    })

@login_required
def answer_question(request: HttpRequest, question_id: int) -> JsonResponse:
    """POST an answer"""
    question = get_object_or_404(Question, id=question_id)
    
    # Check if user is item owner
    if question.item.user != request.user:
        return JsonResponse({'error': 'Only item owner can answer'}, status=403)
    
    data = json.loads(request.body)
    
    question.answer = data['answer'] # Set answer text
    question.answered_at = timezone.now() # Timestamp
    question.save() # Saves to database
    
    return JsonResponse({'success': True})