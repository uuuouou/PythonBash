#! python3
"""
write by liucz 2015-10-14
imitate 'seq' command in Linux Shell
"""

import sys
import argparse


def buildParser():
	parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
	# add usage
	usage = 'seq.py [OPTION] LAST' + '\n' + \
			'   or: seq.py [OPTION] FIRST LAST' + '\n' + \
			'   or: seq.py [OPTION] FIRST INCREMENT LAST' + '\n' + \
			'Print numbers from FIRST to LAST, in steps of INCREMENT'
	parser.usage = usage
	# add description
	description = """
  If FIRST or INCREMENT is omitted, it defaults to 1.  That is, an
  omitted INCREMENT defaults to 1 even when LAST is smaller than FIRST.
  FIRST, INCREMENT, and LAST are interpreted as floating point values.
  INCREMENT is usually positive if FIRST is smaller than LAST, and
  INCREMENT is usually negative if FIRST is greater than LAST.
  FORMAT must be suitable for printing one argument of type `double';
  it defaults to %.PRECf if FIRST, INCREMENT, and LAST are all fixed point
  decimal numbers with maximum precision PREC, and to %g otherwise.
"""
	parser.description = description
	# add arguments
	parser.add_argument('-f', '--format',
						nargs = '?',
						type = str,
						help = 'use printf style FORMAT')
	parser.add_argument('-s', '--separator',
						nargs = '?',
						type = str,
						help = 'use STRING to separate numbers (default \\n)')
	parser.add_argument('-w', '--equal-width',
						action = 'store_true',
						help = 'equalize width by padding with leading zeros')
	parser.add_argument('nums',
						nargs = '+',
						type = str)
	return parser


def processArgs(args):
	if len(args.nums) > 3:
		sys.stderr.write('seq.py: extra operands: [%s]\n' % ' '.join(args.nums[3:]))
		return False
	if args.equal_width and args.format is not None:
		sys.stderr.write('seq.py: format string may not specified when printing equal width strings\n')
		return False

	precision = 0
	for s in args.nums:
		try:
			_ = float(s)
			point = s.find('.')
			if point != -1:
				precision = max(precision, len(s) - point - 1)
		except:
			sys.stderr.write('seq.py: [%s] is an invalid number\n' % s)
			return False

	n = len(args.nums)
	if n == 1:
		args.nums = [1.0, 1.0, float(args.nums[0])]
	elif n == 2:
		args.nums = [float(args.nums[0]), 1.0, float(args.nums[1])]
	else:
		args.nums = [float(x) for x in args.nums]

	if args.format is None:
		if precision != 0:
			args.format = '%%.%df' % precision
		else:
			args.format = '%g'
	if args.separator is None:
		args.separator = '\n'

	return True


def main():
	parser = buildParser()
	args = parser.parse_args()
	print(args)
	if not processArgs(args):
		return

	if not args.equal_width:
		first = True
		while args.nums[0] <= args.nums[2]:
			if first:
				first = False
			else:
				print(args.separator, end = '')
			try:
				print(args.format % args.nums[0], end = '')
			except:
				sys.stderr.write('seq.py: [%s] is an invalid format' % args.format)
				return
			args.nums[0] += args.nums[1]
		print()
	else:
		all = []
		width = 0
		while args.nums[0] <= args.nums[2]:
			all.append(args.format % args.nums[0])
			width = max(width, len(all[-1]) if all[-1][0].isdigit() else len(all[-1]) - 1)
			args.nums[0] += args.nums[1]
		if args.format == '%g':
			print(args.separator.join([s.rjust(width, '0') for s in all]))
		else:
			print(args.separator.join(all))


if __name__ == '__main__':
	main()