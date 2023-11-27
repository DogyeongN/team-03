
from django.shortcuts import render, get_object_or_404, redirect
from .models import Prj
from .forms import PrjForm
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def prj_list(request):
    prjs = Prj.objects.all().order_by('-pk')

    page = request.GET.get('page', '1')
    paginator = Paginator(prjs, 10)
    
    try:
        prjs = paginator.page(page)
    except PageNotAnInteger:
        prjs = paginator.page(1)
    except EmptyPage:
        prjs = paginator.page(paginator.num_pages)    

    return render(
        request,
        'prj_posts/prj_list.html',
        {
            'prjs': prjs, 
            'page_obj': prjs        
        },
    )


def prj_detail(request, prj_id):
    prj = Prj.objects.get(id=prj_id)
    room_name_json = f'/chat/prj{prj_id}/'
    return render(request, 'prj_posts/prj_detail.html', {'prj': prj, 'room_name_json': room_name_json})


@login_required
def prj_create(request):
    if request.method == 'POST':
        form = PrjForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.author = request.user  # 사용자 정보를 글과 연결
            new_item.save()
            return HttpResponseRedirect('/prjs/')
    form = PrjForm()
    return render(request, 'prj_posts/prj_form.html', {'form': form})



@login_required
def prj_delete(request):
    prj_id = request.GET.get('id')
    
    if prj_id:
        item = get_object_or_404(Prj, pk=prj_id)
        
        if request.user != item.author:
            return HttpResponseForbidden("글을 삭제할 권한이 없습니다.")
        
        item.delete()
        
    return redirect('prj_list')


@login_required
def prj_update(request, id):
    item = get_object_or_404(Prj, pk=id)
    
    if request.user != item.author:
        return HttpResponseForbidden("글을 수정할 권한이 없습니다.")

    if request.method == "POST":
        form = PrjForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('prj_detail', prj_id=item.id)
    else:
        form = PrjForm(instance=item)

    return render(request, "prj_posts/prj_update.html", {'form': form})


#검색
def prjsearchResult(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        prjs = Prj.objects.filter(
            Q(prj_name__icontains=query) |
            Q(user_major__icontains=query) |
            Q(user_grade__icontains=query) |
            Q(post_content__icontains=query) |
            Q(prj_membernum__icontains=query) |
            Q(post_title__icontains=query)
        )
        return render(request, 'prj_posts/prj_search.html', {'query': query, 'prjs': prjs})
    else:
        return render(request, 'prj_posts/prj_search.html')
