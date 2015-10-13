#! python
import sys
import re
import argparse


def buildParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--chars', 
						action = 'store_true',
						help = 'print the char counts')
	parser.add_argument('-w', '--words', 
						action = 'store_true',
						help = 'print the word counts')
	parser.add_argument('-l', '--lines', 
						action = 'store_true',
						help = 'print the line counts')
	parser.add_argument('-L', '--max-line-length', 
						action = 'store_true',
						help = 'print the length of the longest line')
	parser.add_argument('files', 
						nargs = '*',
						help = 'files to count')
	return parser


def getColumns(args):
	columns = []
	if args.lines:
		columns.append("lines")
	if args.words:
		columns.append("words")
	if args.chars:
		columns.append("chars")
	if args.max_line_length:
		columns.append("max-line-length")
	if columns:
		return columns
	# user did not specify anything
	args.lines = args.words = args.chars = True
	return ["lines", "words", "chars"]


def count(args):
	stat = {'lines': 0, 'words': 0, 'chars': 0, 'max_line_length': 0}
	while True:
		try:
			line = input()
			if args.lines:
				stat['lines'] += 1
			if args.words:
				stat['words'] += len(re.findall('\w+', line))
			if args.chars:
				stat['chars'] += len(line) + 1
			if args.max_line_length:
				stat['max_line_length'] = max(stat.get('max_line_length', 0), len(line))
		except (IOError, EOFError) as e:
			break
	return stat


def showStatistics(columns, statistics):
	columnSize = [len(col) for col in columns]
	for f, stat in statistics.items():
		# print(stat)
		for i, key in enumerate(columns):
			columnSize[i] = max(columnSize[i], len(str(stat[key])))
	for i, col in enumerate(columns):
		if i:
			print('\t', end = '')
		print(str(col).rjust(columnSize[i], ' '), end = '')
	print()
	for f, stat in statistics.items():
		for i, key in enumerate(columns):
			if i:
				print('\t', end = '')
			print(str(stat[key]).rjust(columnSize[i], ' '), end = '')
		print('\t', f)


def main():
	parser = buildParser()
	args = parser.parse_args()
	# print(args)
	columns = getColumns(args)
	statistics = {}
	if not args.files:
		statistics['stdin'] = count(args)
	else:
		for f in files:
			try:
				fin = open(f, 'r', errors = 'ignore')
			except:
				sys.stderr.write('wc.py: failed to open "%s"\n' % f)
				continue
			statistics[f] = count(args)
			sys.stdin = fin
			fin.close()
		sys.stdin = sys.__stdin__
	showStatistics(columns, statistics)


if __name__ == '__main__':
	main()