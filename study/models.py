from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at", "-id")


class Material(TimeStampedModel):
    """Учебный материал: статья, конспект, ссылка на видео и т.п."""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True, help_text="Текст материала")
    url = models.URLField(blank=True, help_text="Внешняя ссылка (видео, статья)")

    class Meta(TimeStampedModel.Meta):
        verbose_name = "material"

    def __str__(self):
        return self.title


class Assignment(TimeStampedModel):
    """Задание, опционально привязанное к материалу."""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    material = models.ForeignKey(
        Material, null=True, blank=True, on_delete=models.SET_NULL, related_name="assignments"
    )
    due_date = models.DateTimeField(null=True, blank=True)
    max_score = models.PositiveIntegerField(default=100, validators=[MinValueValidator(1)])

    class Meta(TimeStampedModel.Meta):
        verbose_name = "assignment"

    def __str__(self):
        return self.title


class Test(TimeStampedModel):
    """Тест, опционально привязанный к материалу."""

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    material = models.ForeignKey(
        Material, null=True, blank=True, on_delete=models.SET_NULL, related_name="tests"
    )
    time_limit_minutes = models.PositiveIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1)], help_text="Пусто — без ограничения"
    )
    passing_score = models.PositiveIntegerField(
        default=60, validators=[MaxValueValidator(100)], help_text="Проходной балл, %"
    )
    is_published = models.BooleanField(default=False)

    class Meta(TimeStampedModel.Meta):
        verbose_name = "test"

    def __str__(self):
        return self.title
