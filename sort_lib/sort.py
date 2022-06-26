import itertools
import codecs
import os.path
import re
from sort_lib.constants import (FILE_TYPE, FILE_DELIM, EOF, FILE_STUDENT_FORMAT_REGEX,
                                FILE_SUBJECT_FORMAT_REGEX, OUT_DAYS, OUT_STUDENTS)
from sort_lib.student import Student
from sort_lib.day import Day


class Sort:
    class FilePathException(Exception):
        pass

    class FileTypeException(Exception):
        pass

    class FileContentFormatException(Exception):
        pass
    
    def __init__(self):
        # Seznam studentu
        self.__students = []
        # Seznam dnu
        self.__days = []
        # Seznam predmetu
        self.__subjects = set()
    

    @property
    def students(self) -> tuple:
        return tuple(self.__students)


    @property
    def days(self) -> tuple:
        return tuple(self.__days)


    @property
    def subjects(self) -> tuple:
        return tuple(self.__subjects)


    @classmethod
    def load_save_file(path: str) -> 'Sort':
        # TODO:
        return Sort()


    def add_day(self) -> Day:
        """Prida novy den do seznamu

        Returns:
            Day: Instance nove vytvoreneho dne
        """
        day = Day()
        self.__days.append(day)
        self._is_sorted = False
        return day
    

    def remove_day(self, index: int) -> None:
        """Rusi a maze instanci dne ze seznamu

        Indexuje se od 0.

        Args:
            index (int): Index (pozice) dne k smazani
        """
        if index in range(len(self.days)):
            del self.__days[index]
            self._is_sorted = False


    def add_subject(self, name: str):
        """Prida predmet do seznamu

        Args:
            name (str): Jmeno predmetu
        """
        if name is None:
            return
        self.__subjects.add(name)
        self._is_sorted = False
    

    def remove_subject(self, name: str) -> None:
        """Maze jmeno predmetu ze seznamu predmetu

        Args:
            name (str): Jmeno predmetu
        """
        self._is_sorted = False
        self.__subjects.discard(name)
    

    def add_student(self, student: Student) -> bool:
        """Prida studenta do seznamu

        V seznamu se nesmi vyskytovat 2 studenti se stejnym ID. 
        V takovem pripade je ponechan stara verze studenta.

        Args:
            student (Student): Instance studenta

        Returns:
            bool: Nenastala kolize ID studentu a novy student byl uspesne pridan
        """
        if student is None:
            return False
        if len(list(filter(lambda x: x.id == student.id, self.__students))) > 0:
            return False
        self.__students.append(student)
        self._is_sorted = False
        return True


    def remove_student(self, student_id: str) -> None:
        """Maze studenta ze seznamu studentu

        Args:
            student_id (str): ID studenta
        """
        self._is_sorted = False
        self.__students = list(filter(lambda x: x.id != student_id, self.__students))


    def get_students_per_subject(self) -> dict:
        """Vraci statistiku a poctu studentu na predmet

        Returns:
            dict: Vypocitana statistika
        """
        d = {}
        for subj in self.__subjects:
            d[subj] = len(list(filter(lambda x: subj in x.lof_subjects, self.__students)))
        return d


    def load_file_students(self, path: str) -> list:
        """Nacte seznam studentu ze .csv souboru

        Args:
            path (str): Cesta k .csv souboru se studenty

        Raises:
            Sort.FilePathException: Neexistujici soubor
            Sort.FileTypeException: Soubor ma spatnou koncovku
            Sort.FileContentFormatException: Obsah souboru nesouhlasi s ocekavanym formatem

        Returns:
            list: Seznam ID, ktere jiz byly jednou nacteny
        """
        # seznam koliznich ID studentu
        id_collision = []

        # kontrola vybraneho souboru (zda existuje a ma spravnou koncovku)
        if path is None or not isinstance(path, str) or not os.path.isfile(path):
            raise Sort.FilePathException('Invalid path to file')
        if not path.endswith(FILE_TYPE):
            raise Sort.FileTypeException('Invalid file type, .csv file expected!')
        
        # nacitani dat ze souboru
        line_num = 0
        self._is_sorted = False
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
                if len(list(filter(lambda x: x.id == int(data[0]), self.__students))) > 0:
                    id_collision.append(data[0])
                    continue
                
                # vlozi noveho studenta do seznamu studentu
                self.__students.append(Student(
                    data[0], data[1], data[2], data[3], tuple(data[4-len(data):])
                ))
        
        return id_collision 


    def load_file_subjects(self, path: str) -> list:
        """Nacita seznam predmetu z .csv souboru

        Args:
            path (str): Cesta k souboru

        Raises:
            Sort.FilePathException: Neexistujici soubor
            Sort.FileTypeException: Soubor ma spatnou koncovku
            Sort.FileContentFormatException: Obsah souboru nesouhlasi s ocekavanym formatem

        Returns:
            list: Seznam jmen predmetu, ktere jiz byly jednou nacteny
        """
        # seznam koliznich jmen predmetu
        name_collision = []

        # kontrola vybraneho souboru (zda existuje a ma spravnou koncovku)
        if path is None or not isinstance(path, str) or not os.path.isfile(path):
            raise Sort.FilePathException('Invalid path to file')
        if not path.endswith(FILE_TYPE):
            raise Sort.FileTypeException('Invalid file type, .csv file expected!')
        
        # nacitani dat ze souboru
        line_num = 0
        self._is_sorted = False
        with codecs.open(path, encoding='utf-8') as f:
            for line in f:
                line_num += 1
                # kontrola formatu nacteneho radku
                if re.match(FILE_SUBJECT_FORMAT_REGEX, line) is None:
                    raise Sort.FileContentFormatException(f'Invalid data on line: {line_num}')
                # rozdeleni nacteneho radku na pole dat
                data = re.split(FILE_DELIM, line.rstrip(EOF))
                data = list(map(lambda x: x.strip(), data))

                # kontrola, zda neexistuje  se stejnym id
                # pokud student existuje, je preskocen
                if len(list(filter(lambda x: x.id == data[0], self.__students))) > 0:
                    name_collision.append(data[0])
                else:
                    self.__subjects.add(data[0])

        return name_collision 

    
    def sort_data(self) -> None:
        """Setrizuje studenty do jednotlivych predmetu"""
        def convert_combinations(student: Student, comb: tuple) -> tuple:
            """Prevadi kombinace dnu na vyslednou posloupnost predmetu

            Args:
                student (Student): Instance daneho studenta
                comb (tuple): Prislusna kombinace dnu

            Returns:
                tuple: Prevedena kombinace dnu na posloupnost predmetu
            """
            out = []
            # pruchod dny
            for i in range(len(self.__days)):
                # student nema zadny predmet v dany den
                if i not in comb:
                    out.append((None, None))
                else:
                    out.append((student.lof_subjects[comb.index(i)], self.__days[i]))
            return tuple(out)

        for s in self.__students:
            comb = []
            # Pro kazdy predmet zjisti, do jakeho dne by mohl byt zarazen
            for sub in s.lof_subjects:
                list_of_possible_days = list(filter(lambda x: sub in list(map(lambda y: y.name, x.subjects)), self.__days))
                possible_days_indices = list(map(lambda x: self.__days.index(x), list_of_possible_days))
                comb.append(possible_days_indices)
            
            # vytvori vsechny mozne kombinace dnu a ty ulozi do seznamu
            combination_of_days = list(itertools.product(*comb))
            # odstraneni kombinaci, ve kterem jsou 2 a vice predmetu ve stejny den
            filtered_combinations = list(filter(lambda x: len(set(x)) == len(x), combination_of_days))
            
            # konverguje vytvorenou kombinaci na dvojici (jmeno_predmetu, instance_dnu_s_predmetem)
            converted_comb = list(map(lambda x: convert_combinations(s, x), filtered_combinations))
            s.possible_comb = converted_comb

            # nastavi kombinaci u studentu, kteri maji jenom jednu kombinaci
            if len(converted_comb) == 1:
                try:
                    s.set_comb(0)
                except:
                    pass


    def export_data(self, dest_path: str):
        """Vyexportuje data do .csv souboru

        Args:
            dest_path (str): Cesta k cilove slozce

        Raises:
            Sort.FilePathException: Cesta ke slozce neexistuje
        """
        if dest_path is None or not os.path.isdir(dest_path):
            raise Sort.FilePathException('Invalid output directory path')
        
        # vypis rozdeleni studentu do predmetu podle jednotlivych dnu
        with open(os.path.join(dest_path, OUT_DAYS), 'w', encoding='utf-8') as f:
            # vypis dnu
            for i in range(len(self.__days)):
                f.write(f'Den {i+1}\n')
                # vypis predmetu v danem dni
                for subj in self.__days[i].subjects:
                    f.write(subj.name + '\n')
                    # vypis informaci studenta
                    for student in subj.students:
                        f.write(f'{student.id},{student.first_name},{student.last_name},{student.class_id}\n')
                    f.write('\n')
                f.write('\n')
        
        # vypis seznamu zaku a jejich vybrane kombinace predmetu
        with open(os.path.join(dest_path, OUT_STUDENTS), 'w', encoding='utf-8') as f:
            for student in self.__students:
                f.write(f'{student}\n')


    def save_to_json(self):
        # TODO:
        pass


    def clear_data(self):
        """Vymaze vsechna ulozena data"""
        self.__students.clear()
        self.__days.clear()
        self.__subjects.clear()
        self._is_sorted = False