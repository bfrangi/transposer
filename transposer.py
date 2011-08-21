#!/usr/bin/python
# encoding: utf-8
"""
transposer.py

Created by David P�rsson on 2011-08-13.
"""

import sys
import os
import re, getopt

key_list = [('A',), ('A#', 'Bb'), ('B',), ('C',), ('C#', 'Db'), ('D',),
            ('D#', 'Eb'), ('E',), ('F',), ('F#', 'Gb'), ('G',), ('G#', 'Ab')]

sharp_flat = ['#', 'b']
sharp_flat_preferences = {
	'A' : '#',
	'A#': 'b',
	'Bb': 'b',
	'B' : '#',
	'C' : 'b',
	'C#': 'b',
	'Db': 'b',
	'D' : '#',
	'D#': 'b',
	'Eb': 'b',
	'E' : '#',
	'F' : 'b',
	'F#': '#',
	'Gb': '#',
	'G' : '#',
	'G#': 'b',
	'Ab': 'b',
	}

key_regex = re.compile(r"[ABCDEFG][#b]?")

def get_index_from_key(source_key):
	for key_names in key_list:
		if source_key in key_names:
			return key_list.index(key_names)
	raise Exception("Invalid key: %s" % source_key)

def get_key_from_index(index, to_key):
	key_names = key_list[index % len(key_list)]
	if len(key_names) > 1:
		sharp_or_flat = sharp_flat.index(sharp_flat_preferences[to_key])
		return key_names[sharp_or_flat]
	return key_names[0]

def get_transponation_steps(source_key, target_key):
	source_index = get_index_from_key(source_key)
	target_index = get_index_from_key(target_key)
	return target_index - source_index

def transpose(source_chord, direction, to_key):
	source_index = get_index_from_key(source_chord)
	return get_key_from_index(source_index + direction, to_key)

def transpose_file(file_name, from_key, to_key):
	direction = get_transponation_steps(from_key, to_key)
	result = ''
	try:
		for line in open(file_name):
			if line[0] == '|':
				result += transpose_line(line, direction, to_key)
			else:
				result += line
		return result
	except IOError:
		print("Invalid filename!")
		usage()

def transpose_line(source_line, direction, to_key):
	source_chords = key_regex.findall(source_line)
	return recursive_line_transpose(source_line, source_chords, direction, to_key)
	
def recursive_line_transpose(source_line, source_chords, direction, to_key):
	if not source_chords or not source_line:
		return source_line
	source_chord = source_chords.pop(0)
	chord_index = source_line.find(source_chord)
	after_chord_index = chord_index + len(source_chord)
	
	return source_line[:chord_index] + \
		   transpose(source_chord, direction, to_key) + \
		   recursive_line_transpose(source_line[after_chord_index:], source_chords, direction, to_key)


def usage():
	print 'Usage:'
	print '%s --from=Eb --to=F# input_filename' % os.path.basename(__file__)
	sys.exit(2)

def main():
	from_key = 'C'
	to_key = 'C'
	file_name = None
	try:
		options, arguments = getopt.getopt(sys.argv[1:], 'f:t:', ['from=', 'to='])
	except getopt.GetoptError, err:
		print str(err)
		#usage()
		sys.exit(2)
	for option, value in options:
		if option in ('-f', '--from'):
			from_key = value
		elif option in ('-t', '--to'):
			to_key = value
		else:
			usage()
	
	if arguments:
		file_name = arguments[0]
	else:
		usage()
	
	result = transpose_file(file_name, from_key, to_key)
	
	print("Result (%s -> %s):" % (from_key, to_key))
	print(result)
	
#	verify(get_transponation_steps('D', 'C') == -2)
	
#	print "All is OK!"

def verify(expression):
	if not expression:
		raise Exception("Test verification failed")

if __name__ == '__main__':
	main()