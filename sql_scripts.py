# This is a place to put all the sql scripts used for the API


# get the 'current' quarter: current quarter will be following
# quarter if in a break between end of exams and before start of
# classes the following quarter.
current_qtr = """
DECLARE @QTR_CODE SMALLINT;
SET @QTR_CODE = (
	SELECT
		CASE
			WHEN GETDATE() > c.gl_last_day_exams THEN ((c.gl_regis_year * 10) + c.gl_regis_qtr)
			ELSE ((c.current_yr * 10) + c.current_qtr)
		END qtr
		
	FROM sec.sdbdb01 c
);
SELECT @QTR_CODE qtr_code
"""


# STUDENT QUERIES
info_from_sid = """
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
		(
			SELECT STRING_AGG(cm.major_abbr, ', ') AS Result
			FROM sec.student_1_college_major cm
			WHERE s1.system_key = cm.system_key
		),
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
"""


student_from_uw_email = """
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
"""


student_from_alt_email = """
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
"""


student_current_schedule_query = """
DECLARE @YEAR SMALLINT;
DECLARE @QTR TINYINT;

SET @YEAR = (
	SELECT
		CASE
			WHEN GETDATE() > gl_last_day_exams THEN gl_regis_year
			ELSE current_yr
		END
	FROM sec.sdbdb01
);
SET @QTR = (
	SELECT
		CASE
			WHEN GETDATE() > gl_last_day_exams THEN gl_regis_qtr
			ELSE current_qtr
		END
	FROM sec.sdbdb01
);

SELECT 
	rc.regis_yr,
	rc.regis_qtr,
	rc.sln,
	rc.crs_curric_abbr,
	rc.crs_number,
	rc.crs_section_id,
	rc.credits,
	CASE
		WHEN rc.crs_number IN (490, 499, 599, 600, 700, 800) THEN (
			SELECT fac_name 
			FROM sec.sr_course_instr 
			WHERE fac_yr = @YEAR
			AND fac_qtr = @QTR
			AND fac_curric_abbr = rc.crs_curric_abbr 
			AND fac_course_no = rc.crs_number 
			AND fac_sect_id = rc.crs_section_id
			AND fac_seq_no = rc.fac_seq_no
		)
		ELSE (
			SELECT TOP 1 fac_name 
			FROM sec.sr_course_instr 
			WHERE fac_yr = @YEAR
			AND fac_qtr = @QTR
			AND fac_curric_abbr = rc.crs_curric_abbr 
			AND fac_course_no = rc.crs_number 
			AND fac_sect_id = rc.crs_section_id
			AND fac_pct_involve > 45
		)
	END	instructor

FROM sec.registration_courses rc
INNER JOIN sec.student_1 s1
ON rc.system_key = s1.system_key

WHERE rc.regis_yr = @YEAR
AND rc.regis_qtr = @QTR
AND rc.request_status IN ('A', 'C', 'R')
AND LEN(rc.crs_section_id) = 1
AND s1.student_no = ?  

ORDER BY rc.crs_curric_abbr, rc.crs_number

"""


student_transcript_query = """
SELECT DISTINCT
	CONCAT(t.tran_yr, '-', t.tran_qtr) yr_qtr,
	CONCAT(ct.dept_abbrev, ' ', ct.course_number, ct.section_id) course,
	ct.course_credits,
	ct.grade

FROM sec.transcript t
INNER JOIN sec.transcript_courses_taken ct
ON (t.tran_yr = ct.tran_yr AND  t.tran_qtr = ct.tran_qtr)
INNER JOIN sec.student_1 s1
ON ct.system_key = s1.system_key

WHERE s1.student_no = ?
AND LEN(ct.section_id) = 1

ORDER BY yr_qtr, course

"""


current_ee_undergrads_query = """
	SELECT DISTINCT
		s1.student_no,
		s1.student_name_lowc,
		s1.student_name_pn_f,
		a.e_mail_ucs uw_email,
		s1.spp_qtrs_used,
		CASE cm.pathway
			WHEN 0 THEN CONCAT('00','-',cm.major_abbr, '-',cm.deg_level,cm.deg_type)
			ELSE CONCAT(cm.pathway,'-',cm.deg_level,cm.deg_type)
		END degree,
		CASE s1.tot_graded_attmp
			WHEN 0 THEN 0.0
			ELSE CONVERT(DECIMAL(4,2), (s1.tot_grade_points/s1.tot_graded_attmp))
		END cum_gpa

	FROM sec.student_1 s1
	INNER JOIN sec.student_1_college_major cm
	ON s1.system_key = cm.system_key
	INNER JOIN sec.registration_courses rc
	ON s1.system_key = rc.system_key
	INNER JOIN sec.addresses a
	ON s1.system_key = a.system_key

	WHERE cm.deg_level = 1 
	AND rc.regis_yr = (
		SELECT TOP 1 sdb1.current_yr
		FROM sec.sdbdb01 sdb1
	)
	AND rc.regis_qtr = (
		SELECT TOP 1 sdb1.current_qtr
		FROM sec.sdbdb01 sdb1
	)
	AND cm.major_abbr IN ('E E', 'ECENG')
	AND rc.request_status IN ('A' ,'C', 'R')
	AND cm.branch = 0

	ORDER BY s1.student_name_lowc
	;
"""


# COURSE QUERIES
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
		(ts.maj_enroll_10 + ts.non_maj_enr_10),
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


# FACULTY QUERIES
fac_crs_history_query = """
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
	AND ts.course_no NOT IN (490,499,599,600,700,800)

	ORDER BY ts.ts_year, ts.ts_quarter, ts.dept_abbrev, ts.course_no
	;
"""

faculty_code_query = """
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
"""


faculty_list_query = """
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

	WHERE ci.fac_yr > (?) - 2
	AND ci.fac_pct_involve > 49
	AND ci.fac_curric_abbr IN ('E E', 'EE P')
	AND RTRIM(ci.fac_name) <> ''
	ORDER BY inst_name
	;
"""


# COURSE QUERIES
joint_courses_query = """
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
"""

single_course_joins_info = """
	SELECT DISTINCT
        CONCAT(jc.joint_dept_abbrev, jc.joint_course_num) joined_course

	FROM sec.sr_course_titles_joint_course jc
	INNER JOIN sec.sr_course_titles ct
	ON (
			(jc.department_abbrev = ct.department_abbrev) 
			AND (jc.course_number = ct.course_number)
	)

	WHERE jc.department_abbrev = (?)
	AND jc.course_number = (?)
	AND ct.last_eff_yr = 9999

	ORDER BY joined_course
	;
"""

single_course_info = """
	SELECT 
		ct.department_abbrev,
		ct.course_number,
		ct.min_qtr_credits,
		ct.max_credits,
		CASE ct.credit_control
			WHEN 0 THEN 'Zero Cr'
			WHEN 1 THEN 'Fixed Cr'
			WHEN 2 THEN 'Var. Cr.'
			ELSE 'Open Cr.'
		END credit_control,
		CASE ct.grading_system
			WHEN 0 THEN 'Std. or CR/NC'
			WHEN 5 THEN 'CR/NC'
		END grading_system,
		ct.course_title short_title,
		ct.long_course_title long_title,
		CASE ct.resp_course_no
			WHEN 0 THEN 'NA'
			ELSE CONCAT(ct.resp_curric_abbr, resp_course_no)
		END resp_course,
		ct.diversity_crs,
		ct.natural_science,
		ct.social_science,
		ct.arts_hum,
		ct.rsn,
		ct.english_comp,
		ct.writing_crs

	FROM sec.sr_course_titles ct

	WHERE ct.last_eff_yr = 9999
	AND ct.department_abbrev = (?)
	AND ct.course_number = (?)
	AND ct.course_branch = 0
	;
"""

course_prereqs_query = """
SELECT 
    cp.pr_curric_abbr,
	cp.pr_course_no,
    CASE cp.pr_and_or
		WHEN 'O' THEN 'Option'
		ELSE ''
	END pr_and_r,
    CASE cp.pr_concurrency
		WHEN 'N' THEN ''
		ELSE 'Concurrent Allowed'
	END pr_concurrency

FROM sec.sr_course_prereq cp

WHERE cp.department_abbrev  = ?
AND cp.course_number = ?
AND cp.last_eff_yr = 9999
;
"""


course_is_prereq_for_query = """
SELECT 
	cp.department_abbrev.
	cp.course_number,
	cp.pr_and_or,
	cp.pr_concurrency

FROM sec.sr_course_prereq cp

WHERE (cp.pr_curric_abbr = ? and cp.pr_course_no = ?)
AND cp.last_eff_yr = 9999
AND cp.course_branch = 0;
"""


current_time_schedule_link = """
DECLARE @TODAY DATETIME;
SET @TODAY = CONVERT(DATE, GETDATE())

IF (?) > (SELECT CONVERT(DATE, gl_last_day_class) FROM sec.sdbdb01)
	SELECT 
		CONCAT(
			'https://www.washington.edu/students/timeschd/',
			CASE sdb01.gl_regis_qtr
				WHEN 1 THEN 'WIN'
				WHEN 2 THEN 'SPR'
				WHEN 3 THEN 'SUM'
				WHEN 4 THEN 'AUT'
			END,
			sdb01.current_yr,
			'/ee.html'
			) ts_link

	FROM sec.sdbdb01 sdb01
ELSE
	SELECT 
		CONCAT(
			'https://www.washington.edu/students/timeschd/',
			CASE sdb01.current_qtr
				WHEN 1 THEN 'WIN'
				WHEN 2 THEN 'SPR'
				WHEN 3 THEN 'SUM'
				WHEN 4 THEN 'AUT'
			END,
			sdb01.current_yr,
			'/ee.html'
			) ts_link

	FROM sec.sdbdb01 sdb01
"""


# ROOM QUERIES
get_room_attributes = """
SELECT 
	rm.sr_room_bldg,
	rm.sr_room_room_no,
	rm.sr_room_capacity,
	attr.room_char_desc,
	CASE attr.room_char_s25
		WHEN 1 THEN 'True'
		ELSE 'False'
	END has_attr


FROM sec.sr_room_master rm
INNER JOIN sec.sr_room_master_attribute rma
ON (rm.sr_room_bldg = rma.sr_room_bldg AND rm.sr_room_room_no = rma.sr_room_room_no)
INNER JOIN sec.sys_tbl_90_room_attribute attr
ON rma.sr_room_char_no = attr.table_key

WHERE 
	rm.sr_room_campus = 0
	AND rm.sr_room_bldg = ?
	AND rm.sr_room_room_no = ?
"""

get_rooms = """
SELECT DISTINCT
	RTRIM(mt.building) bldg,
	RTRIM(mt.room_number) room_no
	
FROM sec.time_sched_meeting_times mt

WHERE 
	mt.course_branch = 0
	AND mt.ts_year = ? 
	AND mt.ts_quarter = ?

ORDER BY bldg, room_no
"""

get_room_schedule = """
SELECT DISTINCT
	RTRIM(mt.building) bldg,
	RTRIM(mt.room_number) room_no,
	mt.days_of_week,
	mt.start_time,
	mt.end_time,
	ts.room_cap
	
FROM sec.time_sched_meeting_times mt
INNER JOIN sec.time_schedule ts
ON (
		(mt.dept_abbrev = ts.dept_abbrev ) AND
		(mt.course_no = ts.course_no) AND
		(mt.section_id = ts.section_id)
)

WHERE 
	mt.course_branch = 0
	AND mt.ts_year = ? 
	AND mt.ts_quarter = ?
"""


sql_room_search = """
SET NOCOUNT ON;

DECLARE @YEAR SMALLINT;
DECLARE @QTR TINYINT;
DECLARE @START SMALLINT;
DECLARE @END SMALLINT;
DECLARE @DAYS VARCHAR(8);
DECLARE @MIN_CAP SMALLINT;
DECLARE @MAX_CAP SMALLINT;

SET @MIN_CAP = ?;
SET @MAX_CAP = ?;
SET @YEAR = ?;
SET @QTR = ?;
SET @DAYS = ?
SET  @START = ?;
SET @END = ?;

PRINT 'Start Time: ' + CONVERT(VARCHAR, @START);
PRINT 'End Time: ' + CONVERT(VARCHAR, @END);


WITH cte_sched AS (
	SELECT 
		mt.ts_year,
		mt.ts_quarter,
		mt.building,
		mt.room_number,
		mt.days_of_week,
		mt.pm_indicator,
		CASE 
			WHEN TRY_CONVERT(SMALLINT, mt.start_time) < 800 THEN TRY_CONVERT(SMALLINT, mt.start_time) + 1200
			ELSE TRY_CONVERT(SMALLINT, mt.start_time)
		END start_t,
		CASE 
			WHEN TRY_CONVERT(SMALLINT, mt.end_time) < 800 THEN TRY_CONVERT(SMALLINT, mt.end_time) + 1200
			ELSE TRY_CONVERT(SMALLINT, mt.end_time)
		END end_t

	FROM sec.time_sched_meeting_times mt

	WHERE 
		mt.ts_year = @YEAR AND
		mt.ts_quarter = @QTR AND
		mt.course_branch = 0

		AND TRY_CONVERT(SMALLINT, mt.start_time) IS NOT NULL
		AND mt.pm_indicator <> 'P'
)

SELECT DISTINCT
	RTRIM(rs.building) bldg, 
	TRIM(rs.room_number) room_no,
	m.sr_room_capacity capacity

FROM cte_sched rs 
INNER JOIN sec.sr_room_master m
ON 
	(
		rs.building = m.sr_room_bldg AND
		TRIM(rs.room_number) = TRIM(m.sr_room_room_no)
	)

WHERE 
	m.sr_room_gen_assgn = 1
	AND m.sr_room_campus = 0
	AND (m.sr_room_capacity BETWEEN @MIN_CAP AND @MAX_CAP)
	AND CONCAT(RTRIM(rs.building), ' ', TRIM(rs.room_number)) NOT IN (


	SELECT
		CONCAT(RTRIM(s.building), ' ', TRIM(s.room_number))


	FROM cte_sched s
	INNER JOIN sec.sr_room_master rm
	ON ((s.building = rm.sr_room_bldg) AND (TRIM(s.room_number) = TRIM(rm.sr_room_room_no)))

	WHERE 
		s.days_of_week LIKE '%['+@DAYS+']%' AND
		(
			(@START BETWEEN s.start_t AND s.end_t) OR 
			(@END BETWEEN s.start_t AND s.end_t)
		) AND
	rm.sr_room_gen_assgn = 1
	AND rm.sr_room_campus = 0

)
ORDER BY bldg, room_no
;
"""


query_find_new_room = """
SET NOCOUNT ON;

DECLARE @SLN INT;
DECLARE @YEAR SMALLINT;
DECLARE @QTR TINYINT;
DECLARE @START SMALLINT;
DECLARE @END SMALLINT;
DECLARE @DAYS VARCHAR(8);
DECLARE @MIN_CAP SMALLINT;
DECLARE @MAX_CAP SMALLINT;

SET @YEAR = ?;
SET @QTR = ?;
SET @SLN = ?	;
SET @MIN_CAP = ?;
SET @MAX_CAP = ?;
SET  @START = (
	SELECT  
		CASE 
		WHEN TRY_CONVERT(SMALLINT, ts.starting_time) < 800 THEN TRY_CONVERT(SMALLINT, ts.starting_time) + 1200
			ELSE TRY_CONVERT(SMALLINT, ts.starting_time)
		END start_t
	FROM sec.time_schedule ts

	WHERE 
		ts.ts_year = @YEAR AND
		ts.ts_quarter = @QTR AND
		ts.sln = @SLN AND
		ts.course_branch = 0 AND TRY_CONVERT(SMALLINT, ts.starting_time) IS NOT NULL
);

SET @END = (
	SELECT 
		CASE 
			WHEN TRY_CONVERT(SMALLINT,ts.ending_time) < 800 THEN TRY_CONVERT(SMALLINT, ts.ending_time) + 1200
			ELSE TRY_CONVERT(SMALLINT, ts.ending_time)
		END end_t

	FROM sec.time_schedule ts

	WHERE 
		ts.ts_year = @YEAR AND
		ts.ts_quarter = @QTR AND
		ts.sln = @SLN AND
		ts.course_branch = 0 AND TRY_CONVERT(SMALLINT, ts.starting_time) IS NOT NULL
);

SET @DAYS = (
	SELECT 
		ts.day_of_week

	FROM sec.time_schedule ts

	WHERE 
		ts.ts_year = @YEAR AND
		ts.ts_quarter = @QTR AND
		ts.sln = @SLN AND
		ts.course_branch = 0 AND TRY_CONVERT(SMALLINT, ts.starting_time) IS NOT NULL
);

WITH cte_sched AS (
	SELECT 
		mt.ts_year,
		mt.ts_quarter,
		mt.building,
		mt.room_number,
		mt.days_of_week,
		mt.pm_indicator,
		CASE 
			WHEN TRY_CONVERT(SMALLINT, mt.start_time) < 800 THEN TRY_CONVERT(SMALLINT, mt.start_time) + 1200
			ELSE TRY_CONVERT(SMALLINT, mt.start_time)
		END start_t,
		CASE 
			WHEN TRY_CONVERT(SMALLINT, mt.end_time) < 800 THEN TRY_CONVERT(SMALLINT, mt.end_time) + 1200
			ELSE TRY_CONVERT(SMALLINT, mt.end_time)
		END end_t

	FROM sec.time_sched_meeting_times mt

	WHERE 
		mt.ts_year = @YEAR AND
		mt.ts_quarter = @QTR AND
		mt.course_branch = 0

		AND TRY_CONVERT(SMALLINT, mt.start_time) IS NOT NULL
		AND mt.pm_indicator <> 'P'
)

SELECT DISTINCT
	RTRIM(rs.building) bldg, 
	TRIM(rs.room_number) room_no,
	m.sr_room_capacity capacity

FROM cte_sched rs 
INNER JOIN sec.sr_room_master m
ON 
	(
		rs.building = m.sr_room_bldg AND
		TRIM(rs.room_number) = TRIM(m.sr_room_room_no)
	)

WHERE 
	m.sr_room_gen_assgn = 1
	AND m.sr_room_campus = 0
	AND (m.sr_room_capacity BETWEEN @MIN_CAP AND @MAX_CAP)
	AND CONCAT(RTRIM(rs.building), ' ', TRIM(rs.room_number)) NOT IN (


	SELECT
		CONCAT(RTRIM(s.building), ' ', TRIM(s.room_number))

	FROM cte_sched s
	INNER JOIN sec.sr_room_master rm
	ON ((s.building = rm.sr_room_bldg) AND (TRIM(s.room_number) = TRIM(rm.sr_room_room_no)))

	WHERE 
		s.days_of_week LIKE '%['+@DAYS+']%' AND
		(
			(@START BETWEEN s.start_t AND s.end_t) OR 
			(@END BETWEEN s.start_t AND s.end_t)
		) AND
	rm.sr_room_gen_assgn = 1
	AND rm.sr_room_campus = 0

)
ORDER BY bldg, room_no
;
"""
