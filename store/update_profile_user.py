from django.contrib.auth.models import User
from faker import Faker

from store.models import Profile


def update_profiles():
    # Получаем всех пользователей
    users = User.objects.all()
    fake = Faker()

    for user in users:
        try:
            # Пытаемся получить профиль пользователя
            profile = Profile.objects.get(user=user)

            # Вносим изменения в профиль
            profile.phone = fake.phone_number()
            profile.address1 = fake.street_address()
            profile.address2 = fake.secondary_address()
            profile.city = fake.city()
            profile.zipcode = fake.zipcode()
            profile.country = fake.country()
            # и так далее для остальных полей

            # Сохраняем изменения
            profile.save()

            print(f"Профиль обновлен для пользователя: {user.username}")
        except Profile.DoesNotExist:
            print(f"Профиль не найден для пользователя: {user.username}")


# Вызываем функцию для обновления профилей
update_profiles()
