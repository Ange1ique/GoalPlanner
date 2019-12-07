from django.db import models
import datetime
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from crum import get_current_user

# Create your models here.
class Goals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_title = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    progress = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('goal_app:goals')

class SubGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)
    goal = models.ForeignKey(Goals, on_delete=models.CASCADE)
    subgoal_title = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    progress = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    portion = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.user:
            self.user = get_current_user()
            super(SubGoals, self).save(*args, **kwargs)

class Activities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)
    subgoal = models.ForeignKey(SubGoals, on_delete=models.CASCADE)
    activity_title = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    progress = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    portion = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.user:
            self.user = get_current_user()
            super(Activities, self).save(*args, **kwargs)
