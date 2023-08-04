from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Comment
from .forms import CommentForm
from django.contrib import messages

@login_required
def add_comment(request, product_id):
    """ A view to add a comment to a product """
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.rating = request.POST.get('stars')
            comment.save()
            messages.success(request, 'Successfully added comment!')
            return redirect('product_detail', product_id=product_id)
        else:
            messages.error(request, 'Failed to add comment. Please ensure the form is valid.')
    else:
        form = CommentForm()

    context = {
        'form': form,
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.user and not request.user.is_superuser:
        messages.error(request, 'You are not authorized to edit this comment.')
        return redirect('product_detail', product_id=comment.product.id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated comment!')
            return redirect('product_detail', product_id=comment.product.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comments/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.user and not request.user.is_superuser:
        messages.error(request, 'You are not authorized to delete this comment.')
        return redirect('product_detail', product_id=comment.product.id)
    product_id = comment.product.id
    comment.delete()
    messages.success(request, 'Successfully deleted comment!')
    return redirect('product_detail', product_id=product_id)
