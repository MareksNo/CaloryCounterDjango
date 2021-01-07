from django.urls import reverse_lazy
from django.views.generic import edit, View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from videos.models import Video
from django.conf import settings


class VideoView(View):
    def get(self, request, pk):
        video = get_object_or_404(klass=Video, pk=pk)

        return render(request=request, template_name='videos/display_video.html', context={'video': video})


class AddVideoView(LoginRequiredMixin, edit.CreateView):
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('profile-view')

    model = Video
    fields = ['title', 'description', 'file']

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(AddVideoView, self).form_valid(form)
