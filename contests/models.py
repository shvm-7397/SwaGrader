from django.db import models
from django.urls import reverse
from accounts.models import Profile
from django.contrib.auth.models import User


# Create your models here.


class Challenge(models.Model):
    """ Model to Represent a Single Contest """
    challenge_code = models.CharField(max_length=50)
    challenge_name = models.CharField(max_length=50)
    Active, Upcoming, Past = 'Active', 'Upcoming', 'Past'
    Status_Choices = ((Active, 'Active'), (Upcoming, 'Upcoming'), (Past, 'Past'))
    status = models.CharField(max_length=20, choices=Status_Choices, default=Upcoming)

    # Add Questions field

    def __str__(self):
        return self.challenge_name

    def get_absolute_url(self):
        return reverse('contests:details',
                       kwargs={'pk': self.pk})  # detail view requires primary key so we send in the key like that


class Problem(models.Model):
    """ Model to represent a single problem """
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, default=None)
    problem_code = models.CharField(max_length=50)
    problem_name = models.CharField(max_length=50)
    problem_file_url = models.CharField(max_length=50)
    in_practice = models.BooleanField(default=False)

    def __str__(self):
        return self.problem_code

    def get_absolute_url(self):
        return reverse('contests:contest-detail', kwargs={'pk': self.challenge.pk})  # detail view requires primary
        # key so we send in the key like that


class Submission(models.Model):
    """ Model to Represent a submission by a user to a particular problem """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    cpp, c, python = 'cpp', 'c', 'python'
    language_choices = ((cpp, 'cpp'), (c, 'c'), (python, 'python'))
    language = models.CharField(max_length=20, choices=language_choices, default=None)
    CK, AC, WA, TLE, RE, CTE = 'Checking', 'Accepted', 'Wrong Answer', 'Time Limit Exceeded', 'Runtime Error', \
                               'Compile Time Error'
    status_choices = ((AC, 'Accepted'), (WA, 'Wrong Answer'), (TLE, 'Time Limit Exceeded'), (RE, 'Runtime Error'),
                      (CTE, 'Compile Time Error'), (CK, 'Checking'))
    status = models.CharField(max_length=20, choices=status_choices, default=CK)
    source_file = models.FileField()

    def __str__(self):
        return self.user.username + '__' + self.problem.problem_code + '__' + self.status


class UCT(models.Model):
    """ Model to represent user participation in a particular challenge with score """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, default=None)

    score = models.IntegerField(default=0)
