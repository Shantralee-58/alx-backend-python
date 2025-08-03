from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        # Optimized query: only retrieve the fields we need
        return (
            self.filter(receiver=user, read=False)
            .select_related('sender')
            .only('id', 'content', 'timestamp', 'sender')
        )

