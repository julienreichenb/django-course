from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from blog.models import Post, Comment
from blog import model_helpers, navigation
from blog.forms import CreateCommentForm


def post_list(request, category_name=model_helpers.post_category_all.slug()):
    categories = model_helpers.get_categories()
    category, posts = model_helpers.get_category_and_posts(category_name)
    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_POSTS),
        'categories': categories,
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, post_id, message=''):
    post = get_object_or_404(Post, pk=post_id)
    related = model_helpers.get_related_posts(post)
    comments = model_helpers.get_comments(post)

    if request.method == 'POST':
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            args = [post.pk, 'Your comment has been submitted.']
            return HttpResponseRedirect(reverse('post-detail-message', args=args) + '#comments')
    else:
        comment_form = CreateCommentForm()

    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_POSTS),
        'post': post,
        'related': related,
        'comments': comments,
        'comment_form': comment_form,
        'message': message,
    }
    return render(request, 'blog/post_detail.html', context)


def about(request):
    context = {
        'navigation_items': navigation.navigation_items(navigation.NAV_ABOUT),
    }
    return render(request, 'blog/about.html', context)
