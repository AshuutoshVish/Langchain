from pydantic import BaseModel, EmailStr
from typing import Optional

class Student(BaseModel):
    name: str = 'Ashutosh'
    age : Optional[int]=None
    email: EmailStr

new_student = {'age' : 22, 'email' :'ashusharma3535@gmail.com'}

student = Student(**new_student)
print(student)