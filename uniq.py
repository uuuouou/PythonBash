#! python
"""
write by liucz 2015-10-7
imitate 'uniq' command in Linux Shell
"""

import sys
import re
import argparse
from handle_stdin import storeLines


def buildParser():
	parser = argparse.ArgumentParser()

	# options related to output
	parser.add_argument('-u', '--unique',
						action = 'store_true',
						help = 'only print unique lines')
	parser.add_argument('-d', '--repeated',
						action = 'store_true',
						help = 'only print duplicate lines')
	parser.add_argument('-c', '--count',
						action = 'store_true',
						help = 'prefix lines by number of occurences')
	parser.add_argument('-D', '--all-repeated',
						action = 'store_true',
						help = 'print all duplicate lines')
	# options related to processing
	parser.add_argument('-f', '--skip-fields',
						nargs = 1,
						type = int,
						help = 'avoid comparing first N fields')
	parser.add_argument('-s', '--skip-chars',
						nargs = 1,
						type = int,
						help = 'print all duplicate lines')
	parser.add_argument('-i', '--ignore-case',
						action = 'store_true',
						help = 'avoid comparing first N characters')
	parser.add_argument('-w', '--check-chars',
						nargs = 1,
						type = int,
						help = 'compare no more than N characters in lines')
	# positional args
	parser.add_argument('input',
						nargs = '?',
						type = str,
						help = 'input file, use standard input if not given')
	parser.add_argument('output',
						nargs = '?',
						type = str,
						help = 'input file, use standard output if not given')
	return parser


def processArgs(args):
	if args.unique and args.repeated:
		sys.stderr.write('uniq.py: print only unique lines and only duplicate lines is meaningless\n')
		return False
	if args.unique and args.all_repeated:
		sys.stderr.write('uniq.py: print only unique lines and all duplicate lines is meaningless\n')
		return False
	if args.count and args.all_repeated:
		sys.stderr.write('uniq.py: print all duplicate lines and repeat counts is meaningless\n')
		return False

	if args.skip_fields is not None:
		args.skip_fields = args.skip_fields[0]
		if args.skip_fields < 0:
			sys.stderr.write('uniq.py: invalid number of fields to skip: "%d"\n' % args.skip_fields)
			return False
	if args.skip_chars is not None:
		args.skip_chars = args.skip_chars[0]
		if args.skip_chars < 0:
			sys.stderr.write('uniq.py: invalid number of chars to skip: "%d"\n' % args.skip_chars)
			return False
	if args.check_chars is not None:
		args.check_chars = args.check_chars[0]
		if args.check_chars <= 0:
			sys.stderr.write('uniq.py: invalid number of chars to compare: "%d"\n' % args.check_chars)
			return False

	if args.skip_fields is not None and args.skip_chars is not None:
		sys.stderr.write('uniq.py: can not specify skip-fields and skip_chars at the same time\n')
		return False

	if not (args.unique | args.repeated | args.all_repeated):
		args.unique = True
	if args.all_repeated:
		args.repeated = True

	return True


def getKey(line, args):
	if args.ignore_case:
		line = line.lower()

	if args.skip_fields:
		fields = re.findall('\\S+', line)
		if not fields:
			key = ''
		elif args.skip_fields < len(fields):
			key = fields[args.skip_fields]
		else:
			key = fields[-1]
	elif args.skip_chars:
		if line == '':
			key = ''
		elif args.skip_chars < len(line):
			key = line[args.skip_chars:]
		else:
			key = line[-1]
	else:
		key = line

	# limit key size if specified
	if args.check_chars and len(key) > args.check_chars:
		key = key[:args.check_chars]

	return key


def show(line, times, args):
	# print('line = %s, times = %d' % (line, times))
	if line is None:
		return
	if args.unique and times > 1:
		return
	if args.repeated and times < 2:
		return

	if args.count:
		print(str(times).rjust(7), line)
	else:
		print(line)


def doUnique(args):
	prevLine = None
	prevKey = None
	times = 0
	meetEOF = False
	while not meetEOF:
		lines, meetEOF = storeLines(1)
		if lines:
			line = lines[0][:-1]
			# compare with previous line
			key = getKey(line, args)
			# print('key = %s' % key)
			if key == prevKey:
				times += 1
				if args.all_repeated:
					print(prevLine)
			else:
				# print('key = %s, prevKey = %s' % (key, prevKey))
				show(prevLine, times, args)
				prevKey = key
				times = 1
			prevLine = line
	show(prevLine, times, args)


def main():
	parser = buildParser()
	args = parser.parse_args()
	# print(args)
	if not processArgs(args):
		return

	fin, fout = None, None
	if args.input is not None:
		try:
			fin = open(args.input)
		except:
			sys.stderr.write('uniq.py: failed to open input "%s"\n' % args.input)
			return

	if args.output is not None:
		try:
			fout = open(args.output)
		except:
			sys.stderr.write('uniq.py: failed to open output "%s"\n' % args.input)
			if fin:
				fin.close()
			return

	sys.stdin = fin if fin else sys.__stdin__
	sys.stdout = fout if fout else sys.__stdout__
	doUnique(args)

	if fin:
		fin.close()
		sys.stdin = sys.__stdin__
	if fout:
		fout.close()
		sys.stdout = sys.__stdout__


# entry
if __name__ == '__main__':
	main()