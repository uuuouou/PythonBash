"""
write by liucz 2015-10-6
handy functions to deal with stdin
"""


def discardChars(chars, tillEOF = False):
	"""
	write by liucz 2015-10-6
	discard given count of stdin chars, also stop if meet EOF
	NOTICE: input is actually passed to program by LINE

	@chars   -> how many chars to deal with
	@tillEOF -> if True then process till EOF regardless given lines, otherwise till lines < 1 or meet EOF
	@return  -> a tuple: (rest of the last input line, flag of stopped by EOF)
	"""
	return dealWithChars(chars, '', tillEOF)


def echoChars(chars, tillEOF = False):
	"""
	write by liucz 2015-10-6
	echo given count of stdin chars, also stop if meet EOF
	NOTICE: input is actually passed to program by LINE

	@chars   -> how many chars to deal with
	@tillEOF -> if True then process till EOF regardless given lines, otherwise till lines < 1 or meet EOF
	@return  -> a tuple: (rest of the last input line, flag of stopped by EOF)
	"""
	return dealWithChars(chars, 'echo', tillEOF)


def storeChars(chars, tillEOF = False):
	"""
	write by liucz 2015-10-6
	store given count of stdin chars, also stop if meet EOF
	NOTICE: input is actually passed to program by LINE

	@chars   -> how many chars to deal with
	@tillEOF -> if True then process till EOF regardless given lines, otherwise till lines < 1 or meet EOF
	@return  -> a tuple: (list of chars stored, rest of the last input line, flag of stopped by EOF)
	"""
	return dealWithChars(chars, 'store', tillEOF)


def discardLines(lines, tillEOF = False):
	"""
	write by liucz 2015-10-6
	discard given count of stdin lines, also stop if meet EOF

	@lines   -> how many lines to deal with
	@tillEOF -> if True then process till EOF regardless given lines, otherwise till lines < 1 or meet EOF
	@return  -> flag of stopped by EOF
	"""
	return dealWithLines(lines, '', tillEOF)


def echoLines(lines, tillEOF = False):
	"""
	write by liucz 2015-10-6
	echo given count of stdin lines, also stop if meet EOF

	@lines   -> how many lines to deal with
	@tillEOF -> if True then process till EOF regardless given lines, otherwise till lines < 1 or meet EOF
	@return  -> flag of stopped by EOF
	"""
	return dealWithLines(lines, 'echo', tillEOF)


def storeLines(lines, tillEOF = False):
	"""
	write by liucz 2015-10-6
	store given count of stdin lines, also stop if meet EOF, return lines stored

	@lines   -> how many lines to deal with
	@tillEOF -> if True then process till EOF regardless given lines, otherwise till lines < 1 or meet EOF
	@return  -> a tuple: (list of input lines stored, flag of stopped by EOF)
	"""
	return dealWithLines(lines, 'store', tillEOF)


def dealWithLines(lines, option, tillEOF = False):
	"""
	write by liucz 2015-10-6
	method to deal with stdin lines

	@lines   -> how many lines to deal with
	@option  -> indicate the way to deal with: 'echo', 'store', otherwise discard
	@tillEOF -> if True then process till EOF regardless given lines, otherwise till lines < 1 or meet EOF
	@return  -> if option = 'store' then a tuple: (list of input lines stored, flag of stopped by EOF)
	            else flag of stopped by EOF
	"""
	stored = []
	stoppedByEOF = False
	while tillEOF or lines > 0:
		try:
			s = input()
			s += '\n'
			if option == 'echo':
				print(s, end = '')
			elif option == 'store':
				stored.append(s)
			lines -= 1
		except:
			stoppedByEOF = True
			break
	if option == 'store':
		return stored, stoppedByEOF
	return stoppedByEOF


def dealWithChars(chars, option, tillEOF = False):
	"""
	write by liucz 2015-10-6
	method to deal with stdin chars

	@lines   -> how many chars to deal with
	@option  -> indicate the way to deal with: 'echo', 'store', otherwise discard
	@tillEOF -> if True then process till EOF regardless given lines, otherwise till lines < 1 or meet EOF
	@return  -> if option = 'store' then a tuple: (list of chars stored, rest of the last input line, flag of stopped by EOF)
	            else a tuple: (rest of the last input line, flag of stopped by EOF)
	"""
	if tillEOF:
		if option == 'echo':
			return '', dealWithLines(-1, 'echo', True)
		elif option == 'store':
			stored, _ = dealWithLines(-1, 'store', True)
			res = []
			for line in stored:
				res.extend([c for c in line])
				res.append('\n')
			return res, '', True
		else:
			return '', dealWithLines(-1, '', True)

	stored = []
	stoppedByEOF = False
	while chars > 0:
		try:
			s = input()
			s += '\n'
			n = len(s)

			if n < chars:
				# process the whole line
				t = s
				chars -= n
			else:
				# this is the last line, split the remaining chars
				t = s[0:chars]
				s = s[chars:]
				chars = 0

			if option == 'echo':
				print(t, end = '')
			elif option == 'store':
				res.extend([c for c in t])

		except:
			stoppedByEOF = True
			s = ''
			break

	if option == 'store':
		return res, s, stoppedByEOF
	return s, stoppedByEOF
