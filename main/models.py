from django.db import models

from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь один к одному
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=50)  # Роль пользователя
    rating = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Изменил на updated_at для последовательности
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.user.username  # исправлено с self.user_id.username


class SearchCard(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Многие к одному
    created_at = models.DateTimeField(auto_now_add=True)
    name_animal = models.CharField(max_length=30)
    status = models.CharField(max_length=30)  # Статус поиска животного
    animal_type = models.CharField(max_length=30)  # Тип животного
    describe_animal = models.TextField()  # Описание животного
    last_seen_location = models.CharField(max_length=255)  # Последнее местоположение с координатами
    updated_at = models.DateTimeField(auto_now=True)  # Изменил на updated_at для последовательности

    def __str__(self):
        return self.name_animal


class CardMessage(models.Model):
    id = models.AutoField(primary_key=True)
    search_card = models.ForeignKey(SearchCard, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username} on {self.created_at}"


class SearchActivity(models.Model):
    id = models.AutoField(primary_key=True)
    search_card = models.ForeignKey(SearchCard, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    status_activity = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.status_activity}"


class Complaint(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='complaints_by_user')
    target_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='complaints_against_user')
    search_card = models.ForeignKey(SearchCard, on_delete=models.CASCADE)
    reason = models.TextField()  # Причина жалобы
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.user.username}"


class Statistics(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    search_card_created = models.IntegerField(default=0)
    animals_found = models.IntegerField(default=0)
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Statistics for {self.user.username}"


class Achievement(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Achievement {self.type} for {self.user.username}"