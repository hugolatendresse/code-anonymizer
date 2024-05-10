longquery = """

SELECT
    info.EmployeeID,
    COUNT(proj.ProjectID) AS NumberOfProjects,
    SUM(ts.Hours) AS TotalHours,
FROM
    Employees info
LEFT JOIN
    Projects proj ON pa.ProjectID = proj.ProjectID
LEFT JOIN
    TimeSheets ts ON proj.ProjectID = ts.ProjectID
WHERE
    dept.DepartmentName IN ('IT', 'Finance', 'Marketing')
GROUP BY
    info.EmployeeID, dept.DepartmentName, pos.PositionTitle
LIMIT 10;

"""
