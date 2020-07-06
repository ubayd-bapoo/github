from django.db import models
from django.contrib.auth.models import User

# ==============================================================================
class MergeRequest(models.Model):
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    # We make sure there is a one2one relationship with the user model
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    accept = models.BooleanField(default=False)

    title = models.CharField(default=None, max_length=250)
    repo = models.CharField(default=None, max_length=250)
    source_branch = models.CharField(default=None, max_length=250)
    target_branch = models.CharField(default=None, max_length=250)
    assign_email = models.CharField(default=None, max_length=250)

    def __str__(self):
        return str('%s: %s' % (self.title, self.repo))
