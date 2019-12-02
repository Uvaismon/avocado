from tkinter import *
from tkinter import filedialog
from functools import partial

menuwindow=Tk()
menuwindow.geometry('800x500')


class Authenticate:
    def init():
        login=Tk()
        login.geometry('300x300')
        user=Label(login,text="User name")
        passcode=Label(login,text="Passcode ")
        u=Entry(login)
        p=Entry(login)
        passer=partial(Authenticate.GetCredentials,u,p,login)
        l=Button(login,text="Log in",command=passer)
        user.grid(row=0,column=0)
        u.grid(row=0,column=1)
        passcode.grid(row=1,column=0)
        p.grid(row=1,column=1)
        l.grid(row=4,column=0)
        login.mainloop()

    def GetCredentials(u,p,login):
        global Cred
        Cred=[u.get(),p.get()]
        login.destroy()
        try:
            if(int(Cred[1])>9999):
                mes=Tk()
                msg=Label(mes,text="Passcode should contain only 4 digits")
                mok=Button(mes,text='Close',command=mes.destroy)
                msg.grid(row=0,column=0)
                mok.grid(row=1,column=0)
                return
        except:
            mes=Tk()
            msg=Label(mes,text="Passcode should contain only digits")
            mok=Button(mes,text='Close',command=mes.destroy)
            msg.grid(row=0,column=0)
            mok.grid(row=1,column=0)
            return
        EncryptButton.config(state='active')
        DecryptButton.config(state='active')

    def gen(uname):
        global Cred
        pcode=int(Cred[1])
        file=open('temp.txt','w')
        file.write(uname)
        file.close()
        file=open('temp.txt','rb')
        uname2=file.read()
        file.close()
        uname2=bytearray(uname2)
        KEY1=pcode//100
        for i,value in enumerate(uname2):
            uname2[i]=value^KEY1
        KEY2=pcode%100
        if KEY1==KEY2:
            KEY2+=1
        for i,value in enumerate(uname2):
            uname2[i]=value^KEY2
        uname2[::-1]
        file=open('temp.txt','wb')
        file.write(uname2)
        file.close()
        file=open('temp.txt','r')
        uname3=file.read()
        file.close()
        return uname3
        

class Files:
    def openfile():
        filewindow=Tk()
        filewindow.geometry('0x0')
        filewindow.filename=filedialog.askopenfilename(initialdir="/",title="Select a file")
        filewindow.destroy()
        return filewindow.filename

    def savefile(filename,data):
        file=open(filename,'wb')
        file.write(data)
        file.close()

class cipher:
    global filename
    
    def encrypt():
        global process
        process='E'
        global filename
        filename=Files.openfile()
        if(filename!=''):
            cipher.Key()

    def Key():
        keywindow=Tk()
        k=Label(keywindow,text="Enter the key")
        key=Entry(keywindow)
        passer=partial(cipher.getkey,key,keywindow)
        keybutton=Button(keywindow,text='OK',command=passer)
        k.grid(row=0,column=0)
        key.grid(row=1,column=0)
        keybutton.grid(row=2,column=0)

    def getkey(key,keywindow):
        global process
        KEY=key.get()
        try:
            if(int(KEY)>9999):
                mes=Tk()
                msg=Label(mes,text="Passcode should contain only 4 digits")
                mok=Button(mes,text='Close',command=mes.destroy)
                msg.grid(row=0,column=0)
                mok.grid(row=1,column=0)
                return
        except:
            mes=Tk()
            msg=Label(mes,text="Passcode should contain only digits")
            mok=Button(mes,text='Close',command=mes.destroy)
            msg.grid(row=0,column=0)
            mok.grid(row=1,column=0)
            return
        keywindow.destroy()
        if process=='E':
            cipher.encryptL1(KEY)
        else:
            cipher.decryptL1(KEY)

    def encryptL1(KEY):
        global filename
        global Cred
        file=open(filename,'rb')
        DATA=file.read()
        DATA=bytearray(DATA)
        KEY=int(KEY)
        KEY1=KEY//100
        for i,value in enumerate(DATA):
            DATA[i]=value^KEY1
        KEY2=KEY%100
        if KEY2==KEY1:
            KEY2+=1
        for i,value in enumerate(DATA):
            DATA[i]=value^KEY2
        DATA[::-1]
        fname=Authenticate.gen(Cred[0])
        Files.savefile(filename+'.(enc'+fname+')',DATA)

    def decrypt():
        global process
        process='D'
        global filename
        filename=Files.openfile()
        if(filename==''):
            return
        if('.(enc' in filename):
            cipher.Key()
        else:
            mes=Tk()
            msg=Label(mes,text="This file is not encrypted by Avocado Crypt")
            mok=Button(mes,text='Close',command=mes.destroy)
            msg.grid(row=0,column=0)
            mok.grid(row=1,column=0)

    def decryptL1(KEY):
        global filename
        global Cred
        accessinguser=Cred[0]
        actualfilename=filename[:filename.index('(enc')]
        owner=filename[filename.index('.(enc')+5:-1]
        owner=Authenticate.gen(owner)
        if(owner==accessinguser):
            file=open(filename,'rb')
            DATA=file.read()
            DATA=bytearray(DATA)
            KEY=int(KEY)
            DATA[::-1]
            KEY1=KEY%100
            KEY2=KEY//100
            if(KEY1==KEY2):
                KEY1+=1
            for i,value in enumerate(DATA):
                DATA[i]=value^KEY1
            for i,value in enumerate(DATA):
                DATA[i]=value^KEY2
            Files.savefile(actualfilename,DATA)
        else:
            mes=Tk()
            msg=Label(mes,text='You are not the owner of this file')
            mok=Button(mes,text='Close',command=mes.destroy)
            msg.grid(row=0,column=0)
            mok.grid(row=1,column=0)

welcome=Label(menuwindow,text="Welcome to Avocado Crypt",font=('Times New Roman',24),fg='Red',anchor=CENTER,width=80)
welcome.grid(row=0,column=0)
LogButton=Button(menuwindow,text='LogIn',command=Authenticate.init,height=3,width=8,fg='green')
LogButton.grid(row=1,column=0)
EncryptButton=Button(menuwindow,text='Encrypt',command=cipher.encrypt,state='disabled',height=3,width=8,fg='green')
EncryptButton.grid(row=2,column=0)
DecryptButton=Button(menuwindow,text='Decrypt',command=cipher.decrypt,state='disable',height=3,width=8,fg='green')
DecryptButton.grid(row=3,column=0)
ExitButton=Button(menuwindow,text='Exit',command=menuwindow.destroy,fg='green',height=3,width=8)
ExitButton.grid(row=4,column=0)
        
