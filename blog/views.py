from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .models import Post, Author, Tag
from django.views.generic import ListView
from django.views.generic import DetailView
from .forms import CommentForm
from django.views import View


all_posts = [ ]


# Create your views here.
def get_date(post):
    return post['date']

# def starting_page(request):
#     latest_posts = Post.objects.all().order_by('-date')[:3]
#     return render(request, 'blog/index.html', {'posts':latest_posts})
   
class StartingPageView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 3

# def posts(request):
#     all_posts = Post.objects.all().order_by('-date')
#     return render(request, 'blog/all-posts.html', {'all_posts':all_posts})

class AllPostsView(ListView):
    model = Post
    template_name = 'blog/all-posts.html'
    context_object_name = 'all_posts'
    ordering = ['-date']



# def post_detail(request, slug):
    
#     try:
#         identified_post = get_object_or_404(Post, slug=slug)
#         return render(request, 'blog/post-detail.html', {
#             'post': identified_post,
#             'post_tags': identified_post.tag.all()
#             })
#     except:
#         resposta = render_to_string('404.html')
#         return HttpResponseNotFound(resposta)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post-detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwargs = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_tags'] = self.object.tag.all()
        context['comment_form'] = CommentForm()
        context["comments"] = self.object.comments.all()
        stored_posts = self.request.session.get('stored_post', [])
        context["saved_for_later"] = self.object.id in stored_posts

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            return redirect('post-detail-page', slug=self.object.slug)
        
        context = self.get_context_data(**kwargs)
        context["comment_form"] = form
        return self.render_to_response(context)
    
class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get('stored_post')

        context = {}

        if stored_posts is None:
            context['posts'] = []
            context['has_posts'] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts) 
            context['posts'] = posts
            context['has_posts'] = True

        return render(request, 'blog/stored-posts.html', context)       

    def post(self, request):
        stored_posts = request.session.get('stored_post')
        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST.get('post_id'))    

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session['stored_post'] = stored_posts

        return HttpResponseRedirect("/")     
    

class RemoveReadLaterView(View):
    def post (self, request):
        stored_posts = request.session.get('stored_post')
        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST.get('post_id'))
        saved_for_later = False

        if post_id in stored_posts:
            stored_posts.remove(post_id)
        else:
            saved_for_later = True

        request.session['stored_post'] = stored_posts

        return HttpResponseRedirect("/")            