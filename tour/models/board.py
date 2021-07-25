import pymysql

class cBoard :
    def __init__(self, num = None, writer = None, w_date = None, title = None,
                 content = None, img_path = None, email = None, loc = None) :
        self.num = num
        self.writer = writer
        self.w_date = w_date
        self.title = title
        self.content = content
        self.img_path = img_path
        self.email = email
        self.loc = loc


class cBoard_dao :
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
        sql = "insert into board(writer, w_date, title, content, img_path, email, loc) values(%s, now(), %s, %s, %s, %s, %s)"
        vals = (vo.writer, vo.title, vo.content, vo.img_path, vo.email, vo.loc)
        self.cur.execute(sql, vals)
        self.conn.commit()
        self.Disconnect()

    def Delete(self, num) :
        self.Connect()
        sql = "delete from board where num = " + str(num)
        self.cur.execute(sql)
        self.conn.commit()
        self.Disconnect()

    def Update(self, vo) :
        self.Connect()
        sql = "update board set w_date = now(), title = %s, content = %s, img_path = %s, loc = %s where num = %s"
        vals = (vo.title, vo.content, vo.img_path, vo.loc, vo.num)
        self.cur.execute(sql, vals)
        self.conn.commit()
        self.Disconnect()

    def SelectAll(self) :
        self.Connect()
        sql = "select * from board order by num desc"
        self.cur.execute(sql)
        lst = []
        for row in self.cur :
            lst.append(cBoard(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        self.Disconnect()
        return lst

    def Select(self, option, val) :
        self.Connect()
        sql = "select * from board where " + option + " like %s order by num desc"
        vals = ('%' + str(val) + '%',)
        self.cur.execute(sql, vals)
        lst = []
        for row in self.cur :
            lst.append(cBoard(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        self.Disconnect()
        return lst

    def SelectNum(self, num) :
        self.Connect()
        sql = "select * from board where num = " + str(num)
        self.cur.execute(sql)
        row = self.cur.fetchone()
        self.Disconnect()
        return cBoard(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

class cBoard_service :
    def __init__(self) :
        self.dao = cBoard_dao()

    def Add_board(self, vo) :
        return self.dao.Insert(vo)

    def Get_all(self) :
        return self.dao.SelectAll()

    def Get_board(self, option, val) :
        return self.dao.Select(option, val)

    def Delete_board(self, num):
        return self.dao.Delete(num)

    def Edit_board(self, vo) :
        return self.dao.Update(vo)

    def Get_board_num(self, num) :
        return self.dao.SelectNum(num)

