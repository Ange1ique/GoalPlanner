from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from django import forms
from .models import Goals, SubGoals, Activities

class AddForm(forms.ModelForm):
    class Meta:
        model = Goals
        exclude = ["user","progress", "start_date", "end_date", ]
        widgets = {'description': forms.Textarea(attrs={'rows':4, 'cols':15}),}

    def __init__(self, *args, **kwargs):
        super(AddForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

def is_empty_form(form):
    """
    A form is considered empty if it passes its validation,
    but doesn't have any data.

    This is primarily used in formsets, when you want to
    validate if an individual form is empty (extra_form).
    """
    if form.is_valid() and not form.cleaned_data:
        return True
    else:
        # Either the form has errors (isn't valid) or
        # it doesn't have errors and contains data.
        return False

def is_form_persisted(form):
    """
    Does the form have a model instance attached and it's not being added?
    e.g. The form is about an existing Subgoal whose data is being edited.
    """
    if form.instance and not form.instance._state.adding:
        return True
    else:
        # Either the form has no instance attached or
        # it has an instance that is being added.
        return False

# The formset for editing the Activities that belong to a Subgoal.
ActivityFormset = inlineformset_factory(
                            SubGoals,
                            Activities,
                            fields=('activity_title',),
                            extra=1)


class BaseSubgoalsWithActivitiesFormset(BaseInlineFormSet):
    """
    The base formset for editing Subgoals belonging to a Goal, and the
    Activities belonging to those Subgoals.
    """

    def add_fields(self, form, index):
        super().add_fields(form, index)

        # Save the formset for a Subgoal's Activity in the nested property.
        form.nested = ActivityFormset(
                                instance=form.instance,
                                data=form.data if form.is_bound else None,
                                prefix='activities-%s-%s' % (
                                    form.prefix,
                                    ActivityFormset.get_default_prefix()),
                                )

    def is_valid(self):
        """
        Also validate the nested formsets.
        """
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def clean(self):
        """
        If a parent form has no data, but its nested forms do, we should
        return an error, because we can't save the parent.
        For example, if the Subgoal form is empty, but there are Activities.
        """
        super().clean()

        for form in self.forms:
            if not hasattr(form, 'nested') or self._should_delete_form(form):
                continue

            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=_('You are trying to add activities to a subgoal which '
                            'does not yet exist. Please add information '
                            'about the subgoal and add the activities again.'))

    def save(self, commit=True):
        """
        Also save the nested formsets.
        """
        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

    def _is_adding_nested_inlines_to_empty_form(self, form):
        """
        Are we trying to add data in nested inlines to a form that has no data?
        e.g. Adding Activities to a new Subgoal whose data we haven't entered?
        """
        if not hasattr(form, 'nested'):
            # A basic form; it has no nested forms to check.
            return False

        if is_form_persisted(form):
            # We're editing (not adding) an existing model.
            return False

        if not is_empty_form(form):
            # The form has errors, or it contains valid data.
            return False

        # All the inline forms that aren't being deleted:
        non_deleted_forms = set(form.nested.forms).difference(
            set(form.nested.deleted_forms)
        )


        # At this point we know that the "form" is empty.
        # In all the inline forms that aren't being deleted, are there any that
        # contain data? Return True if so.
        return any(not is_empty_form(nested_form) for nested_form in non_deleted_forms)


# This is the formset for the Subgoal belonging to a Goal and the
# Activities belonging to those Subgoals.
#
# You'd use this by passing in a Goal:
#     GoalsSubgoalsWithActivitiesFormset(**form_kwargs, instance=self.object)
GoalsSubgoalsWithActivitiesFormset = inlineformset_factory(
                                Goals,
                                SubGoals,
                                formset=BaseSubgoalsWithActivitiesFormset,
                                # We need to specify at least one Subgoal field:
                                fields=('subgoal_title',),
                                extra=1,
                                # If you don't want to be able to delete Goals:
                                #can_delete=False
                            )
