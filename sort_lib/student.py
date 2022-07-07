import sort_lib.sort
from PySide6.QtCore import QJsonArray

class Student:
    """Trida reprezentujici studenta"""

    class StudentLockedException(Exception):
        """Vyjimka uzamceneho studenta

        Tato vyjimka se vyvola tehdy, kdyz se uzivatel pokousi upravit predmety zamkleho studenta.
        """
        pass

    def __init__(self, id: str, first_name: str, last_name: str, class_id: str,
                 required_subjects: tuple, parent: 'sort_lib.sort.Sort'):
        # Identifikacni cislo studenta
        self.__id = id
        # Jmeno studenta
        self.__first_name   = first_name
        # Prijmeni studenta
        self.__last_name    = last_name
        # Trida studenta
        self.__class_id     = class_id
        # Seznam vybranych predmetu
        self.__required_subjects = tuple(map(lambda x: x if x else None, required_subjects))
        # Hlavni rodic
        self.__parent = parent

        # Seznam vsech moznych kombinaci predmetu,
        # ktery si student muze zapsat
        self.__possible_comb = dict()
        # Vybrana kombinace studenta
        self.__chosen_comb: tuple = None
        # Zamek proti prepisu
        self._is_locked = False
    

    @property
    def id(self) -> str:
        return self.__id
    
    @property
    def first_name(self) -> str:
        return self.__first_name
    
    @first_name.setter
    def first_name(self, value):
        self.__first_name = value

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @property
    def class_id(self) -> str:
        return self.__class_id
    
    @class_id.setter
    def class_id(self, value):
        self.__class_id = value
    
    @property
    def chosen_comb(self) -> tuple:
        if self.__chosen_comb is not None:
            out_tuple = tuple([subj[0] for subj in self.__chosen_comb])
        else:
            out_tuple = None
        return out_tuple

    @property
    def possible_comb(self) -> list:
        # vraci list nazvu kombinaci
        out_list = [tuple([subj[0] for subj in comb]) for comb in self.__possible_comb]
        return out_list

    @property
    def required_subjects(self) -> tuple:
        return self.__required_subjects

    @property
    def is_locked(self) -> bool:
        return self._is_locked

    @is_locked.setter
    def is_locked(self, value):
        if self.__chosen_comb is not None:
            self._is_locked = value
    
    @possible_comb.setter
    def possible_comb(self, value: list):
        # pokud je student zamceny jsou 3 moznosti, 
        # jak bude reagovat na aktualizaci seznamu moznych kombinaci
        # 1. nema zadnou moznost 
        #   -> zrusi se vybrana kombinace; odemkne se
        # 2. ma jedno nebo vice moznosti, ale momentalni kombinace v ni neni
        #   -> zrusi se vybrana kombinace; odemkne se
        # 3. ma jedno nebo vice moznosti; momentalni kombinace tam je
        #   -> vyber a zamek se ponechaji, aktualizuje se jenom seznam moznych kombinaci
        if not self._is_locked or len(value) == 0 or self.__chosen_comb not in value:
            self._is_locked = False
            self.__update_combination(None)
            self.__parent.set_sorted(False)
        self.__possible_comb = value
    

    @required_subjects.setter
    def required_subjects(self, value: tuple):
        """Aktualizuje seznam pozadovanych predmetu.
        
        Seznam nelze aktualizovat, pokud je student uzamcen.

        Args:
            value (tuple): Novy seznam pozadovanych predmetu.

        Raises:
            Student.StudentLockedException: Student je uzamcen, nelze upravovat data.
        """
        if self._is_locked:
            raise Student.StudentLockedException("Cannot edit locked student's data")
        self.__update_combination(None)
        self.__possible_comb = []
        self.__required_subjects = value
        self.__parent.set_sorted(False)
    

    def set_comb(self, index: int) -> None:
        """Nastavi studentovi kombinaci ze seznamu moznych kombinaci.

        Kombinace se vybira podle zadaneho indexu. V pripade, ze uzivatel zada
        index mimo dosah seznamu, bude studentovi nastavena hodnota None.

        Args:
            index (int): Pozice kombinace v Student.possible_comb.

        Raises:
            Student.StudentLockedException: Student je zamknut; opravneni upravovat je odepreno.
        """
        if self._is_locked:
            raise Student.StudentLockedException("Cannot edit locked student's data")
        if index not in range(len(self.__possible_comb)):
            self.__update_combination(None)
        else:
            self.__update_combination(self.__possible_comb[index])
    

    def __update_combination(self, value: tuple):
        """Aktualizuje vybranou kombinaci.

        Odhlasi studenta z predchozich predmetu a zapise do novych predmetu.

        Args:
            value (tuple): Vybrana kombinace.
        """
        # rusi predchozi kombinaci
        if self.__chosen_comb is not None:
            for subj in self.__chosen_comb:
                if subj[0] is not None:
                    subj[1].get_subject(subj[0]).remove_student(self)

        self.__chosen_comb = value
        # zapisuje se na vybranou kombinaci
        if self.__chosen_comb is not None:
            for subj in self.__chosen_comb:
                if subj[0] is not None:
                    subj[1].get_subject(subj[0]).add_student(self)
    

    def clear_data(self):
        """Vynuluje vygenerovana data studenta."""
        self._is_locked = False
        self.__update_combination(None)
        self.__possible_comb = []

    
    def get_qjson(self) -> dict:
        """Vygeneruje JSON objekt pro ulozeni backendu.

        Returns:
            dict: Vygenerovany JSON objekt.
        """
        obj = {}
        obj['_type'] = "Student"
        obj['is_locked'] = self._is_locked
        obj['id'] = self.__id
        obj['first_name'] = self.__first_name
        obj['last_name'] = self.__last_name
        obj['class_id'] = self.__class_id
        obj['required_subjects'] = QJsonArray()
        list(map(lambda x: obj['required_subjects'].push_back(x), self.__required_subjects))
        obj['possible_comb'] = QJsonArray()
        for comb in self.possible_comb:
            arr = QJsonArray()
            list(map(lambda x: arr.push_back(str(x)), comb))
            obj['possible_comb'].push_back(arr)
        obj['chosen_comb'] = QJsonArray()
        if self.__chosen_comb is not None:
            list(map(lambda x: obj['chosen_comb'].push_back(str(x)), self.chosen_comb))
        return obj

    
    def __repr__(self) -> str:
        out_str = f'{self.__id},{self.__first_name},{self.__last_name},{self.__class_id}'
        if self.__chosen_comb is not None:
            for subj in self.chosen_comb:
                out_str += f',{subj}'
        return out_str