from django.db.models import F, Max, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils import timezone

from board.models import Board
from hitcount.models import HitCount


def boardlist(request, page=1, pagesize=10):
    start = (page - 1) * pagesize
    boardlist = Board.objects.all().order_by('-groupno', 'orderno')[start:start+pagesize]
    listcount = Board.objects.count()
    data = {
        'boardlist': boardlist,
        'currentpage': page,
        'listcount': listcount
    }
    return render(request, 'board/list.html', data)


def boardsearchlist(request, page=1, pagesize=10):
    start = (page - 1) * pagesize
    kwd = request.POST['kwd']
    searchlist = Board.objects.filter(Q(title__contains=kwd) | Q(content__contains=kwd)).order_by('-groupno', 'orderno')[start:start+pagesize]
    listcount = Board.objects.filter(Q(title__contains=kwd) | Q(content__contains=kwd)).count()
    data = {
        'boardlist': searchlist,
        'currentpage': page,
        'listcount': listcount
    }
    return render(request, 'board/list.html', data)


def board_writeform(request, id=0):
    try:
        request.session['authuser']
    except KeyError as e:
        print(e)
        return HttpResponseRedirect('/user/loginform')

    if id == 0:
        data = {}
    else:
        data = {
            'id': id
        }
    return render(request, 'board/write.html', data)


def board_write(request):
    parents_id = request.POST['parentsNo']
    board = Board()
    if parents_id == "":
        value = Board.objects.aggregate(max_groupno=Max('groupno'))
        max_groupno = 0 if value["max_groupno"] is None else value["max_groupno"]
        board.groupno = max_groupno + 1
        board.orderno = 1
        board.depth = 0
    else:
        value = Board.objects.filter(id=parents_id)

        # orderno를 하나씩 밀어주기
        Board.objects.filter(orderno__gte=value[0].orderno + 1).update(orderno=F('orderno') + 1)

        board.groupno = value[0].groupno
        board.orderno = value[0].orderno + 1
        board.depth = value[0].depth + 1

    board.user_id = int(request.session['authuser']['id'])
    board.title = request.POST['title']
    board.content = request.POST['content']

    board.save()

    return HttpResponseRedirect('/board')


def get_client_ip(request):
    x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forward_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def board_view(request, id=0):
    if id == 0:
        return HttpResponseRedirect('/board')
    try:
        # user ip 주소 가져오기
        ip = get_client_ip(request)
        # ip주소와 게시글 번호로 기록을 조회함
        hits = HitCount.objects.get(ip=ip, post=id)
    except Exception as e:
        print(e)
        # 처음 게시글을 조회한 경우엔 조회 기록이 없음
        hits = HitCount(ip=ip, post_id=id)
        qs = Board.objects.filter(id=id)
        qs.update(hit=F('hit')+1)
        board = qs[0]
        hits.save()
    else:
        # 조회 기록은 있으나, 날짜가 다른 경우
        if not hits.date == timezone.now().date():
            qs = Board.objects.filter(id=id)
            qs.update(hit=F('hit') + 1)
            board = qs[0]
            hits.date = timezone.now()
            hits.save()
        # 날짜가 같은 경우
        else:
            qs = Board.objects.filter(id=id)
            board = qs[0]
            print(str(ip) + ' has already hit this post. \n\n')

    data = {
        'board': board,
        'page': request.GET['page']
    }
    return render(request, 'board/view.html', data)


def board_modifyform(request, id=0):
    try:
        request.session['authuser']
    except KeyError as e:
        print(e)
        return HttpResponseRedirect('/user/loginform')

    if id == 0:
        return HttpResponseRedirect('/board')

    qs = Board.objects.filter(id=id)
    board = qs[0]

    data = {
        'board': board
    }
    return render(request, 'board/modify.html', data)


def board_modify(request):
    if id == 0:
        return HttpResponseRedirect('/board')
    board_id = request.POST['id']
    print(board_id)
    qs = Board.objects.filter(id=board_id)
    qs.update(title=request.POST['title'])
    qs.update(content=request.POST['content'])

    return HttpResponseRedirect('/board/view/'+str(board_id))


def board_delete(request, id=0):
    board = Board.objects.filter(id=id)
    board.delete()
    return HttpResponseRedirect('/board')

# def counter_max():
#     value = Counter.objects.aggregate(max_groupno=Max('groupno'))
#     max_groupno = 0 if value["max_groupno"] is None else value["max_groupno"]
#
#     value = Board.objects.aggregate(max_orderno=Max('orderno'))
#     max_orderno = 0 if value["max_orderno"] is None else value["max_orderno"]
#
#     return HttpResponse(f'max orderno:{max_orderno}')