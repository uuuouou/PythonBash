#! python

import sys
import argparse
from handle_stdin import storeLines


def buildParser():
	parser = argparse.ArgumentParser()
	parser.usage = 'cat [OPTION] [FILE], concatenate FILE(S) or stdin to stdout'
	parser.add_argument('-E', '--show-ends',
						action = 'store_true',
						help = 'display $ at end of each line')
	parser.add_argument('-s', '--squeeze-blank',
						action = 'store_true',
						help = 'never more than one single blank line')
	parser.add_argument('-n', '--number',
						action = 'store_true',
						help = 'number all output lines')
	parser.add_argument('-b', '--number-nonblank',
						action = 'store_true',
						help = 'number nonblank output lines')
	parser.add_argument('files',
						nargs = '*',
						type = str,
						help = 'files to concatenate')
	return parser


prevLine = None
lineCount = 0
nonblankLineCount = 0

def show(line, args):
	ends = '\n'
	if args.show_ends:
		ends = '$\n'

	if args.number:
		if args.number_nonblank:
			if line != '':
				print(str(nonblankLineCount).rjust(6), '  ', line, sep = '', end = ends)
			else:
				print(end = ends)
		else:
			print(str(lineCount).rjust(6), '  ', line, sep = '', end = ends)
	else:
		print(line, end = ends)


def doCat(args):
	global prevLine, lineCount, nonblankLineCount

	meetEOF = False
	while not meetEOF:
		lines, meetEOF = storeLines(1)
		if not lines:
			continue

		line = lines[0][:-1]
		lineCount += 1

		if line != '':
			nonblankLineCount += 1
			show(line, args)
		else:
			if not args.squeeze_blank or prevLine != '':
				show('', args)
			else:
				lineCount -= 1

		prevLine = line


def main():
	parser = buildParser()
	args = parser.parse_args()
	# print(args)

	if args.files:
		for f in args.files:
			try:
				fin = open(f, 'r', errors = 'ignore')
			except:
				sys.stderr.write('cat.py: failed to open file [%s]\n' % f)
				continue

			sys.stdin = fin
			doCat(args)

			fin.close()
		sys.stdin = sys.__stdin__
	else:
		doCat(args)


if __name__ == '__main__':
	main()

