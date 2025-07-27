from pydantic import BaseModel

class ContactBase(BaseModel):
    name: str
    company: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    mobile_phone: str | None = None

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True
