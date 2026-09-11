from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Pet, ShopItem
import random



def home(request):
    return render(request, 'pets/home.html')


def create_pet(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        pet_type = request.POST.get('pet_type')

        if name and pet_type:
            pet = Pet.objects.create(
                name=name,
                pet_type=pet_type
            )

            return redirect('dashboard', pet_id=pet.id)

    return render(request, 'pets/create_pet.html')


def dashboard(request, pet_id):
    pet = Pet.objects.get(id=pet_id)

    now = timezone.now()

    # Calculate how many minutes have passed
    minutes_passed = int(
        (now - pet.last_updated).total_seconds() / 60
    )

    if minutes_passed > 0:
        pet.hunger = max(0, pet.hunger - minutes_passed)
        pet.happiness = max(0, pet.happiness - minutes_passed)
        pet.energy = max(0, pet.energy - minutes_passed)

        pet.save()

    # Determine mood
    if pet.energy < 20:
        mood = "😴 Sleepy"
    elif pet.hunger < 20:
        mood = "😫 Hungry"
    elif pet.happiness > 70:
        mood = "😄 Happy"
    elif pet.happiness >= 40:
        mood = "🙂 Okay"
    else:
        mood = "😢 Sad"

    # Calculate health
    health = int(
        (pet.hunger + pet.happiness + pet.energy) / 3
    )

    # Determine health status
    if health >= 70:
        health_status = "💚 Healthy"
    elif health >= 40:
        health_status = "💛 Okay"
    else:
        health_status = "❤️‍🩹 Needs Care"

    return render(request, 'pets/dashboard.html', {
        'pet': pet,
        'mood': mood,
        'health': health,
        'health_status': health_status
    })
def feed_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)

    pet.hunger = min(100, pet.hunger + 20)
    pet.energy = max(0, pet.energy - 5)
    pet.coins = max(0, pet.coins - 10)

    pet.save()

    return redirect('dashboard', pet_id=pet.id)


def play_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)

    pet.happiness = min(100, pet.happiness + 20)
    pet.energy = max(0, pet.energy - 15)
    pet.hunger = max(0, pet.hunger - 10)

    pet.save()

    return redirect('dashboard', pet_id=pet.id)


def sleep_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)

    pet.energy = min(100, pet.energy + 30)
    pet.hunger = max(0, pet.hunger - 10)

    pet.save()

    return redirect('dashboard', pet_id=pet.id)


def pet_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)

    pet.happiness = min(100, pet.happiness + 10)

    pet.save()

    return redirect('dashboard', pet_id=pet.id)

def shop(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    items = ShopItem.objects.all()

    return render(request, 'pets/shop.html', {
        'pet': pet,
        'items': items
    })


def buy_item(request, pet_id, item_id):
    pet = Pet.objects.get(id=pet_id)
    item = ShopItem.objects.get(id=item_id)

    if pet.coins >= item.price:
        pet.coins -= item.price

        pet.hunger = min(100, pet.hunger + item.hunger_boost)
        pet.happiness = min(100, pet.happiness + item.happiness_boost)
        pet.energy = min(100, pet.energy + item.energy_boost)

        pet.save()

        message = f"You bought {item.name}! 🐾"
        message_type = "success"

    else:
        message = "Not enough coins! 🪙"
        message_type = "error"

    return render(request, 'pets/shop.html', {
        'pet': pet,
        'items': ShopItem.objects.all(),
        'message': message,
        'message_type': message_type
    })


def mini_game(request, pet_id):
    pet = Pet.objects.get(id=pet_id)

    result = None
    reward = 0

    if request.method == 'POST':
        guess = int(request.POST.get('guess'))
        number = random.randint(1, 5)

        if guess == number:
            reward = 30
            result = f"🎉 Correct! The number was {number}. You earned 30 coins!"
        else:
            reward = 5
            result = f"😅 Wrong! The number was {number}. You earned 5 coins!"

        pet.coins += reward
        pet.energy = max(0, pet.energy - 5)
        pet.happiness = min(100, pet.happiness + 5)

        pet.save()

    return render(request, 'pets/mini_game.html', {
        'pet': pet,
        'result': result
    })