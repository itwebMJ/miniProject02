import pymysql

class cReboard :
    def __init__(self, num = None, writer = None, w_date = None, email = None, content = None, pk = None) :
        self.num = num
        self.writer = writer
        self.w_date = w_date
        self.email = email
        self.content = content
        self.pk = pk


class cReboard_dao :
    def __init__(self) :
        self.conn = None
        self.cur = None

    def Connect(self) :
        self.conn = pymysql.connect(host = "localhost", user = "root", password = "1234",
                                    db = "tour", charset = "utf8")
        self.cur = self.conn.cursor()

    def Disconnect(self) :
        self.cur = None
        self.conn.close()

    def Insert(self, vo) :
        self.Connect()
        sql = "insert into reboard(num, writer, w_date, content, email) values(%s, %s, now(), %s, %s)"
        vals = (vo.num, vo.writer, vo.content, vo.email)
        self.cur.execute(sql, vals)
        self.conn.commit()
        self.Disconnect()

    def Delete(self, pk) :
        self.Connect()
        sql = "delete from reboard where pk = " + str(pk)
        self.cur.execute(sql)
        self.conn.commit()
        self.Disconnect()

    def Update(self, vo) :
        self.Connect()
        sql = "update reboard set w_date = now(), content = %s where pk = " + str(vo.pk)
        vals = (vo.content, )
        self.cur.execute(sql, vals)
        self.conn.commit()
        self.Disconnect()


    def Select(self, num) :
        self.Connect()
        sql = "select * from reboard where num = %s order by pk"
        vals = (num,)
        self.cur.execute(sql, vals)
        lst = []
        for row in self.cur :
            lst.append(cReboard(row[0], row[1], row[2], row[3], row[4], row[5]))
        self.Disconnect()
        return lst


class cReboard_service :
    def __init__(self) :
        self.dao = cReboard_dao()

    def Add_reboard(self, vo) :
        return self.dao.Insert(vo)

    def Get_reboard(self, num) :
        return self.dao.Select(num)

    def Delete_reboard(self, pk):
        return self.dao.Delete(pk)

    def Edit_reboard(self, vo) :
        return self.dao.Update(vo)


