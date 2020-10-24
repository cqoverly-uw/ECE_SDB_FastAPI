# ECE_SDB_FastAPI
 
ECE_SDB_FastAPI is, as the name suggests, a set of scripts, mainly for program coordinators working with advising or the time schedule, that interfaces with the UW's EDW, mainly using the UWSDBDataStore database. 

### **List of current working elements**:

**Find basic student information** based on student number, student's UW email, or student's stored alternate email. (Note, the alternate email is ofteninvalid as it was entered at the student applied to the university.)

**Faculty List** lists faculty who have taught a class in ECE in the past 2 years.

**Find faculty code by faculty name, year and quarter** allows user to enter the last name and first initial of a faculty, the year and the quarter to find that quarter's faculty code needed by students to register for research credit. 

**Faculty course history** to find all courses taught by an instructor witihin a user-defined span of years.

**Course history** search to view how a course has been listed in the time schedule witihin a user-defined span of years.

The connection script works best with the use of a defined DSN on Windows. For Posix-based systems, the use of the FreeBSD driver is used, and will need to be installed by the user. 
 
 
