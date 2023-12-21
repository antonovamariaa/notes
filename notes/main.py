from datetime import datetime
import os
import pathlib



## сканируем весь каталог и кладем все в all_files, тут могут быть и названия папок
## в дальнейшем заметки будут записываться в тот каталог, 
## который открыт в редакторе, а не в котором находится main
currentDirectory = pathlib.Path('.')
all_files = []
files = []
all_files += os.listdir(currentDirectory)

##две строки для проверки 
#print((";  ").join(all_files))
#print(len(all_files))


## пробегаемся по нему и добавляем все, что  .json в отдельный лист для дальнейшей работы с ним
for i in range(len(all_files)):
    basename, extension = os.path.splitext(all_files[i])
    ##строка ниже тоже для проверки
    #print(extension)
    if(extension == ".json"):
        files.append(all_files[i])
        
##две строки ниже тоже для проверки но можно оставить для крассоты
print("------ Все заметки -------")
print((";  ").join(files))

## считываем все id заметок в отдельный лист
ids = []
for i in range (len(files)):
    with open(files[i]) as f:
        lines = f.readlines()
        ids += str(int(lines[0]))



## основная функция выбор
def Choose():
    keep = True
    while keep:
        
        print("\n" + "Чем бы вы хотели заняться? " 
              +"\n" + "1 - Создать и сохранить новую заметку; " 
              + "\n" + "2 - Редактировать существующую заметку;" 
              + "\n" + "3 - Удалить существующую заметку;" 
              + "\n" + "4 - Показать все заметки;"  
              + "\n" + "5 - Показать заметки за определенный день;"    
              + "\n" + "6 - Выход;")
        
        choice = input("Выберите действие: ")
        print()
        if choice == '1': Create_Note()
        elif choice == '2': Modify_Note()
        elif choice == '3': Delete_Note()
        elif choice == '4': Show_All_Notes()
        elif choice == '5': Choose_by_Date()
        elif choice == '6': 
            keep = False
            print("До свидания.")
        else:
            print("Это не вариант. Попробуйте снова.")




## 1 - создание заметки +
def Create_Note():
    ## получаем всю нужную информацию
    id = GetID("Введите id заметки: ") 
    if id == 0:
        print("id не может быть буквой или отрицательной цифрой. Вынуждены прервать создание заметки.")
    else:   
        date = str(datetime.now())
        head = GetHeadline("Введите заголовок заметки: ")
        body = str(input("Введите заметку: "))

        ## задаем полное название файла, с которым будет вестись работа
        ## функция Format заменит пробелы на нижние подчеркивания для более удобного наименования
        file_name = Format(head) + ".json"

        ##открываем файл и записываем все,что есть
        with open(file_name, "w", encoding="UTF-8") as new_note:
            new_note.write(str(id) + '\n' + date + '\n' + '\n' + head + '\n' + '\n' + body)
        print("\n"+"Успешно добавлено." + "\n" +"Возращаемся в меню.")
        ## добавляем новое имя файла в общий список
        files.append(file_name)


        
## 2 - изменение заметки ++
def Modify_Note():
    ## получаем заголовок той заметки, которую хотим изменить
    All_Headlines()
    file_name = Format(CheckHeadline("Введите заголовок заметки, которую хотите изменить (без .json): ") ) + ".json"
    ## печатаем содержимое заметки, чтобы знать,что было раньше
    print("\n" + "++++++++++++++++++++++++++")
    with open(file_name) as f:
            lines = f.readlines()
            for line in lines:
                if not line:
                    break
                print(line.strip())
    print("\n" + "++++++++++++++++++++++++++")
    ##получаем новый заголовок старой заметки
    new_head = GetHeadline("Введите заголовок новой заметки: ") 
    new_name = Format(new_head)

    ##получаем остальную информацию
    body = input("Введите новое тело заметки: ")
    date = str(datetime.now())

    ##задаем полные старое и новое названия файла
    new_file_name = new_name + ".json"

    ##читаем id из файла
    with open(file_name) as f:
        lines = f.readlines()
        id = str(lines[0])

    ##записываем все в файл
    with open(file_name, "w", encoding="UTF-8") as note:
        note.write(str(id) + date + " (modified)" + '\n' + '\n' + new_head + '\n' + '\n' + body)
    
    ##переименовываем файл, удаляем старое название из листа и добавляем новое
    os.rename(file_name, new_file_name)
    files.append(new_file_name)
    files.remove(file_name)
    print("\n"+"Успешно изменено." + "\n" +"Возращаемся в меню.")



## 3 - удаление заметки ++
def Delete_Note():
    
    All_Headlines()
    ##получаем заголовок заметки которую хотим удалить
    headline = Format(CheckHeadline("Введите заголовок заметки, которую хотите удалить: ")) + ".json"
    ##открывем и читаем id
    with open(headline) as f:
        lines = f.readlines()
        id = str(lines[0][0])
    ##удаляем файл и id удаленной заметки из списка
    os.remove(headline)
    ids.remove(id)
    files.remove(headline)
    print("Успешно удалено.")



##4 показать все заметки ++
def Show_All_Notes():
    counter = 0
    print("-----------------------------------------")
    ## бежим по всем файлам, открываем, читаем строки и выводим на экран
    for file in files:
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                if not line:
                    break
                print(line.strip())

        counter = counter + 1
        print("-----------------------------------------")

    print("Всего заметок: " + str(counter))


## 5 - выбор заметки по дате ++
def Choose_by_Date():
    inputdate = str(input("Введите дату в формате гггг-мм-дд (пример - 2020-12-03):"))
    counter = 0
    print("***************************************")
    ## бежим по всем заметкам, открывая их и читаем оттуда дату.
    for file in files:
        
        with open(file) as f:
            lines = f.readlines()
            date = lines[1].split()
            ##если дата совпадает, то выводим заметку
            if date[0] == inputdate:

                for line in lines:
                    if not line:
                        break
                    print(line.strip())

                counter = counter + 1
                print("***************************************")
    
    if counter == 0: print("С горестью сообщаем, что заметок с такой датой нет, либо вы ввели неверную дату...")
    elif counter == 1: print("Нашлась целая одна заметка с такой датой... Ура, как неожиданно.")
    else: print("Вот же повезло! Нашлось аж ", counter , "заметок. Удачного прочтения")


        
        
        

## служебные функции для получения id и заголовков для разных случаев

## вывод всех заголовков
def All_Headlines():
    print("Все заголовки заметок")
    print((";  ").join(files))

def GetID(text = "Введите id заметки: "):
    keep = True
    while keep:
        id = str(input(text))
        ## если это цифра и она больше 0
        if (id.isdigit() ):
            if int(id) > 0:
        ## добавляем id в лист
                ids.append(id)
        else:
        ## если не цифра возвращаем ноль для дальнейшей проверки
            keep = False
            return 0
        ## если длина листа не равна длине приведенного листа, то id там уже было
        ## например добавили новый id, стало res = [1, 2, 3, 3]
        ## длина полного массива и этого же массива после удаления повторяющихся
        ## элементов разная, значит мы ввели существующий id
        if (len(ids) != len(set(ids))):
            print("Такое ID уже существует, как и следующие:")
            print(', '.join(set(ids)))
            ## так как append добавляет в конец, то можно просто удалачть последний
            ## элемент, который как раз и будет являться новым id
            del ids[len(ids) - 1]
            print("Попробуйте еще раз.")
        else: 
            keep = False
            return id
    
## если надо уникальный заголовок
def GetHeadline(text = "Введите заголовок заметки: "):
    keep = True
    while keep:
        head = str(input(text))
        headline = Format(head)
        
        file_name = headline + ".json"

        if (file_name in files):
            print("Такой заголовок уже существует, как и следующие:")
            print('; '.join(files))
            print("Попробуйте еще раз.")
        else: 
            keep = False
            return head

## если надо существующий заголовок  
def CheckHeadline(text = "Введите заголовок заметки: "):
    keep = True
    while keep:
        head = str(input(text))
        name = Format(head)
        file_name = name + ".json"

        if (file_name in files):
            keep = False
            return head
        else: 
            print("Такого заголовка не существует. Попробуйте еще раз.")

## отформатировать название, заменив пробелы на _, чтобы потом записать это  в имя файла
def Format(text):
    words = text.split()
    text_spaced = ("_").join(words)
    return text_spaced




# -------------------------------------------------------

Choose()
