import sort_lib.sort

class Student:

    class StudentLockedException(Exception):
        pass

    def __init__(self, id: str, first_name: str, last_name: str, class_id: str, lof_subjects: tuple):
        # Identifikacni cislo studenta
        self.__id = id
        # Jmeno studenta
        self.__first_name   = first_name
        # Prijmeni studenta
        self.__last_name    = last_name
        # Trida studenta
        self.__class_id     = class_id
        # Seznam vybranych predmetu
        self.__lof_subjects = lof_subjects

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

    @property
    def last_name(self) -> str:
        return self.__last_name

    @property
    def class_id(self) -> str:
        return self.__class_id
    
    @property
    def chosen_comb(self) -> tuple:
        if self.__chosen_comb is not None:
            out_tuple = tuple(map(lambda y: y[0], self.__chosen_comb))
        else:
            out_tuple = None
        return out_tuple

    @property
    def possible_comb(self) -> list:
        # vraci list nazvu kombinaci
        out_list = list(map(lambda x: tuple(map(lambda y: y[0], x)), self.__possible_comb))
        return out_list

    @property
    def lof_subjects(self) -> tuple:
        return self.__lof_subjects

    @property
    def is_locked(self) -> bool:
        return self._is_locked

    @is_locked.setter
    def is_locked(self, value):
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
        self.__possible_comb = value

    @lof_subjects.setter
    def lof_subjects(self, value: set):
        if self._is_locked:
            raise Student.StudentLockedException("Cannot edit locked student's data")
        self.__lof_subjects = value
    

    def set_comb(self, index: int) -> None:
        """Nastavi studentovi kombinaci ze seznamu moznych kombinaci

        Kombinace se vybira podle zadaneho indexu. V pripade, ze uzivatel zada
        index mimo dosah seznamu, bude studentovi nastavena hodnota None.

        Args:
            index (int): Pozice kombinace v Student.possible_comb

        Raises:
            Student.StudentLockedException: Student je zamknut; opravneni upravovat je odepreno
        """
        if self._is_locked:
            raise Student.StudentLockedException("Cannot edit locked student's data")
        if index not in range(len(self.__possible_comb)):
            self.__update_combination(None)
        else:
            self.__update_combination(self.__possible_comb[index])
    

    def __update_combination(self, value: tuple):
        """Aktualizuje vybranou kombinaci

        Odhlasi studenta z predchozich predmetu a zapise do novych predmetu

        Args:
            value (tuple): Vybrana kombinace
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
    

    def clean_data(self):
        """Vynuluje vygenerovana data studenta"""
        self._is_locked = False
        self.__update_combination(None)
        self.__possible_comb = []
    
    def __repr__(self) -> str:
        out_str = f'{self.__id},{self.__first_name},{self.__last_name},{self.__class_id}'
        if self.__chosen_comb is not None:
            for subj in self.chosen_comb:
                out_str += f',{subj}'
        return out_str