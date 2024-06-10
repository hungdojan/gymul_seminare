import sort_lib.subject
import sort_lib.sort
from PySide6.QtCore import QJsonArray

class Day:
    """Trida reprezentujici den"""

    def __init__(self, parent: 'sort_lib.sort.Sort'):
        # Seznam predmetu v danem dni
        self.__subjects = []
        self.__parent = parent
    

    @property
    def subjects(self) -> tuple:
        """Vraci seznam predmetu v danem dni.

        Returns:
            tuple: Nemodifikovatelny seznam predmetu v danem dni.
        """
        self.__subjects = sorted(self.__subjects, key=lambda x: x.name)
        return tuple(self.__subjects)
    

    def get_subject(self, subject_name: str) -> sort_lib.subject.Subject:
        """Vrati instanci nalezeneho predmetu ve dni podle jmena.

        Args:
            subject_name (str): Jmeno predmetu.

        Returns:
            sort_lib.subject.Subject: Instanci nalezeneho predmetu.
        """
        temp = [subject for subject in self.__subjects if subject.name == subject_name]
        return temp[0] if len(temp) > 0 else None
    

    def add_subject(self, subject: sort_lib.subject.Subject) -> bool:
        """Vlozi predmet do dnu.

        Args:
            subject (sort_lib.subject.Subject): Instance predmetu pro vlozeni.

        Returns:
            bool: Pravdivostni hodnota urcujici, zda se predmet podaril vlozit.
        """
        if len([subj for subj in self.__subjects if subj.name == subject.name]) > 0:
            return False
        self.__subjects.append(subject)
        self.__parent.set_sorted(False)
        return True
    

    def add_subject_name(self, subject_name: str) -> sort_lib.subject.Subject:
        """Vlozi predmet do dnu.

        Pokud se dany predmet se stejnym jmenem ve dni jiz nachazi, vrati instanci nalezeneho predmetu.
        V opacnem pripade vytvori novou instanci, vlozi ji do dni a vrati ji.

        Args:
            subject_name (str): Jmeno predmetu.

        Returns:
            sort_lib.subject.Subject: Nalezena, nebo vytvorena instance predmetu.
        """
        subject = [subject for subject in self.__subjects if subject.name == subject_name]
        if len(subject) > 0:
            return subject[0]
        subject = sort_lib.subject.Subject(subject_name)
        self.__subjects.append(subject)
        self.__parent.set_sorted(False)
        return subject
    

    def remove_subject(self, subject_name: str):
        """Vymaze predmet ze dne.

        Args:
            subject_name (str): Jmeno predmetu.
        """
        delete_subj = [subject for subject in self.__subjects if subject.name == subject_name]
        if len(delete_subj) > 0:
            delete_subj[0].clear_data()
        self.__subjects = [subject for subject in self.__subjects if subject.name != subject_name]
        self.__parent.set_sorted(False)
    

    def clear_data(self):
        """Vymaze vsechny predmety v danem dni."""
        list(map(lambda x: x.clear_data(), self.__subjects))
        self.__subjects.clear()
        self.__parent.set_sorted(False)


    def to_dict(self) -> dict:
        """Vygeneruje JSON objekt pro ulozeni backendu.

        Returns:
            dict: Vygenerovany JSON objekt.
        """
        obj = {}
        obj['_type'] = "Day"
        obj['subjects'] = [x.to_dict() for x in self.__subjects]
        return obj
    

    def clear_subjects(self):
        """Vymaze vsechna data ulozene v jednotlivych predmetech."""
        list(map(lambda x: x.clear_data(), self.__subjects))
    
    def __str__(self) -> str:
        return f'Day: {[subj.name for subj in self.subjects]}'