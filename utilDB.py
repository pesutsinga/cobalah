import pymysql
from Crypto.Cipher import AES


class ChopeDB:
    table = None

    def __init__(self, database='u7728567_chopebot'):
        self.connection = pymysql.connect(
            host='bebong.id',
            user='u7728567_chope',
            password='bunuakumz578%&*',
            db=database,
            charset='utf8mb4')

    def set_table(self, tableName):
        self.table = tableName

    def close(self):
        self.connection.close()

    def insert(self, table, data=[]):
        """
        table: string, name of table to insert data into
        data: list of tuples (colname, type, value)
            e.g. ('favCartoonCharacter', "%s", 'Donald Duck')
            "%s" denotes string
            "%d" denotes decimal (number)
            "%f" denotes float
            et cetera.
        """
        # Create strings to concatenate with with SQL statement
        colName = ', '.join([('`' + elm[0] + '`') for elm in data])
        colType = ', '.join([elm[1] for elm in data])

        # Create SQL INSERT query
        statement = (
            "INSERT INTO " + table
            + " (" + colName + ") "
            + "VALUES (" + colType + ")")

        # Create a tuple of the arguments necessary for query
        args = tuple([elm[2] for elm in data])

        try:
            # Execute SQL query with separate argument to prevent SQL injection attacks
            with self.connection.cursor() as cursor:
                cursor.execute(statement, args)
            self.connection.commit()
        finally:
            pass

    def delete(self, table, condition, values):

        """
            table : string of table name
            condition:
            'column = %d OR (other column = %s AND another column = %f)'
            values : values to replace '%d', '%s', etc.
        """

        statement = (
            "DELETE FROM " + table
            + " WHERE " + condition)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(statement, values)
            self.connection.commit()
        finally:
            pass

    def update(self, table, data=[]):
        """
        Update certain columns from data
        data: list of tuples(updateCol, data type1, value1,
                             requireCol, data type2, value2)
        updateCol: Column to be updated
        data type1: data type of updateCol
        value1: new value to update updateCol
        requireCol: Column whose contents will be checked as a
                    requirement for the update
        data type2: data type of requireCol
        value2: value to search in requireCol
        """

        for elm in data:
            statement = (
                "UPDATE " + table
                + " SET " + elm[0]
                + " = " + elm[1]
                + " WHERE " + elm[3]
                + " = " + elm[4])
            args = [elm[2]] + [elm[5]]

            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(statement, args)
                self.connection.commit()
            finally:
                pass

    def select(self, table, targetVariables, data=[]):
        """
        table: string
        data: list of tuples (colName, data type, colValue, colSelect)
        colName: Name of column to be checked
        data type: data type of values within colName
        colValue: Value to find within column colName
        colSelect: list of columns to be selected
        targetVariables: A list to store all the selected data
        (a value returned to the main program)

        """

        # Initialization for various counter/loop control variables
        deletChar = "[]\'"
        Count = len(data)
        targetVariables = []

        # Loop to create multiple queries based on the number of tuples in data
        for i in range(Count):
            elm = data[i]
            FieldNameStr = str(elm[3])

            # Replace characters from FieldNameStr before concatenation so it follows SQL syntax
            for char in deletChar:
                FieldNameStr = FieldNameStr.replace(char, " ")

            # Prepare SQL SELECT query
            statement = (
                "SELECT " + FieldNameStr
                + " FROM " + table
                + " WHERE " + elm[0]
                + " = " + elm[1] + "")
            args = elm[2]

            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(statement, args)
                results = cursor.fetchall()

                # Store selected information into targetVariables
                for row in results:
                    for j in range(len(row)):
                        targetVariables.append((row[j]))

            finally:
                pass
        return targetVariables

    def select_dict(self, tgUsername):
        """
        A select function specific for selecting user's LWN facility priority
        Produces a dictionary instead of a list
        A new connection has been created here in order to exclusively
        use the Dictionary Cursor here
        """

        self.connection = pymysql.connect(
            host='bebong.id',
            user='u7728567_chope',
            password='bunuakumz578%&*',
            db='u7728567_chopebot',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

        sql = ("SELECT COLLAB_BOOTHS, CIRCULAR_PODS, \
            LEARNING_PODS, RECORDING_ROOM, VIDEO_CONFERENCING_ROOM \
            FROM LIBCHOP \
            WHERE TELEGRAMID = %s")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, tgUsername)
            results = cursor.fetchall()
        except:
            print("Query failed")

        return results[0]


def set_username(tgUsername, username):
    # Function to store NTU username, given the telegram username
    db = ChopeDB()

    targetVariables = SelectList = []

    """
    Check if the user's Telegram Username exists in database
    If it does, update user's NTU username
    if not, insert telegram and NTU username into a new row
    The same logic applies for the next function, set_password
    """
    SelectList.append(("TELEGRAMID", "%s", tgUsername, "TELEGRAMID"))

    targetVariables = db.select("LIBCHOP", targetVariables, SelectList)

    if targetVariables == []:
        InsertList = []
        InsertList.append(("TELEGRAMID", '%s', tgUsername))
        InsertList.append(("USERNAME", '%s', username))

        db.insert("LIBCHOP", InsertList)
    else:
        UpdateList = []
        UpdateList.append(("USERNAME", '%s', username,
                           "TELEGRAMID", '%s', tgUsername))
        db.update("LIBCHOP", UpdateList)
    db.close()


def set_password(tgUsername, password, chatID):
    # input chatID as integer, while the rest of the parameters as string

    db = ChopeDB()
    # pad the key until it is 16 characters long before encryption
    encryptKey = str(chatID)
    while len(encryptKey) < 16:
        encryptKey = encryptKey + "]"

    obj = AES.new(encryptKey, AES.MODE_CFB, 'This is an IV456')
    encryptedPass = obj.encrypt(password)

    targetVariables = SelectList = []

    SelectList.append(("TELEGRAMID", "%s", tgUsername, "TELEGRAMID"))

    targetVariables = db.select("LIBCHOP", targetVariables, SelectList)

    if targetVariables == []:
        InsertList = []
        InsertList.append(("TELEGRAMID", '%s', tgUsername))
        InsertList.append(("PASSWORD", '%s', encryptedPass))

        db.insert("LIBCHOP", InsertList)
    else:
        UpdateList = []
        UpdateList.append(("PASSWORD", '%s', encryptedPass,
                           "TELEGRAMID", '%s', tgUsername))
        db.update("LIBCHOP", UpdateList)
    db.close()


def set_prio(tgUsername, seatName='', value=0):
    # Order of priority column in this parameter is based on their order in db

    db = ChopeDB()
    targetVariables = SelectList = []

    SelectList.append(("TELEGRAMID", "%s", tgUsername, "TELEGRAMID"))

    targetVariables = db.select("LIBCHOP", targetVariables, SelectList)

    if targetVariables == []:
        return False
    else:
        UpdateList = []
        UpdateList.append((seatName, '%s', value,
                           "TELEGRAMID", '%s', tgUsername))
        db.update("LIBCHOP", UpdateList)
    db.close()


def get_username(tgUsername):
    db = ChopeDB()

    targetVariables = []
    SelectList = [("TELEGRAMID", "%s", tgUsername, "USERNAME")]
    targetVariables = db.select("LIBCHOP", targetVariables, SelectList)

    if targetVariables == []:
        Username = ""
    else:
        Username = targetVariables[0]

    return Username

    db.close()


def get_password(tgUsername, chatID):
    # tgUsername in string, chatID in integer

    db = ChopeDB()

    encryptKey = str(chatID)
    while len(encryptKey) < 16:
        encryptKey = encryptKey + "]"

    targetVariables = []
    SelectList = [("TELEGRAMID", "%s", tgUsername, "PASSWORD")]
    targetVariables = db.select("LIBCHOP", targetVariables, SelectList)

    if targetVariables == []:
        return ""
    else:
        encryptedPass = targetVariables[0]

    # Decrypt the encrypted password
    obj2 = AES.new(encryptKey, AES.MODE_CFB, 'This is an IV456')
    Password = obj2.decrypt(encryptedPass)
    strPassword = str(Password)
    strPassword = strPassword.strip("b'")
    db.close()
    return strPassword


def get_prio(tgUsername):
    db = ChopeDB()
    Priority = db.select_dict(tgUsername)
    db.close()
    return Priority
