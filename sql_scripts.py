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

course_history = """
SELECT DISTINCT
	ts.ts_year,
	ts.ts_quarter,
	ts.dept_abbrev,
	ts.course_no,
	--ts.section_id,
	ts.section_type_code,
	mt.section_id,
	mt.index1 AS 'meeting_no',
	--ts.day_of_week,
	mt.days_of_week,
	mt.building,
	mt.room_number,
	--ts.starting_time,
	mt.start_time,
	--ts.ending_time,
	mt.end_time,
	ts.current_enroll,
	ts.l_e_enroll,
	ts.students_denied,
	ts.students_added,
	ts.students_dropped,
	ci.fac_name,
	ts.course_title,
	ts.srs_comment

FROM sec.time_schedule ts
LEFT JOIN sec.sr_course_instr ci
ON (
	ci.fac_curric_abbr = ts.dept_abbrev
	AND ci.fac_course_no = ts.course_no
	AND ci.fac_yr = ts.ts_year
	AND ci.fac_qtr = ts.ts_quarter
	AND ci.fac_curric_abbr = ts.dept_abbrev
	AND ci.fac_sect_id = ts.section_id
)
LEFT JOIN sec.time_sched_meeting_times mt
ON (
	mt.dept_abbrev = ts.dept_abbrev
	AND mt.course_no = ts.course_no
	AND mt.ts_year = ts.ts_year
	AND mt.ts_quarter = ts.ts_quarter
	AND mt.section_id = ts.section_id
)
		
WHERE ts.ts_year BETWEEN (?) AND (?)
AND ts.dept_abbrev = (?)
AND ts.course_no = (?)
AND ci.fac_pct_involve > 49

ORDER BY ts.ts_year, ts.ts_quarter, mt.section_id
;
"""


student_from_uw_email = '''
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

WHERE a.e_mail_ucs = (?)
;
'''


student_from_alt_email = '''
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

WHERE a.e_mail_other = (?)
;
'''

fac_crs_history_query = '''
SELECT DISTINCT
	ts.ts_year yr,
	ts.ts_quarter qtr,
	ts.dept_abbrev dept,
	ts.course_no,
	ts.section_type_code sect_type,
	mt.section_id sect,
	mt.index1 AS 'meeting_no',
	mt.days_of_week days,
	mt.building bldg,
	mt.room_number room_no,
	mt.start_time start_t,
	mt.end_time end_t,
	ts.current_enroll curr_enr,
	ts.l_e_enroll limit,
	ts.students_denied denied,
	ts.students_added added,
	ts.students_dropped dropped,
	ci.fac_name,
	ts.course_title title,
	ts.srs_comment

FROM sec.time_schedule ts
LEFT JOIN sec.sr_course_instr ci
ON (
	ci.fac_curric_abbr = ts.dept_abbrev
	AND ci.fac_course_no = ts.course_no
	AND ci.fac_yr = ts.ts_year
	AND ci.fac_qtr = ts.ts_quarter
	AND ci.fac_curric_abbr = ts.dept_abbrev
	AND ci.fac_sect_id = ts.section_id
)
LEFT JOIN sec.time_sched_meeting_times mt
ON (
	mt.dept_abbrev = ts.dept_abbrev
	AND mt.course_no = ts.course_no
	AND mt.ts_year = ts.ts_year
	AND mt.ts_quarter = ts.ts_quarter
	AND mt.section_id = ts.section_id
)
		
WHERE ts.ts_year BETWEEN (?) AND (?)
AND ci.fac_name LIKE (?)
AND LEN(mt.section_id) = 1

ORDER BY ts.ts_year, ts.ts_quarter, ts.dept_abbrev, ts.course_no
;
'''

faculty_code_query = '''
SELECT DISTINCT
	ci.fac_ssn,
	ci.fac_name,
	ci.fac_yr,
	ci.fac_qtr,
	ci.fac_seq_no


FROM sec.sr_course_instr ci
INNER JOIN sec.sr_instructor i
ON ci.fac_ssn = i.instr_ssn


WHERE ci.fac_name LIKE (?)
AND ci.fac_yr = (?)
AND ci.fac_qtr = (?)
AND ci.fac_curric_abbr = 'E E'
AND ci.fac_seq_no > 9999
;
'''


faculty_list_query = '''
DECLARE @CURRENT_YEAR SMALLINT;
SET @CURRENT_YEAR = (
	SELECT sdb1.current_yr
	FROM sec.sdbdb01 sdb1
)

SELECT DISTINCT 
	ci.fac_ssn,
	(
		SELECT TOP 1 inst.instr_name
		FROM sec.sr_instructor inst
		WHERE inst.instr_ssn = ci.fac_ssn
		AND RTRIM(instr_name) <> ''
		ORDER BY inst.instr_updt_dt DESC
) inst_name,
	
	(
		SELECT TOP 1 inst.instr_netid
		FROM sec.sr_instructor inst
		WHERE inst.instr_ssn = ci.fac_ssn
		AND RTRIM(inst.instr_netid) <> ''
		ORDER BY inst.instr_updt_dt DESC
) netid


FROM sec.sr_course_instr ci
INNER JOIN sec.sr_instructor i
ON ci.fac_ssn = i.instr_ssn

WHERE ci.fac_yr > @CURRENT_YEAR - 2
AND ci.fac_pct_involve > 49
AND ci.fac_curric_abbr IN ('E E', 'EE P')
AND RTRIM(ci.fac_name) <> ''
ORDER BY inst_name

;

'''


joint_courses_query = '''
SELECT DISTINCT
	jc.department_abbrev,
	jc.course_number,
	jc.joint_dept_abbrev,
	jc.joint_course_num,
	ct.resp_curric_abbr

FROM sec.sr_course_titles_joint_course jc
INNER JOIN sec.sr_course_titles ct
ON (
		(jc.department_abbrev = ct.department_abbrev) 
		AND (jc.course_number = ct.course_number)
        AND (jc.last_eff_yr = ct.last_eff_yr)
)

WHERE jc.department_abbrev = 'E E'
AND jc.last_eff_yr = 9999

ORDER BY jc.course_number, jc.joint_dept_abbrev
;
'''