import csv
from datetime import datetime

customers = []
accounts = []
loans = []

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
        if (amount + self.fee) <= self.balance:
            self.balance -= (amount + self.fee)
            print(f"{amount}원을 출금하였습니다. 수수료: {self.fee}")
            print(f"남은 잔액: {self.balance}")
            return 0
        else:
            print("잔액이 부족합니다.")
            return -1

class Loan:
    def __init__(self, customer_id, loan_amount, interest_rate, start_date=None, accrued_interest=0):
        self.customer_id = customer_id
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.accrued_interest = accrued_interest
        if start_date:
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        else:
            self.start_date = datetime.now()

    def calculate_amount_due(self):
        today = datetime.now()
        days_passed = (today - self.start_date).days
        interest = self.loan_amount * (self.interest_rate / 100) * (days_passed / 365)
        total_due = self.loan_amount + interest + self.accrued_interest
        return total_due, interest + self.accrued_interest

def load_customer(filename):
    with open(filename, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            customer_id, name, phone, email = line
            customers.append(Bank(customer_id, name, phone, email))

def save_customer(filename):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["customer_id", "name", "phone", "email"])
        for m in customers:
            writer.writerow([m.customer_id, m.name, m.phone, m.email])
    print("파일이 업데이트 되었습니다.\n")

def load_account(filename):
    with open(filename, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            customer_id, password, balance, fee = line
            accounts.append(Account(customer_id, int(password), int(balance), int(fee)))

def save_account(filename):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["customer_id", "password", "balance", "fee"])
        for m in accounts:
            writer.writerow([m.customer_id, m.password, m.balance, m.fee])
    print("파일이 업데이트 되었습니다.\n")

def load_loans(filename):
    with open(filename, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            customer_id, loan_amount, interest_rate, start_date, accrued_interest = line
            loans.append(Loan(customer_id, int(loan_amount), float(interest_rate), start_date, float(accrued_interest)))

def save_loans(filename):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["customer_id", "loan_amount", "interest_rate", "start_date", "accrued_interest"])
        for m in loans:
            writer.writerow([m.customer_id, m.loan_amount, m.interest_rate, m.start_date.strftime("%Y-%m-%d"), m.accrued_interest])
    print("파일이 업데이트 되었습니다.\n")

def find_account(name, phone):
    for customer in customers:
        if customer.name == name and customer.phone == phone:
            return customer.customer_id
    return 0

def add_customer():
    print("\n새 사용자를 추가합니다.")
    customer_id = "C" + str(Bank.customer_num + 1).zfill(3)
    name = input("이름: ")
    phone = input("전화번호: ")
    email = input("이메일: ")
    for customer in customers:
        if customer.name == name and customer.phone == phone and customer.email == email:
            print("이미 고객이 존재합니다.\n")
            return -1
    customers.append(Bank(customer_id, name, phone, email))
    print("\n새 사용자가 추가되었습니다!")
    return 0

def add_account():
    name = input("이름: ")
    phone = input("전화번호: ")
    customer_id = find_account(name, phone)
    if customer_id == 0:
        print("\n고객을 찾을 수 없습니다.\n")
        return -1
    for account in accounts:
        if account.customer_id == customer_id:
            print("\n이미 계좌가 존재합니다.\n")
            return -1
    password = int(input("계좌 비밀번호: "))
    balance = int(input("초기 입금액: "))
    fee = 0
    accounts.append(Account(customer_id, password, balance, fee))
    print("\n새 계좌가 추가되었습니다!\n")
    return 0

def deposit():
    name = input("이름: ")
    phone = input("전화번호: ")
    customer_id = find_account(name, phone)
    if customer_id == 0:
        print("고객을 찾을 수 없습니다.\n")
        return -1
    for account in accounts:
        if account.customer_id == customer_id:
            pw = int(input("비밀번호: "))
            if pw == account.password:
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
    if customer_id == 0:
        print("\n고객을 찾을 수 없습니다.\n")
        return -1
    for account in accounts:
        if account.customer_id == customer_id:
            pw = int(input("비밀번호: "))
            if pw == account.password:
                amount = int(input("출금할 금액: "))
                result = account.withdrawal(amount)
                if result != -1:
                    save_account("accounts.csv")
                    return account
                return -1
            else:
                print("\n비밀번호가 틀렸습니다.\n")
                return -1
    print("\n해당 고객의 계좌가 존재하지 않습니다.\n")
    return -1

def add_loan():
    name = input("이름: ")
    phone = input("전화번호: ")
    customer_id = find_account(name, phone)
    if customer_id == 0:
        print("\n고객을 찾을 수 없습니다.\n")
        return -1
    for loan in loans:
        if loan.customer_id == customer_id and loan.loan_amount > 0:
            print("\n이미 대출이 있습니다. 먼저 갚고 빌리세요.\n")
            return -1
    for account in accounts:
        if account.customer_id == customer_id:
            pw = int(input("비밀번호: "))
            if pw == account.password:
                loan_amount = int(input("대출 금액: "))
                interest_rate = float(input("연 이자율(%): "))
                new_loan = Loan(customer_id, loan_amount, interest_rate)
                loans.append(new_loan)
                print(f"\n대출이 등록되었습니다. 대출일: {new_loan.start_date.strftime('%Y-%m-%d')}\n")
                return new_loan
            else:
                print("\n비밀번호가 틀렸습니다.\n")
                return -1
    print("\n해당 고객의 계좌가 존재하지 않습니다.\n")
    return -1

def check_loan():
    name = input("이름: ")
    phone = input("전화번호: ")
    customer_id = find_account(name, phone)
    if customer_id == 0:
        print("\n고객을 찾을 수 없습니다.\n")
        return -1   
    for account in accounts:
        if account.customer_id == customer_id:
            pw = int(input("비밀번호: "))
            if pw == account.password:
                found = False
                for loan in loans:
                    if loan.customer_id == customer_id:
                        total_due, interest = loan.calculate_amount_due()
                        print(f"\n원금: {loan.loan_amount}원, 이자: {interest:.2f}원, 상환해야 할 금액: {total_due:.2f}원")
                        print(f"대출일: {loan.start_date.strftime('%Y-%m-%d')}\n")
                        found = True
                if not found:
                    print("\n해당 고객의 대출이 없습니다.\n")
                return 0
            else:
                print("\n비밀번호가 틀렸습니다.\n")
                return -1
    print("\n해당 고객의 계좌가 존재하지 않습니다.\n")
    return -1

def loan_repay():
    name = input("이름: ")
    phone = input("전화번호: ")
    customer_id = find_account(name, phone)
    if customer_id == 0:
        print("\n고객을 찾을 수 없습니다.\n")
        return -1

    loan_to_repay = None
    for loan in loans:
        if loan.customer_id == customer_id:
            loan_to_repay = loan
            break
    if loan_to_repay is None:
        print("\n해당 고객의 대출이 없습니다.\n")
        return -1

    for account in accounts:
        if account.customer_id == customer_id:
            pw = int(input("비밀번호: "))
            if pw != account.password:
                print("\n비밀번호가 틀렸습니다.\n")
                return -1

            total_due, interest = loan_to_repay.calculate_amount_due()
            print(f"\n현재 상환해야 할 금액: {total_due:.2f}원 (원금: {loan_to_repay.loan_amount}원, 이자: {interest:.2f}원)")

            amount = int(input("출금할 금액: "))
            if amount + account.fee > account.balance:
                print("\n잔액이 부족합니다.\n")
                return -1

            account.withdrawal(amount)

            if amount >= interest:
                principal_paid = min(amount - interest, loan_to_repay.loan_amount)
                loan_to_repay.loan_amount -= principal_paid
                loan_to_repay.accrued_interest = 0
            else:
                loan_to_repay.accrued_interest = interest - amount
                principal_paid = 0

            loan_to_repay.start_date = datetime.now()

            print(f"\n이자 상환: {min(amount, interest):.2f}원, 원금 상환: {principal_paid:.2f}원")
            print(f"남은 대출 원금: {loan_to_repay.loan_amount}원, 다음 이자 계산 기준일: {loan_to_repay.start_date.strftime('%Y-%m-%d')}\n")

            save_account("accounts.csv")
            save_loans("loans.csv")
            return 0

    print("\n해당 고객의 계좌가 존재하지 않습니다.\n")
    return -1

load_customer("customer.csv")
load_account("accounts.csv")
load_loans("loans.csv")

while True:
    a = input("무엇을 실행하시겠습니까?\n1. 고객추가\n2. 계좌생성\n3. 입금\n4. 출금\n5. 대출등록\n6. 대출확인\n7. 대출상환\n8. 종료\n")
    if a == "고객추가":
        result = add_customer()
        if result != -1:
            save_customer("customer.csv")
    elif a == "계좌생성":
        result = add_account()
        if result != -1:
            save_account("accounts.csv")
    elif a == "입금":
        deposit()
    elif a == "출금":
        withdrawal()
    elif a == "대출등록":
        result = add_loan()
        if result != -1:
            save_loans("loans.csv")
    elif a == "대출확인":
        check_loan()
    elif a == "대출상환":
        loan_repay()
    elif a == "종료":
        break
