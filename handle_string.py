"""
write by liucz 2015-10-7
handy functions to deal with string
"""


def unique(s, table = None, bench = None):
	"""
	write by liucz 2015-10-7
	squeeze continuous repeated chars to one
	
	@s      -> string to be dealt with
	@table  -> replace the repeated char to the corresponding target if exist
	@bench   -> if repeated char not in table and bench is not None then replace the repeated chars to bench
	@return -> string with no continuous repeated chars
	"""
	if not s:
		return s

	t = ''
	lastChar = s[0]
	repeated = False

	for c in s[1:]:
		if c != lastChar:
			t += lastChar if not repeated \
						  else table[lastChar] if table and lastChar in table \
						  					   else bench if bench is not None \
						  					   			  else lastChar
			lastChar = c
			repeated = False
		else:
			repeated = True
	# deal with last char
	if repeated and table and c in table:
		t += table[c]
	elif bench is not None:
		t += bench
	else:
		t += lastChar

	return t


def complementUnique(s, keepSet, table = None, bench = None):
	"""
	write by liucz 2015-10-7
	squeeze continuous repeated chars to one
	
	@s       -> string to be dealt with
	@keepSet -> chars set whose repetition are keeped
	@table   -> replace the repeated char to the corresponding target if exist
	@bench   -> if repeated char not in table and bench is not None then replace the repeated chars to bench
	@return  -> string with no continuous repeated chars except those in keepSet
	"""
	if not s:
		return s

	t = ''
	lastChar = s[0]
	times = 1

	for c in s[1:]:
		if c != lastChar:
			if lastChar in keepSet:
				t += lastChar * times
			elif times == 1:
				t += lastChar
			elif table and lastChar in table:
				t += table[lastChar]
			elif bench is not None:
				t += bench
			else:
				t += lastChar
			lastChar = c
			times = 1
		else:
			times += 1
	# deal with last char
	if lastChar in keepSet:
		t += lastChar * times
	elif times == 1:
		t += lastChar
	elif table and lastChar in table:
		t += table[lastChar]
	elif bench is not None:
		t += bench
	else:
		t += lastChar

	return t


def replace(s, table, removeIfNonexistentInTable = False):
	"""
	write by liucz 2015-10-7
	replace source char to corresponding target in table
	
	@s      -> string to be dealt with
	@table  -> dict of source to target
	@removeIfNonexistentInTable: if true then the no target source is removed otherwise keeped
	@return -> string with char in table being replaced
	"""
	return ''.join((table[c] if table and c in table 
							 else '' if removeIfNonexistentInTable 
							 		 else c
					for c in s))

def delete(s, targetSet):
	"""
	write by liucz 2015-10-7
	remove all chars in targetSet
	
	@s        -> string to be dealt with
	@knownSet -> set of chars to be removed
	@return   -> string with no char in targetSet
	"""
	return ''.join(('' if c in targetSet else c for c in s))


def complement(s, keepSet, t):
	"""
	write by liucz 2015-10-7
	replace chars not in keepSet to t
	
	@s        -> string to be dealt with
	@knownSet -> set of chars to be keeped
	@return   -> string with char not in keepSet being replaced by t
	"""
	return ''.join((c if c in keepSet 
					  else t 
					for c in s))
