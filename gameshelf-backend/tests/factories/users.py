from datetime import timedelta

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from users.models import Profile, UserToken

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@test.com')
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)

    avatar = 'avatars/default.png'
    bio = factory.Faker('text', max_nb_chars=120)
    verified = False

    color_bg = '#79A998'
    role = Profile.Role.USER


class AdminProfileFactory(ProfileFactory):
    role = Profile.Role.ADMIN
    verified = True


class UserTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserToken

    user = factory.SubFactory(UserFactory)
    type = UserToken.TokenType.VERIFY_EMAIL

    expires_at = factory.LazyFunction(lambda: timezone.now() + timedelta(hours=1))


class ExpiredUserTokenFactory(UserTokenFactory):
    expires_at = factory.LazyFunction(lambda: timezone.now() - timedelta(hours=1))
