from blog.models import Post, PostCategory, Comment

post_category_all = PostCategory(name='All')


def get_category_and_posts(category_name):
    posts = Post.objects.filter(published=True)
    if category_name == post_category_all.slug():
        category = post_category_all
    else:
        try:
            category = PostCategory.objects.get(name__iexact=category_name)
            posts = posts.filter(category=category)
        except PostCategory.DoesNotExist:
            category = PostCategory(name=category_name)
            posts = Post.objects.none()
    posts = posts.order_by('-created_at')
    return category, posts,


def get_categories():
    categories = list(PostCategory.objects.all().order_by('name'))
    categories.insert(0, post_category_all)
    return categories


def get_related_posts(post):
    return Post.objects.filter(category=post.category, published=True)\
        .exclude(pk=post.pk).order_by('-created_at')


def get_comments(post):
    return post.comments.exclude(status=Comment.STATUS_HIDDEN).order_by('created_at')
