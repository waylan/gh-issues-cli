import argparse

##################################################
# Utility Functions
##################################################

def get_message():
    """ Get message from EDITOR. """
    return 'some message'

def clean_args(args, exclude_keys=[], exclude_values=[]):
    """ Remove unwanted keys and/or values from args. """
    d = {}
    for k, v in args._get_kwargs():
        if  k not in exclude_keys and v not in exclude_values:
            d[k] = v
    return d

##################################################
# Command Actions
##################################################

def list(args):
    """ Run list command """
    args = clean_args(args, exclude_keys['func'])
    print "Listing issues with filters:", args

def new(args):
    """ Run new command """
    args = clean_args(args, exclude_keys=['func'])
    if args['body'] is None:
        args['body'] = get_message()
    print "New issue:", args

def show(args):
    """ Run show command """
    print "Show Issue %s" % args.issue

def edit(args):
    """ Run the edit command. """
    issue = args.issue
    args = clean_args(args, 
                      exclude_keys=['func', 'issue'],
                      exclude_values = [None])
    if not args:
        print 'Edit issue %s in editor. Args:' % issue, args
    else:
        print 'Edit issue %s with Args:' % issue, args

def comment(args):
    if args.list:
        print "List comments for issue:", args.list
    elif args.show:
        print "Show comment #", args.show
    elif args.new:
        if args.body is None:
            args.body = get_message()
        print "Create comment on issue %s:" %args.new, args.body
    elif args.edit:
        if args.body is None:
            args.body = get_message()
        print "Edit comment #%s to:" %args.edit, args.body
    elif args.delete:
        print "Delete comment#", args.delete

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