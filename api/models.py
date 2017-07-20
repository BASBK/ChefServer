from django.db import models
from django.urls import reverse

# Create your models here.

class DeliveryTypes(models.Model):
    """
    Model representing a delivery type (Pizza, Sushi, etc)
    """

    name = models.CharField(max_length=20, primary_key=True, help_text='Enter a delivery type name')

    def __str__(self):
        return self.name


class Deliveries(models.Model):
    """
    Model representing a delivery
    """

    name = models.CharField(max_length=40, primary_key=True, help_text='Enter a delivery name')
    cook_info = models.ForeignKey('ChatInfo', on_delete=models.SET_NULL, null=True)
    image = models.ForeignKey('Images', on_delete=models.SET_NULL, null=True)
    dtype = models.ForeignKey(DeliveryTypes, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance
        """

        return reverse('delivery-detail', args=[str(self.id)])


class ChatInfo(models.Model):
    """
    Model representing an information about user's chat
    """

    username = models.CharField(max_length=30)
    chat_id = models.IntegerField(null=True)


class Images(models.Model):
    """
    Model representing an image for delivery or menu item
    """

    local_path = models.TextField()
    file_id = models.TextField(null=True)

    def get_absolute_url(self):
        return reverse('image-detail', args=[str(self.id)])


