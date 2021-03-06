from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import secrets


class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def uservote(self, user):
        user_votes = user.vote_set.all()
        q = user_votes.filter(poll=self)
        if q.exists():
            return False
        return True

    def votecount(self):
        return self.vote_set.count()

    def __str__(self):
        return self.text

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    def votecount(self):
        return self.vote_set.count()

        
    def __str__(self):
        return f"{self.poll.text[:25]} - {self.choice_text[:25]}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'