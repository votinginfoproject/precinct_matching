class Headers(object):
	VF_DEDUPED = ['vf_id','house_number','zip','state','street_direction',
			'street_name','street_suffix','address_direction',
			'apartment_number','county','city','vf_precinct_id']
	VFP = ['vf_precinct_id','vf_precinct_county','vf_precinct_city',
		'vf_precinct_zip','vf_precinct_ward','vf_precinct_name',
		'vf_precinct_code','vf_precinct_count']
	VFEP = ['vf_precinct_id','vf_precinct_county','vf_precinct_city',
		'vf_precinct_zip','vf_precinct_ward','vf_precinct_name',
		'vf_precinct_code','vf_precinct_count',
		'address_1_city','address_1_zip','address_1_house_number',
		'address_1_street_direction','address_1_street_name',
		'address_1_street_suffix','address_1_address_direction',
		'address_2_city','address_2_zip','address_2_house_number',
		'address_2_street_direction','address_2_street_name',
		'address_2_street_suffix','address_2_address_direction',
		'address_3_city','address_3_zip','address_3_house_number',
		'address_3_street_direction','address_3_street_name',
		'address_3_street_suffix','address_3_address_direction',
		'address_4_city','address_4_zip','address_4_house_number',
		'address_4_street_direction','address_4_street_name',
		'address_4_street_suffix','address_4_address_direction',
		'address_5_city','address_5_zip','address_5_house_number',
		'address_5_street_direction','address_5_street_name',
		'address_5_street_suffix','address_5_address_direction']

class HashFields(object):
	VF = ['vf_county_name','vf_reg_cass_city','vf_ward',
		'vf_precinct_name','vf_precinct_id',
		'vf_reg_cass_street_num','vf_reg_cass_zip',
		'vf_reg_cass_state','vf_reg_cass_pre_directional',
		'vf_reg_cass_street_name','vf_reg_cass_street_suffix',
		'vf_reg_cass_post_directional','vf_reg_cass_apt_num']
	VFP = ['vf_county_name','vf_reg_cass_city','vf_ward',
		'vf_precinct_name','vf_precinct_id']

class Conversions(object):
	VF = {'house_number':'vf_reg_cass_street_num',
		'zip':'vf_reg_cass_zip',
		'state':'vf_reg_cass_state',
		'street_direction':'vf_reg_cass_pre_directional',
		'street_name':'vf_reg_cass_street_name',
		'street_suffix':'vf_reg_cass_street_suffix',
		'address_direction':'vf_reg_cass_post_directional',
		'apartment_number':'vf_reg_cass_apt_num',
		'county':'vf_county_name',
		'city':'vf_reg_cass_city'}
	VFP = {'vf_precinct_county':'vf_county_name',
		'vf_precinct_city':'vf_reg_cass_city',
		'vf_precinct_ward':'vf_ward',
		'vf_precinct_name':'vf_precinct_name',
		'vf_precinct_code':'vf_precinct_id'}
	VF_EX = ['city','zip','house_number','street_direction',
			'street_name','street_suffix','address_direction']

class Prefixes(object):
	VF = '88'
	PRECINCT = '22'
	VFP_EX = 'address_{0}_'

class Files(object):
	VF_CUT = '{state}_VF.cut'
	VF_DEDUPED = 'vf_deduped/{state}{county}_vf_deduped.txt'
	VF_PRECINCTS = 'vf_precincts/{state}{county}_vf_precincts.txt'
	VF_EX_PRECINCTS = 'vf_ex_precincts/{state}{county}_vf_ex_precincts.txt'
	
