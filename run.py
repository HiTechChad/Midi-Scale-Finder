from mido import MidiFile
import sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help='File Pathway ie. drag and drop')
args = parser.parse_args()


#notes and corosponding midi and offset
Octive_Notes = [[0, 'c'], [1, 'c#'], [2, 'd'], [3, 'd#'], [4, 'e'], [5, 'f'], [6, 'f#'], [7, 'g'], [8, 'g#'], [9, 'a'], [10, 'a#'], [11, 'b']]
All_Midi_Note_Values= [[0, 'c'], [1, 'c#'], [2, 'd'], [3, 'd#'], [4, 'e'], [5, 'f'], [6, 'f#'], [7, 'g'], [8, 'g#'], [9, 'a'], [10, 'a#'], [11, 'b'], [12, 'c'], [13, 'c#'], [14, 'd'], [15, 'd#'], [16, 'e'], [17, 'f'], [18, 'f#'], [19, 'g'], [20, 'g#'], [21, 'a'], [22, 'a#'], [23, 'b'], [24, 'c'], [25, 'c#'], [26, 'd'], [27, 'd#'], [28, 'e'], [29, 'f'], [30, 'f#'], [31, 'g'], [32, 'g#'], [33, 'a'], [34, 'a#'], [35, 'b'], [36, 'c'], [37, 'c#'], [38, 'd'], [39, 'd#'], [40, 'e'], [41, 'f'], [42, 'f#'], [43, 'g'], [44, 'g#'], [45, 'a'], [46, 'a#'], [47, 'b'], [48, 'c'], [49, 'c#'], [50, 'd'], [51, 'd#'], [52, 'e'], [53, 'f'], [54, 'f#'], [55, 'g'], [56, 'g#'], [57, 'a'], [58, 'a#'], [59, 'b'], [60, 'c'], [61, 'c#'], [62, 'd'], [63, 'd#'], [64, 'e'], [65, 'f'], [66, 'f#'], [67, 'g'], [68, 'g#'], [69, 'a'], [70, 'a#'], [71, 'b'], [72, 'c'], [73, 'c#'], [74, 'd'], [75, 'd#'], [76, 'e'], [77, 'f'], [78, 'f#'], [79, 'g'], [80, 'g#'], [81, 'a'], [82, 'a#'], [83, 'b'], [84, 'c'], [85, 'c#'], [86, 'd'], [87, 'd#'], [88, 'e'], [89, 'f'], [90, 'f#'], [91, 'g'], [92, 'g#'], [93, 'a'], [94, 'a#'], [95, 'b'], [96, 'c'], [97, 'c#'], [98, 'd'], [99, 'd#'], [100, 'e'], [101, 'f'], [102, 'f#'], [103, 'g'], [104, 'g#'], [105, 'a'], [106, 'a#'], [107, 'b'], [108, 'c'], [109, 'c#'], [110, 'd'], [111, 'd#'], [112, 'e'], [113, 'f'], [114, 'f#'], [115, 'g'], [116, 'g#'], [117, 'a'], [118, 'a#'], [119, 'b'], [120, 'c'], [121, 'c#'], [122, 'd'], [123, 'd#'], [124, 'e'], [125, 'f'], [126, 'f#'], [127, 'g']]

## Base scales (C)
major = [0,2,4,5,7,9,11]
minor = [0,2,3,5,7,8,10]

##add other scales later
scales = [[major, 'Major'], [minor, 'Minor']]

# Relative scales
relative = [[0,9],[1,10],[2,11],[3,0],[4,1],[5,2],[6,3],[7,4],[8,5],[9,6],[10,7],[11,8]]

#current key and scale
current_key = 0
current_scale = 0


# Transpose function if not in c maj or min
def Transpose(scale):
	new_scale = []
	for i in scale:
		new_scale.append(scale[i] + 1)
	return new_scale
def Transpose(scale, n_notes):
	new_scale = []
	for i in scale:
		new_scale.append(i + n_notes)
	return new_scale


# Get all midi notes in scale 0-127
def Get_Scale_Midi_Notes(scale):
	all_notes_in_scale = []
	for i in scale:
		octive = 0 ## multiplier
		tmparrry = []
		while (octive * 12) + All_Midi_Note_Values[i][0] <= 127:
			tmparrry.append((octive * 12) + All_Midi_Note_Values[i][0])
			octive += 1

		all_notes_in_scale.append(tmparrry)
	return all_notes_in_scale

# Change key and scale functions
def Change_Key():
	global current_key 
	if current_key < len(Octive_Notes) - 1:
		current_key += 1
	else:
		current_key = 0
		Change_Scale()

def Change_Scale():
	global current_scale
	if current_scale < len(scales[current_scale][0]) - 1:
		current_scale += 1
	else:
		#EXIT PROGRAM
		sys.exit("Out of possible key and scale combinations. exiting programg")

# Load Midi notes into array
def Load_Midi_Notes(file):
	mid = MidiFile(file)
	note_array = []
	for i, track in enumerate(mid.tracks):
		for msg in track:
			if not msg.is_meta:
				if hasattr(msg, 'note'):
					note_array.append(msg.note)
	return list(dict.fromkeys(note_array))


def Compare(scale, midi_notes):
	# i = midi value from file note
	for i in midi_notes:
		value_is_found = False
		## j = array of possible note midi values
		for j in scale:
			if i in j:
				value_is_found = True
				break
		if not value_is_found:
			return False

	return True

def Get_Relative(key, scale):
	if scale == 0 or scale == 1:
		if scale == 0:
			return [Octive_Notes[relative[key][1]][1], scales[1][1]]
		if scale == 1:
			for i in relative:
				if key == i:
					return [Octive_Notes[i[0]][1], scales[0][1]]
	return None

def main():
	exit = False
	midi_notes = Load_Midi_Notes(args.file)
	while not exit:
		if Compare(Get_Scale_Midi_Notes(Transpose(scales[current_scale][0], current_key)), midi_notes):
			print str(Octive_Notes[current_key][1]) + " " + str(scales[current_scale][1])
			key_relative = Get_Relative(current_key, current_scale)
			if key_relative != None:
				print "Reltive key is " + str(key_relative[0]) + " " + str(key_relative[1])
			exit = True
		else:
			Change_Key()




if __name__ == '__main__':
    main()