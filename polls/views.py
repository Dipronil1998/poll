from django.shortcuts import render,get_object_or_404, redirect
from .forms import *
from .models import Poll, Choice, Vote
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse

# Create your views here.
@login_required()
def polls_list(request):
    all_polls = Poll.objects.all().order_by('-pub_date')
    search_term = ''
    if 'name' in request.GET:
        all_polls = all_polls.order_by('text')

    if 'date' in request.GET:
        all_polls = all_polls.order_by('pub_date')

    if 'search' in request.GET:
        search_term = request.GET['search']
        all_polls = all_polls.filter(text__icontains=search_term)

    paginator = Paginator(all_polls, 6)  
    page = request.GET.get('page')
    polls = paginator.get_page(page)

    context = {'polls': polls,'search_term': search_term,}
    return render(request, 'polls/polls_list.html', context)



@login_required()
def polls_add(request):
    if request.user.has_perm('polls.add_poll'):
        if request.method == 'POST':
            form = PollAddForm(request.POST)
            if form.is_valid:
                poll = form.save(commit=False)
                poll.owner = request.user
                poll.save()
                new_choice1 = Choice(poll=poll, choice_text=form.cleaned_data['choice1']).save()
                new_choice2 = Choice(poll=poll, choice_text=form.cleaned_data['choice2']).save()

                messages.success(
                    request, "Poll & Choices added successfully", extra_tags='alert alert-success alert-dismissible fade show')

                return redirect('polls:list')
        else:
            form = PollAddForm()

        context = {'form':form}
        return render(request, 'polls/add_poll.html', context)
    else:
        return render(request, 'polls/403.html')
        #return HttpResponse("Sorry but you don't have permission to do that!")

    


@login_required()
def list_by_user(request):
    all_polls = Poll.objects.filter(owner=request.user)
    paginator = Paginator(all_polls, 6)  

    page = request.GET.get('page')
    polls = paginator.get_page(page)

    context = {'polls': polls,}
    return render(request, 'polls/polls_list.html', context)


@login_required()
def poll_detail(request,poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if not poll.active:
        return render(request, 'polls/poll_result.html', {'poll': poll})
    count = poll.choice_set.count()
    choices=poll.choice_set.all
    print(count)
    context={'poll':poll,'loop_time': range(0, count),'choices':choices}
    return render(request, 'polls/poll_detail.html', context)  


@login_required
def polls_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid:
            form.save()
            messages.success(request, "Poll Updated successfully",
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect("polls:list")

    else:
        form = EditPollForm(instance=poll)
    context={'form': form, 'poll': poll,}
    return render(request, "polls/poll_edit.html", context)


@login_required
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST, instance=choice)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice Updated successfully", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:edit', poll.id)
    else:
        form = ChoiceAddForm(instance=choice)
    context = {'form': form,'edit_choice': True,'choice': choice,}
    return render(request, 'polls/add_choice.html', context)




@login_required
def polls_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')
    poll.delete()
    messages.success(request, "Poll Deleted successfully",
                     extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("polls:list")

@login_required
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('home')
    choice.delete()
    messages.success(
        request, "Choice Deleted successfully", extra_tags='alert alert-success alert-dismissible fade show')
    return redirect('polls:edit', poll.id)


@login_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice added successfully", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:edit', poll.id)
    else:
        form = ChoiceAddForm()
    context = {'form': form,}
    return render(request, 'polls/add_choice.html', context)


@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')
    if not poll.uservote(request.user):
        messages.error(
            request, "You already voted this poll", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("polls:list")

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(user=request.user, poll=poll, choice=choice)
        vote.save()
        return render(request, 'polls/poll_result.html', {'poll': poll})
    else:
        messages.error(
            request, "No choice selected", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("polls:detail", poll_id)
    return render(request, 'polls/poll_result.html', {'poll': poll})
    


@login_required
def endpoll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if poll.active is True:
        poll.active = False
        poll.save()
        return render(request, 'polls/poll_result.html', {'poll': poll})
    else:
        return render(request, 'polls/poll_result.html', {'poll': poll})



    
