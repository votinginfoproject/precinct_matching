#this is the main compendium of individual functions that support hc_finalizer.py (currently california_hc_finalizer.py)
#state id = 1
#election_administration id = 2 (for the state office), 3 (for the local office)
#locality id = 4
#source id = 10000867380 (867380 is VIP in dec)
#election id = 100000564950 (564950 is VIP in hex)


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
	election_administration_id = "2"
	state_id = "1"

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

	paste(source_end_loc, source_full)

def make_locality(locality_name, locality_type, final_path):
	"constructs the locality data, linking it to the local election administrator."

	locality_end_loc = final_path + "locality.txt"

	header = "name,state_id,type,election_administration_id,id"

	state_id = "1"
	election_administration_id = "3"
	locality_id = "4"



	locality_data = ",".join([locality_name,state_id,locality_type,election_administration_id,locality_id])

	locality_full = header + "\n" + locality_data

	san_check(locality_full, header, "locality.txt")

	locality = open(locality_end_loc, "w+")
	locality.write(locality_full)




def make_election_admins(state_name, locality_name, start_path, final_path):
	"constructs both a state and a local election administrator."
	"this draws on a templated statewide election administrator, and a local election"
	"administrator drawn from a combination of the spreadsheets put together by dogcatcher"
	"and outside research."

	#TODO:  create the relevant election officials
	#TODO: draw from an external URLs file

	import re
	
	content_type = "election_administration.txt"

	election_admin_end_loc = final_path + content_type

	header = "name,eo_id,ovc_id,physical_address_location_name,\
physical_address_line1,physical_address_line2,physical_address_line3,physical_address_city,\
physical_address_state,physical_address_zip,mailing_address_location_name,mailing_address_line1,\
mailing_address_line2,mailing_address_line3,mailing_address_city,mailing_address_state,\
mailing_address_zip,elections_url,registration_url,am_i_registered_url,absentee_url,\
where_do_i_vote_url,what_is_on_my_ballot_url,rules_url,voter_services,hours,id"

	state_election_admin_header = copy(start_path, content_type)

	
	#TODO: HERE"S WHERE LOCAL ADMINS HAPPEN
	
	local_admin_loc = start_path + state_name + " election admins.txt"

	admin = open(local_admin_loc, "r").read()

	locality_name_short = " ".join(locality_name.split()[0:len(locality_name.split())-1])

	clerk_re = re.compile("\n.+?" + locality_name_short.title() + ".+?\n")

	office_name_re = re.compile("([A-Za-z ]+)[,-].*?\d|.*?\d.*?[,-]([A-Za-z ]+)")

	clerk = clerk_re.findall(admin)[0].strip("\n").split("\t")

	name = clerk[0]
	hours = clerk[33]


	street_1 = clerk[5]
	city = clerk [6]
	state = clerk[7]
	street_zip = clerk[8]


	if office_name_re.findall(street_1):
		if office_name_re.findall(street_1)[0][0]:
			office_name = office_name_re.findall(street_1)[0][0].strip()
		elif office_name_re.findall(street_1)[0][1]:
			office_name = office_name_re.findall(street_1)[0][1].strip()
		
		street_1 = street_1.replace(office_name,"").strip(", ")
	else:
		office_name = ""

	if clerk[9]:
		mail_street_1 = clerk[9]
		mail_city = clerk[10]
		mail_state = clerk[11]
		mail_zip = clerk[12]
	else:
		mail_street_1 = ""
		mail_city = ""
		mail_state = ""
		mail_zip = ""

	elections_url = clerk[32]
	
	address = ",".join([office_name, street_1, "", "", city, state, street_zip])
	mailing_address = ",".join(["", mail_street_1, "", "", mail_city, mail_state, mail_zip])
	url_list = ",".join([elections_url, "", "", "", "", "", ""])

	print mailing_address

	local_election_admin = ",".join([name, "", "", address, mailing_address, url_list, "", hours, "4"])

	election_admin_full = state_election_admin_header + "\n" + local_election_admin

	san_check(election_admin_full, header, content_type)

	paste(election_admin_end_loc, election_admin_full)


def san_check(data, header, filename):
	"these are two basic tests to make sure that the text to be copied is formatted correctly. More can be added."
	"the first ensures that every line in the data has the same number of columns."
	"the second ensures that the header matches the expected header."

	import sys

	testing_data = data.split("\n")

	for line in testing_data[0:len(testing_data)-1]:
		if line.count(",") != testing_data[testing_data.index(line) + 1].count(","):
			print filename + " seems to have an incorrect number of columns in row " + str(testing_data.index(line) + 2) + ". You should fix this."
			print "There are " + str(line.count(",") + 1) + " columns in row " + str(testing_data.index(line) + 1) + " and " + str(testing_data[testing_data.index(line) + 1].count(",") + 1) + " columns in row " + str(testing_data.index(line) + 2) + "."
			print line
			print testing_data[testing_data.index(line) + 1]
			sys.exit()

	if testing_data[0] != header:
		print "It looks like " + filename +  " has the wrong headers. You need to fix this."
		print "Here's the header:"
		print testing_data[0]
		print "Here's what you've said it should be:"
		print header
		sys.exit()