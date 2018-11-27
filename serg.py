import random
from connopt import get_c
import hashlib
from datetime import datetime

class Data:
    def __init__(self):
        self.conn = get_c()
        self.cursor = self.conn.cursor()
        self.help = Helping()
        
        
    def insert_user(self, user, password):
        sql = 'INSERT INTO users(user, hash) values (%s, %s)'
        hesh = self.help.take_hesh(password)#использую слово 'hesh' вместо 'hash', т.к. второе зарезервировано
        self.cursor.execute(sql, (user, hesh))
        result = self.cursor.fetchall()
        self.conn.commit()
        print('New User: '+user)
        
    def autorize(self, user, password):
        hesh = self.help.take_hesh(password)
        word = 'SELECT user, hash FROm Users WHERE user="'+user+'" AND hesh="'+str(hesh)+'";'
        self.cursor.execute(word)
        result = self.cursor.fetchall()
        sessi = 'INSERT INTO Session(user_id, sess) values(%s, %s)'
        new_sess = user+str(datetime.now())
        sess = self.help.take_hesh(new_sess)
        self.cursor.execute(sessi, (result[0]['id'], sess))
        self.conn.commit()
        print("You're Welcome!")
        return(sess)


    def quit_session(self, sess):
        sessi = 'DELETE FROM Session WHERE sess="'+str(sess)+'";'
        self.cursor.execute(sessi)
        self.conn.commit()
        print('Quites')
        
    def view_users(self):
        sql = 'SELECT id, user FROM Users'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for user in result:
            print('id : {}  -  user : {}'.format(user['id'], user['user']))

            
class Blogs(Data):
    def __init__(self):
        self.conn = get_c()
        self.cursor = self.conn.cursor()
        self.help = Helping()
    
    def insert_blog(self, sess, name):
        user_id = self.help.get_user(sess)
        sql = 'INSERT INTO Blog(name, user_id) values (%s, %s)'
        self.cursor.execute(sql, (name, user_id))
        self.conn.commit()
        print('New Blog: '+name)

    def delete_blog(self, sess, blog_id):
        if self.help.check_root(sess, blog_id, 'blog'):
            sql = 'UPDATE blog SET deleted = 1 WHERE id="'+str(blog_id)+'";'
            self.cursor.execute(sql)
            self.conn.commit()
            print('Deleted succesfully!')
        else:
            print('You have no permission to delete this blog')

    def rename_blog(self, sess, blog_id, new_name):
        if self.help.check_root(sess, blog_id, 'blog'):
            sql = 'UPDATE blog SET name="'+new_name+'" WHERE id="'+str(blog_id)+'";'
            self.cursor.execute(sql)
            self.conn.commit()
            print('Renamed succesfully! New name '+new_name)
        else:
            print('You have no permission to rename this blog')

    def get_all_blogs(self):#вернет неудаленные блоги
        sql = 'SELECT id, name FROM blog WHERE deleted=0'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        for blog in res:
            print('id : {}  -  blog : {}'.format(blog['id'], blog['name']))

    def get_user_blogs(self, sess):#вернет неудаленные блоги пользователя сессии
        user_id = self.help.get_user(sess)
        sql = 'SELECT id, name FROM blog WHERE deleted=0 AND user_id="'+str(user_id)+'";'
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        for blog in res:
            print('id : {}  -  blog : {}'.format(blog['id'], blog['name']))


class Posts(Data):
    def __init__(self):
        self.conn = get_c()
        self.cursor = self.conn.cursor()
        self.help = Helping()

    def insert_post(self, sess, name, text, *blogs_ids):
        if (len(blogs_ids)) == 0:
            print ('There were no blogs chosen')
        else:
            user_id = self.help.get_user(sess)
            max_id = 'SELECT MAX(id) FROM Post'
            post_adding = 'INSERT INTO Post(user_id, name, text, blog_id) values (%s, %s, %s, %s)'
            adding = 'INSERT INTO blog_post(post_id, blog_id) values(%s, %s)'  
            for i in blogs_ids:
                self.cursor.execute(post_adding, (user_id, name, text, i))
            self.conn.commit()
            self.cursor.execute(max_id)
            take = self.cursor.fetchall()
            max_post = take[0]['MAX(id)']
            lent = len(blogs_ids)
            for i in blogs_ids:
                post_num = max_post - lent + 1
                lent -= 1
                self.cursor.execute(adding, (post_num, i))
            self.conn.commit() 
            print('New Post: '+name)

    def delete_post(self, sess, post_id):
        if self.help.check_root(sess, post_id, 'post'):
            sql = 'DELETE FROM Post WHERE id="'+str(post_id)+'";'
            self.cursor.execute(sql)
            self.conn.commit()
            print('Deleted succesfully!')
        else:
            print('You have no permission to do this action!')

    def rename_post(self, sess, post_id, new_name):
        if self.help.check_root(sess, post_id, 'post'):
            sql = 'UPDATE post SET name="'+new_name+'" WHERE id="'+str(post_id)+'";'
            self.cursor.execute(sql)
            self.conn.commit()
            print('Renamed succesfully! New name: '+new_name)
        else:
            print('You have no permission to rename this post')

    def change_post_text(self, sess, post_id, new_text):
        if self.help.check_root(sess, post_id, 'post'):
            sql = 'UPDATE post SET text="'+new_text+'" WHERE id="'+str(post_id)+'";'
            self.cursor.execute(sql)
            self.conn.commit()
            print('Post text changed succesfully!')
        else:
            print('You have no permission to rename this post')

    def copy_post(self, sess, post_id, *blogs_ids):#копирует пост в другие блоги
        user_id = self.help.check_root(sess, post_id, 'post')
        if user_id:
            sql = 'SELECT name, text FROM post WHERE id='+str(post_id)+';'
            self.cursor.execute(sql)
            info = self.cursor.fetchone()
            name = info['name']
            text = info['text']
            self.insert_post(sess, name, text, *blogs_ids)
        else:
            print('Error')
            

class Commentary(Data):
    def __init__(self):
        self.conn = get_c()
        self.cursor = self.conn.cursor()
        self.help = Helping()
        
    def insert_comm(self, sess, post_id, comment, comment_id=None):
        user_id = self.help.get_user(sess)
        if comment_id==None:
            sql = 'INSERT INTO Comments(user_id, post_id, comment) values (%s, %s, %s)'
            self.cursor.execute(sql, (user_id, post_id, comment))
            self.cursor.fetchall()
            print('New Comment: '+comment)
            return self.conn.commit()
        else:
            search = 'SELECT post_id FROM Comments WHERE comment_id='+str(comment_id)+';'
            self.cursor.execute(search)
            res = self.cursor.fetchone()
            if post_id == res['post_id']:
                sql = 'INSERT INTO Comments(user_id, post_id, comment_id, comment) values (%s, %s, %s, %s)'
                self.cursor.execute(sql, (user_id, post_id, comment_id, comment))
                self.cursor.fetchall() 
                print('New Comment: '+comment)
                return self.conn.commit()
            else:
                print('Error: there are no comment N'+str(comment_id)+' in post N'+str(post_id))

    def get_user_comments(self, sess, post_id):
        user_id = self.help.get_user(sess)
        sql = 'SELECT id, comment_id, comment FROM Comments Where user_id="'+str(user_id)+'" AND post_id="'+str(post_id)+'";'
        self.cursor.execute(sql)
        comments = self.cursor.fetchall()
        print('All comments by User N'+str(user_id)+' to post N'+str(post_id))
        for comm in comments:
            print('id : {}  to comment : {}  ---  {}'.format(comm['id'], comm['comment_id'], comm['comment']))

    def get_comments(self, blog_id, *user_id):#получает комменты для юзеров из блога (доп. задание)
        if len(user_id)==0:
            print('No users chosen')
        else:
            print('blog N'+str(blog_id))
            read_sql = 'SELECT user_id, comment FROM Comments LEFT JOIN Blog_post Using(post_id) Where blog_id="'+str(blog_id)+'";'
            self.cursor.execute(read_sql)
            comments = self.cursor.fetchall()
            for i in user_id:
                for k in comments:
                    if k['user_id']==i:
                        print(k['comment'])


    def get_comment_line(self, comment_id):#получение дерева комментариев к comment_id (доп. задание)
        join = 'SELECT c2.id, c2.comment_id, c2.comment FROM Comments c1 JOIN Comments c2 on c1.post_id'\
                '= c2.post_id where c1.id="'+str(comment_id)+'";'
        self.cursor.execute(join)
        ids = self.cursor.fetchall()
        comment_ids = list()
        comment_ids.append(comment_id)
        for i in ids:
            if i['comment_id'] in comment_ids:
                print (i['comment'])
                comment_ids.append(i['id'])
##

                    
class Helping(Data):
    def __init__(self):
        self.conn = get_c()
        self.cursor = self.conn.cursor()
        
    def get_user(self, sess):
        sql = 'SELECT user_id FROM Session Where sess="'+str(sess)+'";'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if len(result)==0:
            print('There no such session')
        else:
            return result[0]['user_id']

    def take_hesh(self, password):
        password = password.encode()
        h = hashlib.md5(password)
        hesh = h.hexdigest()
        return hesh

    def check_root(self, sess, ident, typer): #проверяет, является ли хозяин сессии создателем блога/поста
        user_id = self.get_user(sess)
        if typer=='blog':
            root = 'SELECT user_id FROM blog WHERE id="'+str(ident)+'";'
        if typer=='post':
            root = 'SELECT user_id FROM post WHERE id="'+str(ident)+'";'
        self.cursor.execute(root)
        user = self.cursor.fetchone()['user_id']
        if user_id==user:
            return user_id
        else:
            return False


                    
D=Data()
#D.autorize('Man','Man')
C=Commentary()
C.get_comment_line(1)








