#! python3
# cueSheet.py - A script to create cue sheets from a list of files

from pathlib import Path
import sys

def yesNo():
    while True:
        yesNoInput = str(input())
        if yesNoInput.lower() == 'y' or yesNoInput.lower() == 'yes':  
            return 'y'
            break
        if yesNoInput == 'n' or yesNoInput.lower() == 'no':
            return 'n'
            break
        print('Please only answer "yes" or "no", without quotation marks.')
        print()

print('This program creates cue sheets from the files within a folder.')

# Make sure the program is operating in the correct folder
print('Is this program in the directory containing the music files of interest?')
dirYN = yesNo()
if dirYN == 'y':
    p = Path.cwd()
else:
    print('Please type the absolute path of the directory of interest.')
    p = Path(str(input()))
# Ask for the file format to look for
print('Which file extension are you looking for (e.g. flac, mp3, wav, etc.)? Do not include the . symbol.')
print('Note: If you mistype the format, your cue file will be wrong.')
fileType = str(input())
globName = str('*.'+fileType)
fileList = list(p.glob(globName))
if fileList == []:
    print('No files with that extension were found within the specified directory.')
    print('Press Enter to exit the program.')
    input()
    sys.exit()
# Report the number of files found with that extension and give the option of canceling
print('%s file(s) with that extension were found in the specified directory.'%(len(fileList)))
if len(fileList) > 99:
    print('A cue sheet cannot apply to more than 99 files.')
    print('Press Enter to exit the program.')
    input()
    sys.exit()
print('Are you sure you want to create a cue sheet for %s files?'%(len(fileList)))
filesYN = yesNo()
if filesYN == 'n':
    print('Okay. Press Enter to exit the program.')
    input()
    sys.exit()
# Create a track filename list
trackFile = []
for i in range(len(fileList)):
    trackFile.append(fileList[i].name)
trackFile.sort()

# Ask for album artist and title
print('Please provide the album artist exactly as you would like it to appear.')
albumArtist = str(input())
print('Now provide the album title.')
albumTitle = str(input())
'''# Ask if files are listed as 01 - "Name", 02 - "Name", etc.
print('Are the files listed in a manner similar to "01 - TrackTitle.extension"? Please answer yes or no.')
fileYN = yesNo()'''
titleDict = {}
# Offer to give the name and track number of each individual file
#if fileYN == 'n':
for i in range(len(trackFile)):
    # Maybe a dictionary, to assign track titles to track numbers
    # And then make the keys the number list, and the values the track list
    print('What is the correct title for the file "%s"?'%(trackFile[i]))
    print('Note: you can always edit the .cue file if you make a mistake.')
    title = str(input())
    while True:
        print('What is the track number for "%s"?'%(title))
        try:
            number = int(input())
        except:
            print('The track number must be a number between 0 and %s (inclusive).'%(len(trackFile)))
            continue
        if number <= len(trackFile):
            if number >= 0:
                break
            else:
                print('The track number must be a number between 0 and %s (inclusive).'%(len(trackFile)))
        else:
            print('The track number must be a number between 0 and %s (inclusive).'%(len(trackFile)))
    # Make sure the number of digits is uniform
    if len(str(number)) < len(str(len(trackFile))):
        strNumber = "0"+str(number)
    else:
        strNumber = str(number)
    titleDict[strNumber] = title
'''else:
    # TODO - If so, then extract the track title from the file name and create a dictionary from that
    for i in range(len(trackFile)):
        for letter in trackFile[i]:
            try:
                int(letter)'''
# Inform the user of the tracklist
print('According to the data you have entered,')
for number in titleDict:
    print(' Track number "%s" is titled "%s".'%(number, titleDict[number]))
print('If this is incorrect, please either edit the .cue sheet after completion or exit the script now.')
try:
    print('Press Enter to continue or keyboard interrupt (Ctrl+C) to quit.')
    input()
except KeyboardInterrupt:
    print('Thank you for trying cueSheet.py.')
    print('Press Enter to exit.')
    input()
    sys.exit()
    
# Ask if any of the tracks have a different artist from the album artist
print('Do any of the tracks have a different artist from the album artist?')
artistYN = yesNo()
# If so, ask for the artist for each track. Store these and keep them on hold for each track
artistDict = {}
if artistYN == 'y':
    for number in titleDict.keys():
        print('Who is the artist for "%s"?'%(titleDict[number]))
        artist = str(input())
        artistDict[number] = artist
# If not, fill the artistDict with the album artist
else:
    for number in titleDict.keys():
        artistDict[number] = albumArtist

# Sanity check
if len(trackFile) == len(list(titleDict.keys())):
    if len(trackFile) == len(list(titleDict.values())):
        if len(trackFile) == len(list(artistDict.values())):
            sanityCheck = True
        else:
            print('The track artist list does not match the number of tracks.')
            print('Press Enter to exit the program.')
            input()
            sys.exit()
    else:
        print('The track title list does not match the number of tracks.')
        print('Press Enter to exit the program.')
        input()
        sys.exit()
else:
    print('The number of tracks does not match the number of track files.')
    print('Press Enter to exit the program.')
    input()
    sys.exit()

# Sort the dictionaries
# Note: this may not be the most efficienct way to sort these
titleList = sorted((key, value) for (key,value) in titleDict.items()) # flip the first key, value to sort by values instead
sortTitles = dict([(v,k) for v,k in titleList]) # flip the first v,k to sort by values instead
artistList = sorted((key,value) for (key,value) in artistDict.items())
sortArtists = dict([(v,k) for v,k in artistList])

# Inform the user of the order of tracks and track artists
print('The .cue sheet will use the following info in this order:')
for number in sortTitles.keys():
    print('Track %s - %s by %s'%(number,sortTitles[number],sortArtists[number]))
print('If this is incorrect, please either edit the .cue sheet after completion or exit the script now.')
try:
    print('Press Enter to continue or keyboard interrupt (Ctrl+C) to quit.')
    input()
except KeyboardInterrupt:
    print('Thank you for trying cueSheet.py.')
    print('Press Enter to exit.')
    input()
    sys.exit()

# Create the cue sheet, naming it cuePy.cue
cueLoc = p / 'cuePy.cue'
cueFile = open(cueLoc, 'w')
cueFile.write('REM Generated by cueSheet.py\n')
cueFile.write('TITLE "' + albumArtist + '"\n')
cueFile.write('PERFORMER "' + albumTitle + '"\n')
# Important variables right now are sortTitles and sortArtists
print('Creating the .cue sheet ...')
# Take the list of files and create the File, Track number, and track title portions of the cue file
trackNum = list(sortTitles.keys())
trackTitle = list(sortTitles.values())
trackArtist = []
for number in trackNum:
    trackArtist.append(sortArtists[number])
for i in range(len(trackFile)):
    cueFile.write('FILE "' + trackFile[i] + '" WAVE\n')
    cueFile.write('  TRACK ' + trackNum[i] + ' AUDIO\n')
    cueFile.write('    TITLE "' + trackTitle[i] + '"\n')
    cueFile.write('    PERFORMER "' + trackArtist[i] + '"\n')
    cueFile.write('    INDEX 01 00:00:00\n')
cueFile.close()
print('Your cue sheet, cuePy.cue, has been created.')
print('It should be located in the specified directory.')
input('Press Enter to close this program.')
