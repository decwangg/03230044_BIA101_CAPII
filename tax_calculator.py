
class Person:
    def __init__(self, name, age, marital_status, org_type=None, emp_type=None, salary=None, has_children=False, children_in_school=False, num_children_in_school=0):
        self.name = name
        self.age = age
        self.marital_status = marital_status
        self.org_type = org_type
        self.emp_type = emp_type
        self.salary = salary
        self.has_children = has_children
        self.children_in_school = children_in_school
        self.num_children_in_school = num_children_in_school

class Employee(Person):
    def __init__(self, name, age, marital_status, org_type, emp_type, salary, has_children, children_in_school, num_children_in_school):
        super().__init__(name, age, marital_status)
        self.org_type = org_type
        self.emp_type = emp_type
        self.salary = salary
        self.has_children = has_children
        self.children_in_school = children_in_school
        self.num_children_in_school = num_children_in_school

class TaxCalculator:
    def __init__(self, employee):
        self.employee = employee
        self.pit = self.calculate_pit()
        self.surcharge = self.calculate_surcharge()
        self.total_tax = self.pit + self.surcharge
        self.bonus = self.calculate_bonus()
        self.provident_fund = self.calculate_provident_fund()

    def calculate_pit(self):
        if self.employee.age < 18:
            return 0
        if self.employee.salary < 300000:
            return 0

        tax_brackets = [
            (300000, 400000, 0.1),
            (400001, 650000, 0.15),
            (650001, 1000000, 0.2),
            (1000001, 1500000, 0.25),
            (1500001, float('inf'), 0.3)
        ]

        pit = 0
        remaining_income = self.employee.salary

        for lower, upper, rate in tax_brackets:
            if remaining_income <= lower:
                break
            if remaining_income > upper - lower:
                pit += (upper - lower) * rate
                remaining_income -= upper - lower
            else:
                pit += remaining_income * rate
                remaining_income = 0

        return pit

    def calculate_surcharge(self):
        if self.pit >= 1000000:
            return self.pit * 0.1
        else:
            return 0

    def calculate_bonus(self):
        if self.employee.emp_type == 'Regular':
            bonus_rate = 0.1  # 10% bonus will be given to regular employees
        else:
            bonus_rate = 0.05  # 5% bonus will be given to contract employees
        bonus = self.employee.salary * bonus_rate
        return bonus

    def calculate_provident_fund(self):
        provident_fund = 0
        if self.employee.emp_type == 'Regular':
            if self.employee.org_type == 'Government':
                provident_fund_rate = 0.05  # 5% will be given to regular employees of government organizations
            else:
                provident_fund_rate = 0.1  # 10% will be given to regular employees of private/corporate organizations
            provident_fund = self.employee.salary * provident_fund_rate
        elif self.employee.org_type != 'Government':
            provident_fund_rate = 0.05  # 5% will be given to contract employees of private/corporate organizations
            provident_fund = self.employee.salary * provident_fund_rate
        return provident_fund

class Deductions:
    def __init__(self, employee):
        self.employee = employee
        self.deductions = self.calculate_deductions()

    def calculate_deductions(self):
        deductions = 0
        if self.employee.emp_type == 'Regular':
            if self.employee.org_type == 'Government':
                deductions += min(self.employee.salary * 0.1, 350000)  # NPPF
            else:
                deductions += min(self.employee.salary * 0.1, 350000)  # NPPF
            deductions += 200 * 12  # GIS (200 per month)

        if self.employee.marital_status and self.employee.has_children:
            if self.employee.children_in_school:
                deductions += min(350000 * self.employee.num_children_in_school, 350000 * 5)  # Education allowance
            else:
                deductions += 350000  # Education allowance for a child

        deductions += min(350000, self.employee.salary * 0.05)  # Donations
        deductions += min(self.employee.salary * 0.1, 350000)  # Life insurance premium
        deductions += min(350000, self.employee.salary * 0.05)  # Self-education allowance

        return deductions


name = input("Enter your name: ")
age = int(input("Enter your age: "))

# If age is less than 18, we will skip the calculations
if age < 18:
    print("You are below 18 years of age, so you don't need to pay any tax.")
else:
    marital_status = input("Are you married? (Yes/No): ").lower() == 'yes'
    org_type = input("Enter your organization type (Government/Private/Corporate): ").lower()
    emp_type = input("Enter your employee type (Regular/Contract): ").lower()
    salary = int(input("Enter your salary: "))
    has_children = False
    children_in_school = False
    num_children_in_school = 0

    if marital_status:
        has_children = input("Do you have children? (Yes/No): ").lower() == 'yes'
        if has_children:
            children_in_school = input("Are your children going to school? (Yes/No): ").lower() == 'yes'
            if children_in_school:
                num_children_in_school = int(input("Enter the number of children going to school: "))

    person = Person(name, age, marital_status)
    employee = Employee(name, age, marital_status, org_type, emp_type, salary, has_children, children_in_school, num_children_in_school)
    deductions = Deductions(employee)
    tax_calculator = TaxCalculator(employee)

    print(f"Name: {employee.name}")
    print(f"Organization Type: {employee.org_type}")
    print(f"Employee Type: {employee.emp_type}")
    print(f"Age: {employee.age}")
    print(f"Marital Status: {'Married' if employee.marital_status else 'Single'}")
    print(f"Has Children: {'Yes' if employee.has_children else 'No'}")

    if employee.has_children:
        print(f"Children in School: {'Yes' if employee.children_in_school else 'No'}")
        if employee.children_in_school:
            print(f"Number of Children in School: {num_children_in_school}")

    print(f"Salary: {employee.salary}")
    print(f"Deductions: {deductions.deductions}")
    print(f"Personal Income Tax (PIT): {tax_calculator.pit}")
    print(f"Surcharge: {tax_calculator.surcharge}")
    print(f"Total Tax Payable: {tax_calculator.total_tax}")
    print(f"Bonus: {tax_calculator.bonus}")

    