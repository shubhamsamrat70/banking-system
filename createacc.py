import mysql.connector as m
import random 
from datetime import datetime, date,time

conn = m.connect(
            host="localhost",
            user="root",
            password="root",
            database="customer")

class BankingSystem:    

    def add_record(self):
        if conn.is_connected():
            cur = conn.cursor()
            n = input("Enter Your Name: ")
            mn = int(input("Enter Your Mobile No: "))
            e = input("Enter Your Email: ")
            a = input("Enter Your Address: ")
            ad = int(input("Enter Your Adhar No: "))
            ac = input("Enter Your Account Type: ")
            idp = int(input("Enter Your Initial Deposit: "))
            pc = int(input("Enter Your Pin: "))
            query = '''
            INSERT INTO CreateAcc
            (AccountNo,Name, Mobile_Number, Email, Address, AdharNO, AccountType, InitialDeposite, PinCreation)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            acNo = random.randint(10000000,99999999)
            values = (acNo,n, mn, e, a, ad, ac, idp, pc)
            cur.execute(query, values)
            q="select *from CreateAcc" 
            cur.execute(q)
            records=cur.fetchall()
            data=records[-1]
            print(f"Your Account No is:{data[0]} and Pin is: {data[8]}")
            conn.commit()
            print("Record Added Successfully")

    def Login_User(self):
        if conn.is_connected():
            cur = conn.cursor()
            self.acNo=int(input("Enter your Account No:"))
            self.pin=int(input("Enter your pin:"))
            q="select * from createacc"
            cur.execute(q)
            records = cur.fetchall()
            for rec in records:
                if self.acNo==rec[0] and rec[8]==self.pin:
                    print("Login Successfull")
                    print(f"Welcome {rec[1]}")
                    print("================================================")
                    print("Please Choose Any Option:")

            while True:
                        print("1.Deposite Money")
                        print("2.Withdraw Money")
                        print("3.Balance Enqueiry")
                        print("4.Fund Transfer")
                        print("5.Transaction History")
                        print("6. Update Account")
                        print("7. Delete Account")
                        print("8. Logout")
                        print("9. Exit")
                        ch=int(input("Enter Your Coise:"))
                        if ch==1:
                            self.Deposite_Money()
                        elif ch==2:
                            self.Withdraw_Money()
                        elif ch==3:
                            self.Balance_Enquiry()
                        elif ch==4:
                            self.Fund_Transfer()
                        elif ch==5:
                            self.Transaction_history()
                        elif ch==6:
                            self.Update_Account()
                        elif ch==7:
                            self.Delete_Account()
                        elif ch==8:
                            print("Logout Successfull...!!")
                            break
                        elif ch==9:
                            break
                        else:
                            print("Wrong Choise")

    def Deposite_Money(self):
        flag = False
        if conn.is_connected():
            cur=conn.cursor()
            a=int(input("Enter Your Account Number:"))
            p=int(input("Enter Your Pin:"))
            q="select *from createacc"
            cur.execute(q)
            record = cur.fetchall()
            for rec in record:
                if rec[0]==a and rec[8]==p:
                    flag = True
                    amt=int(input("Enter Amount to Deposit:"))
                    new_bal=rec[7]+amt
                    # print(rec[7])
                    cur=conn.cursor()
                    query="update createacc set InitialDeposite=%s where AccountNo=%s"
                    values=(new_bal, a)
                    cur.execute(query,values)
                    print("Deposite Successfully")
                    print("Your Balance: ",new_bal)
                    conn.commit()
                    if flag:
                        cur=conn.cursor()
                        tid = random.randint(10000000,99999999)
                        ttype="Deposit"
                        today = datetime.now()
                        query="insert into transactions (tid, accountNo, ttype, amount, tdate) values(%s, %s, %s, %s, %s)"
                        values = (tid, a, ttype, amt, today)
                        cur.execute(query, values)
                        conn.commit()
                        print("Updated Succcessfully!!!")
            if not flag:
                print("Invalid Account No or Pin")

    def Withdraw_Money(self):
        flag = False
        if conn.is_connected():
            cur=conn.cursor()
            a=int(input("Enter Your Account Number:"))
            p=int(input("Enter Your Pin:"))
            q="select *from createacc"
            cur.execute(q)
            record = cur.fetchall()
            for rec in record:
                if rec[0]==a and rec[8]==p:
                    flag = True
                    amt=int(input("Enter Amount to Withdraw:"))
                    new_bal=rec[7]-amt
                    # print(rec[7])
                    cur=conn.cursor()
                    query="update createacc set InitialDeposite=%s where AccountNo=%s"
                    values=(new_bal, a)
                    cur.execute(query,values)
                    print("Withdraw Successfully")
                    print("your Balance: ",new_bal)
                    conn.commit()
                    if flag:
                        cur=conn.cursor()
                        tid = random.randint(10000000,99999999)
                        ttype="Withdraw"
                        today = datetime.now()
                        query="insert into transactions (tid, accountNo, ttype, amount, tdate) values(%s, %s, %s, %s, %s)"
                        values = (tid, a, ttype, amt, today)
                        cur.execute(query, values)
                        conn.commit()
                        print("Updated Succcessfully!!!")
            if not flag:
                print("Invalid Account No or Pin")
    
    def Balance_Enquiry(self):
        if conn.is_connected():
            cur=conn.cursor()
            ac=int(input("Enter Your Account No:"))
            q="select *from createacc"
            cur.execute(q)
            record = cur.fetchall()
            for rec in record:
                if rec[0]==ac:
                    print("Account Number: ",rec[0])
                    print("Name: Mr.",rec[1])
                    print("Your Balance: ",rec[7])
                        
    def Fund_Transfer(self):
        print("============================ Fund Transfer ==========================")
        sender_acNo=int(input("Enter Your Account No:"))
        receiver_acN=int(input("Enter Receiver's Account No:"))
        amount=int(input("Enter Amount to transfer:"))
        flag=False
        if conn.is_connected():
            cur=conn.cursor()
            q="select *from createacc"
            cur.execute(q)
            data=cur.fetchall()
            sender_data=None
            receiver_data=None
            for rec in data:
                if rec[0] == sender_acNo:
                    sender_data = rec
                if rec[0] == receiver_acN:
                    receiver_data = rec
                flag = True
            if sender_data == None:
                print("Invalid Sender Account No:")
                return
            if receiver_data == None:
                print("Invalid Receiver Account No:")
                return
            if amount > sender_data[7]:
                print("Insufficient Balance:")
                return
            send_balance = sender_data[7] - amount
            new_balance = receiver_data[7] + amount
            update_sender_query = "update createacc set InitialDeposite=%s where AccountNo=%s"
            update_receiver_query= "update createacc set InitialDeposite=%s where AccountNo=%s"
            cur.execute(update_sender_query,(send_balance,sender_acNo))
            cur.execute(update_receiver_query,(new_balance,receiver_acN))
            conn.commit()
            if flag:
                t_id = random.randint(1000000,9999999)
                t_date = datetime.now()
                t_query = "insert into transfer_history(tid,sender_acc,receiver_acc,amount,transfer_date) values(%s,%s,%s,%s,%s)"
                t_val = (t_id,sender_acNo,receiver_acN,amount,t_date)
                cur.execute(t_query,t_val)
                conn.commit()
            print("Amount Transfered Successfully...!")
            print("Amount",amount)
            print("To Amount No",receiver_acN)
        print("===================================================================")

    def Transaction_history(self):
        print("view Your Transactions")
        Acc_No = int(input("Enter Your Account No:"))
        flag=False
        if conn.is_connected():
            cur=conn.cursor()
            q="select *from transactions"
            cur.execute(q)
            data=cur.fetchall()
            for rec in data:
                if rec[1] == Acc_No:
                     while True:
                        print("1.View All Transaction:")
                        print("2.Deposite History:")
                        print("3.Withdraw History:")
                        print("4.Transfer History:")
                        print("5.Exit:")
                        ch=int(input("Enter Your Choise:"))
                        if ch==1:
                            qu="select *from transactions where accountNo=%s"
                            val = (Acc_No,)
                            cur.execute(qu,val)
                            td = cur.fetchall()
                            for i in td:
                                print(i)
                        elif ch==2:
                            qu="select * from transactions where accountNo=%s"
                            val = (Acc_No,)
                            cur.execute(qu,val)
                            td = cur.fetchall()
                            for i in td:
                                if i[2] == "Deposit":
                                    print(i)  
                        elif ch==3:
                            qu="select * from transactions where accountNo=%s"
                            val = (Acc_No,)
                            cur.execute(qu,val)
                            td = cur.fetchall()
                            for i in td:
                                if i[2] == "Withdraw":
                                    print(i)     
                        elif ch==4:
                            qu="select *from transfer_history where sender_acc=%s"
                            val = (Acc_No,)
                            cur.execute(qu,val)
                            td = cur.fetchall()
                            for i in td:
                                print(i)
                        elif ch==5:
                            return
                        else:
                            print("invalid choise:")

    def Update_Account(self):
        print("Update Your Account:")
        if conn.is_connected():
            cur = conn.cursor()
            acNo=int(input("Enter your Account No:"))
            q="select * from createacc"
            cur.execute(q)
            records = cur.fetchall()
            for rec in records:
                if rec[0] == acNo:
                    while True:
                        print("What do you Want to Update:")
                        print("1.Update Mobile:")
                        print("2.Update Email:")
                        print("3.Update Address:")
                        print("4.Change Pin:")
                        print("5.Exit")
                        ch=int(input("Enter Your Choise:"))
                        if ch==1:
                            NM=int(input("Enter New Mobile Number:"))
                            q="update createacc set Mobile_Number=%s where AccountNo=%s"
                            val = (NM,acNo)
                            cur.execute(q,val)
                            conn.commit()
                            print("Mobile Numeber Updated...!! ")
                            break
                        elif ch==2:
                            NE=input("Enter New Email:")
                            q="update createacc set Email=%s where AccountNo=%s"
                            val = (NE,acNo)
                            cur.execute(q,val)
                            conn.commit()
                            print("Email Updated...!! ")
                            break
                        elif ch==3:
                            NE=input("Enter New Address:")
                            q="update createacc set Address=%s where AccountNo=%s"
                            val = (NE,acNo)
                            cur.execute(q,val)
                            conn.commit()
                            print("Address Updated...!! ")
                            break
                        elif ch==4:
                            NP=input("Enter New Pin:")
                            q="update createacc set PinCreation=%s where AccountNo=%s"
                            val = (NP,acNo)
                            cur.execute(q,val)
                            conn.commit()
                            print("Pin Updated...!! ")
                            break
                        else:
                            print("Invalid Choise:")
            else:
                print("Invalid Account No Or Pin...!!")

    def Delete_Account(self):
        
        if conn.is_connected():
            cur = conn.cursor()
            acNo=int(input("Enter your Account No:"))
            q="select * from createacc"
            cur.execute(q)
            records = cur.fetchall()
            for rec in records:
                if rec[0] == acNo:
                    query="DELETE FROM createacc WHERE AccountNo = %s;"
                    value=(acNo,)
                    cur.execute(query,value)
                    conn.commit()
                    print("Account Deleted:")
                    break

    def Login_Admin(self):
        if conn.is_connected():
            count = 0
            while count < 3:
                Uname = input("Enter Your Username: ")
                PassWord = int(input("Enter Your Password: "))
                if Uname == "Admin@123" and PassWord == 5544:
                    print("Login Successful")
                    while True:
                        print("-------ADMIN PANEL-------")
                        print("1.View All Customers")
                        print("2.Search Customers")
                        print("3.Total Bank Balance")
                        print("4.Total Customers")
                        print("5.Richest Customers")
                        print("6.Daily Transactions Report")
                        print("7.Delete Customer Account")
                        print("8.Logout")
                        ch = int(input("Enter Choice: "))
                        if ch == 1:
                            cur = conn.cursor()
                            q = "SELECT * FROM createacc"
                            cur.execute(q)
                            records = cur.fetchall()
                            for rec in records:
                                print(f"Account No: {rec[0]}")
                                print(f"Name: {rec[1]}")
                                print(f"Mobile No: {rec[2]}")
                                print(f"Email: {rec[3]}")
                                print(f"Address: {rec[4]}")
                                print(f"AdharNo: {rec[5]}")
                                print(f"AccountType: {rec[6]}")
                                print(f"InitialDeposite: {rec[7]}")
                                print(f"Pin: {rec[8]}")
                                print("-" * 30)
                        elif ch==2:
                            obj.Search_Customer()
                        elif ch==3:
                            obj.Total_Bank_Balance()
                        elif ch==4:
                            obj.Total_Customers()
                        elif ch==5:
                            obj.Richest_Customer()
                        elif ch==6:
                            obj.Daily_Transactions_Report()
                        elif ch==7:
                            obj.Delete_Customer_Account()
                        elif ch==8:
                            print("Logout Successfull...!!")
                            return

                else:
                    count += 1
                    print("Invalid Username Or Password")
            print("Limit Exceeded")

    def Search_Customer(self):
        print("============Search Customer===========")
        acNo = int(input("Enter Account Number to Search...!!"))
        cur = conn.cursor()
        q = "select * from createacc"
        cur.execute(q)
        data = cur.fetchall()
        for i in data:           
           if i[0] == acNo:
               print(i)

    def Total_Bank_Balance(self):
        print("=============Total Balance===========")
        cur = conn.cursor()
        q = "select *from createacc"
        cur.execute(q)
        data = cur.fetchall()
        total_balance = sum(x[7] for x in data)
        print(f"Total Bank Balance is:{total_balance}")

    def Total_Customers(self):
        print("===============Total Customer===============")
        cur = conn.cursor()
        q = "select *from createacc"
        cur.execute(q)
        data = cur.fetchall()
        total_Customers = (len(data))
        print(f"Total_Customers is:{total_Customers}")

    def Richest_Customer(self):
        print("==============Richest Customer==============")
        cur = conn.cursor()
        q = "select *from createacc"
        cur.execute(q)
        data = cur.fetchall()
        Rich = 0
        for x in data:
            if x[7] > Rich:
                Rich = x[7]
        print(f"Richest Customer is {x[1]} {Rich}")

    def Daily_Transactions_Report(self):
        print("===========DAILY TRANSACTION REPORT===========")
        cur = conn.cursor()
        q = "select *from transactions"
        cur.execute(q)
        data = cur.fetchall()         
        today = date.today()
        filen = f"TransactionReport_{today.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open (filen,"w") as f:
            for rec in data:
                if rec[4]==today:
                    f.write(str(rec)+"\n")

        print("Transaction Report Generated....!!")

    def Delete_Customer_Account(self):
        cur = conn.cursor()
        acNo=int(input("Enter your Account No:"))
        q="select * from createacc"
        cur.execute(q)
        records = cur.fetchall()
        for rec in records:              
              if rec[0] == acNo:
                    query="DELETE FROM createacc WHERE AccountNo = %s;"
                    value=(acNo,)
                    cur.execute(query,value)
                    conn.commit()
                    print("Account Deleted:")
                    break
                                          
obj = BankingSystem()

while True:

    print("\n===== Welcome To BANKING SYSTEM =====")
    print("1. Create Your Account")
    print("2. Login Customer")
    print("3. Login Admin")
    print("4. Exit")

    ch = int(input("Enter Your Choice: "))
    if ch == 1:
        obj.add_record()
    elif ch == 2:
        obj.Login_User()
    elif ch == 3:
        obj.Login_Admin()
    elif ch == 4:
        print("Thank You")
        break

    else:
        print("Invalid Choice")





