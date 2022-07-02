import sort_lib.student
from PySide6.QtCore import QJsonArray

class Subject:
    
    def __init__(self, name: str):
        # jmeno predmetu
        self.__name = name
        # seznam studentu
        self.__students = []
    

    @property
    def name(self):
        return self.__name

    
    @property
    def students(self) -> tuple:
        """Vraci seznam zaku zapsany v danem predmetu

        Returns:
            tuple: Nemodifikovatelny seznam zaku v predmetu
        """
        return tuple(self.__students)
    

    def add_student(self, student: 'sort_lib.student.Student'):
        """Zapisuje studenta do predmetu

        Args:
            student (sort_lib.student.Student): Instance studenta
        """
        self.__students.append(student)

    
    def remove_student(self, student: 'sort_lib.student.Student'):
        """Maze studenta ze seznamu zapsanych studentu predmetu

        Args:
            student (sort_lib.student.Student): Instance studenta
        """
        try:
            self.__students.remove(student)
        except ValueError:
            pass


    def student_count(self) -> int:
        """Vraci pocet zaku v tomto predmetu

        Returns:
            int: Pocet zaku v predmetu
        """
        return len(self.__students)
    

    def clear_data(self) -> None:
        """Vymaze seznam studentu zapsanych v danem predmetu"""
        list(map(lambda x: x.clear_data(), reversed(self.__students)))

    
    def get_qjson(self) -> dict:
        """Vygeneruje JSON objekt pro ulozeni backendu

        Returns:
            dict: Vygenerovany JSON objekt
        """
        obj = {}
        obj['_type'] = 'Subject'
        obj['name'] = self.__name
        obj['students'] = QJsonArray()
        list(map(
            lambda x: obj['students'].push_back(x),
            list(map(lambda x: x.id, self.__students))))
        return obj


    def __repr__(self):
        return self.__name