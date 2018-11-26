# BakaevBlog

    def get_comment_line(self, comment_id):#получение дерева комментариев к comment_id (доп. задание)
        sql = 'SELECT post_id FROM Comments WHERE id='+str(comment_id)+';'
        self.cursor.execute(sql)
        ids = self.cursor.fetchone()
        join = 'SELECT id, comment_id, comment FROM Comments WHERE post_id="'+str(ids['post_id'])+'";'
        self.cursor.execute(join)
        ids = self.cursor.fetchall()
        comment_ids = list()
        comment_ids.append(comment_id)
        for i in ids:
            if i['comment_id'] in comment_ids:
                print (i['comment'])
                comment_ids.append(i['id'])
