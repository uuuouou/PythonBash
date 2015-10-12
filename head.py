#! c:\python34\python
"""
write by liucz 2015-10-6
imitate 'head' command in Linux Shell
"""

import sys
import re
import argparse
from handle_stdin import echoLines, discardLines, echoChars, discardChars


def buildParser():
	parser = argparse.ArgumentParser()

	# add optional arguments
	parser.add_argument('-c',
						dest = 'chars',
						nargs = 1,
						type = str,
						help = 'print first N chars if "-c CHARS" or '
							   'print all chars starting from the Nth char if "-n + CHARS; '
							   'may have a multiplier suffix: b for 512, k for 1K, m for 1 Meg')

	parser.add_argument('-n',
						dest = 'lines',
						nargs = 1, 
						type = str, 	# acceptable pattern is '1000'
						# const = '10',	# default 10, if there is no '-n N' or '-n' does not have a param followed
						help = 'print first N lines if "-n LINES" or '
							   'print all lines starting from the Nth line if "-n +LINES')

	parser.add_argument('-v', '--verbose',
						dest = 'verbose',
						action = 'store_true',
						help = 'always print headers giving file names')

	parser.add_argument('-q', '--quiet',
						dest = 'quiet',
						action = 'store_true',
						help = 'never print headers giving file names')

	# add positional arguments
	parser.add_argument('files',
						nargs = '*',
						help = 'read from stdin if not given')
	return parser


def printHeader(file):
	print('==> %s <==' % file)


def processArgs(args):
	lines_pattern = '^\+?\d+$'
	chars_pattern = '^\+?\d+[bkm]?$'

	if args.lines:
		lines = args.lines[0]
		if not re.match(lines_pattern, lines):
			sys.stderr.write('head.py: invalid lines count!\n')
			return False
		else:
			args.skipLines = False
			if lines[0] == '+':
				args.skipLines = True
			args.lines = int(lines)

	if args.chars:
		chars = args.chars[0]
		if not re.match(chars_pattern, chars):
			sys.stderr.write('head.py: invalid chars count!\n')
			return False
		else:
			args.skipChars = False
			if chars[0] == '+':
				args.skipChars = True
			if chars[-1] == 'b':
				args.chars = int(chars[:-1]) * 512
			elif chars[-1] == 'k':
				args.chars = int(chars[:-1]) * 1024
			elif chars[-1] == 'm':
				args.chars = int(chars[:-1]) * 1024 * 1024
			else:
				args.chars = int(chars)

	return True


def main():
	parser = buildParser()
	args = parser.parse_args()
	# print(args)
	if not processArgs(args):
		return

	# check if given input files
	for i, f in enumerate(args.files + [sys.__stdin__]):
		if i:
			print()
		if args.files:
			if f == sys.__stdin__:
				# done already
				break
			else:
				# redirect input stream
				if args.verbose or not args.quiet and len(args.files) > 1:
					printHeader(f)
				f = open(f, errors = 'ignore')
				sys.stdin = f
		# deal with options
		if args.lines is not None:
			if args.skipLines:
				if not discardLines(args.lines - 1):
					echoLines(-1, tillEOF = True)
			else:
				echoLines(args.lines)
		elif args.chars is not None:
			if args.skipChars:
				# print('discard %d chars' % (args.chars - 1))
				restOfLastLine, meetEOF = discardChars(args.chars - 1)
				if restOfLastLine:
					print(restOfLastLine, end = '')
				if not meetEOF:
					echoLines(-1, tillEOF = True)
			else:
				echoChars(args.chars)
		else:
			echoLines(-1, tillEOF = True)
		# close file
		if args.files:
			f.close()
			sys.stdin = sys.__stdin__


# entry
if __name__ == '__main__':
	main()