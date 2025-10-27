class Dog:
    count = 0

    def __init__(self, name):
        self.name = name
        Dog.count += 1

    def bark(self):
        print(f"{self.name}가 \"월! 월!\"")

    @classmethod
    def show_count(cls):
        print(f"현재 강아지의 수: {cls.count}")

    @staticmethod
    def sound():
        print("개소리 남")

dog1 = Dog("정준우")
dog2 = Dog("이동영")

Dog.show_count()
dog1.bark()
Dog.sound()