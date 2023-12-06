

def choose_action(phonebook):
    while True:
        print('Что вы хотите сделать?')
        print('1 - Импортировать данные\n'
              '2 - Найти контакт\n'
              '3 - Добавить контакт\n'
              '4 - Изменить контакт\n'
              '5 - Удалить контакт\n'
              '6 - Просмотреть все контакты\n'
              '0 - Выйти из приложения\n')

        user_choice = input()

        if user_choice == '1':
            file_to_add = input('Введите название импортируемого файла: ')
            import_data(file_to_add, phonebook)
        elif user_choice == '2':
            find_number(phonebook)
        elif user_choice == '3':
            add_phone_number(phonebook)
        elif user_choice == '4':
            modify_contact(phonebook)
        elif user_choice == '5':
            delete_contact(phonebook)
        elif user_choice == '6':
            show_phonebook(phonebook)
        elif user_choice == '0':
            print('До свидания!')
            break
        else:
            print('Неправильно выбрана команда!\n')

def import_data(file_to_add, phonebook):
    try:
        with open(file_to_add, 'r', encoding='utf-8') as new_contacts, open(phonebook, 'a', encoding='utf-8') as file:
            file.writelines(new_contacts.readlines())
        print(f'Данные из {file_to_add} успешно импортированы.')
    except FileNotFoundError:
        print(f'{file_to_add} не найден.')


def search_parameters():
    print('По какому полю выполнить поиск?')
    print('1 - по фамилии\n2 - по имени\n3 - по номеру телефона\n')

    valid_choices = {'1', '2', '3'}

    while True:
        search_field = input()
        if search_field in valid_choices:
            break
        else:
            print('Некорректный выбор. Пожалуйста, введите 1, 2 или 3.')

    search_value = input(f'Введите {search_field_dict[search_field]} для поиска: ')
    return search_field, search_value

def find_number(file_name):
    try:
        contact_list = read_file_to_dict(file_name)
        search_field, search_value = search_parameters()
        found_contacts = [contact for contact in contact_list if contact[search_field] == search_value]
        
        if not found_contacts:
            print('Контакт не найден!')
        else:
            print_contacts(found_contacts)

            # Предложим дополнительные действия с найденным контактом
            print('\nВыберите действие:')
            print('1 - Изменить контакт')
            print('2 - Удалить контакт')
            print('0 - Вернуться в главное меню')

            user_choice = input()

            if user_choice == '1':
                modify_contact(file_name, found_contacts)
            elif user_choice == '2':
                delete_contact(file_name, found_contacts)
            elif user_choice == '0':
                pass
            else:
                print('Неправильно выбрана команда!\n')
                
        return found_contacts

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        
def add_phone_number(file_name):
    info = ' '.join(get_new_number())
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(f'{info}\n')
    print('Контакт успешно добавлен.')

def show_phonebook(file_name):
    list_of_contacts = sorted(read_file_to_dict(file_name), key=lambda x: x['Фамилия'])
    print_contacts(list_of_contacts)
    return list_of_contacts

def search_to_modify(contact_list):
    field_mapping = {'1': 'Фамилия', '2': 'Имя', '3': 'Номер телефона'}
    
    search_field, search_value = search_parameters()
    
    if search_field not in field_mapping:
        print('Некорректный выбор поля для поиска.')
        return None
    
    real_search_field = field_mapping[search_field]
    
    search_result = [contact for contact in contact_list if contact[real_search_field] == search_value]
    
    if not search_result:
        print('Контакт не найден.')
        return None
    elif len(search_result) == 1:
        return search_result[0]
    else:
        print('Найдено несколько контактов')
        for i, contact in enumerate(search_result, 1):
            print(f'{i} - {contact}')
        
        while True:
            try:
                num_count = int(input('\nВыберите номер контакта, который нужно изменить/удалить: '))
                if 1 <= num_count <= len(search_result):
                    selected_contact = search_result[num_count - 1]
                    return selected_contact
                else:
                    print('Некорректный ввод. Пожалуйста, введите корректный номер контакта.')
            except ValueError:
                print('Некорректный ввод. Пожалуйста, введите корректный номер контакта.')


def modify_contact(file_name):
    contact_list = read_file_to_dict(file_name)
    contact_to_modify = search_to_modify(contact_list)

    if contact_to_modify:
        print('Какое поле вы хотите изменить?')
        print('1 - Фамилия\n2 - Имя\n3 - Номер телефона\n')
        field = input()

        if field == '1':
            contact_to_modify['Фамилия'] = input('Введите фамилию: ')
        elif field == '2':
            contact_to_modify['Имя'] = input('Введите имя: ')
        elif field == '3':
            contact_to_modify['Номер телефона'] = input('Введите номер телефона: ')

        # Удаляем старые данные, связанные с измененным контактом
        contact_list = [contact for contact in contact_list if contact != contact_to_modify]

        # Добавляем обновленные данные
        contact_list.append(contact_to_modify)

        # Записываем все контакты в файл
        with open(file_name, 'w', encoding='utf-8') as file:
            for contact in contact_list:
                line = ' '.join(contact.values()) + '\n'
                file.write(line)

        print('Контакт успешно изменен.')

def delete_contact(file_name):
    contact_list = read_file_to_dict(file_name)
    contact_to_delete = search_to_modify(contact_list)
    
    if contact_to_delete:
        contact_list.remove(contact_to_delete)
        with open(file_name, 'w', encoding='utf-8') as file:
            for contact in contact_list:
                line = ' '.join(contact.values()) + '\n'
                file.write(line)
        print('Контакт успешно удален.')

def print_contacts(contact_list):
    for contact in contact_list:
        print(contact)

def read_file_to_dict(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    headers = ['Фамилия', 'Имя', 'Номер телефона']
    contact_list = [dict(zip(headers, line.strip().split())) for line in lines]
    return contact_list

def get_new_number():
    last_name = input('Введите фамилию: ')
    first_name = input('Введите имя: ')
    phone_number = input('Введите номер телефона: ')
    return last_name, first_name, phone_number

if __name__ == '__main__':
    file = './phonebook.txt'
    search_field_dict = {'1': 'фамилию', '2': 'имя', '3': 'номер телефона'}
    choose_action(file)