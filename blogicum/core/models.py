from django.db import models


class PublishedCreatedModel(models.Model):
    """
    Абстрактная модель.
    Добавляет флаг is_published и
    дату добавления публикации created_at.
    """
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        verbose_name = 'Дата добавления публикации'
        verbose_name_plural = 'Дата добавления публикаций'


class TitleModel(models.Model):
    """Абстрактная модель заголовка."""
    title = models.CharField(
        'Заголовок',
        max_length=256
    )

    class Meta:
        abstract = True
        verbose_name = 'Заголовок'
        verbose_name_plural = 'Заголовок'
