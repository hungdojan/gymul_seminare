import sort_lib.subject

class Day:

    def __init__(self):
        # Seznam predmetu v danem dni
        self.__subjects = []
    

    @property
    def subjects(self) -> tuple:
        """Vraci seznam predmetu v danem dni

        Returns:
            tuple: Nemodifikovatelny seznam predmetu v danem dni
        """
        self.__subjects = sorted(self.__subjects, key=lambda x: x.name)
        return tuple(self.__subjects)
    

    def get_subject(self, subject_name: str) -> sort_lib.subject.Subject:
        temp = list(filter(lambda x: x.name == subject_name, self.__subjects))
        return temp[0] if len(temp) > 0 else None
    

    def add_subject(self, subject: sort_lib.subject.Subject) -> bool:
        """Vlozi predmet do dnu

        Args:
            subject (sort_lib.subject.Subject): Instance predmetu pro vlozeni

        Returns:
            bool: Pravdivostni hodnota urcujici, zda se predmet podaril vlozit
        """
        if len(list(filter(lambda x: x.name == subject.name, self.__subjects))) > 0:
            return False
        self.__subjects.append(subject)
        return True
    

    def add_subject_name(self, subject_name: str) -> sort_lib.subject.Subject:
        """Vlozi predmet do dnu

        Pokud se dany predmet se stejnym jmenem ve dni jiz nachazi, vrati instanci nalezeneho predmetu.
        V opacnem pripade vytvori novou instanci, vlozi ji do dni a vrati ji.

        Args:
            subject_name (str): Jmeno predmetu

        Returns:
            sort_lib.subject.Subject: Nalezena, nebo vytvorena instance predmetu
        """
        subject = list(filter(lambda x: x.name == subject_name, self.__subjects))
        if len(subject) > 0:
            return subject[0]
        subject = sort_lib.subject.Subject(subject_name)
        self.__subjects.append(subject)
        return subject
    

    def remove_subject(self, subject_name: str):
        """Vymaze predmet ze dne

        Args:
            subject_name (str): Jmeno predmetu
        """
        delete_subj = list(filter(lambda x: x.name == subject_name, self.__subjects))
        if len(delete_subj) > 0:
            delete_subj[0].clear_data()
        self.__subjects = list(filter(lambda x: x.name != subject_name, self.__subjects))
    

    def clear_data(self):
        """Vymaze vsechny predmety v danem dni"""
        list(map(lambda x: x.clear_data(), self.__subjects))
        self.__subjects.clear()
    

    def clear_subjects(self):
        """Vymaze vsechna data ulozene v jednotlivych predmetech"""
        self.__subjects = list(map(lambda x: x.clear_data(), self.__subjects))