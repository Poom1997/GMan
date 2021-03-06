import plugin.image as imageHandle

##Class to create a user as an object##

##Main User##
class user:
    def __init__(self, data, username, address):
        self.id = data.user_id
        self.firstname = data.name
        self.surname = data.surname
        self.email = data.email
        self.address = address
        self.username = username

    def getID(self):
        return self.id

    def getName(self):
        return self.firstname

    def getSurname(self):
        return self.surname

    def getEmail(self):
        return self.email

    def getAddress(self):
        temp = self.address.houseNumber + " " + self.address.street + "\n" + self.address.subDistrict\
               + " " + self.address.district + "\n" + self.address.province + " " + self.address.zipCode
        return temp

    def getAddressRecord(self):
        return self.address

    def pictureGen(self):
        self.image = imageHandle.imageHandler(self.id)
        self.image.createImageFile()
        return self.image.getPath()

    def pictureDataProtect(self):
        self.image.deleteData()

    def getUsername(self):
        return self.username

##Type of Student, Inherited from main user##
class student(user):
    def __init__(self, data, username, address, faculty, major):
        super().__init__(data,username, address)
        self.status = data.status
        self.faculty = faculty
        self.major = major
        self.year = data.year
        self.gpa = data.gpa
        self.term = data.term

    def getFacultyName(self):
        temp = self.faculty.facultyName
        return temp

    def getMajorName(self):
        temp = self.major.degree
        return temp

    def getFacultyID(self):
        temp = self.faculty.facultyID
        return temp

    def getMajorID(self):
        temp = self.major.majorID
        return temp

    def getTerm(self):
        return self.term

    def getYear(self):
        return self.year

    def getGpa(self):
        return self.gpa

    def getStatus(self):
        return self.status

    def type(self):
        return "STUDENT"

    def getStatusString(self):
        if (self.status == 0):
            return  "Learning"
        elif (self.status == 1):
            return  "Probation"
        elif (self.status == 2):
            return  "Retired"
        elif (self.status == 3):
            return  "Withdrawn"
        elif (self.status == 4):
            return  "Suspended"
        elif (self.status == 5):
            return "Graduated/Alumni"
        else:
            return "Unknown"


##Type of Professor, Inherited from main user##
class professor(user):
    def __init__(self, data, username, address, faculty):
        super().__init__(data,username, address)
        self.status = data.status
        self.faculty = faculty

    def getFacultyName(self):
        temp = self.faculty.facultyName
        return temp

    def getMajorName(self):
        return "N/A"

    def getMajorID(self):
        temp = "N/A"
        return temp

    def getFacultyID(self):
        temp = self.faculty.facultyID
        return temp

    def getStatus(self):
        return self.status

    def getYear(self):
        return "N/A"

    def type(self):
        return "PROFESSOR"

##Type of Administrator, Inherited from main user##
class admin(user):
    def __init__(self, data, username, address):
        super().__init__(data, username, address)
        self.status = data.status

    def getStatus(self):
        return self.status

    def getYear(self):
        return "N/A"

    def getFacultyName(self):
        temp = "N/A"
        return temp

    def getMajorName(self):
        temp = "N/A"
        return temp

    def getFacultyID(self):
        temp = "N/A"
        return temp

    def getMajorID(self):
        temp = "N/A"
        return temp

    def type(self):
        return "ADMIN"