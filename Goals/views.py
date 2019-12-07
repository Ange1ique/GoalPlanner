from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View, TemplateView, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from . import models
from .forms import AddForm, GoalsSubgoalsWithActivitiesFormset
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class GoalsSubgoalsUpdateView(LoginRequiredMixin, SingleObjectMixin, FormView):
    """
    For adding subgoals to a goal, or editing them.
    """

    model = models.Goals
    template_name = 'goals_subgoals_update.html'

    def get(self, request, *args, **kwargs):
        # The goal we're editing:
        self.object = self.get_object(queryset=models.Goals.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # The goal we're uploading for:
        self.object = self.get_object(queryset=models.Goals.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        """
        Use our big formset of formsets, and pass in the Goals object.
        """
        return GoalsSubgoalsWithActivitiesFormset(
                            **self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes were saved.'
        )

        return JsonResponse('success', safe=False)

    def form_invalid(self, form):
        return JsonResponse('error', safe=False)


class AllGoalsView(LoginRequiredMixin, TemplateView):
    template_name = 'goals.html'
    form_class = AddForm
    login_url = '/'

    # get data from all models
    def get_context_data(self, *args, **kwargs):
        context = super(AllGoalsView, self).get_context_data(*args, **kwargs)
        context['goals_page'] = 'active'
        context['allgoals'] = models.Goals.objects.filter(user=self.request.user)
        context['allsubgoals'] = models.SubGoals.objects.filter(user=self.request.user)
        context['allactivities'] = models.Activities.objects.filter(user=self.request.user)
        # all subgoal_id's of activities
        actsubgoalid = []
        for activity in context['allactivities']:
            actsubgoalid.append(activity.subgoal.pk)
        context['actsubgoalid'] = actsubgoalid
        # calculate progress of each subgoal
        subgoalprogress = {}
        for subgoal in context['allsubgoals']:
            subgoalprogress[subgoal.pk] = 0
            counter = 0
            for activity in context['allactivities']:
                if subgoal.pk == activity.subgoal.pk:
                    subgoalprogress[subgoal.pk] += activity.progress
                    counter += 1
            if subgoalprogress[subgoal.pk] != 0:
                subgoalprogress[subgoal.pk] = subgoalprogress[subgoal.pk]/counter
                subgoalprogress[subgoal.pk] = int(subgoalprogress[subgoal.pk])
        context['subgoalprogress'] = subgoalprogress
        # calculate progress of each goal
        goalprogress = {}
        for goal in context['allgoals']:
            goalprogress[goal.pk] = 0
            counter = 0
            for subgoal in context['allsubgoals']:
                if goal.pk == subgoal.goal.pk:
                    goalprogress[goal.pk] += subgoalprogress[subgoal.pk]
                    counter += 1
            if goalprogress[goal.pk] != 0:
                goalprogress[goal.pk] = goalprogress[goal.pk]/counter
                goalprogress[goal.pk] = int(goalprogress[goal.pk])
        context['goalprogress'] = goalprogress
        return context

def save_goal_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            data['form_is_valid'] = True
            goals = models.Goals.objects.all()
            data['html_goal_list'] = render_to_string('goal_list.html', {'goals': goals})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required
def goal_create(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
    else:
        form = AddForm()
    return save_goal_form(request, form, 'goal_create.html')

@login_required
def goal_update(request, pk):
    goal = get_object_or_404(models.Goals, pk=pk)
    if request.method == 'POST':
        form = AddForm(request.POST, instance=goal)
    else:
        form = AddForm(instance=goal)
    return save_goal_form(request, form, 'goal_update.html')

@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(models.Goals, pk=pk)
    data = dict()
    if request.method == 'POST':
        goal.delete()
        data['form_is_valid'] = True
        goals = models.Goals.objects.all()
        data['html_goal_list'] = render_to_string('goal_list.html', {'goals': goals})
    else:
        context = {'goal': goal}
        data['html_form'] = render_to_string('goal_delete.html',
            context, request=request, )
    return JsonResponse(data)

@login_required
def subgoal_delete(request, pk):
    subgoal = get_object_or_404(models.SubGoals, pk=pk)
    data = dict()
    if request.method == 'POST':
        subgoal.delete()
        data['form_is_valid'] = True
    else:
        context = {'subgoal': subgoal}
        data['html_form'] = render_to_string('subgoal_delete.html',
            context, request=request, )
    return JsonResponse(data)

@login_required
def activity_delete(request, pk):
    activity = get_object_or_404(models.Activities, pk=pk)
    data = dict()
    if request.method == 'POST':
        activity.delete()
        data['form_is_valid'] = True
    else:
        context = {'activity': activity}
        data['html_form'] = render_to_string('activity_delete.html',
            context, request=request, )
    return JsonResponse(data)

@login_required
def check_activity(request):
    if request.method == 'POST':
        activity_id = request.POST['activity_id']
        progress = request.POST['progress']
        check = get_object_or_404(models.Activities, pk=activity_id)
        check.progress = progress
        check.save(update_fields=["progress"])
        return JsonResponse('success', safe=False)
    else:
        return JsonResponse('error')
