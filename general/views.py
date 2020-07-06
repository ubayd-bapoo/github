from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . import models

from general.github_controller import GithubController
from general.email_interface import EmailInterface

# ------------------------------------------------------------------------------
def home(request):
    if request.user.is_authenticated:
        github = None
        github_details = {}
        try:
            # If there's a break in connection between the system and Github, the system will handle it.
            github = GithubController(request.user)
            github_details = github.get_gituhub_details()
        except:
            messages.warning(request, 'Error while getting Github details. Reload page')

        if request.method == 'POST':
            if github and github.validate_branches(request.POST['repo'], request.POST['source_branch'], request.POST['target_branch']):
                source_branch = request.POST['source_branch'].split(': ')[1]
                target_branch = request.POST['target_branch'].split(': ')[1]

                merge_request = models.MergeRequest.objects.get_or_create(user=request.user,
                                                                          title=request.POST['title'],
                                                                          repo=request.POST['repo'],
                                                                          source_branch=source_branch,
                                                                          target_branch=target_branch,
                                                                          assign_email=request.POST['email'],)

                email_interface = EmailInterface(request.user)
                email_interface.create_request(merge_request[0], request.META['HTTP_HOST'])
                messages.success(request, 'Merge Request Created')
            else:
                messages.warning(request, 'Repo or Branches not matching. Select the correct Branches from the Repo')

        return render(request, 'index.html', {'nav_item_heading': 'Create Merge Request',
                                              'github_details': github_details})
    else:
        return render(request, 'registration/login.html')

# ------------------------------------------------------------------------------
@login_required
def merge_request(request, merge_request_id=None):
    view_merge = True
    merge_request = None
    if not merge_request_id:
        view_merge = False
        messages.warning(request, 'No merge request ID supplied. Check your emails for the URL with the ID.')
    else:
        try:
            merge_request = models.MergeRequest.objects.get(id=merge_request_id)
            if merge_request.assign_email != request.user.email:  # Only assigned members can access the merge request
                view_merge = False
                messages.warning(request, 'You are not assigned to this Merge Request.')
        except:
            messages.warning(request, 'Could not find Merge Request')

    return render(request, 'merge_request.html', {'nav_item_heading': 'Approve Merge Request',
                                                  'merge_request': merge_request,
                                                  'view_merge': view_merge})

# ------------------------------------------------------------------------------
@login_required
def merge_request_update(request, merge_request_id=None, status=None):
    view_merge = True
    merge_request = None
    email_interface = EmailInterface(request.user)

    if not merge_request_id:
        view_merge = False
        messages.warning(request, 'No merge request ID supplied. Check your emails for the URL with the ID.')
    else:
        try:
            merge_request = models.MergeRequest.objects.get(id=merge_request_id)
        except:
            messages.warning(request, 'Could not find Merge Request')

        if status == 'merge':
            try:
                github = GithubController(request.user)
                merge_status = github.merge_branches(merge_request)
                if merge_status:  # if something goes wrong between the merging we will catch it hear
                    email_interface.approve_request(merge_request)
                    merge_request.accept = True
                    merge_request.save()
                    messages.success(request, 'Successfully Merged Branches')
                else:
                    messages.success(request, 'Failed Merge Branches')
            except:
                messages.warning(request, 'Error connecting to Github. Reload page')

        elif status == 'reject':
            messages.warning(request, 'Merge Request Rejected')
            merge_request.accept = False  # We save this for audit reasons
            merge_request.save()
            email_interface.reject_request(merge_request)

    return render(request, 'merge_request.html', {'nav_item_heading': 'Approve Merge Request',
                                                  'merge_request': merge_request,
                                                  'view_merge': view_merge})
