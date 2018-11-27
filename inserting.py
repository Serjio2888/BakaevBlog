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
        namen = list()
        for i in range(how_many):
            name1 = random.choice(self.names)
            hesh = self.take_hesh(name1)
            name2 = random.choice(self.names)
            num = random.randint(1000, 10000)
            name = name1+name2+str(num)
            namen.append((name, hesh))
        self.cursor.executemany(sql, namen)
        result = self.cursor.fetchall()
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
        namen = list()
        for i in range(how_many):
            user_id = random.choice(result)['id']
            name = random.choice(self.names)
            blog_name = str(user_id)+name+'Blog'
            namen.append((blog_name, user_id))
        self.cursor.executemany(sql, namen)
        self.conn.commit()
        print('Thank you for waiting, '+self.prog_user)

    def post_insert(self, how_many=10000):
        users = self.get_ids('users')
        blogs = self.get_ids('blogs')
        posted = list()
        blogged = list()
        max_id = 'SELECT MAX(id) FROM Post'
        self.cursor.execute(max_id)
        take = self.cursor.fetchall()
        max_post = take[0]['MAX(id)']
        for i in range(how_many):
            a = random.choice(blogs)['id']
            ident = random.choice(users)['id']
            namen = str(random.choice(self.names))
            name = ('About '+namen)
            text = (random.choice(self.day)+' '+namen+' was '+random.choice(self.emotion))
            posted.append((ident, name, text, a))
            blogged.append((max_post+1, a))
        post_adding = 'INSERT INTO Post(user_id, name, text, blog_id) values (%s, %s, %s, %s)'
        self.cursor.executemany(post_adding, posted)
        adding = 'INSERT INTO blog_post(post_id, blog_id) values(%s, %s)'
        self.cursor.executemany(adding, blogged)
        self.conn.commit() 
        print('Thank you for waiting, '+self.prog_user)  
            

    def comm_insert(self, how_many=100000):
        max_id = 'SELECT MAX(id) FROM Comments'
        sql = 'INSERT INTO Comments(user_id, post_id, comment) values (%s, %s, %s)'
        to_comment = 'INSERT INTO Comments(user_id, post_id, comment_id, comment) values(%s, %s, %s, %s)' 
        users = self.get_ids('users')
        posts = self.get_ids('posts')
        commo = list()
        self.cursor.execute(max_id)
        maximum = self.cursor.fetchone()['MAX(id)']
        for i in range(1000):
            user_id = random.choice(users)['id']
            post_id = random.choice(posts)['id']
            emo = random.choice(self.emotion)
            comment = 'Oh, very '+emo
            commo.append((user_id, post_id, comment))
        self.cursor.executemany(sql, commo)
        self.conn.commit()
        new_commo = list()
        for k in range(10000):
            user_id = random.choice(users)['id']
            emo = random.choice(self.emotion)
            commento = 'Yes, too '+emo
            for i in range(10):
                print(commo[k][1])
                new_commo.append((user_id, str(commo[k][1]), maximum+k+1, commento))
        self.cursor.executemany(to_comment, new_commo)
        self.conn.commit()
        print('Thank you for waiting, '+self.prog_user)




def main():
    I = Insert()
    I.user_insert(100)
    #I.blog_insert()
    #I.post_insert()
    #I.comm_insert()

if __name__ == '__main__':
    main()




