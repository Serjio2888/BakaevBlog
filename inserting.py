import random
from connopt import get_c
import urllib.request
import hashlib
import os

class Insert:
    def __init__(self):
        self.conn = get_c()
        self.cursor = self.conn.cursor()
        self.prog_user = os.getlogin()#environ.get( "USERNAME" )
        self.names = ('Adam', 'Andrey', 'Arseny', 'Agony', 'August', 'Artur', 'Apollon','Alex',
                    'Boris', 'Bob', 'Baddy', 'Colya', 'Cort','Col','Cop','Corey','Dmitry',
                    'Dock', 'Donny','Darko','Duffy','Derek','Donald','Dima','Dora','Diana','Darpa',
                    'Douglas','Engier','Ella','Elbow','Easter','Ear','Endy','Eva','Est','Fedor',
                    'Fest','Fenya','Festal','Ferdinand','Fem','Gogy','Gregory','Grisha','Gena',
                    'Got','Harry','Herry','Hermion','Igor','Ivan','Irakly','Jack','Julia','July',
                    'Katya','Katerina','Karina','Kolya','Karl','Kandy','Kort','Leon','Lolly','Lolita',
                    'Mary','Marina','Marya','MaRussia','Mama','North','Nikolay','Never','Nancy',
                    'Oleg','Oleksandr','Olga','Omar','Pedro','Petr','Petya','Qupid','Roma','Roman',
                    'Rock','Sanya','Sonya','Timofey','Tacker','Uniq','User','Umberto','Vladimir',
                    'Vova','Vanya','Vano','Vadim','Vadik','Vlad','Vladislaff','Vladislav','Voron',
                    'Xenia','Yigor','Ynona','Zolla','Zibert','Zack','Zelda')
        self.day = ('On Monday', 'On weekends', 'On Christmas', 'On Birthday','Yestarday','Yesterday evening',
                    'Yesterday morning', 'On Friday','On Saturday','On Thursday','On Sunday')
        self.emotion = ('Strong','Happy','Nice','Ugly','Beautiful','Cheerfull','Greedy','Evil','Cool',
                        'Weird','Popular','Clever','Stupid','Smart','Fast','Alive','Weak','Pretty')

    def user_insert(self, how_many=1000):
        sql = 'INSERT INTO users(user, hash) values (%s, %s)'
        for i in range(how_many):
            name1 = random.choice(self.names)
            hesh = self.take_hesh(name1)
            name2 = random.choice(self.names)
            num = random.randint(1000, 10000)
            name = name1+name2+str(num)
            self.cursor.execute(sql, (name, hesh))
            result = self.cursor.fetchall()
            print(str(i+1)+' new user: '+name)
        self.conn.commit()
        print('Thank you for waiting, '+self.prog_user)
        
    def take_hesh(self, password):
        password = password.encode()
        h = hashlib.md5(password)
        hesh = h.hexdigest()
        return hesh

    def get_ids(self, typer):
        if typer == 'users':
            ids = 'SELECT id FROM Users'
        if typer == 'blogs':
            ids = 'SELECT id FROM Blog'
        if typer == 'posts':
            ids = 'SELECT id FROM Post'
        self.cursor.execute(ids)
        result = self.cursor.fetchall()
        return result

    def blog_insert(self, how_many=100):
        result = self.get_ids('users')
        sql = 'INSERT INTO Blog(name, user_id) values (%s, %s)'
        for i in range(how_many):
            user_id = random.choice(result)['id']
            name = random.choice(self.names)
            blog_name = str(user_id)+name+'Blog'
            self.cursor.execute(sql, (blog_name ,user_id))
            print(str(i+1)+' New Blog: '+blog_name)
        self.conn.commit()
        print('Thank you for waiting, '+self.prog_user)

    def post_insert(self, how_many=10000):#10000 постов занимают меньше минуты времени 
        how_many = how_many//20
        users = self.get_ids('users')
        blogs = self.get_ids('blogs')
        for i in range(how_many):
            a = random.choice(blogs)['id']
            b = random.choice(blogs)['id']
            c = random.choice(blogs)['id']
            d = random.choice(blogs)['id']
            ident = random.choice(users)['id']
            namen = str(random.choice(self.names))
            name = ('About '+namen)
            text = (random.choice(self.day)+' '+namen+' was '+random.choice(self.emotion))
            self.insert_post(ident, name, text, a,b,c,d,a,b,c,d,a,b,c,d,a,b,c,d,a,b,c,d)
        self.conn.commit() 
        print('Thank you for waiting, '+self.prog_user)  
            
    def insert_post(self, user_id, name, text, *blogs_ids):
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
        print('New Post: {} ---- Text: {}'.format(name, text))

    def comm_insert(self, how_many=100000):#100000 комментариев добавляются менее чем за две минуты
        max_id = 'SELECT MAX(id) FROM Comments'
        sql = 'INSERT INTO Comments(user_id, post_id, comment) values (%s, %s, %s)'
        to_comment = 'INSERT INTO Comments(user_id, post_id, comment_id, comment) values(%s, %s, %s, %s)' 
        users = self.get_ids('users')
        posts = self.get_ids('posts')
        for i in range(how_many//1000):
            user_id = random.choice(users)['id']
            post_id = random.choice(posts)['id']
            emo = random.choice(self.emotion)
            comment = 'Oh, very '+emo
            self.cursor.execute(sql, (user_id, post_id, comment))
            self.conn.commit()
            self.cursor.execute(max_id)
            maximum = self.cursor.fetchone()['MAX(id)']
            for k in range(1000):
                user_id = random.choice(users)['id']
                commento = 'Yes, too '+emo
                self.cursor.execute(to_comment, (user_id, post_id, maximum, commento))
            self.conn.commit()
            print(str((i+1)*1000)+' comments already posted')
        print('Thank you for waiting, '+self.prog_user)




def main():
    I = Insert()
    I.user_insert()
    I.blog_insert()
    I.post_insert()
    I.comm_insert()

if __name__ == '__main__':
    main()





    
