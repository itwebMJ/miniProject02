import pymysql

class cMember :
    def __init__(self, email = None, pwd = None, name = None, interest = None) :
        self.email = email
        self.pwd = pwd
        self.name = name
        self.interest = interest

class cMember_dao :
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
        sql = "insert into member(email, pwd, name) values(%s, %s, %s)"
        vals = (vo.email, vo.pwd, vo.name)
        self.cur.execute(sql, vals)
        self.conn.commit()
        self.Disconnect()

    def SelectAll(self) :
        self.Connect()
        sql = "select * from member"
        self.cur.execute(sql)
        mem = []
        for row in self.cur :
           mem.append(cMember(row[0], row[1], row[2], row[3]))
        self.Disconnect()
        return mem

    def Select(self, email) :
        self.Connect()
        sql = "select * from member where email = %s"
        vals =(email,)
        self.cur.execute(sql, vals)
        row = self.cur.fetchone()
        self.Disconnect()
        if row :
            return cMember(row[0], row[1], row[2], row[3])



class cMember_service :
    def __init__(self) :
        self.dao = cMember_dao()

    def Add_member(self, vo) :
        return self.dao.Insert(vo)

    def Get_all(self) :
        return self.dao.SelectAll()

    def Get_member(self, email) :
        return self.dao.Select(email)









