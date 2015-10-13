#! python3
"""
written by liucz 2015-10-13
imitate 'echo' in linux shell
"""

import sys
import argparse
from handle_string import escaped


def buildParser():
	description = \
"""
 Output the contents.  If -n is specified, the trailing newline is suppressed.
 If the -e option is given, interpretation of the following backslash-escaped 
 characters is turned on:
     \\a      alert (bell)
     \\b      backspace
     \\f      form feed
     \\n      new line
     \\r      carriage return
     \\t      horizontal tab
     \\v      vertical tab
     \\\\      backslash
     \\num    the character whose ASCII code is NUM (octal).
"""
	parser = argparse.ArgumentParser(description = description,
									 formatter_class = argparse.RawDescriptionHelpFormatter)
	parser.usage = 'echo.py [-neE] [content ...]'
	parser.add_argument('-n',
						action = 'store_true',
						help = 'suppress trailing newline')
	parser.add_argument('-e',
						action = 'store_true',
						help = 'turn on interpretation of backslash-escaped chars')
	parser.add_argument('-E',
						action = 'store_true',
						help = 'turn off interpretation of backslash-escaped chars')
	parser.add_argument('content',
						type = str,
						nargs = '+')
	return parser


def main():
	parser = buildParser()
	args = parser.parse_args()
	# print(args)
	if not args.e:
		args.E = True
	if args.E:
		line = ' '.join(args.content)
	else:
		line = ' '.join([escaped(s) for s in args.content])
	print(line, end = '')
	if not args.n:
		print()


if __name__ == '__main__':
	main()
