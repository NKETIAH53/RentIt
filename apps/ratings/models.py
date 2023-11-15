from django.db import models
from django.utils.translation import gettext_lazy as _
from real_estate.settings import AUTH_USER_MODEL
from apps.common.models import TimeStampedModel
from apps.profiles.models import Profile


class Rating(TimeStampedModel):
    class RatingRange(models.IntegerChoices):
        RATING_1 = 1, _("Poor")
        RATING_2 = 2, _("Fair")
        RATING_3 = 3, _("Good")
        RATING_4 = 4, _("Very Good")
        RATING_5 = 5, _("Excellent")

    client = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name=_("User providing the rating"), null=True)
    agent = models.ForeignKey(Profile, related_name="agent_rating", verbose_name=_("Agent being rated"), on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(verbose_name=_("Rating"), choices=RatingRange.choices, default=0, help_text=_("1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent"))
    comment = models.TextField(verbose_name=_("Comments"))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['client', 'agent'], name='unique agent rating')
        ]

    def __str__(self) -> str:
        return f"{self.agent} rated at {self.rating}"