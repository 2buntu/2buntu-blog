#Contributing

Thank you for contributing to the [2buntu Django Blog][main-project-url] project. This guide is divided into two sections - reporting issues and working on features/bug-fixes.

## Reporting Issues

All issues, bugs, feature-requests, etc., should be filed and maintained at the [2buntu Django Blog's Issues page on Github][issues-page]. 

Please ensure clarity and follow the [OpenRespect Guidelines](http://openrespect.org/) when commenting, etc..

## Working on features/bug-fixes

This guide will help you with the different steps involved in contributing to the development of the [2buntu Django Blog][main-project-url] project. The overview of the guide is as follows:

1. Fork the project
2. Clone your forked repo
3. Checkout a new branch with the feature/bug-fix
4. Committing, pushing and submitting a pull request 
5. Deleting your branches (local and remotes)
6. Rebasing to stay synced with upstream

### Step 1: Fork the project

Head over to the [main project page][main-project-url] and click on the fork button.

[![main-repo-fork-screenshot](http://i.imgur.com/WyyPzQ3l.jpg?1)](http://i.imgur.com/WyyPzQ3.jpg?1)

I prefer changing my repo name from the original, if you want to do the same, you could do that from the **Settings** tab of your repo.

[![forked-repo-settings-screenshot-1](http://i.imgur.com/6T9yiEsl.jpg)](http://i.imgur.com/6T9yiEs.jpg)

[![forked-repo-settings-screenshot-2](http://i.imgur.com/2uTq3t4l.jpg)](http://i.imgur.com/2uTq3t4.jpg)

### Step 2: Clone your project

If you haven't setup GitHub to use SSH and would like to do so, please follow the [Generating SSH Keys](https://help.github.com/articles/generating-ssh-keys) guide on GitHub Help. For any other assistance with setup, please refer to the [GitHub Help Pages on SSH](https://help.github.com/categories/56/articles)

Copy the URL of your project to clone it.

[![git-clone-url-screenshot](http://i.imgur.com/RVW9POPl.jpg)](http://i.imgur.com/RVW9POP.jpg)

We use `git clone <repo-url>` to clone our forked repo locally and work with it. When you clone the repo, you'll notice that the `origin` remote is already added for you.

    #cloning
    nitin@jane-saucy:~$ git clone git@github.com:nitstorm/2buntu-Django-Blog-Nitin-fork.git
    Cloning into '2buntu-Django-Blog-Nitin-fork'...
    remote: Counting objects: 544, done.
    remote: Compressing objects: 100% (359/359), done.
    remote: Total 544 (delta 269), reused 382 (delta 157)
    Receiving objects: 100% (544/544), 625.20 KiB | 5.00 KiB/s, done.
    Resolving deltas: 100% (269/269), done.
    Checking connectivity... done
    
    #remote origin details
    nitin@jane-saucy:~$ cd 2buntu-Django-Blog-Nitin-fork/
    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git remote show origin 
    * remote origin
      Fetch URL: git@github.com:nitstorm/2buntu-Django-Blog-Nitin-fork.git
      Push  URL: git@github.com:nitstorm/2buntu-Django-Blog-Nitin-fork.git
      HEAD branch: master
      Remote branch:
        master tracked
      Local branch configured for 'git pull':
        master merges with remote master
      Local ref configured for 'git push':
        master pushes to master (up to date)

### Step 3: Checkout a new branch with the feature/bug-fix

To work on a feature/bug-fix, we create a branch and make the required changes to it. This is done with the `git checkout -b <branch-name>` command. Remember to keep the branch name meaningful to the feature/bug-fix you're working on.

    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git checkout -b contrib_guide
    Switched to a new branch 'contrib_guide'

As you can see, you're already switched to the new branch, so you can start working on the changes right away.

### Step 4: Committing, pushing and submitting a pull request

Once you have completed making the changes you wanted, you can commit the changes using `git commit -am "<commit-message>"`. Please ensure that the commit message is meaningful and reflects the changes you've made clearly.

    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git commit -am "Adds the contribution guide link to the README"
    [contrib_guide 577da9c] Adds the contribution guide link to the README
     1 file changed, 3 insertions(+)

Once the changes have been committed, next we push the changes to our remote origin with the `git push origin <branch-name>` command

    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git push origin contrib_guide Counting objects: 5, done.
    Delta compression using up to 6 threads.
    Compressing objects: 100% (3/3), done.
    Writing objects: 100% (3/3), 407 bytes | 0 bytes/s, done.
    Total 3 (delta 2), reused 0 (delta 0)
    To git@github.com:nitstorm/2buntu-Django-Blog-Nitin-fork.git
     * [new branch]      contrib_guide -> contrib_guide

Now that our changes are pushed to the remote origin, we are ready to submit a pull request to the remote upstream. When you send a pull request, one of the maintainers of the upstream project will review the changes and accept the pull request, effectively merging your branch with the upstream one and thus add your feature/bug-fix.

To submit a pull request, head over to your remote origin's repo on GitHub and you should see a big, honking button that says - **Compare & Pull request** for the branch you just pushed (GitHub is smart that way).  Go ahead and click that button.

[![pull-request-screenshot-1](http://i.imgur.com/38dlmz8l.jpg)](http://i.imgur.com/38dlmz8.jpg)

Please make sure any additional comments, images, etc., are added in the commenting section provided and click on the **Send pull request** button.

[![pull-request-screenshot-2](http://i.imgur.com/qvPTQZjl.jpg)](http://i.imgur.com/qvPTQZj.jpg)

You should see a screen similar to this once you have sent a pull request. This page will contain all the progress your pull request makes. Maintainers and other contributors can comment here and get clarifications or provide suggestions, etc.. 

*Note: You won't be able to see the **This pull request can be merged automatically** banner and buttons unless you are a maintainer of the [2buntu Django Blog][main-project-url]  *

[![pull-request-screenshot-3](http://i.imgur.com/lZO965ul.jpg)](http://i.imgur.com/lZO965u.jpg)

Once, you're pull request has been accepted and merged, you should see something similar to the following screen.

[![](http://i.imgur.com/GE0Ycnhl.jpg)](http://i.imgur.com/GE0Ycnh.jpg)

### Step 5: Deleting your branches

Once you've finished work on a branch, you might want to delete it in order to avoid cluttering up your workflow. You'll want to delete your branch in two places - your local repository (on your machine) and the remote repository (origin)

To delete a branch on your local repository, you can run the command `git branch -d <branch-name>` . Remember you need to switch to another branch before you can delete your current branch.

Let's assume I had worked on another branch called `fix_search_form` and submitted a pull request which was accepted and merged with the upstream repo. I run `git branch -d fix_search_form` and it's deleted from my local repository.

    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git branch -d fix_search_form 
    Deleted branch fix_search_form (was 2fab8fe).

To delete it from the remote repository - you can either do it from the command-line using `git push origin :<branch-name>` or from the page where the pull-request was submitted and merged.

    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git push origin :fix_search_form 
    To git@github.com:nitstorm/2buntu-Django-Blog-Nitin-fork.git
     - [deleted]         fix_search_form

### Step 6: Rebasing to stay synced with upstream

Now, after some time you notice some new changes in the upstream repo and you've thought of another feature/bug-fix that you want to contribute, but you're repo is not updated with the latest changes made to the upstream. This is where [Git Rebasing](http://git-scm.com/book/en/Git-Branching-Rebasing) comes into play. Why do we do a rebase instead of a simple pull? Because rebasing keeps the commit history clean.

First things first, let's add a new remote  called [upstream][upstream-url]. The command to do that is `git remote add upstream git@github.com:2buntu/2buntu-Django-Blog.git`

    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git remote add upstream git@github.com:2buntu/2buntu-Django-Blog.git

I prefer keeping my `master` branch up-to-date with the `upstream` branch, since it makes things easier for me to when I have to create a new branch for a feature/bug-fix. So let's switch to master first and check to see if we are up-to-date with the `upstream` branch.
    
    # To switch branches - git checkout <branch-name>
    
    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git checkout master
    Switched to branch 'master'
    
    # To view information about a remote - git remote show <branch-name>
    
    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git remote show upstream
    * remote upstream
      Fetch URL: git@github.com:2buntu/2buntu-Django-Blog.git
      Push  URL: git@github.com:2buntu/2buntu-Django-Blog.git
      HEAD branch: master
      Remote branch:
        master tracked
      Local ref configured for 'git push':
        master pushes to master (local out of date)

As we can see, the last line tells us that our local `master` branch is out of date. For confirmation's sake, let's look at the [upstream repo's commit page](https://github.com/2buntu/2buntu-Django-Blog/commits/master) and our own `git log`.

[![upstream-commits-screenshot](http://i.imgur.com/uPp44i9l.jpg)](http://i.imgur.com/uPp44i9.jpg)

Now, our `git log`:

    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git log --oneline -5
    2fab8fe Merge pull request #26 from nitstorm/fix_search_form
    38413cf Fixes form so search button appears next to input box
    ac7100e Finished implementing basic article editor (closes #7).
    ed7df0c Implemented 'save' and 'save and continue' buttons in editor.
    19e4328 Fixed bug that caused author of post to change depending on last edit.

Clearly, the last two commits made in the `upstream` have to be updated in our forked version as well. Let's update our local repository with the `git fetch upstream` command.

    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git fetch upstream
    remote: Counting objects: 1, done.
    remote: Total 1 (delta 0), reused 0 (delta 0)
    Unpacking objects: 100% (1/1), done.
    From github.com:2buntu/2buntu-Django-Blog
       2fab8fe..86d06a4  master     -> upstream/master

Now let's rebase with `git rebase upstream/master`

    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git rebase upstream/master 
    First, rewinding head to replay your work on top of it...
    Fast-forwarded master to upstream/master.

As you can see, the commits have been played back for you so you don't have to create a new commit or anything for updating your repo.
    
    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git log --oneline -5
    86d06a4 Merge pull request #27 from nitstorm/contrib_guide
    577da9c Adds the contribution guide link to the README
    2fab8fe Merge pull request #26 from nitstorm/fix_search_form
    38413cf Fixes form so search button appears next to input box
    ac7100e Finished implementing basic article editor (closes #7).

Finally, running a `git status` tells us that our local repo is two commits ahead of our remote origin. Those are the two commits that were updated in the upstream which we fetched earlier. Doing a simple push updates your remote origin and solves that.

    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git status
    # On branch master
    # Your branch is ahead of 'origin/master' by 2 commits.
    #   (use "git push" to publish your local commits)
    #
    nothing to commit, working directory clean
    nitin@jane-saucy:~/2buntu-Django-Blog-Nitin-fork$ git push origin master 
    Counting objects: 1, done.
    Writing objects: 100% (1/1), 287 bytes | 0 bytes/s, done.
    Total 1 (delta 0), reused 0 (delta 0)
    To git@github.com:nitstorm/2buntu-Django-Blog-Nitin-fork.git
       2fab8fe..86d06a4  master -> master

And that's it! Thank you for contributing to the [2buntu Django Blog][main-project-url] and happy git-ting :D




  [main-project-url]: https://github.com/2buntu/2buntu-Django-Blog
  [upstream-url]: git://git@github.com:2buntu/2buntu-Django-Blog.git
  [issues-page]: https://github.com/2buntu/2buntu-Django-Blog/issues