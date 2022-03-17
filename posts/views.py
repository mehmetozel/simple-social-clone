from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404
from django.views import generic

# pip install django-braces
from braces.views import SelectRelatedMixin

# Create your views here.

from . import models
from . import  forms

from django.contrib.auth import get_user_model
User = get_user_model() #when someone's logged into a session, I'm gonna be able to use this user object as the current user and then call things off of that.

class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ('user', 'group') #the mixin that allows us to provide a tuple related model.
                                       #foreign keys for this post and that is gonna be the user that the post belongs to
                                        #We use select_related when the object that you're going to select is a single object, which means forward ForeignKey, OneToOne and backward OneToOne.
class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'post/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.object.prefetch_related('posts').get(username__iexact=self.kwargs.get("username")) #We use prefetch_related when we’re going to get a set of things.That means forward ManyToMany and backward ManyToMany, ForeignKey. prefetch_related does a separate lookup for each relationship, and performs the “joining” in Python.

            #self.post_user olmasının sebebi, self parameter alması ve yeni objeye atanması gerekli(post_user)                                                                                            #iexact, Case-insensitive exact match.
            #??? kwargs parametre olarak girilmeden kullanılabiliyor mu??? #base.py'daki self.kwargs=kwargs'dan çekiyor.
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username"))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message', 'group')
    model = models.Post

        # def get_form_kwargs(self):
        #     kwargs = super().get_form_kwargs()
        #     kwargs.update({"user": self.request.user})
        #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user  #it's just connect the actual post to the user itself
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)

