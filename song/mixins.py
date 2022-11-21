class UserSongFilterMixin:
    def get_queryset(self):
        query = super().get_queryset()
        user = self.request.user
        return query.filter(album__user=user)
