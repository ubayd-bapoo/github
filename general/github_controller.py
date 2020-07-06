from github import Github

from django.conf import settings

from allauth.socialaccount.models import SocialToken


# ==============================================================================
class GithubController(object):
    # --------------------------------------------------------------------------
    def __init__(self, user):
        token = SocialToken.objects.get(account__user=user, account__provider='github')
        self._github = Github(token.token)
        self._repos = self._github.get_user().get_repos()

    # --------------------------------------------------------------------------
    def get_gituhub_details(self):
        """"
        Gets details from Github and return them.
        """
        github_details = {}
        github_details['repos'] = self._get_repos()
        github_details['branches'] = self._get_branches()
        return github_details

    # --------------------------------------------------------------------------
    def _get_repos(self):
        repos = []
        for repo in self._repos:
            repos.append([repo.name, repo.full_name])
        return repos

    # --------------------------------------------------------------------------
    def _get_branches(self):
        branches = {}
        for repo in self._repos:
            for repo_branches in repo.get_branches():
                branches.setdefault(repo.name, [])
                branches[repo.name].append(repo_branches.name)
        return branches

    # --------------------------------------------------------------------------
    def _get_repo(self, full_name):
        return self._github.get_repo(full_name)

    # --------------------------------------------------------------------------
    def _get_branch(self, repo, branch_name):
        return repo.get_branch(branch_name)

    # --------------------------------------------------------------------------
    def validate_branches(self, repo, source_branch, target_branch):
        """"
        Validates that the branches are from the same repo.
        """
        if source_branch == target_branch:
            return False

        # repo has the full name of the repo, we just want the actual repo name and check if that name is in the branch name
        if (repo.split('/')[1] not in source_branch) or (repo.split('/')[1] not in target_branch):
            return False

        return True

    # --------------------------------------------------------------------------
    def merge_branches(self, merge_request):
        """"
        Merges the source branch to the target branch.
        """
        repo = self._get_repo(merge_request.repo)
        source_branch = self._get_branch(repo, merge_request.source_branch)
        target_branch = self._get_branch(repo, merge_request.target_branch)

        try:
            repo.merge(target_branch.name, source_branch.commit.sha, "merge %s to %s" % (source_branch.name, target_branch.name))
            return True
        except:
            return False
