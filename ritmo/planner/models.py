from django.db import models
from django.contrib.auth.models import User
import json


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    task_id = models.CharField(max_length=64)
    name = models.CharField(max_length=200)
    tag_id = models.CharField(max_length=32, default='focus')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'task_id')

    def __str__(self):
        return f"{self.user.username}: {self.name}"


class DayData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='day_data')
    day_key = models.CharField(max_length=12)  # YYYY-MM-DD
    times_json = models.TextField(default='[]')
    sched_json = models.TextField(default='{}')
    theme = models.CharField(max_length=10, default='dark')

    class Meta:
        unique_together = ('user', 'day_key')

    def get_times(self):
        return json.loads(self.times_json)

    def set_times(self, v):
        self.times_json = json.dumps(v)

    def get_sched(self):
        return json.loads(self.sched_json)

    def set_sched(self, v):
        self.sched_json = json.dumps(v)

    def __str__(self):
        return f"{self.user.username}: {self.day_key}"


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    theme = models.CharField(max_length=10, default='dark')

    def __str__(self):
        return f"{self.user.username} prefs"
