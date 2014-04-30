#starting with [a whole bunch of data in the /[State]/[Locality]/Working_Data folder:
#create election.txt, source.txt, polling_location.txt, precinct.txt,
#precinct_polling_location.txt, street_segment.txt, election_administration.txt,
#locality.txt and state.txt, all in [State]/[Locality]/Final_Data, as well as early_vote_site.txt (if it exists)
#to do this, we need to:
#1. clean and translate street_segment.xls, precinct.xls, and polling_location.xls
#(This is mostly a straight transfer, with some rows being ommitted.)
#2. construct precinct_polling_location out of precinct.xls and polling_location.xls
#3. construct state.txt from <[the aether].???>
#4. Constuct an election.txt file <(possibly by copying one that already exists in /[State]).>
#5. Constuct a source.txt file. <(This should be doable without any background data.)>
#6. Obtain election_administration information from an appropriate source. <(Probably an election_administration file in /[State])>, and construct election_administration.txt.
#7. Construct early_vote_site.txt, if the files to create it exist.
#8. Construct a locality.txt file <this should be doable from <sources>>
#9. ???
#10. profit!

import os
import xlrd
import finalize
import sys

print "_________________________________"

#TODO: make locality an inputted variable
#TODO: make state folder name an inputted variable
#TODO: make the base string of state_path flexible to different configs

locality_name = "testing county"
state_folder = "california primary"

state_path = "c:/users/paul kominers/google drive/vip/hand-collected data/" + state_folder + "/"
working_path = state_path + locality_name + "/working data/"
final_path = state_path + locality_name + "/final data/"



#this section of the code checks for reasonable initial conditions

if not os.access(state_path, os.F_OK):
	print "The state folder path appears to be incorrect. Please make sure the directories are appropriately configured."
	sys.exit()
elif not os.access(working_path, os.F_OK):
	print "The working data folder path appears to be incorrect. Please make sure the directories are appropriately configured."
	sys.exit()
elif not os.access(final_path, os.F_OK):
	print "The final data folder path appears to be incorrect. Please make sure the directories are appropriately configured."
	sys.exit()

print "All the necessary directories appear to be in good working order. Mazel tov! Now, the fun part."

#this will be the section of the code that accomplishes #1
#this will be the section of the code that accomplishes #2
#this is the section of the code that accomplishes #3

print "Now creating state.txt. And..."

state_header = "name,election_administration_id,id"
state_name = state_folder.split()[0].title()

finalize.make_state(final_path, state_name, state_header)

print "Victory!"

#this is the section of the code that accomplishes #4

print "Now copying election.txt. And..."

election_header = "date,election_type,state_id,statewide,registration_info,absentee_ballot_info,results_url,polling_hours,election_day_registration,registration_deadline,absentee_request_deadline,id"

finalize.copy_paste(state_path, final_path, election_header, "election.txt")

print "Success!"

#this is the section of the code that accomplishes #5

print "Now making source.txt. And..."

finalize.make_source(final_path)

print "It's done!"

#this will be the section of the code that accomplishes #6
#this will be the section of the code that accomplishes #7
#this will be the section of the code that accomplishes #8