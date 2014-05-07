#starting with [a whole bunch of data in the /[State]/[Locality]/Working_Data folder:
#create election.txt, source.txt, polling_location.txt, precinct.txt,
#precinct_polling_location.txt, street_segment.txt, election_administration.txt,
#locality.txt and state.txt, all in [State]/[Locality]/Final_Data, as well as early_vote_site.txt (if it exists)
#to do this, we need to:
#1.1,1.2,1.3. clean and translate street_segment.xls, precinct.xls, and polling_location.xls
#(This is mostly a straight transfer, with some rows being ommitted.)
#2. construct precinct_polling_location out of precinct.xls and polling_location.xls
#3. construct state.txt from (DONE!)
#4. Constuct an election.txt file (DONE!)
#5. Constuct a source.txt file. (DONE!)
#6. Obtain election_administration information from an appropriate source. <(Probably an election_administration file in /[State])>, and construct election_administr
#7. Construct early_vote_site.txt, if the files to create it exist.
#8. Construct a locality.txt file. (DONE!)
#9. ???
#10. profit!

import os
import xlrd
import finalize
import sys

print "_________________________________"

#TODO: make state folder name an inputted variable
#TODO: make the base string of state_path flexible to different configs

locality = raw_input("Please tell me the locality we're working on. ")
locality = "lake county 033"
locality_name = " ".join(locality.split(" ")[0:-1])
print locality_name

#TODO: write in the remaining types of locality
#TODO: make state_id intelligently determined

locality_type_check = locality_name.split(" ")[-1]
if locality_type_check.lower() == "county":
	locality_type = "county"
else:
	locality_type = raw_input("Please tell me the type of locality this is. ")
state_folder = "california primary"
locality_fips = locality.split(" ")[-1]

state_path = "c:/users/paul kominers/google drive/vip/hand-collected data/" + state_folder + "/"
working_path = state_path + locality + "/working data/"
final_path = state_path + locality + "/final data/"



#this section of the code checks for reasonable initial conditions

if not os.access(state_path, os.F_OK):
	print "The state folder path appears to be incorrect. Please make sure the directories are appropriately configured."
	print "state_path: " + state_path
	sys.exit()
elif not os.access(working_path, os.F_OK):
	print "The working data folder path appears to be incorrect. Please make sure the directories are appropriately configured."
	print "working_path: " + working_path
	sys.exit()
elif not os.access(final_path, os.F_OK):
	print "The final data folder path appears to be incorrect. Please make sure the directories are appropriately configured."
	print "final_path: " + final_path
	sys.exit()

print "-All the necessary directories appear to be in good working order. Mazel tov! Now, the fun part."

#this will be the section of the code that accomplishes #2
#This runs before #1 because we need to use #1 to overwrite the bad precinct.txt that this creates.


#TODO: give precinct_polling_loc its own function that doesn't require that overwriting.
#TODO: make precinct_polling_loc able to handle precincts with multiple polling places.

print "-Now creating precinct_polling_location.txt. And..."

finalize.make_precinct_polling_loc(working_path, final_path)

print "-Achievement unlocked!"

#this will be the section of the code that accomplishes #1.1

print "-Now creating street_segment.txt. And..."

segment_header = "start_house_number,end_house_number,odd_even_both,\
start_apartment_number,end_apartment_number,non_house_address_house_number,\
non_house_address_house_number_prefix,non_house_address_house_number_suffix,\
non_house_address_street_direction,non_house_address_street_name,\
non_house_address_street_suffix,non_house_address_address_direction,\
non_house_address_apartment,non_house_address_city,non_house_address_state,\
non_house_address_zip,precinct_id,precinct_split_id,id"

finalize.transform_xls(working_path, final_path, segment_header, "street_segment")

print "-We're good!"

#this will be the section of the code that accomplishes #1.2

print "-Now creating precinct.txt. And..."

precinct_header = "name,number,locality_id,ward,mail_only,ballot_style_image_url,id"

finalize.transform_xls(working_path, final_path, precinct_header, "precinct")

print "-Boom!"

#this will be the section of the code that accomplishes #1.3

print "-Now creating polling_location.txt. And..."

polling_loc_header = "address_location_name,address_line1,address_line2,address_line3,address_city,address_state,address_zip,directions,polling_hours,photo_url,id"

finalize.transform_xls(working_path, final_path, polling_loc_header, "polling_location")

print "-It's set!"

#this is the section of the code that accomplishes #3

print "-Now creating state.txt. And..."

state_header = "name,election_administration_id,id"
state_name = state_folder.split()[0].title()

finalize.make_state(final_path, state_name, state_header)

print "-Victory!"

#this is the section of the code that accomplishes #4

print "-Now copying election.txt. And..."

election_header = "date,election_type,state_id,statewide,registration_info,absentee_ballot_info,results_url,polling_hours,election_day_registration,registration_deadline,absentee_request_deadline,id"

finalize.copy_paste(state_path, final_path, election_header, "election.txt")

print "-Success!"

#this is the section of the code that accomplishes #5

print "-Now making source.txt. And..."

finalize.make_source(final_path)

print "-It's done!"

#this will be the section of the code that accomplishes #6

print "-Now making election_administration.txt. And..."

finalize.make_election_admins(state_name, locality_name, locality_fips, state_path, final_path)

print "-Glory is ours!"

#this will be the section of the code that accomplishes #7

print "-Now trying to make early_vote_site.txt. And..."

if not os.access(working_path + "early_vote_site.txt", os.F_OK):
	print "-There appears to be no early_vote_site file. If this is in error, please add it and re-run."
else:
	finalize.transform_xls(working_path, final_path, early_vote_site_header, "early_vote_site")
	finalize.make_locality_ev(final_path, locality_fips)
	print "-Great justice!"

#this will be the section of the code that accomplishes #8

print "-Now making locality.txt. And..."

finalize.make_locality(locality_name, locality_fips, locality_type, final_path)

print "-Alakazam!"
