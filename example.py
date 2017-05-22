import warnings
import json
warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer

# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)

if __name__ == '__main__':

	# create a Dejavu instance
	djv = Dejavu(config)

	# Fingerprint all the mp3's in the directory we give it
	djv.fingerprint_directory("mp3_bt", [".mp3"])

	# Recognize audio from a file
	jiangdiao_song = djv.recognize(FileRecognizer, "mp3/jiangdiaoban.mp3")
	print "jiangdiao_song: %s\n" % jiangdiao_song

	man4 = djv.recognize(FileRecognizer, "mp3/man4.mp3")
	print "man4: %s\n" % man4

	xianchangban = djv.recognize(FileRecognizer, "mp3/xianchangban.mp3")
	print "xianchangban: %s\n" % xianchangban

	yanchanghui = djv.recognize(FileRecognizer, "mp3/yanchanghui.mp3")
	print "yanchanghui: %s\n" % yanchanghui

	liyifeng = djv.recognize(FileRecognizer, "mp3/liyifeng.mp3")
	print "liyifeng: %s\n" % liyifeng

	gaoshengmei = djv.recognize(FileRecognizer, "mp3/gaoshengmei_quanxinbianqu.mp3")
	print "gaoshengmei_quanxinbianqu.mp3: %s\n" % gaoshengmei

	other = djv.recognize(FileRecognizer, "mp3/other.mp3")
	print "othder.mp3: %s\n" % other

	# Or recognize audio from your microphone for `secs` seconds
	# secs = 5
	# song = djv.recognize(MicrophoneRecognizer, seconds=secs)
	# if song is None:
		# print "Nothing recognized -- did you play the song out loud so your mic could hear it? :)"
	# else:
		# print "From mic with %d seconds we recognized: %s\n" % (secs, song)

	# Or use a recognizer without the shortcut, in anyway you would like
	# recognizer = FileRecognizer(djv)
	# song = recognizer.recognize_file("mp3/Josh-Woodward--I-Want-To-Destroy-Something-Beautiful.mp3")
	# print "No shortcut, we recognized: %s\n" % song
