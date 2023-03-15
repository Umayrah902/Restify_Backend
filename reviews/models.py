from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users.models import CustomUser

# seperated Rating and Comment because follow-up comments by hosts and clients do not have a rating

class Rating(models.Model):
    rating_num = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(5.0)], null=True, blank=True)
    reviewer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    rating_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    rating_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('rating_type', 'rating_id')

    # Use GenericForeignKey:
        # - Host leaves rating on client (CustomUser) who has completed reservation 
        # - Client leaves rating on properties (Property) where they have terminated or completed booking

class Comment(models.Model):
    rating_num = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(5.0)], null=True, blank=True)
    comment_text = models.TextField(max_length=500, null=False, blank=False)
    reviewer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    is_followup = models.BooleanField(default=False)
    comment_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    comment_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('comment_type', 'comment_id')
    your_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies_to_your_comments')
    owner_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies_to_owner_comments')

    # Use GenericForeignKey:
        # - Host leave comment on client (CustomUser) who has completed reservation 
        # - Client leave comment on properties (Property) where they have terminated or completed booking
        # - Host can respond to comments (Comment) made on their properties
        # - Client can respond to host’s follow-up comments (Comment) that was made on host’s properties

    

