from django.db import models


class LogEntry(models.Model):
    beleg = models.ForeignKey(
        "belege.Beleg",
        verbose_name="Beleg",
        on_delete=models.CASCADE,
        related_name="log_entry",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Zeitstempel")
    username = models.CharField(
        max_length=100, verbose_name="Username", default="unbekannt"
    )
    payload = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
        ordering = ["created_at", "beleg"]

    def __str__(self):
        return f"{self.beleg} ({self.created_at})"

    def save(self, *args, **kwargs):
        self.payload = self.beleg.sanitize_representation()
        super().save(*args, **kwargs)
