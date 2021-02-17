from django.db import models
from django.contrib.auth import get_user_model

# Job entry model
class Entry(models.Model):
    # "company" field
    company = models.CharField(max_length=100)
    # "position" field
    position = models.CharField(max_length=100)
    # "link" field
    link = models.URLField()
    # "date applied" field
    date_applied = models.DateInput()
    # "status" field
    status = models.CharField(max_length=100)
    # "notes" field
    notes = models.TextField()
    # Creator link
    creator = models.ForeignKey(
            get_user_model(),
            on_delete=models.CASCADE
    )

    def as_dict(self):
        """'Returns dictionary version of Entry Models'"""
        return {
            'id': self.id,
            'creator': self.creator,
            'company': self.company,
            'position': self.position,
            'link': self.link,
            'date_applied': self.date_applied,
            'status': self.status,
            'notes': self.notes
        }
