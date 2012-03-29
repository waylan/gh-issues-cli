import argparse

##################################################
# Utilitiy Functions
##################################################

def get_message(args):
    return 'some message'

##################################################
# Command Actions
##################################################

def list(args):
    print "Listing issues with filters:", args

def new(args):
    print "New issue:", args

def show(args):
    print "Show Issue:", args

def edit(args):
    if args.message:
        print 'Edit message in editor. Args:', args
    elif not args.title:
        print 'Edit issue in editor. Args:', args
    else:
        print 'No editor. Args:', args

def comment(args):
    print "Comment:", args

##################################################
# Command Line Parser
##################################################

message_epilog = 'If the "-m, --message" argument is not provided, a blank document ' \
                 'will be opened in the default editor for a message to be provided. ' \
                 'If the editor is closed with a blank document, the action will be aborted.' \
                 'The default editor is determined by the "VISUAL" or "EDITOR" ' \
                 'environment variables (in that order).'

# The "issue" command
parser = argparse.ArgumentParser(description="Manage Github Issues from the Command Line")
subparsers = parser.add_subparsers(title='Available Subcommands',
        description='Run "%(prog)s {subcommand} -h" for more information on each subcommand below.')

# The "list" command
list_parser = subparsers.add_parser('list', help='List existing issues')
list_parser.add_argument('-m', '--milestone', 
                            help='Filter by Milestone ID, "none" or "*" (default all)')
list_parser.add_argument('--state', choices=['open', 'closed'], 
                            help='Filter by State, Default: "open"')
list_parser.add_argument('-a', '--assignee', help='Filter by Assignee')
list_parser.add_argument('-@', '--mentioned', help='Filter by @MentionedUser')
list_parser.add_argument('-l', '--labels', nargs='+', help='Filter by Labels')
list_parser.add_argument('--sort', choices=['created', 'updated', 'comments'],
                            help='Sort order, Default: "created"')
list_parser.add_argument('-d', '--direction', choices=['asc', 'desc'],
                            help='Sort direction, Default: "desc"')
list_parser.add_argument('--since' , help='Filter by date (string of a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ)')
list_parser.set_defaults(func=list)

# The "new" command
create_parser = subparsers.add_parser('new', help='Create a new issue', epilog=message_epilog)
create_parser.add_argument('title', help='Title of issue')
create_parser.add_argument('-m', '--message', dest='body', help='Description of issue')
create_parser.add_argument('-a', '--assignee', 
                            help='Login for the user that this issue should be assigned to')
create_parser.add_argument('--milestone', type=int, help='Milestone to associate this issue with')
create_parser.add_argument('-l', '--labels', nargs='+', help='Labels to associate with this issue')
create_parser.set_defaults(func=new)

# The "show" command
show_parser = subparsers.add_parser('show', help='Display an existing issue')
show_parser.add_argument('issue', type=int, help='Issue ID number')
show_parser.set_defaults(func=show)

# The "edit" command
edit_parser = subparsers.add_parser('edit', help='Edit an existing issue', 
        epilog='If no flags are set, the entire issue will be opened as a document in the editor.'
               'If the "-m, --message" flag is set, a document containing only the '
               'Description will be opened in the default editor.'
               'In either case, any changes saved to the document will be applied. '
               'If the editor is closed with a blank document, the entire action will be aborted.'
               'The default editor is determined by the "VISUAL" or "EDITOR" environment variables '
               '(in that order).')
edit_parser.add_argument('issue', type=int, help='Issue ID number')
edit_parser.add_argument('-m', '--message', action='store_const', const=True, default=False,
                         dest='body', help='Edit Description of issue')
edit_parser.add_argument('-t', '--title', help='Title of issue')
edit_parser.add_argument('-a', '--assignee', 
                            help='Login for the user that this issue should be assigned to')
edit_parser.add_argument('--milestone', type=int, help='Milestone to associate this issue with')
edit_parser.add_argument('-l', '--labels' , nargs='+', help='Labels to associate with this issue')
edit_parser.set_defaults(func=edit)

# The "comment" command
comment_parser = subparsers.add_parser('comment', help='Comment on an existing issue', 
                                    epilog=message_epilog)
comment_parser.add_argument('issue', help='Issue ID number')
#comment_parser.add_argument('-m', '--message', dest='body', 
#                            help='Comment body (use markdown for formatting)')
comment_parser.add_argument('-l', '--list', help='List comments')
comment_parser.add_argument('-s', '--show', help='Display a comment')
comment_parser.add_argument('-n', '--new', dest='body', help='Create a comment')
comment_parser.add_argument('-e', '--edit', dest='body', help='Edit a comment')
comment_parser.add_argument('-d', '--delete', help='Delete a comment')
comment_parser.set_defaults(func=comment)

if __name__ == '__main__':
    args = parser.parse_args()
    if hasattr(args, 'body') and args.body is None:
        args.body = get_message(args)
    args.func(args)