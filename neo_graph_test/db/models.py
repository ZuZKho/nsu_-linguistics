from django.db import models

class Corpus(models.Model):
    GENRE = [
        ('fiction', 'Художественная литература'),
        ('scientific', 'Научная литература'),
        ('news', 'Новости'),
        ('academic', 'Академические тексты'),
        ('technical', 'Техническая документация'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Название корпуса")
    description = models.TextField(verbose_name="Описание корпуса")
    genre = models.CharField(
        max_length=20, 
        choices=GENRE, 
        verbose_name="Жанр корпуса"
    )
    
    def __str__(self):
        return f"{self.name} ({self.genre[0]})"

class Text(models.Model):
    title = models.CharField(max_length=300, verbose_name="Название текста")
    description = models.TextField(verbose_name="Описание текста")
    content = models.TextField(verbose_name="Текст")
    
    # Связь с корпусом
    corpus = models.ForeignKey(
        Corpus, 
        on_delete=models.CASCADE, 
        related_name='texts',
        verbose_name="Корпус"
    )
    
    # Связь с самим собой для перевода
    has_translation = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='translations',
        verbose_name="Перевод текста"
    )
    
    def __str__(self):
        return self.title
    