from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from blog.models import Post, Comment, Newletter
from .forms import CommentForm, NewsletterForm, ContactForm, PostForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# Create your views here.

#POST BLOG
@login_required
def postblog(request):
    
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():  
            post = post_form.save()
            print(post)
            emails = Newletter.objects.filter()
            # post = Post.objects.filter(id=post_form.id)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = "Welcome to Swifttech Where we give You the latest Tech and Educational news"
            #message = f'{post.title}\n\n.{post.image.url} {post.descriptions[:40]}\n{post_url}'
            #send_mail(subject, message, 'omotoshomicheal93@gmail.com', [ user.email for user in emails ])
            with open(settings.BASE_DIR + "/blog/templates/blog/postform_email.txt") as f:
                postblog = f.read()
            message = EmailMultiAlternatives(subject=subject, body=postblog, from_email='omotoshomicheal93@gmail.com', to=[ user.email for user in emails ])
            html_template = get_template("blog/postform_email.html").render({'post' : post, 'post_url':post_url})
            message.attach_alternative(html_template, 'text/html')
            message.send()
            print(message.send())

            return redirect('post_blog')
    else:
        post_form = PostForm()
    
    return render(request, 'blog/postform.html', {'post_form': post_form})

#POST LIST
def postView(request):
    postlist = Post.objects.filter(status='published').order_by('-created')
    latest_product = Post.objects.filter(status='published', categories='product').order_by('-created')[0:3]
    #category = Category.objects.all()
    paginator = Paginator(postlist, 6) # 3 posts in each page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_query = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        paginated_query = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        paginated_query = paginator.page(paginator.num_pages)

    #CONTACT FORM
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #name = cd['name']
            #email_from = cd['email_from']
            subject_message = 'This is a mail from :{}, Email:{}, Subject:{}'.format(cd['name'], cd['email_from'], cd['subject'])
            message = cd['message']
            send_mail(subject_message, message, 'omotoshomicheal93@gmail.com', ['omotoshomicheal93@gmail.com'])
            messages.success(request, 'item saved')
            return redirect("posts")
    else:
        form = ContactForm()

    #NEWSLETTER SUBSCRIPTION FORM
    if request.method == 'POST':
        newsform = NewsletterForm(request.POST or None)
        if newsform.is_valid():
            instance = newsform.save(commit=False)
            if Newletter.objects.filter(email=instance.email).exists():
                messages.warning(request, 'This email alreay exist')
                return redirect('posts')
            else:
                instance.save()
                messages.success(request, 'Subscription successful')
                subject_message = 'NEWSLETTER SUBSCRIPTION'
                message = 'Thank you for subscribing to our blog. We will Updating you will all of our blog posts'
                send_mail(subject_message, message, 'omotoshomicheal93@gmail.com', [instance.email])
                return redirect('posts')
    else:
        newsform = NewsletterForm()


    context = {
        'query' : paginated_query,
        'page_request_var' : page_request_var,
        #'category': category,
        'newsform': newsform,
        'latest_product' : latest_product,
        'form' : form
    }
    return render(request, 'blog/index.html', context)

#POST DETAIL
def detailView(request, post):
    recent_post = Post.objects.order_by('-created')[0:1]
    postdetail = get_object_or_404(
        Post, slug=post,
        status='published', 
        #publish__year = year,
        #publish__month = month,
        #publish__day = day
    )

    #List of active comments for this post
    comments = postdetail.comments.filter(active=True)

    if request.method == 'POST':
        #A comment was posted
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            #create comment object but don't save to the database yet
            new_comment = comment_form.save(commit=False)
            #Assign the comment post to the comment
            new_comment.post = postdetail
            new_comment.save()
            return redirect(reverse("post-detail", args = [
                postdetail.slug,
            ]))
    else:
        comment_form = CommentForm()

    latest_product = Post.objects.filter(status='published', categories='product').order_by('-created')[0:3]
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #name = cd['name']
            #email_from = cd['email_from']
            subject_message = 'This is a mail from :{}, Email:{}, Subject:{}'.format(cd['name'], cd['email_from'], cd['subject'])
            message = cd['message']
            send_mail(subject_message, message, 'omotoshomicheal93@gmail.com', ['omotoshomicheal93@gmail.com'])
            messages.success(request, 'item saved')
            return redirect("posts")
    else:
        form = ContactForm()
    context = {
        'postdetail' : postdetail,
        'comments' : comments,
        'comment_form' : comment_form,
        'recent_post': recent_post,
        'latest_product' : latest_product,
        'form' : form
    }
    return render(request, 'blog/post_detail.html', context)

#POST LIST FOR TECH
def TechList(request):
    techpost = Post.objects.filter(categories='tech', status='published')
    latest_product = Post.objects.filter(status='published', categories='product').order_by('-created')[0:3]
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #name = cd['name']
            #email_from = cd['email_from']
            subject_message = 'This is a mail from :{}, Email:{}, Subject:{}'.format(cd['name'], cd['email_from'], cd['subject'])
            message = cd['message']
            send_mail(subject_message, message, 'omotoshomicheal93@gmail.com', ['omotoshomicheal93@gmail.com'])
            messages.success(request, 'item saved')
            return redirect("posts")
    else:
        form = ContactForm()
    context = {
        'techpost' : techpost,
        'latest_product' : latest_product,
        'form' : form
    }
    return render(request, 'blog/single-tech.html', context)

#POST LIST FOR EDUCATION
def EducationList(request):
    educationpost = Post.objects.filter(categories='education', status='published')
    latest_product = Post.objects.filter(status='published', categories='product').order_by('-created')[0:3]
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #name = cd['name']
            #email_from = cd['email_from']
            subject_message = 'This is a mail from :{}, Email:{}, Subject:{}'.format(cd['name'], cd['email_from'], cd['subject'])
            message = cd['message']
            send_mail(subject_message, message, 'omotoshomicheal93@gmail.com', ['omotoshomicheal93@gmail.com'])
            messages.success(request, 'item saved')
            return redirect("posts")
    else:
        form = ContactForm()
    context = {
        'educationpost' : educationpost,
        'latest_product' : latest_product,
        'form' : form
    }
    return render(request, 'blog/education.html', context)

def ProductList(request):
    #educationpost = Post.objects.filter(categories='education', status='published')
    latest_product = Post.objects.filter(status='published', categories='product').order_by('-created')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #name = cd['name']
            #email_from = cd['email_from']
            subject_message = 'This is a mail from :{}, Email:{}, Subject:{}'.format(cd['name'], cd['email_from'], cd['subject'])
            message = cd['message']
            send_mail(subject_message, message, 'omotoshomicheal93@gmail.com', ['omotoshomicheal93@gmail.com'])
            messages.success(request, 'item saved')
            return redirect("posts")
    else:
        form = ContactForm()
    context = {
        #'educationpost' : educationpost,
        'latest_product' : latest_product,
        'form' : form
    }
    return render(request, 'blog/single-product.html', context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Login Successful")
                    return redirect("post_blog")
                else:
                    return HttpResponse("Account disabled")
            else:
                return HttpResponse("Invalid Account")
    else:
        form = LoginForm()

    latest_product = Post.objects.filter(status='published', categories='product').order_by('-created')[0:3]
    
    if request.method == 'POST':
        conform = ContactForm(request.POST)
        if conform.is_valid():
            cd = conform.cleaned_data
            #name = cd['name']
            #email_from = cd['email_from']
            subject_message = 'This is a mail from :{}, Email:{}, Subject:{}'.format(cd['name'], cd['email_from'], cd['subject'])
            message = cd['message']
            send_mail(subject_message, message, 'omotoshomicheal93@gmail.com', ['omotoshomicheal93@gmail.com'])
            messages.success(request, 'item saved')
            return redirect("posts")
    else:
        conform = ContactForm()
    return render(request, 'registration/login.html', {'form':form, 'latest_product' : latest_product, 'conform' : conform})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

