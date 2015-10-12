#! c:\python34\python
"""
write by liucz 2015-10-7
imitate 'tr' command in Linux Shell
"""

import sys
import re
import argparse
from handle_stdin import echoLines, storeLines
from handle_string import delete, unique, complement, complementUnique


def buildParser():
	parser = argparse.ArgumentParser()

	parser.add_argument('-c', '--complement',
						action = 'store_true',
						help = 'replace all those chars not in src by the single char of rep')
	parser.add_argument('-d', '--delete',
						action = 'store_true',
						help = 'delete all those chars in src')
	parser.add_argument('-s', '--squeeze',
						action = 'store_true',
						help = 'remove redundant continuous repeated chars in src or ' 
							   'replace continuous repeated chars in src by corresponding char in rep')
	parser.add_argument('-t', '--truncate',
						action = 'store_true',
						help = 'truncate src if len(src) > len(rep) otherwise use last char in rep if len(src) > len(rep)')
	parser.add_argument('src',
						nargs = 1,
						help = 'source char set')
	parser.add_argument('rep',
						nargs = '?',
						help = 'replace char set')
	# parser.add_help()
	return parser


def processArgs(args):
	args.src = args.src[0]
	# if args.complement:
	# 	if not args.delete and args.rep is None:
	# 		sys.stderr.write('tr.py: rep must be given when translating\n')
	# 		return False

	if args.truncate:
		if args.rep is None:
			sys.stderr.write('tr.py: rep must be given when truncating\n')
			return False

	if args.delete:
		if args.rep is not None:
			sys.stderr.write('tr.py: rep is ignored when deleting\n')

	# check src and rep
	if args.rep is not None:
		repLen = len(args.rep)
		srcLen = len(args.src)
		if srcLen > repLen:
			if args.truncate:
				args.src = args.src[:repLen]
			else:
				args.rep += args.rep[-1] * (srcLen - repLen)
		elif srcLen < repLen:
			args.rep = args.rep[:srcLen]

	return True


def doDelete(targetSet):
	# print("doDelete")
	# print(targetSet)
	meetEOF = False
	while not meetEOF:
		lines, meetEOF = storeLines(1)
		if lines:
			print(delete(lines[0], targetSet), end = '')


def doComplementDelete(keepSet):
	# print("doComplementDelete")
	meetEOF = False
	while not meetEOF:
		lines, meetEOF = storeLines(1)
		if lines:
			print(complement(lines[0], keepSet, ''), end = '')


def doSqueeze(src, rep):
	# print("doSqueeze")
	transformTable = None
	if rep:
		transformTable = {src[i]:rep[i] for i in range(len(src))}
	meetEOF = False
	while not meetEOF:
		lines, meetEOF = storeLines(1)
		if lines:
			print(unique(lines[0], transformTable), end = '')


def doComplementSqueeze(src, rep):
	# print("doComplementSqueeze")
	# print('rep = %s' % rep)
	keepSet = set(src)
	meetEOF = False
	while not meetEOF:
		lines, meetEOF = storeLines(1)
		if lines:
			print(complementUnique(lines[0], keepSet, None, rep), end = '')


def main():
	parser = buildParser()
	args = parser.parse_args()
	# print(args)
	if not processArgs(args):
		return

	if args.delete:
		if args.complement:
			# delete those not in src
			doComplementDelete(set(args.src))
		else:
			# delete those in src
			doDelete(set(args.src))

	elif args.squeeze:
		if args.complement:
			doComplementSqueeze(args.src, args.rep)
		else:
			doSqueeze(args.src, args.rep)
	else:
		echoLines(-1, tillEOF = True)


# entry
if __name__ == '__main__':
	main()