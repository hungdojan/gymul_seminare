from os import linesep

FILE_STUDENT_FORMAT_REGEX = '^\d+[;,][ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮĚÓ\w ]+[;,][ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮĚÓ\w ]+[;,]\w+[;,][\w-]+([;,][\w-]+){2}\s?$'
FILE_SUBJECT_FORMAT_REGEX = '^[ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮĚÓ\w-]+\s?$'
FILE_TYPE = '.csv'
FILE_DELIM = ',|;'
EOF = linesep
OUT_STUDENTS = 'output_zaci.csv'
OUT_DAYS = 'output_dny.csv'