#! python3
"""
write by liucz 2015-10-10
imitate 'tee' command in Linux Shell
"""

import sys
import signal
import argparse


def buildParser():
	parser = argparse.ArgumentParser()
	parser.usage = 'tee.py [OPTION] [FILE], copy stdin to each FILE, and also to stdout'
	parser.add_argument('-a', '--append',
						action = 'store_true',
						help = 'append to the given FILES, do not overwrite')
	parser.add_argument('-i', '--ignore-interrupts',
						action = 'store_true',
						help = 'ignore interrupt signals')
	parser.add_argument('files',
						nargs = '*',
						type = str,
						help = 'files to write to')
	return parser


def main():
	parser = buildParser()
	args = parser.parse_args()

	if args.ignore_interrupts:
		signal.signal(signal.SIGBREAK, signal.SIG_IGN)
		signal.signal(signal.SIGINT,   signal.SIG_IGN)
		signal.signal(signal.SIGTERM,  signal.SIG_IGN)

	outs = []
	mode = 'a' if args.append else 'w'
	if args.files:
		for f in args.files:
			try:
				fout = open(f, mode, errors = 'ignore')
				outs.append(fout)
			except:
				sys.stderr.write('tee.py: failed to open file [%s]\n' % f)
				continue
	outs.append(sys.__stdout__)

	while True:
		try:
			line = input()
			for fout in outs:
				fout.write(line)
				fout.write('\n')
		except (EOFError, IOError) as e:
			break

	outs.pop(-1)
	for fout in outs:
		fout.close()


if __name__ == '__main__':
	main()