#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import re
import time
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

blog_remote_url = "https://github.com/slegetank/MyBlogOrg"
blog_local_path = os.path.abspath("static/MyBlogOrg")
blog_org_path = "%s/blog" % blog_local_path

def getFileInfo(filename):
    with open(filename, 'r') as orgfile:
        retDic = {}
        content = orgfile.read()

        # title
        retDic["title"] = re.search(r'(?<=#\+title:).*?(?=\n)', content, re.I).group().strip().encode("utf8")

        # writetime
        date = re.search(r'(?<=#\+date:).*?(?=\n)', content, re.I).group().strip()
        date = time.strptime(date, "<%Y-%m-%d %H:%M>")
        retDic["writetime"] = time.strftime("%Y-%m-%d %H:%M:%S", date)

        # type
        retDic["type"] = re.search(r'(?<=#\+blogtype:).*?(?=\n)', content, re.I).group().strip()

        # desc
        retDic["desc"] = re.search(r'(?<=#\+BEGIN_COMMENT PREVIEW).*?(?=#\+END_COMMENT)', content, re.S|re.I).group().strip()

        # mtime
        retDic["lastupdate"] = os.path.getmtime(filename)

        # pics
        picDir = os.path.abspath("../static/")
        prefix = os.path.splitext("%s/%s" % (picDir, filename))[0]
        files = glob.glob("%s*" % prefix)
        imageStr = ""
        for i in range(0, len(files)):
            imagePath = files[i]
            if i == 2:
                break

            imagePath = os.path.basename(imagePath)
            imageStr += imagePath+","

        if len(imageStr) != 0:
            imageStr = imageStr[:-1]
        retDic["image"] = imageStr

        return retDic

if __name__ == '__main__':
    conn = MySQLdb.connect(
        host=os.getenv('MYWEBSITE_HOST'),
        port = 3306,
        user='root',
        passwd=os.getenv('MYWEBSITE_DB_PASS'),
        db ='mywebsite',
        charset="utf8"
    )
    cur = conn.cursor()

    if not os.path.exists(blog_local_path):
        os.system("git clone %s %s" % (blog_remote_url, blog_local_path))

    os.chdir(blog_org_path)
    os.system("git reset --hard && git fetch && git rebase")

    db_blogs = cur.execute("select filename, lastupdate from blog")
    db_blogs = cur.fetchmany(db_blogs)

    local_blogs = glob.glob("*.org")

    update_arr = []
    insert_arr = []
    delete_arr = []

    for blog in db_blogs:
        filename = blog[0]
        modifytime = blog[1]
        if filename in local_blogs:
            if modifytime != os.path.getmtime(filename):
                update_arr.append(blog[0])

            del(local_blogs[local_blogs.index(filename)])
        else:
            delete_arr.append(filename)

    insert_arr.extend(local_blogs)

    for filename in delete_arr:
        cur.execute("delete from blog where filename=%s" % filename)

    insertsql_arr = []
    for filename in insert_arr:
        infoDic = getFileInfo(filename)
        insertsql_arr.append((None, infoDic['title'], infoDic['type'], infoDic['writetime'], infoDic['desc'], filename, infoDic['lastupdate'], infoDic["image"]))

    sqli="insert into blog values(%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.executemany(sqli, insertsql_arr)

    updatesql_arr = []
    for filename in update_arr:
        infoDic = getFileInfo(filename)
        updatesql_arr.append((infoDic['title'], infoDic['type'], infoDic['writetime'], infoDic['desc'], infoDic['lastupdate'], infoDic['image'], filename))

        sqlu="update blog set title=%s,type=%s,writetime=%s,`desc`=%s,lastupdate=%s,image=%s where filename=%s"
        cur.executemany(sqlu, updatesql_arr)

    cur.close()
    conn.commit()
    conn.close()
