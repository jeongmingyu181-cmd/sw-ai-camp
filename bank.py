import csv

customers = []
accounts = []

class Bank:
    customer_num = 0

    def __init__(self, customer_id, name, phone, email):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email
        Bank.customer_num += 1
    
    def display_info(self):
        print(f"아이디: {self.customer_id}, 이름: {self.name}, 전화번호: {self.phone}, 이메일: {self.email}")

class Account:
    def __init__(self, customer_id, password, balance, fee):
       self.customer_id = customer_id
       self.password = password
       self.balance = balance
       self.fee = fee

    def deposit(self, amount):
        self.balance += amount
        print(f"{amount}원이 입금되었습니다. 현재 잔액: {self.balance}")

    def withdrawal(self, amount):
        if((amount + self.fee) <= self.balance):
            self.balance -= (amount + self.fee)
            print(f"{amount}원을 출금하였습니다. 수수료: {self.fee}")
            print(f"남은 잔액: {self.balance}")
            return 0
        else:
            print("잔액이 부족합니다.")
            return -1

def load_customer(filename):
    f = open(filename, "r", encoding="utf-8-sig")
    reader = csv.reader(f)
    header = next(reader)
    for line in reader:
        customer_id, name, phone, email = line
        customer = Bank(customer_id, name, phone, email)
        customers.append(customer)
    f.close()

def load_account(filename):
    f = open(filename, "r", encoding="utf-8-sig")
    reader = csv.reader(f)
    header = next(reader)
    for line in reader:
        customer_id, password, balance, fee = line
        account = Account(customer_id, int(password), int(balance), int(fee))
        accounts.append(account)
    f.close()
    
def add_customer():
    print("\n새 사용자를 추가합니다.")
    customer_id = "C" + str(Bank.customer_num + 1).zfill(3)
    name = input("이름: ")
    phone = input("전화번호: ")
    email = input("이메일: ")
    for customer in customers:
        if ((customer.name == name) and (customer.phone == phone) and (customer.email == email)):
            print("이미 고객이 존재합니다.\n")
            return -1
    new_customer = Bank(customer_id, name, phone, email)
    customers.append(new_customer)
    print("\n새 사용자가 추가되었습니다!")
    return 0

def save_customer(filename):
    f = open(filename, "w", newline="", encoding="utf-8-sig")
    writer = csv.writer(f)
    writer.writerow(["customer_id", "name", "phone", "email"])
    for m in customers:
        writer.writerow([m.customer_id, m.name, m.phone, m.email])
    print("파일이 업데이트 되었습니다.\n")
    f.close()

def add_account():
    a = input("이름: ")
    b = input("전화번호: ")
    customer_id = find_account(a, b)
    if(customer_id == 0):
        print("\n고객을 찾을 수 없습니다.\n")
        return -1
    for account in accounts:
        if account.customer_id == customer_id:
            print("\n이미 계좌가 존재합니다. 한 고객당 계좌는 하나만 생성할 수 있습니다.\n")
            return -1
    print("\n새 계좌를 추가합니다.\n")
    password = int(input("계좌 비밀번호: "))
    balance = int(input("초기 입금액: "))
    fee = 0
    new_account = Account(customer_id, password, balance, fee)
    accounts.append(new_account)
    print("\n새 계좌가 추가되었습니다!\n")
    return 0

def save_account(filename):
    f = open(filename, "w", newline="", encoding="utf-8-sig")
    writer = csv.writer(f)
    writer.writerow(["customer_id", "password", "balance", "fee"])
    for m in accounts:
        writer.writerow([m.customer_id, m.password, m.balance, m.fee])
    print("파일이 업데이트 되었습니다.\n")
    f.close()

def find_account(name, phone):
    for customer in customers:
        if((customer.name == name) and (customer.phone == phone)):
            return customer.customer_id
    return 0

def deposit():
    name = input("이름: ")
    phone = input("전화번호: ")
    customer_id = find_account(name, phone)
    if(customer_id == 0):
        print("고객을 찾을 수 없습니다.\n")
        return -1
    for account in accounts:
        if(account.customer_id == customer_id):
            a = int(input("비밀번호: "))
            if(a == account.password):
                amount = int(input("입금할 금액: "))
                account.deposit(amount)
                save_account("accounts.csv")
                return account
            else:
                print("\n비밀번호가 틀렸습니다.\n")
                return -1
    print("\n해당 고객의 계좌가 존재하지 않습니다.\n")
    return -1

def withdrawal():
    name = input("이름: ")
    phone = input("전화번호: ")
    customer_id = find_account(name, phone)
    if(customer_id == 0):
        print("\n고객을 찾을 수 없습니다.\n")
        return -1
    for account in accounts:
        if(account.customer_id == customer_id):
            a = int(input("비밀번호: "))
            if(a == account.password):
                amount = int(input("출금할 금액: "))
                result = account.withdrawal(amount)
                if(result != -1):
                    save_account("accounts.csv")
                    return account
                return -1
            else:
                print("\n비밀번호가 틀렸습니다.\n")
                return -1
    print("\n해당 고객의 계좌가 존재하지 않습니다.\n")
    return -1


load_customer("customer.csv")
load_account("accounts.csv")

while True:
    a = input("무엇을 실행하시겠습니까?\n1. 고객추가\n2. 계좌생성\n3. 입금\n4. 출금\n5. 종료\n")
    if(a == "고객추가"):
        result = add_customer()
        if(result != -1):
            save_customer("customer.csv")
    elif(a == "계좌생성"):
        result = add_account()
        if(result != -1):
            save_account("accounts.csv")
    elif(a == "입금"):
        deposit()
    elif(a == "출금"):
        withdrawal()
    elif(a == "종료"):
        break