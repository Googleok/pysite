from django.db.models import F, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board


def boardlist(request, page=1, pagesize=5):
    start = (page - 1) * pagesize
    boardlist = Board.objects.all().order_by('-regdate')[start:start+pagesize]
    listcount = Board.objects.count()
    print(page)
    print(listcount)
    data = {
        'boardlist': boardlist,
        'currentpage': page,
        'listcount': listcount
    }
    print(boardlist)
    return render(request, 'board/list.html', data)


def board_writeform(request, id=0):
    if id == 0:
        data = {}
    else:
        data = {
            'id': id
        }
    return render(request, 'board/write.html', data)


def board_write(request):
    parentsNo = request.POST['parentsNo']
    board = Board()
    if request.POST['parentsNo'] == "":
        value = Board.objects.aggregate(max_groupno=Max('groupno'))
        max_groupno = 0 if value["max_groupno"] is None else value["max_groupno"]
        board.groupno = max_groupno
        board.orderno = 1
        board.depth = 0
    else:
        board.groupno = parentsNo

    board.user_id = int(request.session['authuser']['id'])
    board.title = request.POST['title']
    board.content = request.POST['content']

    board.save()

    return HttpResponseRedirect('/board')


def board_view(request, id=0):
    if id == 0:
        return HttpResponseRedirect('/board')

    qs = Board.objects.filter(id=id)
    qs.update(hit=F('hit')+1)
    board = qs[0]

    # board.hit = board.hit + 1
    # board.regdate = board.regdate
    #
    # board.save()
    data = {
        'board': board
    }
    return render(request, 'board/view.html', data)


def board_modifyform(request, id=0):
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


def board_reply(reequest, id=0):
    print('board_reply', id)
    board = Board.objects.filter(id=id)
    print(board)
    return HttpResponseRedirect('/board')

# def counter_max():
#     value = Counter.objects.aggregate(max_groupno=Max('groupno'))
#     max_groupno = 0 if value["max_groupno"] is None else value["max_groupno"]
#
#     value = Board.objects.aggregate(max_orderno=Max('orderno'))
#     max_orderno = 0 if value["max_orderno"] is None else value["max_orderno"]
#
#     return HttpResponse(f'max orderno:{max_orderno}')