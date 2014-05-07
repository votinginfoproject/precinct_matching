#this is the compendium of individual functions that support hc_finalizer.py (currently california_hc_finalizer.py)
#state id = 1
#election_administration id = 2 (for the state office), 3 (for the local office)
#vip id = 0
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
	vip_id = "0"
	description = "VIP aggregates this data from official state sources"
	organization_url = "http://votinginfoproject.org"
	datetime = time.strftime("%Y-%m-%dT%X")

	source_data = ",".join([name,vip_id,datetime,description,organization_url,"","",source_id])
	source_full = header + "\n" + source_data

	san_check(source_full, header, "source.txt")

	paste(source_end_loc, source_full)

def make_locality(locality_name, fips, locality_type, final_path):
	"constructs the locality data, linking it to the local election administrator."

	locality_end_loc = final_path + "locality.txt"

	header = "name,state_id,type,election_administration_id,id"

	state_id = "1"
	election_administration_id = "3"
	locality_id = fips



	locality_data = ",".join([locality_name,state_id,locality_type,election_administration_id,locality_id])

	locality_full = header + "\n" + locality_data

	san_check(locality_full, header, "locality.txt")

	locality = open(locality_end_loc, "w+")
	locality.write(locality_full)

def make_precinct_polling_loc(working_path, final_path):
	"this creates the precinct_polling_location.txt file."

	import xlrd
	import sys

	starting_header = "id,polling_location_id"
	final_header = "precinct_id,polling_location_id"

	source_header = []
	master_index = []
	final_content = final_header

	starting_spreadsheet_loc = working_path +  "precinct_working.xlsx"
	end_spreadsheet_loc = final_path +  "precinct_polling_location.txt"

	source_data = xlrd.open_workbook(starting_spreadsheet_loc).sheet_by_index(0)

	source_header_row = source_data.row(0)
	for item in source_header_row:
		item_index = source_header_row.index(item)
		source_header.append(str(source_data.cell(0, item_index).value))


	working_header_split = starting_header.split(",")

	for element in working_header_split:

		if element not in source_header:
			print "It looks like \"" + element + "\" is missing from the source file. Try fixing this."
			sys.exit()
		else:
			element_pos = working_header_split.index(element)
			element_source_pos = source_header.index(element)
			master_index.append([element, element_pos, element_source_pos])

	for row in range(1, source_data.nrows):

		working_row = source_data.row(row)

		transformed_row = ""

		for needed_element in range(0, len(master_index)):
			needed_value = source_data.cell(row,master_index[needed_element][2]).value
			try:
				if str(int(needed_value)) == str(needed_value).replace(".0",""):
					transformed_row = transformed_row + "," + str(int(needed_value))
				else:
					transformed_row = transformed_row + "," + str(needed_value)
			except ValueError:
				transformed_row = transformed_row + "," + str(needed_value)

		transformed_row = transformed_row.strip(",").replace(".0","") #excel naturally adds ".0" to integers for precision. we don't like that shit.

		if transformed_row.count(",") > 1: #to catch precincts with multiple polling locs
			decomposed_row = transformed_row.split(",")
			transformed_row = ""
			for polling_loc_id in decomposed_row[1:len(decomposed_row)]:
				transformed_row = transformed_row + "\n" + decomposed_row[0].strip() + "," + polling_loc_id.strip()
			transformed_row = transformed_row.strip("\n")


		final_content = final_content + "\n" + transformed_row



	san_check(final_content, final_header, "precinct_polling_location.txt")

	paste(end_spreadsheet_loc, final_content)

def make_election_admins(state_name, locality_name, fips, start_path, final_path):
	"constructs both a state and a local election administrator."
	"this draws on a templated statewide election administrator, and a local election"
	"administrator drawn from a combination of the spreadsheets put together by dogcatcher"
	"and outside research."

	#TODO: draw from an external URLs file

	import re
	
	content_type = "election_administration.txt"
	url_loc = start_path + "admin_urls.txt"

	election_admin_end_loc = final_path + content_type

	header = "name,eo_id,ovc_id,physical_address_location_name,\
physical_address_line1,physical_address_line2,physical_address_line3,physical_address_city,\
physical_address_state,physical_address_zip,mailing_address_location_name,mailing_address_line1,\
mailing_address_line2,mailing_address_line3,mailing_address_city,mailing_address_state,\
mailing_address_zip,elections_url,registration_url,am_i_registered_url,absentee_url,\
where_do_i_vote_url,what_is_on_my_ballot_url,rules_url,voter_services,hours,id"

	state_election_admin_header = copy(start_path, content_type)
	
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

	address = ",".join([office_name, street_1, "", "", city, state, street_zip])
	mailing_address = ",".join(["", mail_street_1, "", "", mail_city, mail_state, mail_zip])


	urls = open(url_loc, "r").read()

	url_line_re = re.compile("\n" + locality_name.title() + ",(.+)")

	url_list = url_line_re.findall(urls)[0]

	local_election_admin = ",".join([name, "", "", address, mailing_address, url_list, "", hours, fips])

	election_admin_full = state_election_admin_header + "\n" + local_election_admin

	san_check(election_admin_full, header, content_type)

	paste(election_admin_end_loc, election_admin_full)


# def make_ev_sites(working_path, final_path, fips):
# 	"this makes the early_vote.txt file."
# 	#TODO: this won't work at all. roll this over to transform_xls when you need to.

# 	content_type = "early_vote_site.txt"
# 	ev_path = working_path + content_type
# 	paste_path = final_path + content_type

# 	header = "name,address_location_name,address_line1,address_line2,address_line3,address_city,address_state,address_zip,directions,voter_services,start_date,end_date,days_times_open,id"

# 	copy_paste(working_path, final_path, header, content_type)

# 	#TODO: validate EV sites on construction of date/time variables

# 	make_locality_ev(final_path, fips)


def make_locality_ev(final_path, fips):
	"this makes the locality_early_vote_site.txt file. It's called only"
	"if there are EV sites to be linked to localities at all."
	"It opens the EV_site file, and then systematically adds the ev_site"
	"IDs to the file, paired with the locality_id (which should just be the state FIPs)."

	header = "locality_id,early_vote_site_id"

	content_type = "locality_early_vote_site.txt"

	local_ev_end_loc = final_path + content_type

	ev_site_list = copy(final_path,"early_vote_site.txt").split("\n")

	ev_site_list.pop(0)

	locality_ev_site = open(local_ev_end_loc, "w")

	locality_ev_site_full = header

	for ev_site in ev_site_list:
		ev_site_id = ev_site.split(",").pop()
		locality_ev_site_full = locality_ev_site_full + "\n" + fips + "," + ev_site_id

	san_check(locality_ev_site_full, header, "locality_early_vote_site.txt")

	paste(local_ev_end_loc, locality_ev_site_full)

def transform_xls(working_path, final_path, header, content_type):
	"this searches a .xlsx for a specified set of headers, and then obtains"
	"all the data contained in those headers, correctly ordered."

	import xlrd
	import sys

	working_content_type = content_type + "_working.xlsx"
	final_content_name = content_type + ".txt"
	source_header = []
	master_index = []
	final_content = header #final_content will get expanded later, but it has to start with the header

	starting_spreadsheet_loc = working_path + working_content_type
	end_spreadsheet_loc = final_path + final_content_name

	print "Opening source data."

	source_data = xlrd.open_workbook(starting_spreadsheet_loc).sheet_by_index(0)

	print "Source data open. Identifying header."

	source_header_row = source_data.row(0)
	for item in source_header_row:
		item_index = source_header_row.index(item)
		source_header.append(str(source_data.cell(0, item_index).value))

	header_split = header.split(",")

	for element in header_split:

		if element not in source_header:
			print "It looks like \"" + element + "\" is missing from the source file. Try fixing this."
			sys.exit()
		else:
			element_pos = header_split.index(element)
			element_source_pos = source_header.index(element)
			master_index.append([element, element_pos, element_source_pos])

	print "Header identified. Parsing."

	for row in range(1, source_data.nrows):

		working_row = source_data.row(row)

		transformed_row = ""

		for needed_element in range(0, len(master_index)):
			needed_value = source_data.cell(row,master_index[needed_element][2]).value
			try:
				if str(int(needed_value)) == str(needed_value).replace(".0",""):
					transformed_row = transformed_row + "," + str(int(needed_value))
				else:
					transformed_row = transformed_row + "," + str(needed_value)
			except ValueError:
				transformed_row = transformed_row + "," + str(needed_value)

		transformed_row = transformed_row.strip(",").replace(".0","") #excel naturally adds ".0" to integers for precision. we don't like that shit.

		if row % 1000 == 0:
			print str(row) + " lines processed so far."

		final_content = final_content + "\n" + transformed_row

	print "Sanity checking now."

	san_check(final_content, header, final_content_name)

	paste(end_spreadsheet_loc, final_content)

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
			print [line]
			print [testing_data[testing_data.index(line) + 1]]
			sys.exit()

	if testing_data[0] != header:
		print "It looks like " + filename +  " has the wrong headers. You need to fix this."
		print "Here's the header:"
		print testing_data[0]
		print "Here's what you've said it should be:"
		print header
		sys.exit()