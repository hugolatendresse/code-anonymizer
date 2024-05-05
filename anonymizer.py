import re
import string
import random

from reserved_words import sql_reserved_words

longquery = """SELECT
    info.EmployeeID,
    info.FirstName,
    info.LastName,
    dept.DepartmentName,
    pos.PositionTitle,
    COUNT(proj.ProjectID) AS NumberOfProjects,
    SUM(ts.Hours) AS TotalHours,
    AVG(ts.Hours) AS AverageHoursPerProject,
    MAX(ts.Date) AS LastProjectDate
FROM
    Employees info
JOIN
    Departments dept ON info.DepartmentID = dept.DepartmentID
JOIN
    Positions pos ON info.PositionID = pos.PositionID
LEFT JOIN
    ProjectAssignments pa ON info.EmployeeID = pa.EmployeeID
LEFT JOIN
    Projects proj ON pa.ProjectID = proj.ProjectID
LEFT JOIN
    TimeSheets ts ON proj.ProjectID = ts.ProjectID
WHERE
    dept.DepartmentName IN ('IT', 'Finance', 'Marketing')
    AND info.StartDate BETWEEN '2020-01-01' AND '2023-01-01'
    AND ts.Date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR)
GROUP BY
    info.EmployeeID, dept.DepartmentName, pos.PositionTitle
HAVING
    TotalHours > 100
ORDER BY
    TotalHours DESC, LastName ASC
LIMIT 10;
"""


def replace_in_string(token, replacement, string):
    token = r"\b" + token + r"\b"
    modified_string = re.sub(token, replacement, string)
    return modified_string


def convert_SQL(sql_query):
    d = {}

    sql_reserved_words_upper = {word.upper() for word in sql_reserved_words}

    def generate_random_string(length=8):
        # TODO the list should be constantly refreshed in the background the avoid the cost of processing
        # TODO the random strings should have null intersection with: sql reserved words, and ideally original tokens

        # TODO can have "levels" of anonymization. For example, a table name as 'A' or common words like "data", "info"
        #  etc probably don't need to be anonymized

        # TODO even better here would be random words from the dictionary, without replacement
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def replace_non_reserved_words(query):
        # TODO need to consider that sql is NOT case sensitive, and therefore col1 and COL1 are the same thing!!
        tokens = re.findall(r'\b\w+\b', query)
        # TODO compare the performance of using tokens1 and parsing the list vs tokens2
        # tokens1 = re.split(r"(\s+|,|;|\(|\))", query)
        for i, token in enumerate(tokens):
            if token.upper() not in sql_reserved_words_upper and re.match(r'\w+', token):
                if token not in d:
                    d[token] = generate_random_string()
                # TODO there MUST be a more efficient way where we go through only once instead of <number of tokens>
                #  times, especially since we can hash the tokens and find they quickly. The only challenge is that as
                #  we go throught the query, we have to know where tokens start and end
                # TODO can always implement a string pattern algorithm directly in C/C++
                query = replace_in_string(token=token, replacement=d[token], string=query)
        return query

    new_query = replace_non_reserved_words(sql_query)
    return new_query, d


def unanonymize(query, d):
    for original_token, sanitized_token in d.items():
        query = replace_in_string(token=sanitized_token, replacement=original_token, string=query)
    return query



def test_quick(query):
    print("Original:")
    print(query)
    res1, d = convert_SQL(query)
    print("\nAnon:")
    print(res1)
    unres1 = unanonymize(res1, d=d)
    print("\nRestored:")
    print(unres1)

# test_quick("SELECT EmployeeID, LastName FROM Employees WHERE Department = 'Sales';")
test_quick(longquery)