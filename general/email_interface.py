from django.core.mail import send_mail

from django.conf import settings


# ==============================================================================
class EmailInterface(object):
    # --------------------------------------------------------------------------
    def __init__(self, user):
        self._user = user

    # --------------------------------------------------------------------------
    def _send_email(self, email_details):
        send_mail(email_details['subject'], email_details['msg'], self._user.email, [email_details['to']])

    # --------------------------------------------------------------------------
    def create_request(self, merge_request, host):
        """"
        Once a request has been created. This function send an email informing the assignee that a merge request has been created.
        """
        email_details = {}
        email_details['subject'] = 'Merge Request Create: %s' % merge_request.title
        email_details['msg'] = 'You have been requested to review the following merge request:\n' \
              'Title: %s\n' \
              'Repo: %s\n' \
              'Source Branch: %s\n' \
              'Target Branch: %s\n' \
              'URL: %s/merge_request/%s/' % (merge_request.title, merge_request.repo,
                                             merge_request.source_branch, merge_request.target_branch, host, merge_request.id)
        email_details['to'] = merge_request.assign_email

        self._send_email(email_details)

    # --------------------------------------------------------------------------
    def reject_request(self, merge_request):
        """"
        Once a request has been rejected. This function send an email informing the user that created the reuqest that the
        merge request has been rejected.
        """
        email_details = {}
        email_details['subject'] = 'Merge Request Rejected: %s' % merge_request.title
        email_details['msg'] = 'The following Merge Request has been rejected:\n' \
              'Title: %s\n' \
              'Repo: %s\n' \
              'Source Branch: %s\n' \
              'Target Branch: %s' % (merge_request.title, merge_request.repo,
                                     merge_request.source_branch, merge_request.target_branch)
        email_details['to'] = merge_request.user.email

        self._send_email(email_details)

    # --------------------------------------------------------------------------
    def approve_request(self, merge_request):
        """"
        Once a request has been approved. This function send an email informing the user that created the request that the
        merge request has been approved.
        """
        email_details = {}
        email_details['subject'] = 'Merge Request Approved: %s' % merge_request.title
        email_details['msg'] = 'The following Merge Request has been approved:\n' \
              'Title: %s\n' \
              'Repo: %s\n' \
              'Source Branch: %s\n' \
              'Target Branch: %s' % (merge_request.title, merge_request.repo,
                                     merge_request.source_branch, merge_request.target_branch)
        email_details['to'] = merge_request.user.email

        self._send_email(email_details)
