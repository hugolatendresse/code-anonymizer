import re
import string
import random

from reserved_words import sql_reserved_words

longquery = """SELECT
    emp.EmployeeID,
    emp.FirstName,
    emp.LastName,
    dept.DepartmentName,
    pos.PositionTitle,
    COUNT(proj.ProjectID) AS NumberOfProjects,
    SUM(ts.Hours) AS TotalHours,
    AVG(ts.Hours) AS AverageHoursPerProject,
    MAX(ts.Date) AS LastProjectDate
FROM
    Employees emp
JOIN
    Departments dept ON emp.DepartmentID = dept.DepartmentID
JOIN
    Positions pos ON emp.PositionID = pos.PositionID
LEFT JOIN
    ProjectAssignments pa ON emp.EmployeeID = pa.EmployeeID
LEFT JOIN
    Projects proj ON pa.ProjectID = proj.ProjectID
LEFT JOIN
    TimeSheets ts ON proj.ProjectID = ts.ProjectID
WHERE
    dept.DepartmentName IN ('IT', 'Finance', 'Marketing')
    AND emp.StartDate BETWEEN '2020-01-01' AND '2023-01-01'
    AND ts.Date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR)
GROUP BY
    emp.EmployeeID, dept.DepartmentName, pos.PositionTitle
HAVING
    TotalHours > 100
ORDER BY
    TotalHours DESC, LastName ASC
LIMIT 10;
"""

def convert_SQL(sql_query):
    d = {}

    # TODO ask chatgpt if i'm missing anything
    dividers = [r'\s+', '\.', ',', ';', '\{', '\}', '\[', '\]', r'\(', r'\)', '\+', '-', '\*', '/', '=', '!', '<', '>']
    divider_all = r"(" + "|".join(dividers) + ")"

    sql_reserved_words_upper = {word.upper() for word in sql_reserved_words}

    def generate_random_string(length=8):
        # TODO the list should be constantly refreshed in the background the avoid the cost of processing
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def replace_in_string(token, replacement, string):
        token = r"\b" + token + r"\b"
        modified_string = re.sub(token, replacement, string)
        return modified_string

    def replace_non_reserved_words(query):
        # TODO need to consider that sql is NOT case sensitive, and therefore col1 and COL1 are the same thing!!
        tokens = re.split(divider_all, query)
        # TODO compare the performance of using tokens1 and parsing the list vs tokens2
        # tokens1 = re.split(r"(\s+|,|;|\(|\))", query)
        for i, token in enumerate(tokens):
            if token.upper() not in sql_reserved_words_upper and re.match(r'\w+', token):
                d[token] = generate_random_string()
                # TODO there MUST be a more efficient way where we go through only once instead of <number of tokens>
                #  times, especially since we can hash the tokens and find they quickly. The only challenge is that as
                #  we go throught the query, we have to know where tokens start and end
                query = replace_in_string(token=token, replacement=d[token], string=query)
        return query

    new_query = replace_non_reserved_words(sql_query)
    return new_query


# print(convert_SQL(longquery))  # TODO
print(convert_SQL("SELECT EmployeeID, LastName FROM Employees WHERE Department = 'Sales';"))
