longquery = """

SELECT
    INFO.EmployeeID,
    DEPT.DepartmentName,
    POS.PositionTitle,
    COUNT(PROJ.ProjectID) AS NumberOfProjecTIMESHEET,
    SUM(TS.Hours) AS TotalHours
FROM
    Employees AS INFO
LEFT JOIN
    ProjectAssignments AS pa ON INFO.EmployeeID = pa.EmployeeID
LEFT JOIN
    Projects AS PROJ ON pa.ProjectID = PROJ.ProjectID
LEFT JOIN
    TimeSheets AS TS ON PROJ.ProjectID = TS.ProjectID
LEFT JOIN
    Departments AS DEPT ON INFO.DepartmentID = DEPT.DepartmentID
LEFT JOIN
    Positions AS POS ON INFO.PositionID = POS.PositionID
WHERE
    DEPT.DepartmentName IN ('IT', 'Finance', 'Marketing')
GROUP BY
    INFO.EmployeeID, DEPT.DepartmentName, POS.PositionTitle;


"""
