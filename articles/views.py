from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Author
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .models import CommentForm



def home(request):
    posts = Post.objects.all()
    ctx = {'posts': posts}
    return render(request, 'index.html', ctx)

def create_post(request):
    if request.method =='POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        short_content = request.POST.get('short_content')
        long_content = request.POST.get('long_content')
        author_id = request.POST.get('author')
        image = request.FILES.get('image')

        if title and category and  short_content and long_content and author_id and image:
            author = Author.objects.get(id=author_id)
            Post.objects.create(
                title=title,
                category=category,
                short_content=short_content,
                long_content=long_content,
                author=author,
                image=image
            )
            return redirect('home')
    authors = Author.objects.all()
    ctx = {'authors': authors}
    return render(request, 'articles/create-article.html', ctx)


def create_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        email = request.POST.get('email')

        if name and bio and email:
            Author.objects.create(
                name=name,
                bio=bio,
                email=email
            )
            return redirect('home')
    return render(request, 'articles/create-author.html')


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(post.get_detail_url())


    ctx = {'post': post, 'form': form}
    return render(request, 'articles/blog-detail.html', ctx)


def article_by_category(request, category):
    posts = Post.objects.filter(category=category)
    ctx = {'posts': posts, 'category': category}
    return render(request, 'articles/articles-by-category.html', ctx)




def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        created_at__year=year,
        created_at__month=month,
        created_at__day=day,
    )
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:3]

    ctx = {'post': post,
           'related_posts': related_posts,
           }
    return render(request, 'articles/blog-detail.html', ctx)