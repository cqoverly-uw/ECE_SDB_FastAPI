# This is a place to put all the sql scripts used for the API


info_from_sid = '''
SELECT 
	s1.student_no,
	s1.student_name_lowc,
	s1.student_name_pn_f,
	s1.spp_qtrs_used,
	a.e_mail_ucs,
	a.e_mail_other,
	CASE cm.branch
		WHEN 0 THEN 'Seattle'
		WHEN 1 THEN 'Bothell'
		WHEN 2 THEN 'Tacoma'
		ELSE 'X'
	END campus,
	cm.major_abbr,
	cm.pathway,
	cm.deg_level,
	cm.deg_type,
	CASE 
		WHEN di.deg_status BETWEEN 3 AND 5 THEN 'APPLIED'
		WHEN di.deg_status = 1 THEN 'WITHDRAWN'
		WHEN di.deg_status = 9 THEN 'GRANTED'
		ELSE 'None'
	END deg_status,
	di.deg_earned_yr,
	CASE di.deg_earned_qtr
		WHEN 1 THEN 'Win'
		WHEN 2 THEN 'Spr'
		WHEN 3 THEN 'Sum'
		WHEN 4 THEN 'Aut'
	END deg_earned_qtr

FROM sec.student_1 s1
INNER JOIN sec.addresses a
ON s1.system_key = a.system_key
INNER JOIN sec.student_1_college_major cm
ON s1.system_key = cm.system_key
LEFT JOIN sec.student_2_uw_degree_info di
ON s1.system_key = di.system_key

WHERE s1.student_no = (?)

;
'''

