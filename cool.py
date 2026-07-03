def write_a_line_of_stars():
    print("\n" + "*" * 50 + "\n")


def print_something_like_hello_world_here():
    print("Hello,world!")


def do_something_here():
    write_a_line_of_stars()
    print_something_like_hello_world_here()
    write_a_line_of_stars()


print(" Oh , that is something really fantasitc")

print("You know what , I want to write something reasonable")

print("Hello, world!")

do_something_here()

x = 1


def make_x_equal_2(x):
    return 2


def make_x_mul_2(x):
    return x * 2


def make_x_move_3(x):
    return x - 3


def do_something_to_x(x):
    x = make_x_equal_2(x)
    x = make_x_move_3(x)
    x = make_x_mul_2(x)
    return x


x = do_something_to_x(x)
print(x)

y = 3.14
z = 2.71


def return_y_x_z(y, z):
    return y * z


print("y * z =  " + str(return_y_x_z(y, z)))


class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
        self.is_finished = False

    def introduce(self):
        print(f"《{self.title}》\nauthor: {self.author} \npages:{self.pages}")

    def read(self, page_read):
        print(f"you read 《{self.title}》 : {page_read} pages")

        if (page_read >= self.pages):
            self.is_finished = True
            print("You are already read this book")
        else:
            remaining = self.pages - page_read
            print(f"Still has {remaining} pages unread")

    def finish(self):
        self.is_finished = True
        print(f"You have already finish read《{self.title}》")


book1 = Book("Pincess", "I", 1006)

book1.introduce()
book1.read(300)
book1.finish()


class Student:
    def __init__(self, score):
        self.score = score


Jack = Student(99)


class Teacher:
    def judge(self, Student):
        print("let me see who you are ")
        if (Student.score > 90):
            print("good boy!")
        elif (Student.score > 70):
            print("Just Okay")
        elif (Student.score > 60):
            print("Not bad")
        else:
            print("Need more practice")


teacher1 = Teacher()
teacher1.judge(Jack)


class AlmostHumanStudent(Student):
    def __init__(self, name, age, hobby, score):
        super().__init__(score)
        self.name = name
        self.age = age
        self.hobby = hobby

    def introduce(self):
        print(f"Hello,every one, my name is {self.name}")
        print(f"My age is {self.age}")
        print(f"My hobby is {self.hobby}")
        print(
            f"Although I do not want to mention my score, but teacher asked, it is : {self.score}")


Jack = AlmostHumanStudent("Jack", 14, "Computer", 59)
teacher1.judge(Jack)


class Educator():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def help_student(Student):
        print(f"I see your name, {Student.name}")
        print(f"I see your hobby ,it is {Student.hobby}")
        print("So you are not just a score")
        print(f"maybe we can start from your hobby: {Student.hobby}")


linus = Educator("linux", 34)
linus.help_student(Jack)
