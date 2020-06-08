from django.contrib.auth.models import User, Group as AuthGroup
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.conf import settings


from sport.models import Semester, Sport, Trainer, Group, Schedule


@receiver(post_save, sender=Semester)
def special_groups_create(sender, instance, created, **kwargs):
    if created:
        # get_or_create returns (object: Model, created: bool)
        other_sport, _ = Sport.objects.get_or_create(name="Other", special=True)
        trainer_group = AuthGroup.objects.get(verbose_name=settings.TRAINER_GROUP_VERBOSE_NAME)
        sport_dep_user, _ = User.objects.get_or_create(
            first_name="Sport",
            last_name="Department",
            email=settings.SPORT_DEPARTMENT_EMAIL,
            defaults={
                "is_active": True,
                "username": settings.SPORT_DEPARTMENT_EMAIL,
            }
        )
        sport_dep_user.groups.add(trainer_group)
        sport_dep, _ = Trainer.objects.get_or_create(user=sport_dep_user)
        trainer_group = Group(name=settings.SC_TRAINERS_GROUP_NAME, capacity=9999,
                              is_club=False, sport=other_sport,
                              semester=instance,
                              trainer=sport_dep)
        trainer_group.save()
        sport_event_group = Group(name="Extra sport events", capacity=9999,
                                  is_club=False, sport=other_sport,
                                  semester=instance,
                                  trainer=sport_dep)
        sport_event_group.save()
    else:
        # if semester changed, recalculate all future related schedules
        semester_schedules = Schedule.objects.filter(group__semester=instance.pk)
        for schedule in semester_schedules:
            post_save.send(sender=Schedule, instance=schedule, created=False)
