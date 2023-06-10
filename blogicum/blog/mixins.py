from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views import View


class DispatchDetailMixin(View):
    """Mixin для редактирования и удаления."""

    def dispatch(self, request, *args, **kwargs):
        objects = get_object_or_404(self.model, pk=kwargs['pk'])
        if objects.author != request.user:
            return redirect('blog:post_detail', id=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
