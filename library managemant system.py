# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 23:35:28 2020

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 23:19:17 2020

@author: user
"""

import tkinter
from datetime import *
from tkinter import *
import mysql.connector as sqltor
con=sqltor.connect(host="localhost",user="root",password="this@is@my@sql",database="library")
cur=con.cursor()
cur.execute("SELECT USER_NAME,USER_ID FROM USERS")
record=cur.fetchall()
d={}
for i in record:
    d[i[0]]=str(i[1])

#user defined functions------------------------------------------
def read1():
    cur.execute("SELECT BOOK_ID, BOOK_NAME FROM BOOKS")
    record=cur.fetchall()
    d={}
    for i in record:
        d[i[1]]=str(i[0])
    i1=k1.get()
    i2=k2.get()
    i3=e2.get()
    if i2 in d.keys() and i1 in d[i2]:
        l1=tkinter.Label(show1,text="BOOK ISSUED:"+i2,font=("Arial",30,"bold"),bg="orange")
        l1.place(x=0,y=400)
        today=str(date.today())
        r=str(date.today()+timedelta(7))
        l1=tkinter.Label(show1,text="issue date:"+today,font=("Arial",30,"bold"),bg="orange")
        l1.place(x=0,y=500)
        l1=tkinter.Label(show1,text="FINE WILL BE CHARGED RS 2 PER DAY IF BOOK IS NOT RETURNED WITHIN:"+r,font=("Arial",15,"bold"))
        l1.place(x=0,y=550)
        cur.execute("UPDATE USERS SET ISSUE_DATE='{}' WHERE USER_ID='{}'".format(today,i3))
        con.commit()
    
#------------------------------------------------------------------
def issue():
    global k1,k2,show1
    show1=tkinter.Tk()
    show1.geometry("900x600")
    show1.configure(bg="Orange")
    l1=tkinter.Label(show1,text="ISSUE BOOK:",font=("Arial",40,"bold"),bg="orange")
    l1.place(x=100,y=0)
    l2=tkinter.Label(show1,text="BOOK_ID:",font=("Arial",20,"bold"),bg="orange")
    l2.place(x=10,y=100)
    k1=tkinter.Entry(show1,width=40,font=("Arial",20,"bold"))
    k1.place(x=200,y=100)
    l3=tkinter.Label(show1,text="BOOK_NAME:",font=("Arial",20,"bold"),bg="Orange")
    l3.place(x=10,y=200)
    k2=tkinter.Entry(show1,width=40,font=("Arial",20,"bold"))
    k2.place(x=200,y=200)
    b1=tkinter.Button(show1,text="ISSUE",font=("Arial",30,"bold"),bg="Blue",command=read1)
    b1.place(x=400,y=300)
#---------------------------------------------------------------------
def read2():
    cur.execute("SELECT BOOK_NAME,BOOK_ID FROM BOOKS")
    record=cur.fetchall()
    d={}
    for i in record:
        d[i[1]]=str(i[0])
    i1=t1.get()
    i2=t2.get()
    i3=e2.get()
    l1=tkinter.Label(show2, text="BOOK RETURNED:"+i2,font=("Arial",30,"bold"),bg="Orange")
    l1.place(x=0,y=400)
    today=str(date.today())
    l1=tkinter.Label(show2, text="RETURN DATE:"+today,font=("Arial",30,"bold"),bg="Orange")
    l1.place(x=0,y=500)
    cur.execute("UPDATE USERS SET RETURN_DATE='{}' WHERE USER_ID='{}'".format(today,i3))
    con.commit()
    cur.execute("SELECT ISSUE_DATE,RETURN_DATE FROM USERS WHERE USER_ID={}".format(i3))
    record=cur.fetchall()
    for i in record:
            a,b,=i
            delta=b-a
            a=(delta.days)
            if a>7 :
                k=(a-7)*2 
                cur.execute("UPDATE USERS SET FINE='{}' WHERE USER_ID={}".format(k,i3))
                con.commit()
                l1=tkinter.Label(show2,text="YOU HAVE TO PAY FINE = Rs."+str(k),font=("Arial",30,"bold"),bg="Yellow")
                l1.place(x=0,y=550)

def returnn():
    global t1,t2,show2
    show2=tkinter.Tk()
    show2.geometry("900x600")
    show2.configure(bg="Orange")
    l1=tkinter.Label(show2,text="RETURN BOOK",font=("Arial",40,"bold"),bg="Orange")
    l1.place(x=100,y=0)
    l1=tkinter.Label(show2,text="BOOK_ID",font=("Arial",20,"bold"),bg="Orange")
    l1.place(x=10,y=100)
    t1=tkinter.Entry(show2,width=40,font=("Arial",20,"bold"))
    t1.place(x=200,y=100)
    l3=tkinter.Label(show2,text="BOOK_NAME",font=("Arial",20,"bold"),bg="Yellow")
    l3.place(x=10,y=200)
    t2=tkinter.Entry(show2,width=40,font=("Arial",20,"bold"))
    t2.place(x=200,y=200)
    b1=tkinter.Button(show2,text="RETURN",font=("Arial",30,"bold"),bg="Red",command=read2)
    b1.place(x=400,y=300)

#**********************************VIEW****************************************************************

def view() :
    show3=tkinter.Tk()
    show3.geometry("700x600")
    show3.configure(bg="Orange")
    cur.execute("SELECT * FROM BOOKS")
    record=cur.fetchall()
    r=0
    for i in record :
        c=0 
        for j in i :
            e=Entry(show3,width=30,bg="pink")
            e.grid(row=r,column=c)
            e.insert(END,j)
            c=c+1
        r=r+1
    show3.mainloop()
    
#********************************FINE TO BE PAID*********************************************************
def read3():
	i2=e2.get()
	q1=s1.get()
	cur.execute("SELECT FINE FROM USERS WHERE USER_ID={}".format(i2))
	record=cur.fetchall()
	for i in record:
		r,=i
		if int(q1)==r:
			l1=tkinter.Label(show4,text="USER_ID::"+i2+ "FINE PAID",font=("Arial",30,"bold"),bg="Orange")
			l1.place(x=0,y=300)
			cur.execute("UPDATE USERS SET FINE='{}' WHERE USER_ID={}".format(0,i2))
			con.commit()
		else:
			l1=tkinter.Label(show4,text="ENTERED AMOUNT IS WRONG", font=("Arial",20,"bold"),bg="Orange")
			l1.place(x=0,y=300)
			l1=tkinter.Label(show4,text="TO PAY Rs."+str(r),font=("Arial",20,"bold"),bg="Orange")
			l1.place(x=0,y=350)
def fine():
   global s1,show4
   show4=tkinter.Tk()
   show4.geometry("800x400")
   show4.configure(bg="Orange")
   l1=tkinter.Label(show4,text="PAY FINE", font=("Arial",40,"bold"),bg="Orange")
   l1.place(x=100,y=0)
   l2=tkinter.Label(show4,text="AMOUNT", font=("Arial",20,"bold"),bg="Orange")
   l2.place(x=0,y=100)
   s1=tkinter.Entry(show4,width=10,font=("Arial",20,"bold"))
   s1.place(x=150,y=100)
   b=tkinter.Button(show4,text="PAY", font=("Arial",30,"bold"),bg="red",command=read3)
   b.place(x=150,y=200)
    
    
def check():
 i1=e1.get()
 i2=e2.get()
 if (i1) in d.keys() and (i2) in d[i1]:
		b2=tkinter.Button(wind, text="ISSUE BOOK", font=("Arial",30,"bold"),bg="Pink",command=issue)
		b2.place(x=100,y=400)
		b3=tkinter.Button(wind,text="RETURN BOOK", font=("Arial",30,"bold"),bg="Pink", command=returnn)
		b3.place(x=500,y=400)
		b4=tkinter.Button(wind,text="VIEW BOOK", font=("Arial",30,"bold"),bg="Pink", command=view)
		b4.place(x=100,y=500)
		b5=tkinter.Button(wind,text="PAY FINE", font=("Arial",30,"bold"),bg="Pink", command=fine)
		b5.place(x=500,y=500)
 else:
		k1=tkinter.Label(wind,text="LOGIN UNSUCCESSFUL",font=("Arial",50,"bold"))
		k1.place(x=100,y=500)
choice=input('ARE YOU A NEW USER? Y/N ')
if choice=='Y':
    x=input('ENTER NEW USER ID:')
    y=input('ENTER NEW USER NAME:')
    sql = "INSERT INTO USERS VALUES(%s,%s,'00-00-00','00-00-00',0)"
    val = (x,y)
    cur.execute(sql,val)
    con.commit()
elif choice=="N":
    wind=tkinter.Tk()
    wind.configure(bg="Yellow")
    l1=tkinter.Label(wind,text="WELCOME TO THE LIBRARY",font=("Arial",40,"bold"),bg="Yellow")
    l1.place(x=50,y=0)
    l2=tkinter.Label(wind,text="USER NAME",font=("Arial",20,"bold"),bg="Yellow")
    l2.place(x=10,y=100)
    e1=tkinter.Entry(wind,width=40,font=("Arial",20,"bold"),bg="Yellow")
    e1.place(x=200,y=100)
    l3=tkinter.Label(wind,text="USER_ID",font=("Arial",20,"bold"),bg="Yellow")
    l3.place(x=10,y=200)
    e2=tkinter.Entry(wind,width=20,font=("Arial",20,"bold"))
    e2.place(x=200,y=200)
    b1=tkinter.Button(wind,text="SUBMIT",font=("Arial",20,"bold"),bg="Red",command=check)
    b1.place(x=400,y=300)
    root=Tk()
    root.mainloop()
















    
        
