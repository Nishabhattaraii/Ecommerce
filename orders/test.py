class Book:
    total_books = 0

    def __init__(self,title):
        self.title=title
        Book.total_books +=1 
        

obj1 =Book('Electrical Machine')
obj2 = Book('Physics')
obj3 = Book('Electromagnetics')

print(Book.total_books)