import factory

from .models import Project, User, Membership, Box


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user-%d' % n)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Sequence(lambda n: 'project-%d' % n)
    creator = factory.SubFactory(UserFactory)


class MembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Membership

    user = factory.SubFactory(UserFactory)
    creator = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)


class BoxFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Box
