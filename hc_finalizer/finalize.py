#this is the main compendium of individual functions that support hc_finalizer.py (currently california_hc_finalizer.py)


def copy(start_path, content_type):
	"returns a standard piece of data housed in a specified location."

	original_loc = start_path + content_type

	carbon_copy = open(original_loc, "r").read()

	return carbon_copy

def paste(final_full_path,content):
	"prints known data to a known location"

	output_file = open(final_full_path, "w")
	output_file.write(content)



def copy_paste(start_path, final_path, header, content_type):
	"takes a standard file housed in the state-level folder, and makes a new copy housed in the final_data folder"
	"after performing a few validations"

	import sys

	carbon_copy = copy(start_path,content_type)

	san_check(carbon_copy,header,content_type)

	paste_loc = final_path + content_type

	paste(paste_loc,carbon_copy)


def make_state(final_path, state_name, header):
	"makes the state.txt file, deposits it in the finalized data folder"

	state_end_loc = final_path + "state.txt"

	name = state_name
	#Since we will only ever have one state-level election administrator associated with 
	#a given hand-matched feed, we can match election_administration_id based on a fixed ID.
	election_administration_id = "1"
	state_id = "2"

	state_data = ",".join([name,election_administration_id,state_id])
	state_full = header + "\n" + state_data

	san_check(state_full, header, "state.txt")

	state = open(state_end_loc, "w")
	state.write(state_full)


def make_source(final_path):

	import time

	source_end_loc = final_path + "source.txt"

	header = "name,vip_id,datetime,description,organization_url,feed_contact_id,tou_url,id"
	
	name = "VIP"	
	source_id = "10000867380"
	description = "VIP aggregates this data from official state sources"
	organization_url = "http://votinginfoproject.org"
	datetime = time.strftime("%Y-%m-%dT%X")

	source_data = ",".join([name,"",datetime,description,organization_url,"","",source_id])
	source_full = header + "\n" + source_data

	san_check(source_full, header, "source.txt")

	source = open(source_end_loc, "w+")
	source.write(source_full)


def make_election_admins(start_path, final_path):
	"constructs both a state and a local election administrator."
	"this draws on a templated statewide election administrator, and a local election"
	"administrator drawn from a combination of the spreadsheets put together by dogcatcher"
	"and outside research."
	#todo: actually write this!

def san_check(data, header, filename):
	"these are two basic tests to make sure that the text to be copied is formatted correctly. More can be added."
	"the first ensures that every line in the data has the same number of columns."
	"the second ensures that the header matches the expected header."

	import sys

	testing_data = data.split("\n")

	for line in testing_data[0:len(testing_data)-1]:
		if line.count(",") != testing_data[testing_data.index(line)+1].count(","):
			print filename + " seems to have an incorrect number of columns in row " + str(testing_data.index(line)+2) + ". You should fix this."
			print line
			print testing_data[testing_data.index(line)+1]
			sys.exit()

	if testing_data[0] != header:
		print "It looks like " + filename +  " has the wrong headers. You need to fix this."
		print "Here's the header:"
		print testing_data[0]
		sys.exit()