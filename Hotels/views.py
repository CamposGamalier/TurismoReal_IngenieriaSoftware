from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .forms import SignUpForm, ProfileForm, CartItemForm
from .models import Room, CartItem
from .forms import RoomForm
from django.http import HttpResponse
from datetime import date
from decimal import Decimal
from django.utils import timezone
from django.template.loader import render_to_string

# Create your views here.
def index(request):
    return render(request, 'index.html', {'user': request.user})

@login_required
def catalogo(request):
    rooms = Room.objects.all()
    cart_items = CartItem.objects.filter(user=request.user)

    context = {
        'rooms': rooms,
        'cart_items': cart_items,
    }
    
    return render(request, 'catalogo.html', context)
@login_required
def perfil(request):
    return render(request, 'perfil.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear un perfil asociado al usuario
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')  # Redirige a la página de inicio después del registro
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirige a la página de inicio después del login exitoso
        else:
            # Handle login unsuccessful
            return render(request, 'registration/login.html', {'error_message': 'Nombre de usuario o contraseña incorrectos.'})
    else:
        return render(request, 'registration/login.html')

    
@login_required    
def logout_view(request):
    auth_logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('index')

def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    else:
        profile_form = ProfileForm(instance=profile)
    
    return render(request, 'editar.html', {'profile_form': profile_form})

def search_rooms(request):
    query = request.GET.get('q')
    capacity = request.GET.get('capacity')

    rooms = Room.objects.all()

    if query:
        rooms = rooms.filter(name__icontains=query)
    
    if capacity:
        rooms = rooms.filter(capacity__gte=capacity)

    context = {
        'rooms': rooms
    }
    return render(request, 'catalogo.html', context)

def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            # Aquí puedes realizar otras validaciones o procesamientos antes de guardar
            room.save()
            return redirect('catalogo')  # Redirige a donde deseas después de crear la habitación
    else:
        form = RoomForm()
    
    return render(request, 'create_room.html', {'form': form})

@login_required
def add_to_cart(request, room_id):
    room = Room.objects.get(pk=room_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('days', 1))
        has_breakfast = request.POST.get('has_breakfast', False) == 'on'
        has_lunch = request.POST.get('has_lunch', False) == 'on'
        has_transportation = request.POST.get('has_transportation', False) == 'on'
        
        # Calcular el precio base
        base_price = room.price_per_night * quantity
        
        # Sumar costos adicionales si están seleccionados
        if has_breakfast:
            base_price += Decimal('30000') * quantity
        
        if has_lunch:
            base_price += Decimal('30000') * quantity
        
        if has_transportation:
            base_price += Decimal('50000')
        
        # Crear un nuevo objeto CartItem con check_out_date calculado
        check_in_date = timezone.now().date()
        check_out_date = check_in_date + timezone.timedelta(days=quantity)
        
        cart_item = CartItem(
            user=request.user,
            room=room,
            quantity=quantity,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            has_breakfast=has_breakfast,
            has_lunch=has_lunch,
            has_transportation=has_transportation,
            total_price=base_price
        )
        
        # Guardar el objeto en la base de datos
        cart_item.save()
        
        # Mensaje de éxito y redirección a donde corresponda
        messages.success(request, 'Habitación agregada al carrito.')
        return redirect('catalogo')  # Ajustar la redirección según tu aplicación
    
    # Si no es POST, manejar el caso adecuadamente
    return redirect('index')  # Ajustar la redirección según tu aplicación


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    messages.success(request, "El artículo ha sido eliminado del carrito.")
    return redirect('catalogo')

def reservar(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    profile = Profile.objects.get(user=request.user)

    # Lógica para realizar la reserva y cualquier otro procesamiento necesario
    
    # Eliminar el ítem del carrito después de la reserva
    item.delete()

    # Mostrar mensaje de reserva exitosa
    messages.success(request, '¡Reserva exitosa!')

    # Renderizar la boleta y mostrarla
    context = {
        'item': item,
        'profile': profile,
    }
    boleta_html = render_to_string('boleta.html', context)

    # Devolver la boleta como respuesta
    return HttpResponse(boleta_html)

def search_room(request):
    query = request.GET.get('q')
    rooms = Room.objects.filter(name__icontains=query)
    return render(request, 'catalogo.html', {'rooms': rooms, 'query': query})