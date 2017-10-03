import pymysql
from util import VPrinter


class ChopeDB:
    table = None
    """
        jadi kalo mau connect ke db tinggal MySQLConnector(namadb)
        terus di assign ke variable mis:
        db = MySQLConnector("apalah")

        terus pas misal mau insert tinggal
        db.insert('tablename', arguments)
        coba liat trial-mysql.py kalo mo coba"
        makasih :)
    """
    def __init__(self, database='u7728567_chopebot'):
        self.connection = pymysql.connect(
            host='bebong.id',
            user='u7728567_chope',
            password='bunuakumz578%&*',
            db=database,
            charset='utf8mb4')
        """
            cursorclass=pymysql.cursors.DictCursor
            bagian ini tak buang karena kalo pake
            cursorclass ini, ngaruh ke hasil query sql
            select

            misal mo ngeselect field username sm password
            contoh hasil query kalo pake cursorclass nya:
            {('USERNAME' : 'iniusername', 'PASSWORD' : 'inipassword')}
            lupa persisnya gimana, intinya jd gbs w akses per elemen
            kalo ga pake:
            (('iniusername', 'inipassword'),)

            suda mencoba untuk fungsi lainnya, jalan2 aja ga ada efek

        """

    def set_table(self, tableName):
        self.table = tableName

    def close(self):
        self.connection.close()

    def insert(self, table, data=[]):
        """
        insert documentation

        table: string
            nama table yang lw mo masukin

        data: list of tuples (colname, type, value)
            e.g. ('favCartoonCharacter', "%s", 'Donald Duck')
            "%s" denotes string
            "%d" denotes decimal (number)
            "%f" denotes float
            et cetera.
        """
        v = VPrinter(True)

        colName = ', '.join([('`' + elm[0] + '`') for elm in data])
        v.vprint(colName)
        colType = ', '.join([elm[1] for elm in data])
        v.vprint(colType)

        statement = (
            "INSERT INTO " + table
            + " (" + colName + ") "
            + "VALUES (" + colType + ")")
        v.vprint(statement)

        args = tuple([elm[2] for elm in data])
        v.vprint(args)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(statement, args)
            self.connection.commit()
        finally:
            pass

    def delete(self, table, condition, values):
        # TODO: benerin docstring benda ini  jerrell ngantuk ini jam 5:20
        """
            table ya tablename
            condition dibikin sendiri like
            'kolomapa = %d OR (kolomlain = %s AND yang lain = %f)'
            values ya list of barang lah buat isi persen"nya
        """

        v = VPrinter(True)
        statement = (
            "DELETE FROM " + table
            + " WHERE " + condition)
        v.vprint(statement)

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

        v = VPrinter(True)

        colName1 = ', '.join([('`' + elm[0] + '`') for elm in data])
        v.vprint(colName1)
        colType1 = ', '.join([(elm[1]) for elm in data])
        v.vprint(colType1)
        colName2 = ', '.join([('`' + elm[3] + '`') for elm in data])
        v.vprint(colName2)
        colType2 = ', '.join([(elm[4]) for elm in data])
        v.vprint(colType2)

        for elm in data:
            statement = (
                "UPDATE " + table
                + " SET " + elm[0]
                + " = " + elm[1]
                + " WHERE " + elm[3]
                + " = " + elm[4])
            v.vprint(statement)
            args = [elm[2]] + [elm[5]]
            v.vprint(args)

            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(statement, args)
                self.connection.commit()
            finally:
                pass

    def select(self, table, targetVariables, data=[]):
        """
        table: string
        data: list of tuples (colName, data type, colValue, colSelect,
                              targetVariables)
                              (targetVariables nya gagal msk bagian dr list
                              jadi w masukkin parameter, more info ahead)
        colName: Name of column to be checked
        data type: data type of values within colName
        colValue: Value to find within column colName
        colSelect: list of columns to be selected
        targetVariables: list of variables to assign values from the
                        selected columns (listed in the same order
                        as colSelect)
                        P.S. : hai jerrell, berhubung bagian ini
                        gagal w bikin (bc apparently ucannot make
                        a list of variables in python sorry am clueless)
                        instead of individual variables
                        smw values yg keselect dlm 1 argum w taro smw
                        dlm 1 list aja ye maapkan q suda berusaha
                        (nama listnya targetVariables)

        """

        v = VPrinter(True)

        # Initialization for various counter/loop control variables
        deletChar = "[]\'"
        Count = len(data)
        targetVariables = []

        for i in range(Count):
            elm = data[i]
            FieldNameStr = str(elm[3])

            for char in deletChar:
                FieldNameStr = FieldNameStr.replace(char, " ")

            statement = (
                "SELECT " + FieldNameStr
                + " FROM " + table
                + " WHERE " + elm[0]
                + " = " + elm[1] + "")
            v.vprint(statement)
            args = elm[2]
            v.vprint(args)

            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(statement, args)
                results = cursor.fetchall()
                print(results)

                for row in results:
                    for j in range(len(row)):
                        targetVariables.append((row[j]))

            finally:
                pass
        return targetVariables


def get_credential(tgUsername, chatID):
    # return tuple username, password
    # btw inget enkripsi ya, btw cari aja lib apapun
    # yng buat enkripsi dekripsi jadinya lw return gua decrypted
    # TODO: fill this whole function
    # XXX: delete this huge junk of comments
    pass


def store_credential(tgUsername, chatID, username, password):
    # jadinya lw bikin fungsi yang nge store username, password
    # lw encrypt passwordnya pake chatID soalnya itu unique untuk kita
    # kek kebalikannya get_credential
    # yang satunya store
    # yang satunya narik
    # TODO: fill this whole function
    # XXX: delete this huge junk of comments
    pass
