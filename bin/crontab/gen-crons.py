#!/usr/bin/env python
import os
from optparse import OptionParser

HEADER = '!!AUTO-GENERATED!! Edit bin/crontab/crontab.tpl instead.'
TEMPLATE = open(os.path.join(os.path.dirname(__file__), 'crontab.tpl')).read()


def main():
    parser = OptionParser()
    parser.add_option('-w', '--webapp',
                      help='Location of web app (required)')
    parser.add_option('-u', '--user',
                      help=('Prefix cron with this user. '
                            'Only define for cron.d style crontabs.'))
    parser.add_option('-p', '--python', default='/usr/bin/python2.6',
                      help='Python interpreter to use.')
    parser.add_option("-d", "--deprecations", default=False,
                      help="Show deprecation warnings")

    (opts, args) = parser.parse_args()

    if not opts.webapp:
        parser.error('-w must be defined')

    if not opts.deprecations:
        opts.python += ' -W ignore::DeprecationWarning'

    ctx = {'django': 'cd %s; %s manage.py' % (opts.webapp, opts.python)}

    if opts.user:
        for k, v in ctx.iteritems():
            ctx[k] = '%s %s' % (opts.user, v)

    # Needs to stay below the opts.user injection.
    ctx['python'] = opts.python
    ctx['header'] = HEADER

    print TEMPLATE % ctx


if __name__ == '__main__':
    main()
