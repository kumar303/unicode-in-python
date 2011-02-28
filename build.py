#!/usr/bin/env python
import os
import optparse
from subprocess import check_call
import codecs

def setup_doctest():
    u = 'Ivan Krsti\xc4\x87'.decode('utf-8')
    f = open('/tmp/ivan_utf8.txt','w')
    f.write(u.encode('utf-8'))
    f.close()
    f = open('/tmp/ivan_utf16.txt','w')
    f.write(u.encode('utf-16'))
    f.close()

def main():
    p = optparse.OptionParser(usage='%prog [options]')
    p.add_option('-u', '--upload', action='store_true', default=False,
                 help="rsync / copy files to farmdev")
    (options, args) = p.parse_args()
    setup_doctest()
    check_call(['nosetests', '--with-doctest', '--doctest-extension=txt',
                './unicode.txt'])
    output = './unicode.html'
    check_call(['./custom_rst2s5.py', './unicode.txt', './index.html'])
    print "Wrote %s" % output
    check_call(['open', './index.html'])

if __name__ == '__main__':
    main()
