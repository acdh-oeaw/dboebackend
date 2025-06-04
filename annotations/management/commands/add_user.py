from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from guardian.shortcuts import assign_perm
from annotations.models import Collection


class Command(BaseCommand):
    help = "Adds a new user add assigns necessary permissions"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)
        parser.add_argument("first_name", type=str)
        parser.add_argument("last_name", type=str)
        parser.add_argument("email", type=str)

    def handle(self, *args, **options):

        user = User.objects.create(username=options["username"], email=options["email"])
        user.is_staff = True
        user.first_name = options["first_name"]
        user.last_name = options["last_name"]
        user.save()
        g, _ = Group.objects.get_or_create(name="general")
        g.user_set.add(user)
        # a new user has to have an access to view all public collections and their annotations
        for collection in Collection.objects.all():
            if collection.public is True:
                assign_perm("view_collection", user, collection)
                if collection.annotations.all():
                    for annotation in collection.annotations.all():
                        assign_perm("view_annotation", user, annotation)
            else:
                pass
