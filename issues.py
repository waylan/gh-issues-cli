#!/usr/bin/env python

from __future__ import print_function
import argparse
import os
import sys
import re
from tempfile import mkstemp
from subprocess import check_call, check_output, CalledProcessError

try:
    if check_output('git rev-parse --is-inside-working-tree', shell=True) == 'true' or \ 
       check_output('git rev-parse --is-inside-git-dir', shall=True) == 'true':
        GIT_EDITOR = check_output('git var GIT_EDITOR', shell=True)
        GIT_PAGER = check_output('git var GIT_PAGER', shell=True)
        GIT_DIR = check_output('git rev-parse --git-dir', shall=True)
        GIT_USER_NAME = check_output('git config user.name', shell=True)
        GIT_USER_EMAIL = check_output('git config user.email', shell=True)
        GIT_REMOTE = check_output('git config branch.master.remote', shell=True) # Assume "master"
        GIT_REMOTE_URL = check_output('git config remote.%s.url' % GIT_REMOTE, shell=True)
    else:
        sys.exit('fatal: Not a git repository (or any of the parent directories)')
except CalledProcessError, e:
    sys.exit("Git not configured properly: %s" % e)

##################################################
# Utility Functions
##################################################

def run_editor(txt):
    """ Edit the given text in the system default text editor. """        
    
    fd, tmpfile = mkstemp()
    os.write(fd, txt or "")
    os.close(fd)
    
    try:
        check_call("%s %s" % (GIT_EDITOR, tmpfile), shell=True)
    except CalledProcessError, e:
        os.unlink(tmpfile)
        sys.exit("Action aborted: %s" % e)

    contents = open(tmpfile).read()
    os.unlink(tmpfile)
    return contents

ARG_RE = re.compile(r'^([A-Z]+): (.*)')

def get_message(args, template, context=None):
    """ Get message from EDITOR. """
    if context is None:
        context = {}
    for k, v in args.items():
        if v is None:
            v = ''
        elif k == 'labels':
            v = ' '.join(v)
        context[k] = v
    message = run_editor(template % context)
    body = []
    end_of_body = False
    for line in message.split('\n'):
        if not line.startswith('#') and not end_of_body:
            body.append(line)
        else:
            end_of_body = True
            m = ARG_RE.match(line)
            if m:
                key = m.group(1).lower()
                value = m.group(2)
                if key == 'labels':
                    value = value.split()
                args[key] = value
    args['body'] = '\n'.join(body).strip()
    if not args['body']:
        sys.exit("Action aborted! Message is empty.")

def clean_args(args, exclude_keys=[], exclude_values=[]):
    """ Remove unwanted keys and/or values from args. """
    d = {}
    for k, v in args._get_kwargs():
        if  k not in exclude_keys and v not in exclude_values:
            d[k] = v
    return d

##################################################
# Message Templates
##################################################

issue_tmp ="""%(body)s
# Please enter/edit a description for your issue above. You may use 
# Markdown to format your text. Lines starting with a '#' will be 
# ignored. A blank description will abort the action. To edit other 
# attributes of an issue, edit the text after each colon below:
TITLE: %(title)s
MILESTONE: %(milestone)s
LABELS: %(labels)s"""

comment_tmp ="""%(body)s
# Please enter a comment for issue %(issue)s above. You may use 
# Markdown to format your text. Lines starting with a '#' will be 
# ignored. A blank description will abort creation of the comment."""


##################################################
# Command Actions
##################################################

def list(args):
    """ Run list command """
    args = clean_args(args, exclude_keys['func'])
    print("Listing issues with filters:", args)

def new(args):
    """ Run new command """
    args = clean_args(args, exclude_keys=['func'])
    if args['body'] is None:
        get_message(args, issue_tmp)
    print("New issue:", args)

def show(args):
    """ Run show command """
    print("Show Issue %s" % args.issue)

def edit(args):
    """ Run the edit command. """
    issue = args.issue
    args = clean_args(args, 
                      exclude_keys=['func', 'issue'],
                      exclude_values = [None])
    if not args:
        print('Edit issue %s in editor. Args:' % issue, args)
    else:
        print('Edit issue %s with Args:' % issue, args)

def comment(args):
    if args.list:
        print("List comments for issue:", args.list)
    elif args.show:
        print("Show comment #", args.show)
    elif args.new:
        if args.body is None:
            get_message(args, comment_tmp, {'issue': args.new})
        print("Create comment on issue %s:" %args.new, args.body)
    elif args.edit:
        if args.body is None:
            args.body = get_message()
        print("Edit comment #%s to:" %args.edit, args.body)
    elif args.delete:
        print("Delete comment#", args.delete)

##################################################
# Command Line Parser
##################################################

message_epilog = 'If the BODY is not provided, a blank document ' \
                 'will be opened in the default editor for a message ' \
                 ' to be provided. If the editor is closed with a blank ' \
                 'document, the action will be aborted. The default editor ' \
                 'is determined by the "VISUAL" or "EDITOR" environment ' \
                 'variables (in that order).'

# The "issue" command
parser = argparse.ArgumentParser(description="Manage Github Issues from the Command Line")
subparsers = parser.add_subparsers(title='Available Subcommands',
        description='Run "%(prog)s {subcommand} -h" for more information on each subcommand below.')

# The "list" command
ls_psr = subparsers.add_parser('list', help='List existing issues')
ls_psr.add_argument('-m', '--milestone', 
    help='Filter by Milestone ID, "none" or "*" (default all)')
ls_psr.add_argument('--state', choices=['open', 'closed'], 
                    help='Filter by State, Default: "open"')
ls_psr.add_argument('-a', '--assignee', 
                    help='Filter by Assignee')
ls_psr.add_argument('-@', '--mentioned', 
                    help='Filter by @MentionedUser')
ls_psr.add_argument('-l', '--labels', nargs='+', 
                    help='Filter by Labels')
ls_psr.add_argument('--sort', choices=['created', 'updated', 'comments'],
                    help='Sort order, Default: "created"')
ls_psr.add_argument('-d', '--direction', choices=['asc', 'desc'],
                    help='Sort direction, Default: "desc"')
ls_psr.add_argument('--since' , 
    help='Filter by date (string of a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ)')
ls_psr.set_defaults(func=list)


# The "new" command
new_psr = subparsers.add_parser('new', 
                help='Create a new issue', epilog=message_epilog)
new_psr.add_argument('title', help='Title of issue')
new_psr.add_argument('-m', '--message', dest='body', 
                     help='Description of issue')
new_psr.add_argument('-a', '--assignee', 
                    help='User this issue should be assigned to')
new_psr.add_argument('--milestone', type=int, 
                     help='Milestone to associate this issue with')
new_psr.add_argument('-l', '--labels', nargs='+', 
                     help='Labels to associate with this issue')
new_psr.set_defaults(func=new)

# The "show" command
show_psr = subparsers.add_parser('show', 
                help='Display an existing issue')
show_psr.add_argument('issue', type=int, 
                      help='Issue ID number')
show_psr.set_defaults(func=show)

# The "edit" command
edt_psr = subparsers.add_parser('edit', 
                help='Edit an existing issue', 
                epilog='If no flags are set, the entire issue ' \
                'will be opened as a document in the editor. ' \
                'If any flags are set, only the attributes ' \
                'defined will be updated.')
edt_psr.add_argument('issue', type=int, help='Issue ID number')
edt_psr.add_argument('-m', '--message', dest='body',
                     help='Edit Description of issue')
edt_psr.add_argument('-t', '--title', help='Title of issue')
edt_psr.add_argument('-a', '--assignee', 
                     help='Login for the user that this issue should be assigned to')
edt_psr.add_argument('--milestone', type=int, 
                     help='Milestone to associate this issue with')
edt_psr.add_argument('-l', '--labels' , nargs='+', 
                     help='Labels to associate with this issue')
edt_psr.set_defaults(func=edit)


# The "comment" command
cmnt_psr = subparsers.add_parser('comment', 
                 help='Comment on an existing issue', 
                 epilog=message_epilog)
cmnt_gp = cmnt_psr.add_mutually_exclusive_group(required=True)
cmnt_gp.add_argument('-l', '--list',  metavar='ISSUE_ID',
                     help='List comments for given issue')
cmnt_gp.add_argument('-s', '--show', metavar='COMMENT_ID',
                     help='Display a comment')
cmnt_gp.add_argument('-n', '--new', metavar='ISSUE_ID', 
                     help='Create a comment')
cmnt_gp.add_argument('-e', '--edit', metavar='COMMENT_ID', 
                     help='Edit a comment')
cmnt_gp.add_argument('-d', '--delete', metavar='COMMENT_ID',
                     help='Delete a comment')
cmnt_psr.add_argument('-m', '--message', dest='body', 
                      help='Comment body (use markdown for formatting)')
cmnt_psr.set_defaults(func=comment)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)