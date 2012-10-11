#!/usr/bin/python
from csv import DictReader, DictWriter
from hashlib import md5
import sys
from argparse import ArgumentParser
from countyconf import Headers, HashFields, Conversions, Prefixes, Files

LOC_COUNTY = ['AL','AR','AZ','CA','DE','GA','ID','IL','IN','LA','ND','NY','TN','TX','WV','WY']

def get_hash(row, field_list):
	m = md5()
	for field in field_list:
		m.update(row[field])
	return m.hexdigest()

def get_conversion(row, conversion):
	temp_dict = {}
	for key, val in conversion.iteritems():
		temp_dict[key] = row[val]
	return temp_dict

def process_vf(loc_data):
	precinct_data = {}
	with open(Files.VF_CUT.format(**loc_data), "r") as r, open(Files.VF_DEDUPED.format(**loc_data), "w") as w:
		reader = DictReader(r, dialect='excel-tab')
		writer = DictWriter(w, fieldnames=Headers.VF_DEDUPED)
		writer.writeheader()
		vf_hashes = set()
		p_count = 0
		for row in reader:
			if len(loc_data['county']) > 0 and not row['vf_county_name'].upper() == loc_data['county'].upper():
				continue
			vf_hash = get_hash(row, HashFields.VF)
			if vf_hash in vf_hashes:
				continue
			vf_hashes.add(vf_hash)
			vfp_hash = get_hash(row, HashFields.VFP)
			row_zip = row['vf_reg_cass_zip']
			if vfp_hash not in precinct_data:
				p_count += 1
				precinct_data[vfp_hash] = get_conversion(row, Conversions.VFP)
				precinct_data[vfp_hash]['vf_precinct_id'] = Prefixes.PRECINCT + str(p_count)
				precinct_data[vfp_hash]['zips'] = {row_zip:1}
				precinct_data[vfp_hash]['examples'] = []
			elif row_zip not in precinct_data[vfp_hash]['zips']:
				precinct_data[vfp_hash]['zips'][row_zip] = 1
			else:
				precinct_data[vfp_hash]['zips'][row_zip] += 1
			vf_output = get_conversion(row, Conversions.VF)
			if len(precinct_data[vfp_hash]['examples']) < 5:
				precinct_data[vfp_hash]['examples'].append(vf_output)
			vf_output["vf_precinct_id"] = precinct_data[vfp_hash]['vf_precinct_id'] 
			vf_output["vf_id"] = str(Prefixes.VF + row["voterbase_id"][3:])
			writer.writerow(vf_output)
	return precinct_data

def get_vf_precincts(loc_data, precinct_data):
	with open(Files.VF_PRECINCTS.format(**loc_data), "w") as vfp_w, open(Files.VF_EX_PRECINCTS.format(**loc_data), "w") as vfep_w:
		vfp_writer = DictWriter(vfp_w, fieldnames=Headers.VFP)
		vfp_writer.writeheader()
		vfep_writer = DictWriter(vfep_w, fieldnames=Headers.VFEP)
		vfep_writer.writeheader()
		for key, vfp_dict in precinct_data.iteritems():
			zips = vfp_dict.pop('zips')
			max_count = 0
			max_zip = 0
			total_count = 0
			for zip_val, zip_count in zips.iteritems():
				total_count += zip_count
				if zip_count > max_count:
					max_count = zip_count
					max_zip = zip_val
			vfp_dict['vf_precinct_zip'] = max_zip
			vfp_dict['vf_precinct_count'] = total_count
			examples = vfp_dict.pop('examples')
			vfp_writer.writerow(vfp_dict)
			ex_count = 1
			for ex in examples:
				for key in Conversions.VF_EX:
					vfp_dict[Prefixes.VFP_EX.format(ex_count)+key] = ex[key]
				ex_count += 1
			vfep_writer.writerow(vfp_dict)

def main():
	usage='Input state and optional county values'
	description='Accepts input to process cut voter files'
	parser = ArgumentParser(usage=usage,description=description)

	parser.add_argument('-s','--state',action='store',dest='state',help='State value to process',required=True)
	parser.add_argument('-c','--county',action='store',dest='county',help='Option county in state process')

	args = parser.parse_args()
	
	loc_data = {'state':args.state,'county':''}
	if loc_data['state'] not in LOC_COUNTY:
		print loc_data
		sys.exit('Localities for this state and not county based')
	if args.county:
		loc_data['county'] = args.county
	precinct_data = process_vf(loc_data)
	get_vf_precincts(loc_data, precinct_data)	
	
if __name__ == "__main__":
	main()
