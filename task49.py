"""
Задача №49. Решение в группах
Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной
"""
from dataclasses import dataclass
import os

KEYS = ("name", "surname", "lastname", "phone_number")


class MyInt:
    def __init__(self, value, control=None):
        if control is None:
            control = -float('inf')
        self.value = float('inf')
        try:
            self.value = int(value)
        except ValueError:
            print("Вы ввели не число")
        else:
            if self.value > control:
                self.value = float('inf')
                print("Нет такого контакта")


@dataclass
class Contact:
    name: str
    surname: str
    lastname: str
    phone_number: str

    def values(self) -> list:
        return [self.name, self.surname, self.lastname, self.phone_number]

    def __setitem__(self, item, value):
        setattr(self, item, value)

    def __str__(self) -> str:
        return (
                self.name
                + " "
                + self.surname
                + " "
                + self.lastname
                + " "
                + self.phone_number
        )


@dataclass
class PhoneBook:
    contacts: list[Contact]

    def search_contact(self, search_string: str) -> list:
        search_list = [str(contact) for contact in self.contacts]
        # print(search_list)
        result = [
            index
            for index, contact in enumerate(search_list)
            if search_string in contact
        ]
        return [self.contacts[index] for index in result]


class ImportPhoneBook:
    def __init__(self, file_name) -> None:
        self.file_name = file_name

    def import_from_file(self):
        with open(self.file_name, encoding="utf-8") as file:
            return file.readlines()


class ExportPhoneBook:
    def __init__(self, file_name, phone_book, format_data) -> None:
        self.file_name = file_name
        self.phone_book = phone_book
        self.format_data = format_data

    def export_to_file(self):
        with open(self.file_name, "w", encoding="utf-8") as file:
            print(self.phone_book.contacts)
            lst = [contact.values() for contact in self.phone_book.contacts]
            data = self.format_data(lst)
            file.writelines(data)


class FormatData:
    def __call__(self, *args: any, **kwds: any) -> list:
        phone_book = args[0]
        if len(args) == 1:
            data = [",".join(contact) + "\n" for contact in phone_book]
        else:
            data = ','.join(phone_book)
            data += '\n'
        return data


def manual_input(lst: PhoneBook = None) -> PhoneBook:
    print("Введите Имя Отчество Фамилию НомерТелефона через пробел в одну строку")
    print("Для выхода введите quit")
    if not lst:
        lst = []
    else:
        lst = lst.contacts
    phone_book = PhoneBook(lst)
    while (input_string := input("Ваш ввод:")) != "quit":
        phone_book.contacts.append(Contact(*input_string.split()))
    return phone_book


def import_phone(lst=None) -> PhoneBook:
    import_from_txt = ImportPhoneBook("phones.txt").import_from_file()
    # print(import_from_txt)
    import_from_txt = [
        Contact(*contact.strip().split(",")) for contact in import_from_txt
    ]
    phone_book = PhoneBook(import_from_txt)
    return phone_book


def search_contact(phone_book: PhoneBook) -> None:
    search_string = input("Введите строку для поиска: ")
    result = PhoneBook(phone_book.search_contact(search_string))
    show_contacts(result)


def export_phones(phone_book: PhoneBook) -> None:
    ExportPhoneBook("phones.txt", phone_book, FormatData()).export_to_file()


def show_contacts(phone_book: PhoneBook, pause: bool = True) -> None:
    for index, contact in enumerate(phone_book.contacts):
        print(index, ".", *contact.values())
    if pause:
        input("Нажмите ENTER для продолжения...")


def edit_contact(phone_book: PhoneBook) -> None:
    show_contacts(phone_book, False)
    index = MyInt(input("Введите номер контакта, который хотите изменить: "), len(phone_book.contacts))
    if index.value == float('inf'):
        return
    print(*KEYS, sep="\n")
    field = input("Введите поле, которое хотите изменить: ")
    if field in KEYS:
        input_string = input(f"Введите новое значение для {field}: ")
        phone_book.contacts[index.value][field] = input_string
        show_contacts(phone_book)
    else:
        print("Не правильно введено имя поля!!!")


def delete_contact(phone_book: PhoneBook) -> None:
    show_contacts(phone_book, False)
    index = MyInt(input("Введите номер контакта, который хотите удалить: "), len(phone_book.contacts))
    if index.value == float('inf'):
        return
    phone_book.contacts.pop(index.value)


def copy_to_another_file(phone_book: PhoneBook) -> None:
    show_contacts(phone_book, False)
    number_string = MyInt(input("Введите номер строки для копирования: "), len(phone_book.contacts))
    if number_string.value == float('inf'):
        return
    new_file_name = input("Введите имя нового файла: ")
    flag = 'a'
    format_data = FormatData()
    if not os.path.exists(new_file_name):
        flag = 'w'
    with open(new_file_name, flag, encoding='utf-8') as file:
        data = format_data(phone_book.contacts[number_string.value].values(), True)
        file.write(data)


def main():
    COMMANDS = {
        "1": manual_input,
        "2": export_phones,
        "3": search_contact,
        "4": import_phone,
        "5": edit_contact,
        "6": delete_contact,
        "7": show_contacts,
        "8": copy_to_another_file
    }
    list_of_commands = """
    1. Ручной ввод телефонного справочника
    2. Экспорт справочника в текстовый файл phones.txt
    3. Найти контакт в справочнике
    4. Импортировать справочник из текстового файла phones.txt
    5. Редактировать контакт
    6. Удалить контакт
    7. Показать все контакты
    8. Скопировать строку из справочника в другой файл
    0. Выход"""
    phone_book = None
    print(list_of_commands)
    while (input_string := input("Введите команду: ")) != "0":
        if input_string in "14":
            phone_book = COMMANDS.get(input_string, "0")(phone_book)
        elif phone_book:
            COMMANDS.get(input_string, "0")(phone_book)
        else:
            print("Справочник пустой!!!")
        print(list_of_commands)


if __name__ == "__main__":
    main()
