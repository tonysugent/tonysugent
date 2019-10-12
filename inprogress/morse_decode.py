import scipy.io.wavfile
import numpy
import sys
import statistics as s

numpy.set_printoptions(threshold=sys.maxsize)

rate, wav = scipy.io.wavfile.read(sys.argv[1])


def piece_maker(beepsandboops):
    # Take input from word_maker() and return a piece of the morse code

    if 'hold' in beepsandboops:
        return 'hold'

    elif 'hold' not in beepsandboops:
        return 'boop'

    else:
        print("Error: Can't tell if boop or hold")


def letter_maker(pieces):
    # switcher for morse to english

    if pieces == ['boop', 'hold']:
        return 'A'
    elif pieces == ['hold', 'boop', 'boop', 'boop']:
        return 'B'
    elif pieces == ['hold', 'boop', 'hold', 'boop']:
        return 'C'
    elif pieces == ['hold', 'boop', 'boop']:
        return 'D'
    elif pieces == ['boop']:
        return 'E'
    elif pieces == ['boop', 'boop', 'hold', 'boop']:
        return 'F'
    elif pieces == ['hold', 'hold', 'boop']:
        return 'G'
    elif pieces == ['boop', 'boop', 'boop', 'boop']:
        return 'H'
    elif pieces == ['boop', 'boop']:
        return 'I'
    elif pieces == ['boop', 'hold', 'hold', 'hold']:
        return 'J'
    elif pieces == ['hold', 'boop', 'hold']:
        return 'K'
    elif pieces == ['boop', 'hold', 'boop', 'boop']:
        return 'L'
    elif pieces == ['hold', 'hold']:
        return 'M'
    elif pieces == ['hold', 'boop']:
        return 'N'
    elif pieces == ['hold', 'hold', 'hold']:
        return 'O'
    elif pieces == ['boop', 'hold', 'hold', 'boop']:
        return 'P'
    elif pieces == ['hold', 'hold', 'boop', 'hold']:
        return 'Q'
    elif pieces == ['boop', 'hold', 'boop']:
        return 'R'
    elif pieces == ['boop', 'boop', 'boop']:
        return 'S'
    elif pieces == ['hold']:
        return 'T'
    elif pieces == ['boop', 'boop', 'hold']:
        return 'U'
    elif pieces == ['boop', 'boop', 'boop', 'hold']:
        return 'V'
    elif pieces == ['boop', 'hold', 'hold']:
        return 'W'
    elif pieces == ['hold', 'boop', 'boop', 'hold']:
        return 'X'
    elif pieces == ['hold', 'boop', 'hold', 'hold']:
        return 'Y'
    elif pieces == ['hold', 'hold', 'boop', 'boop']:
        return 'Z'
    else:
        print("error: Character not recognized " + str(pieces))


def word_maker(peaks, splitter):
    wav_data = splitter[0]
    spaces = splitter[1]
    counter_list = splitter[2]
    hold = peaks[0]
    boop = peaks[1]

    # containers for morse data.
    # pieces from strings of sounds go into the container, after a long enough pause is in the audio
    # they get put through letter_maker() and get translated into letters. After the space exceeds a certain
    # number they turn into complete words and get printed.
    container = []
    pieces = []
    letters = []
    words = []

    for i in range(1, len(wav_data)):
        # go through the wav data and find peaks in the audio (found in usable_datamaker()) and put them into containers
        if wav_data[i-1] in peaks:

            if wav_data[i-1] == hold:
                container.append('hold')

            elif wav_data[i-1] == boop:
                container.append('boop')

            else:
                print('!!!!!!!!!!!!!!Error!!!!!!!!!!!!!!!')
        # see if the current piece of the wav file is equivalent to a number deemed a space in split_detector()
        if wav_data[i-1] in counter_list[:-1]:
            # first space at the 0 position of the list of positions from split detector should be a piece to make
            # a letter

            if hold < wav_data[i-1] <= spaces[0]:
                pieces.append(piece_maker(container))
                container = []
            # the second largest space should be a letter

            elif spaces[0] < wav_data[i-1] < spaces[-1]:
                pieces.append(piece_maker(container))
                letters.append(letter_maker(pieces))
                pieces = []
                container = []
            # the thirst largest space should be a whole word
            elif spaces[0] < wav_data[i-1] <= spaces[-1]:
                pieces.append(piece_maker(container))
                letters.append(letter_maker(pieces))
                words.append(letters)
                words.append(' ')
                pieces = []
                letters = []
                container = []

    pieces.append(piece_maker(container))
    letters.append(letter_maker(pieces))
    words.append(letters)
    return words


def usable_data_maker(info):
    # get the peaks from the audio that will be the doos and the dahs that make up letters
    usable_info = []
    for i in info:
        if i not in usable_info:
            usable_info.append(i)

    # sort to grab the peaks so we can easily detect them
    usable_info.sort(reverse=True)

    return usable_info


def split_detector(peaks, data):
    # use the data we got from the usable data maker. using the knowledge of what is a peak we can go through
    # and find where spaces are and so we can see where spaces are and sort the spaces into gaps of pieces, letters and
    # words

    hold = peaks[0]
    boop = peaks[1]
    blanks = s.median(peaks)
    wav_data = []
    counter = 0
    counter_list = []
    for i in data:
        if i == boop:
            if counter != 0:
                wav_data.append(counter)
                counter_list.append(counter)
            wav_data.append(i)
            counter = 0
        elif i == hold:
            if counter != 0:
                wav_data.append(counter)
                counter_list.append(counter)
            wav_data.append(i)
            counter = 0
        elif i == blanks:
            counter = counter + 1
    counter_list.sort()
    highest_counters = []
    for x in range(1, len(counter_list)):
        if 200 > counter_list[x] - counter_list[x - 1] > 0:
            highest_counters.append(counter_list[x])
    highest_counters.append(counter_list[-1])
    counter_list.sort(reverse=True)
    splits = [wav_data, highest_counters, counter_list]
    return splits


peaks = usable_data_maker(wav)
splitter = split_detector(peaks, wav)

for i in word_maker(peaks, splitter):
    for j in i:
        print(j, end='')

print("\n")

