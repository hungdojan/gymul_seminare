import itertools
import json
import codecs
import os
import re
from collections import OrderedDict
from sort_lib.constants import (FILE_TYPE, FILE_DELIM, EOF, FILE_STUDENT_FORMAT_REGEX,
                                FILE_SUBJECT_FORMAT_REGEX, OUT_DAYS, OUT_STUDENTS)
from sort_lib.student import Student
from sort_lib.day import Day
from PySide6.QtCore import QJsonArray, QJsonDocument, QFile, QIODevice, Signal, QObject


class Sort(QObject):
    """Hlavni trida modelu dat.

    Tato trida si uklada data o studentech, predmetech a dnech. Pres tuto tridu
    uzivatel spravuje jednotlive objekty.
    """
    class FilePathException(Exception):
        """Vyjimka pro neexistujici soubor.
        
        Tato vyjimka nastane v pripade, ze uzivatel se snazi nacist soubor, ktery neexistuje.
        """
        pass

    class FileTypeException(Exception):
        """Vyjimka pro spatnou koncovku souboru.

        Tato vyjimka nastane v pripade, ze uzivatel se snazi pracovat se souborem,
        u ktereho se ocekava jiny typ.
        """
        pass

    class FileContentFormatException(Exception):
        """Vyjimka pro spatny obsah souboru.

        Tato vyjimka nastane v pripade, ze obsah souboru dodany uzivatelem
        nesplnuje ocekavany format.
        """
        pass

    class JsonFileCorruptedException(Exception):
        """Vyjimka pro spatny/poskozeny soubor JSON.

        Tato vyjimka nastane v pripade, ze nactenemu JSON souboru chybi
        nejaky predem definovany obsah. 
        """
        pass

    sort_toggle = Signal(bool)
    student_id_counter = 1

    def __init__(self):
        super().__init__()
        # Seznam studentu
        self.__students: OrderedDict[str, Student] = OrderedDict()
        # Seznam dnu
        self.__days: list[Day] = []
        # Seznam predmetu
        self.__subjects: dict[str, list[Student]] = {}
        self._is_sorted = False
        self._file_path = None
    

    @property
    def students(self) -> tuple[Student]:
        return tuple(self.__students.values())


    @property
    def days(self) -> tuple[Day]:
        return tuple(self.__days)


    @property
    def subjects(self) -> dict[str, list[Student]]:
        return self.__subjects

    
    @property
    def is_sorted(self) -> bool:
        return self._is_sorted


    @property
    def file_path(self) -> str:
        return self._file_path
    

    def set_sorted(self, value: bool) -> None:
        """Aktualizuje stav dat

        Args:
            value (bool): Nova hodnota dat
        """
        self._is_sorted = value
        self.sort_toggle.emit(value)


    def add_day(self, day: Day=None, index: int=-1) -> Day:
        """Prida novy den do seznamu.

        Args:
            index (int, optional): Vlozi instanci dne na zadanou pozici. Defaults to -1.
        Returns:
            Day: Instance nove vytvoreneho dne.
        """
        if day is None:
            day = Day(self)
        if index < 0:
            self.__days.append(day)
        else:
            self.__days.insert(index, day)
        self.set_sorted(False)
        return day
    

    def remove_day(self, model: Day):
        if model not in self.__days:
            return
        model.clear_subjects()
        self.__days.remove(model)
        self.set_sorted(False)


    def add_subject(self, name: str):
        """Prida predmet do seznamu.

        Args:
            name (str): Jmeno predmetu.
        """
        if name is None or name in self.__subjects.keys():
            return
        self.__subjects[name] = []
    

    def remove_subject(self, name: str) -> None:
        """Maze jmeno predmetu ze seznamu predmetu.

        Args:
            name (str): Jmeno predmetu.
        """
        if self.__subjects.get(name) is None:
            return
        self.set_sorted(False)
        self.notify_students(name)

        list(map(lambda x: x.remove_subject(name), self.__days))
        del self.__subjects[name]
    

    def add_student(self, student: Student) -> bool:
        """Prida studenta do seznamu.

        V seznamu se nesmi vyskytovat 2 studenti se stejnym ID. 
        V takovem pripade je ponechan stara verze studenta.

        Args:
            student (Student): Instance studenta.

        Returns:
            bool: Nenastala kolize ID studentu a novy student byl uspesne pridan.
        """
        if student is None:
            return False
        if self.__students.get(student.id) is not None:
            return False

        self.__students[student.id] = student
        
        student.attach()
        self.set_sorted(False)
        return True
    

    def get_student(self, student_id: str) -> Student:
        """Vyhleda studenta podle ID a vraci jeho instanci.

        Args:
            student_id (str): Identifikacni hodnota studenta.

        Returns:
            Student: Nalezena instance studenta; None pokud nic nenasel.
        """
        return self.__students.get(student_id)


    def remove_student_id(self, student_id: str) -> None:
        """Maze studenta ze seznamu studentu.

        Args:
            student_id (str): ID studenta.
        """
        student = self.__students.get(student_id)
        if student is None:
            return
        
        self.set_sorted(False)
        student.detach()
        del self.__students[student_id]
    

    def remove_student(self, student: Student) -> None:
        if self.__students.get(student.id) is None:
        # if student not in self.__students:
            return
        student.detach()
        self.set_sorted(False)
        # self.__students.remove(student)
        del self.__students[student.id]
    

    def attach_student(self, student: Student, subject_name: str):
        if subject_name is None:
            return
        if self.__subjects.get(subject_name) is None:
            self.__subjects[subject_name] = []
        self.__subjects[subject_name].append(student)
    

    def detach_student(self, student: Student, subject_name: str):
        if subject_name is None or self.__subjects.get(subject_name) is None:
            return
        try:
            self.__subjects[subject_name].remove(student)
        except:
            pass


    def notify_students(self, subject_name: str):
        if self.__subjects.get(subject_name) is None:
            return
        for i in range(len(self.__subjects[subject_name]) - 1, -1, -1):
            self.__subjects[subject_name][i].receive_msg(subject_name)
            
    
    def load_file_students(self, path: str) -> tuple[list[str], list[str]]:
        """Nacte seznam studentu ze .csv souboru.

        Args:
            path (str): Cesta k .csv souboru se studenty.

        Raises:
            Sort.FilePathException: Neexistujici soubor.
            Sort.FileTypeException: Soubor ma spatnou koncovku.
            Sort.FileContentFormatException: Obsah souboru nesouhlasi s ocekavanym formatem.

        Returns:
            tuple[list[str], list[str]]: Dvojice seznamu ID nove pridanych studentu a jmen novych predmetu.
        """
        # seznam ID novych studentu
        new_students_id = []
        new_subjects = []

        # kontrola vybraneho souboru (zda existuje a ma spravnou koncovku)
        if path is None or not isinstance(path, str) or not os.path.isfile(path):
            raise Sort.FilePathException('Invalid path to file')
        if not path.endswith(FILE_TYPE):
            raise Sort.FileTypeException('Invalid file type, .csv file expected!')
        
        # nacitani dat ze souboru
        line_num = 0
        self.set_sorted(False)
        with codecs.open(path, encoding='utf-8') as f:
            for line in f:
                line_num += 1
                # kontrola formatu nacteneho radku
                if re.match(FILE_STUDENT_FORMAT_REGEX, line) is None:
                    raise Sort.FileContentFormatException(f'Invalid data on line: {line_num}')
                # rozdeleni nacteneho radku na pole dat
                data = re.split(FILE_DELIM, line.rstrip(EOF))
                data = list(map(lambda x: x.strip(), data))

                # kontrola, zda neexistuje student se stejnym id
                # pokud student existuje, je preskocen
                if self.__students.get(data[0]) is not None:
                    continue

                # kontrola predmetu
                for subj in data[4-len(data):]:
                    if subj and self.__subjects.get(subj) is None and subj not in new_subjects:
                        new_subjects.append(subj)
                
                # vlozi noveho studenta do seznamu studentu
                student = Student(
                    data[1], data[2], data[3], tuple(data[4-len(data):]), self, data[0]
                )
                student.attach()
                self.__students[data[0]] = student
                new_students_id.append(data[0])
                __class__.student_id_counter += 1
        
        return new_students_id, new_subjects 


    def load_file_subjects(self, path: str) -> list:
        """Nacita seznam predmetu z .csv souboru.

        Args:
            path (str): Cesta k souboru.

        Raises:
            Sort.FilePathException: Neexistujici soubor.
            Sort.FileTypeException: Soubor ma spatnou koncovku.
            Sort.FileContentFormatException: Obsah souboru nesouhlasi s ocekavanym formatem.

        Returns:
            list: Seznam jmen nove pridanym predmetu.
        """
        # seznam koliznich jmen predmetu
        new_subjs = []

        # kontrola vybraneho souboru (zda existuje a ma spravnou koncovku)
        if path is None or not isinstance(path, str) or not os.path.isfile(path):
            raise Sort.FilePathException('Invalid path to file')
        if not path.endswith(FILE_TYPE):
            raise Sort.FileTypeException('Invalid file type, .csv file expected!')
        
        # nacitani dat ze souboru
        line_num = 0
        self.set_sorted(False)
        with codecs.open(path, encoding='utf-8') as f:
            for line in f:
                line_num += 1
                # kontrola formatu nacteneho radku
                if re.match(FILE_SUBJECT_FORMAT_REGEX, line) is None:
                    raise Sort.FileContentFormatException(f'Invalid data on line: {line_num}')
                # rozdeleni nacteneho radku na pole dat
                data = re.split(FILE_DELIM, line.rstrip(EOF))
                data = list(map(lambda x: x.strip(), data))

                # kontrola, zda neexistuje se stejnym jmenem
                # pokud predmet existuje, je preskocen
                if self.__subjects.get(data[0]) is None:
                    self.__subjects[data[0]] = []
                    new_subjs.append(data[0])

        return new_subjs 

    
    def sort_data(self) -> None:
        """Setrizuje studenty do jednotlivych predmetu."""
        def convert_combinations(student: Student, comb: tuple) -> tuple:
            """Prevadi kombinace dnu na vyslednou posloupnost predmetu.

            Args:
                student (Student): Instance daneho studenta.
                comb (tuple): Prislusna kombinace dnu.

            Returns:
                tuple: Prevedena kombinace dnu na posloupnost predmetu.
            """
            out = []
            # pruchod dny
            for i in range(len(self.__days)):
                # student nema zadny predmet v dany den
                if i not in comb:
                    out.append((None, None))
                else:
                    out.append((student.required_subjects[comb.index(i)], self.__days[i]))
            return tuple(out)

        for s in self.students:
            comb = []
            # Pro kazdy predmet zjisti, do jakeho dne by mohl byt zarazen
            for sub in s.required_subjects:
                list_of_possible_days = [day for day in self.__days 
                                         if sub in [subject.name for subject in day.subjects]]
                possible_days_indices = [self.__days.index(i) for i in list_of_possible_days]
                comb.append(possible_days_indices)
            
            # vytvori vsechny mozne kombinace dnu a ty ulozi do seznamu
            combination_of_days = list(itertools.product(*comb))
            # odstraneni kombinaci, ve kterem jsou 2 a vice predmetu ve stejny den
            filtered_combinations = [days_comb for days_comb in combination_of_days
                                     if len(set(days_comb)) == len(days_comb)]
            
            # konverguje vytvorenou kombinaci na dvojici (jmeno_predmetu, instance_dnu_s_predmetem)
            s.possible_comb = [convert_combinations(s, comb) for comb in filtered_combinations]

            # nastavi kombinaci u studentu, kteri maji jenom jednu kombinaci
            if len(s.possible_comb) == 1:
                try:
                    s.set_comb(0)
                except:
                    pass
        self.set_sorted(True)


    def export_data(self, dest_path: str):
        """Vyexportuje data do .csv souboru.

        Args:
            dest_path (str): Cesta k cilove slozce.

        Raises:
            Sort.FilePathException: Cesta ke slozce neexistuje.
        """
        if dest_path is None or not os.path.isdir(dest_path):
            raise Sort.FilePathException('Invalid output directory path')
        
        # vypis rozdeleni studentu do predmetu podle jednotlivych dnu
        with codecs.open(os.path.join(dest_path, OUT_DAYS), 'w', encoding='utf-8') as f:
            # vypis dnu
            for i in range(len(self.__days)):
                f.write(f'Den {i+1}\n')
                # vypis predmetu v danem dni
                for subj in self.__days[i].subjects:
                    f.write(subj.name + '\n')
                    # vypis informaci studenta
                    for student in sorted(subj.students, key=lambda x: int(x.id)):
                        f.write(f'{student.id},{student.first_name},{student.last_name},{student.class_id}\n')
                    f.write('\n')
                f.write('\n')
        
        # vypis seznamu zaku a jejich vybrane kombinace predmetu
        with codecs.open(os.path.join(dest_path, OUT_STUDENTS), 'w', encoding='utf-8') as f:
            for student in self.students:
                f.write(f'{str(student)}\n')


    def save_to_json(self, path: str=None) -> str:
        """Vraci retezcovou reprezentaci backend objektu v JSON formatu.

        Je potreba pred ulozenim backendu setridit data.

        Returns:
            str: Vygenerovany retezec JSON objektu.
        """
        if path is None and self._file_path is None:
            raise FileNotFoundError('No destination path found')
        if path is not None:
            self._file_path = path

        main_obj = {}
        main_obj['_type'] = "Sort"
        main_obj['students'] = [x.to_dict() for x in self.students]

        # seznam json objektu Day
        main_obj['days'] = {}
        for i in range(len(self.__days)):
            main_obj['days'][f'{i+1}'] = self.__days[i].to_dict()
            
        # seznam predmetu
        main_obj['subjects'] = list(sorted(self.__subjects.keys()))

        with open(self._file_path, "w") as f:
            f.write(json.dumps(main_obj, indent=4))
        


    def clear_data(self):
        """Vymaze vsechna ulozena data."""
        self.__students.clear()
        self.__days.clear()
        self.__subjects.clear()
        self.set_sorted(False)


    @staticmethod
    def load_save_file(path: str) -> 'Sort':
        """Generuje objekt Sort ze vstupniho JSON souboru.

        Args:
            path (str): Cesta k JSON souboru.

        Raises:
            Sort.JsonFileCorruptedException: Vstupni JSON soubor je poskozeny/neodpovida zakladnimu formatu.

        Returns:
            Sort: Inicializovany Sort objekt.
        """
        def convert_combination(model: Sort, student: Student, comb: tuple) -> list:
            out = []
            for i in range(len(model.__days)):
                if model.__days[i].get_subject(comb[i]) is None:
                    out.append((None, None))
                else:
                    out.append((comb[i], model.__days[i]))
            return tuple(out)

        try:
            with codecs.open(path, "r", encoding="utf-8") as f:
                _data = f.read()
            main_obj = json.loads(_data)
        except:
            raise Sort.JsonFileCorruptedException(f'JSON file {path} is corrupted')

        # nacitani dat
        model = Sort()
        model._file_path = path
        if main_obj['_type'] != 'Sort':
            raise Sort.JsonFileCorruptedException('JSON error: Expected Sort object')
        
        # predmety
        subj_arr = main_obj['subjects']
        for name in subj_arr:
            model.__subjects[name] = []

        # dny
        for day_index in sorted(main_obj['days']):
            if main_obj['days'][day_index]['_type'] != 'Day':
                raise Sort.JsonFileCorruptedException('JSON error: expected Day object')
            day = model.add_day()

            for subject in main_obj['days'][day_index]['subjects']:
                if subject['_type'] != 'Subject':
                    raise Sort.JsonFileCorruptedException('JSON error: expected Subject object')
                day.add_subject_name(subject['name'])


        # studenti
        for student_json in main_obj['students']:
            if student_json['_type'] != 'Student':
                raise Sort.JsonFileCorruptedException('JSON error: expected Student object')
            student = Student(
                student_json['first_name'],
                student_json['last_name'],
                student_json['class_id'],
                tuple(student_json['required_subjects']),
                model,
                student_json['id'],
                is_locked=student_json['is_locked']
            )

            model.__students[student.id] = student
            student.attach()
            
            # nacteni validnich kombinaci
            possible_comb = []
            for comb_list in student_json['possible_comb']:
                comb_tuple = tuple([comb if comb != 'None' else None for comb in comb_list])
                comb = convert_combination(model, student, comb_tuple)
                possible_comb.append(comb)
            student.possible_comb = possible_comb

            # nastaveni vybrane kombinace
            if len(student_json['chosen_comb']) > 1:
                selected_comb = tuple([comb if comb != 'None' else None for comb in student_json['chosen_comb']])
                student.set_comb(student.possible_comb.index(selected_comb))
            student.is_locked = student_json['is_locked']

        return model