GitHub Issues Command Line Interface
====================================

Would you like to aviod using a browser when managing "Issues" for your 
projects hosted on GutHub? Do you prefer using emacs or vim as your text editor
of choice? Do you prefer your entire workflow to remain on the command line 
when developing? Then the GitHub Issues Command Line Interface may be for you.
 
All attributes of an "issue" can be viewed and edited right from the command 
line. In fact inspiration was taken from projects like TicGit-ng_ and 
git-issues_. However, inlike those projects, which store the issues in a 
special branch on the Repo, this project uses GitHub's API to store issues on 
GitHub's servers. Therefore, your users can create and comment on issues on 
GitHub's nice web interface without the need to install git or work from the 
command line. At the same time, you can stay in your prefered command line 
development environment without ever needing a browser to review, edit, label, 
comment on, or open/close issues.

.. _TicGit-ng: https://github.com/jeffWelling/ticgit#readme
.. _git-issues: https://github.com/jwiegley/git-issues#readme

.. note::
   This is **beta** software. Various parts are not fully implemented yet and/or
   may be buggy. Additionaly, the API (including command line arguments) is 
   subject to change without notice. Consider yourself warned.

Documention
-----------

The entire command line interface is documented within the command's help 
interface. Simply use the ``-h/--help`` flag from the command line for usage 
documentation::

    $ issues.py -h

Included in the help is a list of subcommands. You may also get help on each 
subcommand like this::

    $ issues.py subcommand -h

where "subcommand" is replaced with the appropriate subcommand you would like 
help with.

Workflow
--------

It is expected that the issues command will be run from within a Git 
repositories' working tree. In fact, an error will be generated if you try to 
use the command outside of a working three. As long as the repo's "remote" for 
the "master" branch points to a writable GitHub hosted repo (see Configuration 
below for specifics), the issues command will read from and write to that 
repo's issues.
    
Assuming everything is configured properly, ``cd`` into our working tree and 
view a list of open issues::

    $ cd myproject
    $ issues.py list
     5 Bug in foo
     2 Typo in Docs

Suppose we want to view the new issue someone reported as issue #5 listed 
above::

    $ issues.py show 5
    #5 Bug in foo

    Whenever I pass "bar" to `foo()` it gives me an error.

Obliviously, the original reporter did not provide enough information. Let's 
add a comment asking for clarification::

    $ issues.py comment --new -m "What error does it give you?" 5

Note that if we wanted to provide a longer comment and perhaps add some 
formatting, just like Git's ``commit`` command, we could have left off the 
``-m/--message`` flag and the text editor defined by GIT_EDITOR would have been
opened for us. Upon saving and closing, the comment would then be forwarded to 
GitHub.

Now, let's check to see if we have a response to our request for more info::
    
    $ issues.py comments --list 5
    #1 What error does it give you?
    #2 It says "Bad Foo" when I do `foo("bar")`.

After pushing our fix, which included the text "fixed #5" in your commit 
message, GitHub should have closed the issue automaticaly for us. Lets check::
    
    $ issues.py list
     2 Typo in Docs

Sure enough, Issue #5 is no longer listed as an open issue. Lets make sure and 
list all closed issues::

    $ issues.py list --state closed
     5 Bug in foo
     4 Some weirdness
     3 Silly typo
     1 A bad issue description

Excellant! Now let's look at the alledged typo in the docs (issue #2)::

    $ issues.py show 2
    #2 Typo in Docs

    What is this "foo"? My spell checker keeps tripping up on it.

Hmm, err, well, that's not a bug. Guess we need to educate our users::

    $ issue.py comment --new -m '"Foo" is sometimes used as a placeholder 
    name in computer programming or computer-related documentation. See 
    [Wikipedia](https://en.wikipedia.org/wiki/Foobar) for more info.'

And now we can close the issue manually::

    $ issue.py edit --state closed 2

Setup and Installation
----------------------

Dependencies
~~~~~~~~~~~~

The issues command is written in Python and relies on Git's command line 
interface, so at a minimum the following needs to be installed on your system:

* Git_
* `Python 2.7+`_

.. _Git: http://git-scm.com/
.. _Python 2.7+: http://python.org

No doubt, some of you may have older versions of python installed on your 
system. Unfortunately, gh-issues uses some features that were only introduced 
in Python 3 (and backported to version 2.7). Perhaps in the future, some of 
those features will be backported within the gh-issues project to at least 
support Python 2.6. Patches (merge requests) are certainly welcome. It is not 
likely that gh-issues will ever work on any Python versions earlier than 2.6.

Additionaly, the following python libraries are needed (and should be installed
automaticaly when you install gh-issues):

* PyGithub_
* Requests_

.. _PyGithub: http://vincent-jacques.net/PyGithub
.. _Requests: http://docs.python-requests.org/en/latest/index.html

Configuration
~~~~~~~~~~~~~
After running ``pip install gh-issues-cli``, the issues command should have 
been installed on your path. If not, use the appropriate means to rectify that 
on your system.

GitHub's API requires authentication to write data to GitHub (and read from 
private repos). As the API works over http(s) rather than ssh, we cannot use 
git's standard authentication methods. The API allows two alternatives:

* Provide a username and password with every request.
* Provide an OAuth token with every request.

Because gh-issues is a command line program, there is no long-running-process 
which can hold the username and password in memory between requests. Therefore,
the username and password would need to be provided with every command. While 
this is possable, it can become rather tedious. Therefore, an OAuth token can 
be created and stored for later use. To create a token... **[TODO]** (write 
code and docs) **[/TODO]**

.. note::
   If you push and pull from GitHub over http(s), and you don't want to use an 
   OAuth token, gh-issues will extract your GitHub username from your git 
   config and will only prompt for your password. The workflow becomes very 
   similar to using git over http(s).

   Be aware that gh-issues requires the password for *every command*, whereas 
   git over http(s) only requires a password when you push or pull, not for 
   every command (commit, log, status, add, rebase, ...).

License
-------

| Copyright (c) 2012, Waylan Limberg
| All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this 
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, 
  this list of conditions and the following disclaimer in the documentation 
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
