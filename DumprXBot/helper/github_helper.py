from github import Github, GithubException, InputGitAuthor, UnknownObjectException

from DumprXBot import GH_EMAIL, GH_TOKEN, GH_USER, LOGGER, PR_REPO, PR_REPO_BRANCH


class __Github:
    def __init__(self):
        self.g = Github(login_or_token=GH_TOKEN)
        self.committer = InputGitAuthor(name=GH_USER, email=GH_EMAIL)
        self.user = self.g.get_user()

    def cleanup(self):
        try:
            repo_name = PR_REPO.split("/")[1]
            old = self.g.get_repo(f"{GH_USER}/{repo_name}")
            LOGGER.info("Cleanning up old repo...")
            old.delete()
        except UnknownObjectException:
            pass

    def fork(self, repo):
        try:
            self.cleanup()
            self.repo_fork = self.g.get_repo(repo)
            LOGGER.info("Making fork of latest repo...")
            return self.user.create_fork(self.repo_fork)
        except GithubException as err:
            LOGGER.error(err)

    def make_pr(self, link, user):
        forkee = self.fork(PR_REPO)
        # contents = forkee.get_contents("ROM_URL.txt")
        contents = self.g.get_repo(PR_REPO).get_contents("ROM_URL.txt")
        try:
            forkee.update_file(
                path=contents.path,
                message="CI: New dump [BOT]",
                content=link,
                sha=contents.sha,
                branch=PR_REPO_BRANCH,
                committer=self.committer,
            )
            LOGGER.info("Making pull request...")
            return self.repo_fork.create_pull(
                title="New dump request [BOT]",
                body=user,
                base=f"{PR_REPO_BRANCH}",
                head=f"{GH_USER}:{PR_REPO_BRANCH}",
                maintainer_can_modify=True,
            )
        except GithubException as err:
            LOGGER.error(err)
            if err_msg := err.data["message"]:
                return err_msg
            else:
                return "Something fucked while making Pull Request, plox check logs."


GithubHandler = __Github()
