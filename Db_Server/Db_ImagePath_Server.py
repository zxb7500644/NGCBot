from OutPut import OutPut
import sqlite3
import yaml
import os

class Db_ImagePath_Server:
    def __init__(self):
        current_path = os.path.dirname(__file__)
        # 数据库存放地址
        self.db_file = current_path + '/../Config/ImagePath_db.db'

        
    # 打开数据库
    def open_db(self):
        conn = sqlite3.connect(database=self.db_file, )
        cursor = conn.cursor()
        return conn, cursor
    
    # 关闭数据库
    def close_db(self, conn, cursor):
        cursor.close()
        conn.close()
        
    def db_init(self):
        """初始化图片地址数据库。"""
        OutPut.outPut('[*]: 图片地址数据库正在初始化... ...')
        conn, cursor = self.open_db()

        # 创建图片地址表
        create_image_table_sql = '''
        CREATE TABLE IF NOT EXISTS image (
            wx_id TEXT,
            wx_name TEXT,
            room_id TEXT,
            room_name TEXT,
            imagePath TEXT,
            base64 TEXT
        );
        '''
        # 执行SQL语句
        cursor.execute(create_image_table_sql)
        
        # 提交事务
        conn.commit()

        # 关闭数据库连接
        self.close_db(conn, cursor)
        OutPut.outPut('[+]: 图片地址数据库初始化成功！！！')
        

    def judge_user(self, wx_id, room_id):
        """判断用户是否存在于图片地址表中。"""
        conn, cursor = self.open_db()
        query_sql = '''SELECT COUNT(*) FROM image WHERE wx_id = ? AND room_id = ?'''
        cursor.execute(query_sql, (wx_id, room_id))
        result = cursor.fetchone()[0]
        self.close_db(conn, cursor)
        return result > 0

    def add_user(self, wx_id, wx_name, room_id, room_name, image_path):
        """添加新用户到图片地址表中，如果用户不存在。"""
        if not self.judge_user(wx_id=wx_id, room_id=room_id):
            conn, cursor = self.open_db()
            add_user_sql = '''INSERT INTO image (wx_id, wx_name, room_id, room_name, imagePath) VALUES (?, ?, ?, ?, ?)'''
            cursor.execute(add_user_sql, (wx_id, wx_name, room_id, room_name, image_path))
            conn.commit()
            self.close_db(conn, cursor)
            OutPut.outPut(f'[+]: 用户 {wx_name} 已成功添加到图片地址表中。')
        else:
            OutPut.outPut(f'[-]: 用户 {wx_name} 已存在于图片地址表中。')

    def query_imagePath(self, wx_id, wx_name, room_id, room_name):
        """查询当前用户的图片地址。"""
        if self.judge_user(wx_id=wx_id, room_id=room_id):
            conn, cursor = self.open_db()
            query_imagePath_sql = '''SELECT imagePath FROM image WHERE wx_id = ? AND room_id = ?'''
            cursor.execute(query_imagePath_sql, (wx_id, room_id))
            data = cursor.fetchone()
            image_path = data[0] if data else None
            self.close_db(conn, cursor)
        else:
            self.add_user(wx_id=wx_id, wx_name=wx_name, room_id=room_id, room_name=room_name, image_path="")
            image_path = self.query_imagePath(wx_id=wx_id, wx_name=wx_name, room_id=room_id, room_name=room_name)
        return image_path

    def update_imagePath(self, wx_id, wx_name, room_id, room_name, image_path):
        """更新用户的图片地址。"""
        if self.judge_user(wx_id=wx_id, room_id=room_id):
            conn, cursor = self.open_db()
            update_imagePath_sql = '''UPDATE image SET imagePath = ? WHERE wx_id = ? AND room_id = ?'''
            cursor.execute(update_imagePath_sql, (image_path, wx_id, room_id))
            conn.commit()
            self.close_db(conn, cursor)
            msg = f'您的图片地址已更新为: {image_path}'
        else:
            self.add_user(wx_id=wx_id, wx_name=wx_name, room_id=room_id, room_name=room_name, image_path=image_path)
            msg = f'用户不存在，已添加新用户并设置图片地址为: {image_path}'
        return msg

    def query_base64(self, wx_id, room_id):
        """查询当前用户的图片地址。"""
        base64 = ""
        if self.judge_user(wx_id=wx_id, room_id=room_id):
            conn, cursor = self.open_db()
            query_base64_sql = '''SELECT base64 FROM image WHERE wx_id = ? AND room_id = ?'''
            cursor.execute(query_base64_sql, (wx_id, room_id))
            data = cursor.fetchone()
            base64 = data[0] if data else None
            self.close_db(conn, cursor)
        return base64
    
    def update_base64(self, wx_id, room_id, base64):
        """更新用户的图片地址。"""
        msg = ""
        if self.judge_user(wx_id=wx_id, room_id=room_id):
            conn, cursor = self.open_db()
            update_base64_sql = '''UPDATE image SET base64 = ? WHERE wx_id = ? AND room_id = ?'''
            cursor.execute(update_base64_sql, (base64, wx_id, room_id))
            conn.commit()
            self.close_db(conn, cursor)
            msg = f'您的base64已更新为: {base64}'
        return msg