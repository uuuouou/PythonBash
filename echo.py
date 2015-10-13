#! python3
#--*- coding:utf-8 -*--
"""
written by liucz 2015-10-13
imitate echo in linux shell
"""

import sys
import argparse


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


mapping = {
	'a': '\a',
	'b': '\b',
	'f': '\f',
	'n': '\n',
	'r': '\r',
	't': '\t',
	'v': '\v',
	'\\': '\\'
}


def escaped(s):
	i, n = 0, len(s)
	t = ''
	while i < n:
		c = s[i]
		if c != '\\':
			t += c
			i += 1
		elif i+1 < n and s[i+1] in 'abfnrtv\\':
			t += mapping[s[i+1]]
			i += 2
		elif i+1 < n and s[i+1] in '01234567':
			num = 0
			k = i+1
			for j in range(3):
				if k < n and s[k] in '01234567':
					num = (num << 3) + int(s[k])
					k += 1
				else:
					break
			if num > 127:
				num = (num - int(s[k-1])) >> 3
				k -= 1
			t += chr(num)
			i = k
		else:
			t += c
			i += 1
	return t


def main():
	parser = buildParser()
	args = parser.parse_args()
	print(args)
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
