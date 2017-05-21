import psycopg2
import psycopg2.extras
import bcrypt

class invalidQueryException(Exception): pass

class database:
    def __init__(self):
        self.__HOST = "myawsdatabase.c7mfxxgrjakk.ap-southeast-1.rds.amazonaws.com"
        #self.__HOST = "localhost" **EMERGENCY_DEBUG**
        self.__DATABASE = "crazypetData"
        self.__DBUSER = "app"
        self.__DBPASS = "2rG3RSfTZ1"
        try:
            self.connection = psycopg2.connect(host=self.__HOST,database=self.__DATABASE, user=self.__DBUSER, password=self.__DBPASS)
            self.query = self.connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        except psycopg2.OperationalError:
            raise invalidQueryException("Database Connection Error!")
        
    def disconnect(self):
        self.connection.close()

    def execute(self, command):
        self.query.execute(command)
        resultset = cur.fetchall()
        return resultset

class databaseLogin(database):
    def __init__(self):
        super().__init__()

    def userLogin(self, username, password):
        password = bytes(password, encoding="ascii")
        SQL = "SELECT password, user_id, user_type FROM \"GMan\".user_login WHERE username = %s"
        DATA = (username,)
        self.query.execute(SQL,DATA)
        resultset = self.query.fetchone()
        if(resultset == None):
            raise invalidQueryException("Either Username or Password is Incorrect")
        hashed = bytes(resultset.password, encoding="ascii")
        if (bcrypt.hashpw(password, hashed) == hashed):
            return True, resultset.user_id, resultset.user_type 
        else:
            print('invalid')
            raise invalidQueryException("Either Username or Password is Incorrect")
        
    def createLogin(self,userid,username,password,email,userStatus= 0, userType = 0):
        passwd_enc = bytes(password,encoding ="ascii")
        passwd_hashed = bcrypt.hashpw(passwd_enc, bcrypt.gensalt(14))
        passwd_hashed_dec = passwd_hashed.decode(encoding = "ascii")
        SQL = "INSERT INTO \"GMan\".user_login(user_id, username, password, email, status, user_type)VALUES(%s,%s,%s,%s,%s,%s)"
        DATA = (userid, username, passwd_hashed_dec, email, str(userStatus), str(userType))
        try:
            self.query.execute(SQL, DATA)
            self.connection.commit()
        except psycopg2.IntegrityError as e:
            raise invalidQueryException("UserID or Username already exists")
        
    def editLogin(self, username, email, userStatus=0):
        SQL = "UPDATE \"GMan\".user_login SET username=%s,email=%s,status=%s WHERE username=%s"
        DATA = (username, email, str(userStatus),username)
        self.query.execute(SQL, DATA)
        self.connection.commit()

    def changePassword(self, username, oldPassword, newPassword):
        password = bytes(oldPassword, encoding="ascii")
        SQL = "SELECT password FROM \"GMan\".user_login WHERE username = %s"
        DATA = (username,)
        self.query.execute(SQL,DATA)
        resultset = self.query.fetchone()
        if(resultset == None):
            raise invalidQueryException("Either Username or Password is Incorrect")
        hashed = bytes(resultset.password, encoding="ascii")
        if (bcrypt.hashpw(password, hashed) == hashed):
            print('correct')
            passwd_enc = bytes(newPassword,encoding ="ascii")
            passwd_hashed = bcrypt.hashpw(passwd_enc, bcrypt.gensalt(14))
            passwd_hashed_dec = passwd_hashed.decode(encoding = "ascii")
            SQL = "UPDATE \"GMan\".user_login SET password=%s WHERE username = %s"
            DATA = (passwd_hashed_dec,username)
            self.query.execute(SQL, DATA)
            self.connection.commit()
        else:
            raise invalidQueryException("Either Username or Password is Incorrect")
        
    def deleteLogin(self,userid,username):
        SQL = "DELETE FROM \"GMan\".user_login WHERE user_id=%s AND username =%s";
        DATA = (userid, username)
        self.query.execute(SQL, DATA)
        self.connection.commit()

    def terminate(self):
        self.disconnect()

class databaseUser(database):
    def __init__(self):
        super().__init__()

    def getInfo(self, inp_data):
        if(inp_data[2] == 0):
            SQL = "SELECT * FROM \"GMan\".student WHERE user_id =%s"
            DATA = (inp_data[1],)
            self.query.execute(SQL, DATA)
            resultset = self.query.fetchone()
            return resultset

    def getAddress(self, inp_data):
        if (inp_data[2] == 0):
            SQL = "SELECT * FROM \"GMan\".address WHERE user_id =%s"
            DATA = (inp_data[1],)
            self.query.execute(SQL, DATA)
            resultset = self.query.fetchone()
            return resultset

    def getFaculty(self, inp_data):
        SQL = "SELECT * FROM \"GMan\".faculty WHERE \"facultyID\" =%s"
        DATA = (inp_data,)
        self.query.execute(SQL, DATA)
        resultset = self.query.fetchone()
        return resultset

    def getMajor(self, inp_data):
        SQL = "SELECT * FROM \"GMan\".majors WHERE \"majorID\" =%s"
        DATA = (inp_data,)
        self.query.execute(SQL, DATA)
        resultset = self.query.fetchone()
        return resultset

class databaseCourse(database):
    def __init__(self):
        super().__init__()

    def termCourse(self, faculty, major, year, term):
        SQL = "SELECT * FROM \"GMan\".course WHERE \"facultyID\"=%s AND \"majorID\"=%s AND \"year\"=%s AND term =%s"
        DATA = (faculty, major, year, term)
        self.query.execute(SQL, DATA)
        resultset = self.query.fetchall()
        return resultset

    def currentCourse(self, user_id):
        SQL = "SELECT course.* FROM \"GMan\".\"data\" data,\"GMan\".course  WHERE data.user_id=%s AND \
                data.grade IS NULL AND data.\"courseID\" = course.\"courseID\""
        DATA = (user_id,)
        self.query.execute(SQL, DATA)
        resultset = self.query.fetchall()
        return resultset

    def addCourse(self, information):
        try:
            SQL = "INSERT INTO \"GMan\".course (\"courseID\", \"courseName\", \"facultyID\",\
              		\"majorID\", \"professorID\", \"year\", term, \"time\", building, room, credits,\"maxStud\", pre)\
             		 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            DATA = (information["courseID"],information["courseName"],information["facultyID"],\
                    information["majorID"],information["lecturer"], information["year"],  information["term"], \
                    information["period"],information["building"], information["room"],information["credit"], \
                    information["student_limit"],information["pre"])
            self.query.execute(SQL, DATA)
            self.connection.commit()
            return 1
        except psycopg2.IntegrityError as e:
            print(e.pgcode, e.pgerror)
            return (str(e.pgcode), e.pgerror)
        except psycopg2.DataError as e:
            print(e.pgcode, e.pgerror)
            return (str(e.pgcode), e.pgerror)

    def dropCourseUser(self, user_id, courseID, year_taken):
        SQL = "DELETE FROM  \"GMan\".\"data\" WHERE user_id=%s AND \"courseID\"=%s AND year_taken=%s"
        DATA = (user_id, courseID, year_taken)
        self.query.execute(SQL, DATA)
        self.connection.commit()
        return 1

    def addCourseUser(self, user_id, year, term, courseID, year_taken):
        try:
            SQL = "INSERT INTO \"GMan\".\"data\" (user_id, \"courseID\", year_taken, \"year\", term) \
                    VALUES(%s, %s, %s, %s, %s)"
            DATA = (user_id, courseID, year_taken, year, term)
            self.query.execute(SQL, DATA)
            self.connection.commit()
            return 1
        except psycopg2.IntegrityError as e:
            print(e.pgcode, e.pgerror)
            return (str(e.pgcode), e.pgerror)

    def allUserCourse(self, user_id):
        SQL = "SELECT * FROM  \"GMan\".\"data\" WHERE user_id=%s AND GRADE IS NOT NULL"
        DATA = (user_id,)
        self.query.execute(SQL, DATA)
        resultset = self.query.fetchall()
        return resultset
