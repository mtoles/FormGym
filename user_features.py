from enum import Enum
from utils import *

### ENUMS ###


class ResidenceStatusEnum(Enum):
    Buying = "Buying"
    Renting = "Renting"
    LivingWithRelatives = "Living with relatives"
    Other = "Other"
    Own = "Own"


class LoanTypeEnum(Enum):
    Vehicle = "Vehicle"
    Personal = "Personal"
    Credit = "Credit"


class VehicleLoanConditionEnum(Enum):
    New = "New"
    Used = "Used"
    Refinance = "Refinance"


class VehicleLoanTypeEnum(Enum):
    Auto = "Auto"
    Boat = "Boat"
    Motorcycle = "Motorcycle"
    RV = "RV"
    TruckOrSUV = "Truck or SUV"
    Watercraft = "Watercraft"


class MarriageStatusEnum(Enum):
    Married = "Married"
    Single = "Single"
    Separated = "Separated"


class EnterpriseTypeEnum(Enum):
    Corporation = "Corporation"
    Partnership = "Partnership"
    Proprietorship = "Proprietorship"
    NoEnterprise = "No Enterprise Type"
    LLC = "LLC"


class GrossIncomePeriodEnum(Enum):
    Monthly = "Monthly"
    Yearly = "Yearly"


## USER ATTRIBUTES ###


class UserAttributeMeta(type):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_p_attr = super().__new__(cls, name, bases, attrs)
        if name not in  ["BaseUserAttr", "BaseUserDbAttr"]:
            assert name not in cls.registry, f"User attribute {name} already exists"
            cls.registry[name] = new_p_attr
        return new_p_attr


class UserProfile:
    def __init__(self, idx):
        class Features:
            pass

        self.features = Features()
        for name, attr_class in UserAttributeMeta.registry.items():
            if hasattr(attr_class, "options") and isinstance(attr_class.options, list):
                setattr(self.features, name, attr_class.options[idx])
            else:
                raise AttributeError(f"Class {name} must have an 'options' list.")

    def get_nl_profile(self):
        nl_profile = []
        for name, attr_class in UserAttributeMeta.registry.items():
            nl_profile.append(attr_class.nl_desc(getattr(self.features, name)))
        return nl_profile


class BaseUserAttr(metaclass=UserAttributeMeta):
    pass

class BaseUserDbAttr(metaclass=UserAttributeMeta):
    form_name, cell_id = __name__.split("_")
    @staticmethod
    def nl_desc(option):
        # form_name, cell_id = __class__.__name__.split("_")
        return f"The user's value for form {__class__.form_name} in cell {__class__.cell_id} ({__class__.__doc__}) is: {option}"


### AUTO LOAN FEATURES ###

class FirstName(BaseUserAttr):
    options = ["Lucas", "Ava", "Ethan", "Mia"]

    @staticmethod
    def nl_desc(option):
        return f"The user's first name is: {option}"


class LastName(BaseUserAttr):
    options = ["Reynolds", "Chen", "Patel", "Nguyen"]

    @staticmethod
    def nl_desc(option):
        return f"The user's last name is: {option}"


class MiddleName(BaseUserAttr):
    options = ["James", "Marie", "Olivia", "Daniel"]

    @staticmethod
    def nl_desc(option):
        return f"The user's middle name is: {option}"


class SocialSecurityNumber(BaseUserAttr):
    options = ["314-22-5612", "562-78-4132", "901-45-2796", "274-63-9185"]

    @staticmethod
    def nl_desc(option):
        return f"The user's social security number is: {option}"


class BirthYear(BaseUserAttr):
    options = ["1979", "1992", "1988", "2000"]

    @staticmethod
    def nl_desc(option):
        return f"The user's birth year is: {option}"


class BirthMonth(BaseUserAttr):
    options = ["2", "9", "12", "5"]

    @staticmethod
    def nl_desc(option):
        return f"The user's birth month is: {option}"


class BirthDay(BaseUserAttr):
    options = ["7", "19", "23", "30"]

    @staticmethod
    def nl_desc(option):
        return f"The user's birth day is: {option}"


class JointBirthYear(BaseUserAttr):
    options = ["1979", "1992", "1988", "2000"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's birth year is: {option}"


class JointBirthMonth(BaseUserAttr):
    options = ["02", "09", "12", "05"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's birth month is: {option}"


class JointBirthDay(BaseUserAttr):
    options = ["07", "19", "23", "30"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's birth day is: {option}"


class PhoneNumber(BaseUserAttr):
    options = ["310-555-7891", "415-555-2034", "202-555-6970", "646-555-0311"]

    @staticmethod
    def nl_desc(option):
        return f"The user's phone number is: {option}"


class CellPhone(BaseUserAttr):
    options = ["310-555-1499", "415-555-8282", "202-555-7788", "646-555-9666"]

    @staticmethod
    def nl_desc(option):
        return f"The user's cell phone is: {option}"


class EmailAddress(BaseUserAttr):
    options = [
        "lucas.work@example.com",
        "ava.personal@example.net",
        "ethan.home@example.org",
        "mia.contact@example.com",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's email address is: {option}"


class HouseNumber(BaseUserAttr):
    options = ["742", "315", "89", "251"]

    @staticmethod
    def nl_desc(option):
        return f"The user's house number is: {option}"


class StreetName(BaseUserAttr):
    options = ["Park Boulevard", "Heather Lane", "Cedar Court", "Magnolia Circle"]

    @staticmethod
    def nl_desc(option):
        return f"The user's street name is: {option}"


class City(BaseUserAttr):
    options = ["Brookhaven", "Fairview", "Hillside", "Willowdale"]

    @staticmethod
    def nl_desc(option):
        return f"The user's city is: {option}"


class State(BaseUserAttr):
    options = ["TX", "CA", "NJ", "GA"]

    @staticmethod
    def nl_desc(option):
        return f"The user's state is: {option}"


class Zip(BaseUserAttr):
    options = ["73301", "90007", "07030", "30301"]

    @staticmethod
    def nl_desc(option):
        return f"The user's zip code is: {option}"


class Country(BaseUserAttr):
    options = ["US"] * 4

    @staticmethod
    def nl_desc(option):
        return f"The user's country is: {option}"


class ResidenceStatus(BaseUserAttr):
    options = [
        ResidenceStatusEnum.Buying.value,
        ResidenceStatusEnum.Renting.value,
        ResidenceStatusEnum.LivingWithRelatives.value,
        ResidenceStatusEnum.Own.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's residence status ({", ".join([e.value for e in ResidenceStatusEnum])}) is: {option}"


class JointResidenceStatus(BaseUserAttr):
    options = [
        ResidenceStatusEnum.Renting.value,
        ResidenceStatusEnum.Other.value,
        ResidenceStatusEnum.Own.value,
        ResidenceStatusEnum.LivingWithRelatives.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's residence status ({", ".join([e.value for e in ResidenceStatusEnum])}) is: {option}"


class MortgageCompany(BaseUserAttr):
    options = [
        "Sunrise Mortgage LLC",
        "Oakwood Home Loans",
        "Guardian Mortgage Co.",
        "Stonegate Lending",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's mortgage company is: {option}"


class MonthlyMortgageOrRent(BaseUserAttr):
    options = ["$1,200", "$1,450", "$1,750", "$2,100"]

    @staticmethod
    def nl_desc(option):
        return f"The user's monthly mortgage or rent is: {option}"


class PreviousHouseNumber(BaseUserAttr):
    options = ["560", "912", "47", "893"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous house number is: {option}"


class PreviousStreetName(BaseUserAttr):
    options = ["Mulberry Rd", "Orchard St", "Pinecrest Dr", "Willow Way"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous street name is: {option}"


class PreviousCity(BaseUserAttr):
    options = ["Northfield", "Springview", "Lakeport", "Bayview"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous city is: {option}"


class PreviousState(BaseUserAttr):
    options = ["CO", "NC", "PA", "ME"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous state is: {option}"


class PreviousZip(BaseUserAttr):
    options = ["80203", "27601", "19019", "04401"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous zip code is: {option}"


class JointPreviousHouseNumber(BaseUserAttr):
    options = ["560", "912", "47", "893"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous house number is: {option}"


class JointPreviousStreetName(BaseUserAttr):
    options = ["Mulberry Rd", "Orchard St", "Pinecrest Dr", "Willow Way"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous street name is: {option}"


class JointPreviousCity(BaseUserAttr):
    options = ["Northfield", "Springview", "Lakeport", "Bayview"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous city is: {option}"


class JointPreviousState(BaseUserAttr):
    options = ["CO", "NC", "PA", "ME"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous state is: {option}"


class JointPreviousZip(BaseUserAttr):
    options = ["80203", "27601", "19019", "04401"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous zip code is: {option}"


class ReferenceName(BaseUserAttr):
    options = ["Cynthia Park", "Malik Evans", "Serena Lewis", "Diego Ramirez"]

    @staticmethod
    def nl_desc(option):
        return f"The user's reference's name is: {option}"


class ReferenceRelationship(BaseUserAttr):
    options = ["Sister", "Uncle", "Friend", "Cousin"]

    @staticmethod
    def nl_desc(option):
        return f"The user's reference's relationship is: {option}"


class Reference2Relationship(BaseUserAttr):
    options = ["Sister", "Uncle", "Friend", "Cousin"][::-1]

    @staticmethod
    def nl_desc(option):
        return f"The user's reference's relationship is: {option}"


class ReferenceHouseNumber(BaseUserAttr):
    options = ["4502", "128", "67", "999"]

    @staticmethod
    def nl_desc(option):
        return f"The user's reference's house number is: {option}"


class ReferenceStreetName(BaseUserAttr):
    options = ["Sunset Blvd", "Highland Ave", "Rivergate Ln", "Oak Terrace"]

    @staticmethod
    def nl_desc(option):
        return f"The user's reference's street name is: {option}"


class ReferenceCity(BaseUserAttr):
    options = ["Brighton", "Fairmont", "Riverside", "Rosewood"]

    @staticmethod
    def nl_desc(option):
        return f"The user's reference's city is: {option}"


class ReferenceState(BaseUserAttr):
    options = ["AZ", "KY", "OH", "ND"]

    @staticmethod
    def nl_desc(option):
        return f"The user's reference's state is: {option}"


class ReferenceZip(BaseUserAttr):
    options = ["85001", "40202", "43210", "58201"]

    @staticmethod
    def nl_desc(option):
        return f"The user's reference's zip code is: {option}"


class ReferencePhone(BaseUserAttr):
    options = ["310-555-0101", "415-555-2020", "202-555-3300", "646-555-4040"]

    @staticmethod
    def nl_desc(option):
        return f"The user's reference's phone number is: {option}"


class JointReferencePhone(BaseUserAttr):
    options = ["310-555-0202", "415-555-2021", "202-555-3301", "646-555-4041"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's reference's phone number is: {option}"


class Employment(BaseUserAttr):
    options = ["Data Scientist", "HR Manager", "Graphic Designer", "Account Executive"]

    @staticmethod
    def nl_desc(option):
        return f"The user's job title is: {option}"


class EmployeNamer(BaseUserAttr):
    options = [
        "Atlas Corp.",
        "Meridian Solutions",
        "NextGen Innovations",
        "Skyline Ventures",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The employer name is: {option}"


class LengthEmployed(BaseUserAttr):
    options = ["1 year", "3 years", "6 months", "9 years"]

    @staticmethod
    def nl_desc(option):
        return f"The user has been employed at their current job for: {option}"


class GrossMonthlyIncome(BaseUserAttr):
    options = ["$3,800", "$5,200", "$6,400", "$4,100"]

    @staticmethod
    def nl_desc(option):
        return f"The user's gross monthly income is: {option}"


class AdditionalIncome(BaseUserAttr):
    options = ["$400", "$900", "$1,100", "$600"]

    @staticmethod
    def nl_desc(option):
        return f"The user's additional monthly income is: {option}"


class IncomeSource(BaseUserAttr):
    options = ["Tutoring", "Online Sales", "Consulting", "Stock Dividends"]

    @staticmethod
    def nl_desc(option):
        return f"The user's additional income comes from: {option}"


class BankName(BaseUserAttr):
    options = ["MidFirst Bank", "KeyBank", "Fifth Third Bank", "PNC Bank"]

    @staticmethod
    def nl_desc(option):
        return f"The user's bank's name is: {option}"


class BankAccountNumber(BaseUserAttr):
    options = ["787412345", "341278945", "512709384", "109857236"]

    @staticmethod
    def nl_desc(option):
        return f"The user's bank account number is: {option}"


class BankruptcyStatus(BaseUserAttr):
    options = ["Yes", "No"]

    @staticmethod
    def nl_desc(option):
        return f"Has the user previously gone bankrupt: {option}"


class AutoCreditReference(BaseUserAttr):
    options = [
        "Experian",
        "Equifax",
        "TransUnion",
        "USA Credit",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's auto credit reference company is: {option}"


class AutoBalanceDue(BaseUserAttr):
    options = ["$5,200", "$9,700", "$14,300", "$6,600"]

    @staticmethod
    def nl_desc(option):
        return f"The user's remaining auto balance is: {option}"


class TradingInCar(BaseUserAttr):
    options = ["Yes", "No"]

    @staticmethod
    def nl_desc(option):
        return f"The user is trading in a car: {option}"


class RegisteredCarOwner(BaseUserAttr):
    options = ["Self", "Spouse"]

    @staticmethod
    def nl_desc(option):
        opt = "the user" if option == "Self" else "the user's spouse"
        return f"The new car will be registered with: {opt}"


class AutoAmountRequested(BaseUserAttr):
    options = ["$8,000", "$12,000", "$18,500", "$7,300"]

    @staticmethod
    def nl_desc(option):
        return f"The auto amount requested by the user is: {option}"


class Term(BaseUserAttr):
    options = ["24 months", "36 months", "48 months", "60 months"]

    @staticmethod
    def nl_desc(option):
        return f"The term of the auto loan is: {option}"


class Vin(BaseUserAttr):
    options = [
        "1GCHK292X1E123456",
        "WBA3B5G59FNR12345",
        "JM1BK343211234567",
        "2HKYF18794H123456",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The new vehicle VIN is: {option}"


class VehicleYear(BaseUserAttr):
    options = ["2019", "2020", "2021", "2022"]

    @staticmethod
    def nl_desc(option):
        return f"The new vehicle year is: {option}"


class VehicleMake(BaseUserAttr):
    options = ["Hyundai", "Subaru", "Volkswagen", "Nissan"]

    @staticmethod
    def nl_desc(option):
        return f"The new vehicle make is: {option}"


class VehicleModel(BaseUserAttr):
    options = ["Elantra", "Outback", "Golf", "Sentra"]

    @staticmethod
    def nl_desc(option):
        return f"The new vehicle model is: {option}"


class VehicleMiles(BaseUserAttr):
    options = ["12,345", "22,678", "35,890", "9,450"]

    @staticmethod
    def nl_desc(option):
        return f"The miles on the new vehicle is: {option}"


class ApplyingWithJointCredit(BaseUserAttr):
    options = ["Yes", "No"]

    @staticmethod
    def nl_desc(option):
        return f"Is the user applying with joint filer's credit: {option}"


class Age(BaseUserAttr):
    options = ["22", "34", "41", "57"]

    @staticmethod
    def nl_desc(option):
        return f"The user's age is: {option}"


class HomePhoneNumber(BaseUserAttr):
    options = ["209-555-1112", "307-555-3344", "469-555-5566", "762-555-7788"]

    @staticmethod
    def nl_desc(option):
        return f"The user's home phone number is: {option}"


class CellPhoneNumber(BaseUserAttr):
    options = ["209-555-9922", "307-555-8734", "469-555-1133", "762-555-8877"]

    @staticmethod
    def nl_desc(option):
        return f"The user's cell phone number is: {option}"


class JointFirstName(BaseUserAttr):
    options = ["Mary", "Peter", "Emily", "Adam"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's first name is: {option}"


class JointMiddleName(BaseUserAttr):
    options = ["Elara", "Kaia", "Niamh", "Sage"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's middle name is: {option}"


class JointLastName(BaseUserAttr):
    options = ["Connors", "Smith", "Mills", "Jones"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's last name is: {option}"


class JointAge(BaseUserAttr):
    options = ["29", "36", "50", "61"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's age is: {option}"


class JointHomePhoneNumber(BaseUserAttr):
    options = ["208-555-1234", "308-555-5678", "469-555-9012", "763-555-3456"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's home phone number is: {option}"


class JointEmailAddress(BaseUserAttr):
    options = [
        "maryconnors@example.com",
        "petersmith@example.com",
        "emilymills@example.com",
        "adamjones@example.com",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's email address is: {option}"


class JointCellPhoneNumber(BaseUserAttr):
    options = ["208-555-8888", "308-555-5670", "469-555-9010", "763-555-3400"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's cell phone number is: {option}"


class JointCity(BaseUserAttr):
    options = ["Clearwater", "Riverton", "Maplewood", "Eastfield"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's city is: {option}"


class JointHouseNumber(BaseUserAttr):
    options = ["123", "456", "789", "101"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's house number is: {option}"


class JointStreetName(BaseUserAttr):
    options = ["Main st.", "Second st.", "Third ave.", "Fourth ave."]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's street name is: {option}"


class JointState(BaseUserAttr):
    options = ["FL", "WA", "NY", "CA"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's state is: {option}"


class JointZip(BaseUserAttr):
    options = ["60608", "98008", "10029", "35006"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's zip code is: {option}"


class JointSocialSecurityNumber(BaseUserAttr):
    options = ["111-22-3344", "445-66-7788", "221-33-4455", "778-89-9900"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's social security number is: {option}"


class TimeAtAddressYears(BaseUserAttr):
    options = ["1", "3", "4", "7"]

    @staticmethod
    def nl_desc(option):
        return f"The years the user has been at this address: {option}"


class TimeAtAddressMonths(BaseUserAttr):
    options = ["2", "5", "8", "10"]

    @staticmethod
    def nl_desc(option):
        return f"The months the user has been at this address: {option}"


class JointTimeAtAddressYears(BaseUserAttr):
    options = ["2", "4", "6", "9"]

    @staticmethod
    def nl_desc(option):
        return f"The years the joint filer has been at this address: {option}"


class JointTimeAtAddressMonths(BaseUserAttr):
    options = ["3", "6", "9", "11"]

    @staticmethod
    def nl_desc(option):
        return f"The months the joint filer has been at this address: {option}"


class MortgageCompanyLandlord(BaseUserAttr):
    options = [
        "BrightStar Mortgage",
        "BlueRiver Realty",
        "Prime Homes Rentals",
        "Heritage Lending",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The mortgage company or landlord is: {option}"


class JointMortgageCompanyLandlord(BaseUserAttr):
    options = [
        "Pinecone Mortgage",
        "Horizon Realty",
        "Metro Homes Rentals",
        "Summit Lending",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's mortgage company or landlord is: {option}"


class JointMortgageRent(BaseUserAttr):
    options = ["$900", "$1,100", "$1,400", "$2,000"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's monthly mortgage rent is: {option}"


class PreviousResidenceStatus(BaseUserAttr):
    options = [
        ResidenceStatusEnum.Other.value,
        ResidenceStatusEnum.Buying.value,
        ResidenceStatusEnum.Renting.value,
        ResidenceStatusEnum.LivingWithRelatives.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's most recent previous residence status ({", ".join([e.value for e in ResidenceStatusEnum])}) is: {option}"


class JointPreviousResidenceStatus(BaseUserAttr):
    options = [
        ResidenceStatusEnum.LivingWithRelatives.value,
        ResidenceStatusEnum.Other.value,
        ResidenceStatusEnum.Buying.value,
        ResidenceStatusEnum.Renting.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's most recent previous residence status ({", ".join([e.value for e in ResidenceStatusEnum])}) is: {option}"


class TimeAtPreviousAddressYears(BaseUserAttr):
    options = ["1", "2", "4", "6"]

    @staticmethod
    def nl_desc(option):
        return f"The user's time at previous address in years is: {option}"


class TimeAtPreviousAddressMonths(BaseUserAttr):
    options = ["1", "4", "7", "11"]

    @staticmethod
    def nl_desc(option):
        return f"The user's time at previous address in months is: {option}"


class JointTimeAtPreviousAddressYears(BaseUserAttr):
    options = ["1", "3", "5", "7"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's time at previous address in years is: {option}"


class JointTimeAtPreviousAddressMonths(BaseUserAttr):
    options = ["2", "5", "8", "12"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's time at previous address in months is: {option}"


class ReferenceCellPhone(BaseUserAttr):
    options = ["310-555-0000", "415-555-1111", "202-555-2222", "646-555-3333"]

    @staticmethod
    def nl_desc(option):
        return f"The user's reference's cell phone is: {option}"


class ReferenceHomePhone(BaseUserAttr):
    options = ["310-555-4444", "415-555-5555", "202-555-6666", "646-555-7777"]

    @staticmethod
    def nl_desc(option):
        return f"The user's reference's home phone is: {option}"


class JointReferenceFirstName(BaseUserAttr):
    options = ["Derek", "Hannah", "Gabriel", "Nina"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's reference's first name is: {option}"


class JointReferenceLastName(BaseUserAttr):
    options = ["Bennett", "Peterson", "Martinez", "Foster"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's reference's last name is: {option}"


class JointReferenceRelationship(BaseUserAttr):
    options = ["Father", "Sister", "Friend", "Cousin"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's reference's relationship is: {option}"


class JointReferenceHouseNumber(BaseUserAttr):
    options = ["510", "808", "72", "43"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's reference's house number is: {option}"


class JointReferenceStreetName(BaseUserAttr):
    options = ["Evergreen Rd", "Silver Lake Dr", "Crescent Ave", "Sunrise Blvd"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's reference's street name is: {option}"


class JointReferenceCity(BaseUserAttr):
    options = ["Springfield", "Havenport", "Lakeshire", "Brightvale"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's reference's city is: {option}"


class JointReferenceState(BaseUserAttr):
    options = ["SC", "UT", "AK", "LA"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's reference's state is: {option}"


class JointReferenceZip(BaseUserAttr):
    options = ["29201", "84321", "99501", "70112"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's reference's zip code is: {option}"


class JointReferenceCellPhone(BaseUserAttr):
    options = ["210-555-8888", "414-555-9999", "203-555-1010", "641-555-1111"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's reference's cell phone is: {option}"


class JointReferenceHomePhone(BaseUserAttr):
    options = ["210-555-1212", "414-555-3434", "203-555-5656", "641-555-7878"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's reference's home phone is: {option}"


class Reference2Name(BaseUserAttr):
    options = ["Ana Wilson", "Corey Bell", "Tanya Singh", "Oscar Phillips"]

    @staticmethod
    def nl_desc(option):
        return f"The user's second reference's name is: {option}"


class Reference2HouseNumber(BaseUserAttr):
    options = ["2211", "654", "899", "1420"]

    @staticmethod
    def nl_desc(option):
        return f"The user's second reference's house number is: {option}"


class Reference2StreetName(BaseUserAttr):
    options = ["Lakewood Dr", "Vine St", "Forest Ave", "Kingston Rd"]

    @staticmethod
    def nl_desc(option):
        return f"The user's second reference's street name is: {option}"


class Reference2City(BaseUserAttr):
    options = ["Madison", "Rockford", "Bloomfield", "Lincoln Park"]

    @staticmethod
    def nl_desc(option):
        return f"The user's second reference's city is: {option}"


class Reference2State(BaseUserAttr):
    options = ["WI", "IL", "MI", "NJ"]

    @staticmethod
    def nl_desc(option):
        return f"The user's second reference's state is: {option}"


class Reference2Zip(BaseUserAttr):
    options = ["53703", "61107", "48302", "07052"]

    @staticmethod
    def nl_desc(option):
        return f"The user's second reference's zip code is: {option}"


class Reference2CellPhone(BaseUserAttr):
    options = ["240-333-3333", "241-444-4444", "242-555-5555", "243-666-6666"]

    @staticmethod
    def nl_desc(option):
        return f"The user's second reference's cell phone is: {option}"


class Reference2HomePhone(BaseUserAttr):
    options = ["240-111-1111", "241-222-2222", "242-777-7777", "243-888-8888"]

    @staticmethod
    def nl_desc(option):
        return f"The user's second reference's home phone is: {option}"


class JointReference2Name(BaseUserAttr):
    options = ["Lucille Gray", "Tyler Morgan", "Fiona Cruz", "Adrian Lopez"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's second reference's name is: {option}"


class JointReference2FullAddress(BaseUserAttr):
    options = [
        "988 South Oak Dr, Glendale, CA, 91204",
        "530 West Pine Ln, Troy, MI, 48083",
        "234 Maple Circle, Bentonville, AR, 72712",
        "1608 Birch Ave, Orlando, FL, 32801",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's second reference's full address is: {option}"


class JointReference2CellPhone(BaseUserAttr):
    options = ["270-999-9999", "271-123-1234", "272-456-4567", "273-789-7890"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's second reference's cell phone is: {option}"


class JointReference2HomePhone(BaseUserAttr):
    options = ["274-234-2345", "275-345-3456", "276-567-5678", "277-678-6789"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's second reference's home phone is: {option}"


class EmployerName(BaseUserAttr):
    options = [
        "BrightTech Solutions",
        "Crest Marketing",
        "Secure Finances",
        "Transit Logistics",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's employer's name is: {option}"


class EmployerLengthYears(BaseUserAttr):
    options = ["1", "3", "5", "9"]

    @staticmethod
    def nl_desc(option):
        return f"The user's years at their current employer is: {option}"


class EmployerPosition(BaseUserAttr):
    options = [
        "Software Engineer",
        "Marketing Manager",
        "Financial Analyst",
        "Project Coordinator",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's current job title is: {option}"


class EmployerWorkPhone(BaseUserAttr):
    options = ["310-555-7211", "415-555-9222", "202-555-7333", "646-555-8444"]

    @staticmethod
    def nl_desc(option):
        return f"The user's work phone is: {option}"


class JointEmployerName(BaseUserAttr):
    options = ["DeltaTech Corp", "Zenith Consulting", "Lunar Finance", "Apex Partners"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's employer's name is: {option}"


class JointEmployerCity(BaseUserAttr):
    options = ["Weston", "Bridgeport", "Fairford", "Millcreek"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's employer's city is: {option}"


class JointEmployerLengthYears(BaseUserAttr):
    options = ["2", "4", "6", "10"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's years at their current employer is: {option}"


class JointEmployerPosition(BaseUserAttr):
    options = ["Supervisor", "Manager", "Analyst", "Director"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's current job title is: {option}"


class JointEmployerWorkPhone(BaseUserAttr):
    options = ["310-555-5559", "415-555-6667", "202-555-7774", "646-555-8883"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's work phone is: {option}"


class JointGrossMonthlyIncome(BaseUserAttr):
    options = ["$2,800", "$4,200", "$5,000", "$5,900"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's gross monthly income is: {option}"


class AdditionalIncomeSource(BaseUserAttr):
    options = ["Freelancing", "Part-time Tutoring", "Investments", "Online Business"]

    @staticmethod
    def nl_desc(option):
        return f"The user's additional monthly income source is: {option}"


class AdditionalMonthlyIncome(BaseUserAttr):
    options = ["$300", "$600", "$1,200", "$900"]

    @staticmethod
    def nl_desc(option):
        return f"The user's additional monthly income is: {option}"


class JointAdditionalIncomeSource(BaseUserAttr):
    options = ["Child Support", "Small Business", "Online Sales", "Stocks/Dividends"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's additional income source is: {option}"


class JointAdditionalMonthlyIncome(BaseUserAttr):
    options = ["$400", "$800", "$1,300", "$700"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's additional monthly income is: {option}"


class PreviousEmployerName(BaseUserAttr):
    options = [
        "Sunrise Tech",
        "Green Leaf Marketing",
        "Balanced Finance Group",
        "LogiPlus",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous employer name is: {option}"


class PreviousEmployerCity(BaseUserAttr):
    options = ["Somerset", "Eagleton", "Ridgeville", "Clayton"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous employer city is: {option}"


class PreviousEmployerPosition(BaseUserAttr):
    options = ["Clerk", "Analyst", "Manager", "Supervisor"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous employer position is: {option}"


class PreviousLengthEmployed(BaseUserAttr):
    options = ["8 months", "1 year", "2 years", "4 years"]

    @staticmethod
    def nl_desc(option):
        # return f"The user's : {option}"
        return f"The user was employed at their previous position for: {option}"


class JointPreviousEmployerName(BaseUserAttr):
    options = [
        "Moonlight Software",
        "Terrace Marketing",
        "New Age Finance",
        "Global Express",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer was employed at their previous position for: {option}"


class JointPreviousEmployerCity(BaseUserAttr):
    options = ["Bartlett", "Waterford", "Sanford", "Coralview"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous employer's city is: {option}"


class JointPreviousEmployerPosition(BaseUserAttr):
    options = ["Clerk", "Analyst", "Manager", "Supervisor"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous employer's position is: {option}"


class JointPreviousLengthEmployed(BaseUserAttr):
    options = ["8 months", "1 year", "2 years", "4 years"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer was previously employed for: {option}"


class BankAddress(BaseUserAttr):
    options = [
        "430 Mason St, Dallas, TX, 75202",
        "902 Redwood Ave, Seattle, WA, 98109",
        "123 Pine Circle, Denver, CO, 80202",
        "567 Oak Blvd, Miami, FL, 33131",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's bank's address is: {option}"


class JointBankName(BaseUserAttr):
    options = ["Union Bank", "HSBC", "BB&T", "SunTrust"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's bank's name is: {option}"


class JointBankAddress(BaseUserAttr):
    options = [
        "210 Elm St, Boston, MA, 02108",
        "781 Maple Ln, Portland, OR, 97205",
        "345 Alder Ave, Chicago, IL, 60611",
        "190 Redwood Dr, Phoenix, AZ, 85004",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's bank's address is: {option}"


class JointBankAccountNumber(BaseUserAttr):
    options = ["511111111", "522222222", "533333333", "544444444"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's bank's account number is: {option}"


class BankruptcyYear(BaseUserAttr):
    options = ["2015", "2018", "2020", "2022"]

    @staticmethod
    def nl_desc(option):
        return f"The user went bankrupt in: {option}"


class JointBankruptcyStatus(BaseUserAttr):
    options = ["Yes", "No"]

    @staticmethod
    def nl_desc(option):
        return f"Has the joint filer previously gone bankrupt: {option}"


class JointBankruptcyYear(BaseUserAttr):
    options = ["None", "2018", "2020", "2022"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer went bankrupt in: {option}"


class TodaysDate(BaseUserAttr):
    options = ["02/17/2023", "07/10/2023", "11/28/2024", "03/06/2025"]

    @staticmethod
    def nl_desc(option):
        return f"Today's date is (MM/DD/YYYY): {option}"


class LoanType(BaseUserAttr):
    options = [o.value for o in list(LoanTypeEnum) * 4]

    @staticmethod
    def nl_desc(option):
        return f"The user's loan type is: {option}"


class VehicleLoanCondition(BaseUserAttr):
    options = [o.value for o in VehicleLoanConditionEnum]

    @staticmethod
    def nl_desc(option):
        return f"The condition of the user's trade-in vehicle is: {option}"


class VehicleLoanType(BaseUserAttr):
    options = [o.value for o in VehicleLoanTypeEnum]

    @staticmethod
    def nl_desc(option):
        return f"The user is applying for a loan to buy a: {option}"


class PersonalAmountRequested(BaseUserAttr):
    options = ["None", "None", "None", "None"]

    @staticmethod
    def nl_desc(option):
        return f"The amount the user is requesting for a personal loan is: {option}"


class CreditAmountRequested(BaseUserAttr):
    options = ["None", "None", "None", "None"]

    @staticmethod
    def nl_desc(option):
        return f"The amount the user is requesting for a line of credit is: {option}"


class CreditLoanPurpose(BaseUserAttr):
    options = ["None", "None", "None", "None"]

    @staticmethod
    def nl_desc(option):
        return f"The purpose the user is requesting for a line of credit is: {option}"


class PersonalLoanPurpose(BaseUserAttr):
    options = ["None", "None", "None", "None"]

    @staticmethod
    def nl_desc(option):
        return f"The purpose the user is requesting for a personal loan is: {option}"


class AfcuAccountNo(BaseUserAttr):
    options = ["72340865", "72340866", "72340867", "72340868"]

    @staticmethod
    def nl_desc(option):
        return f"The user's AFCU account number is: {option}"


class JointAfcuAccountNo(BaseUserAttr):
    options = ["69749832", "69749833", "69749834", "69749835"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's AFCU account number is: {option}"


class EmployerHouseNumber(BaseUserAttr):
    options = ["2551", "4821", "16", "156"]

    @staticmethod
    def nl_desc(option):
        return f"The user's employer's house number is: {option}"


class JointEmployerHouseNumber(BaseUserAttr):
    options = ["2273", "Po Box 573", "1005", "138"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's employer's house number is: {option}"


class EmployerStreetName(BaseUserAttr):
    options = ["Vista Dr", "Ridge Top Cir", "Rr 2", "Michael Ct"]

    @staticmethod
    def nl_desc(option):
        return f"The user's employer's street name is: {option}"


class JointEmployerStreetName(BaseUserAttr):
    options = ["Cox Rd", "Woodlands Cv", "Patterson Dr"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's employer's street name is: {option}"


class EmployerCity(BaseUserAttr):
    options = ["Juneau", "Anchorage", "Ketchikan", "Anchorage"]

    @staticmethod
    def nl_desc(option):
        return f"The user's employer's city is: {option}"


class EmployerState(BaseUserAttr):
    options = ["AK", "AK", "AK", "AK"]

    @staticmethod
    def nl_desc(option):
        return f"The user's employer's state is: {option}"


class JointEmployerState(BaseUserAttr):
    options = ["AL", "AL", "AL", "AL"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's employer's state is: {option}"


class EmployerZip(BaseUserAttr):
    options = ["99801", "99508", "99901", "99504"]

    @staticmethod
    def nl_desc(option):
        return f"The user's employer's zip is: {option}"


class JointEmployerZip(BaseUserAttr):
    options = ["36832", "35671", "35080", "36040"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's employer's zip is: {option}"


class EmployerHireDate(BaseUserAttr):
    options = ["01/01/2000", "01/01/2001", "01/01/2002", "01/01/2003"]

    @staticmethod
    def nl_desc(option):
        return f"The user's hire date at their current employer is: {option}"


class JointEmployerHireDate(BaseUserAttr):
    options = ["02/02/2000", "02/02/2001", "02/02/2002", "02/02/2003"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's hire date at their current employer is: {option}"


class EmployerLengthMonths(BaseUserAttr):
    options = [
        # must match `EmployerHireDate`
        str(25 * 12),
        str(24 * 12),
        str(23 * 12),
        str(22 * 12),
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user has been working for their current employer for (months): {option}"


class JointEmployerLengthMonths(BaseUserAttr):
    options = [
        # must match `JointEmployerHireDate`
        str(25 * 12 - 1),
        str(24 * 12 - 1),
        str(23 * 12 - 1),
        str(22 * 12 - 1),
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer has been working for their current employer for (months): {option}"


class DriversLicenseNo(BaseUserAttr):
    options = ["4789109349", "4789109348", "4789109347", "4789109346"]

    @staticmethod
    def nl_desc(option):
        return f"The user's driver license number is: {option}"


class JointDriversLicenseNo(BaseUserAttr):
    options = ["4789109345", "4789109344", "4789109343", "4789109342"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's driver license number is: {option}"


class DriversLicenseExpirationDate(BaseUserAttr):
    options = ["01/01/2030", "01/01/2031", "01/01/2032", "01/01/2033"]

    @staticmethod
    def nl_desc(option):
        return f"The user's driver license expiration date is: {option}"


class JointDriversLicenseExpirationDate(BaseUserAttr):
    options = ["02/02/2030", "02/02/2031", "02/02/2032", "02/02/2033"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's driver license expiration date is: {option}"


class DriversLicenseState(BaseUserAttr):
    options = ["AK", "AL", "AR", "AZ"]

    @staticmethod
    def nl_desc(option):
        return f"The user's driver license state is: {option}"


class JointDriversLicenseState(BaseUserAttr):
    options = ["CA", "CO", "CT", "DC"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's driver license state is: {option}"


class MarriageStatus(BaseUserAttr):
    options = [o.value for o in MarriageStatusEnum]

    @staticmethod
    def nl_desc(option):
        return f"The user's marriage status is: {option}"


class JointMarriageStatus(BaseUserAttr):
    options = [o.value for o in MarriageStatusEnum][::-1]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's marriage status is: {option}"


class NumDependents(BaseUserAttr):
    options = ["0", "1", "2", "3"]

    @staticmethod
    def nl_desc(option):
        return f"The user's dependents number: {option}"


class JointNumDependents(BaseUserAttr):
    options = ["4", "5", "6", "7"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's dependents number: {option}"


class Suffix(BaseUserAttr):
    options = [
        "Jr.",
        "Sr.",
        "",
        "",
    ]

    @staticmethod
    def nl_desc(option):
        if option == "":
            option = "no suffix"
        return f"The user's suffix is: {option}"


class JointSuffix(BaseUserAttr):
    options = [
        "",
        "",
        "Sr.",
        "Jr.",
    ]

    @staticmethod
    def nl_desc(option):
        if option == "":
            option = "no suffix"
        return f"The joint filer's suffix is: {option}"


class EnterpriseType(BaseUserAttr):
    options = ["N/A"] * 4

    @staticmethod
    def nl_desc(option):
        return f"The user's enterprise type (for the purpose of auto loan applications) is: {option}"


class BusinessType(BaseUserAttr):
    options = [
        "Not a business",
    ] * 4

    @staticmethod
    def nl_desc(option):
        return f"The user's business type (for the purpose of auto loan applications) is: {option}"


class TimeInBusinessYears(BaseUserAttr):
    options = ["N/A"] * 4

    @staticmethod
    def nl_desc(option):
        if option == "":
            option = "N/A"
        return f"The user's time in business (for the purpose of auto loan applications) is: {option}"


class TimeInBusinessMonths(BaseUserAttr):
    options = ["N/A"] * 4

    @staticmethod
    def nl_desc(option):
        if option == "":
            option = "N/A"
        return f"The user's time in business (for the purpose of auto loan applications) is: {option}"


class JointEnterpriseType(BaseUserAttr):
    options = ["N/A"] * 4

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's enterprise type (for the purpose of auto loan applications) is: {option}"


class JointBusinessType(BaseUserAttr):
    options = [
        "Not a business",
    ] * 4

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's business type (for the purpose of auto loan applications) is: {option}"


class JointTimeInBusinessYears(BaseUserAttr):
    options = ["N/A"] * 4

    @staticmethod
    def nl_desc(option):
        if option == "":
            option = "N/A"
        return f"The joint filer's time in business (for the purpose of auto loan applications) is: {option}"


class JointTimeInBusinessMonths(BaseUserAttr):
    options = ["N/A"] * 4

    @staticmethod
    def nl_desc(option):
        if option == "":
            option = "N/A"
        return f"The joint filer's time in business (for the purpose of auto loan applications) is: {option}"


class GrossIncomePeriod(BaseUserAttr):
    options = [
        GrossIncomePeriodEnum.Monthly.value,
        GrossIncomePeriodEnum.Yearly.value,
    ] * 4

    @staticmethod
    def nl_desc(option):
        return f"The user's gross income period is: {option}"


class JointGrossIncomePeriod(BaseUserAttr):
    options = [
        GrossIncomePeriodEnum.Yearly.value,
        GrossIncomePeriodEnum.Monthly.value,
    ] * 4

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's gross income period is: {option}"

### CONSOLIDATED REPORT OF INCOME FEATURES ###
class CROI_4435(BaseUserDbAttr):
    """1.a.(1)(a): Loans secured by 1–4 family residential properties"""
    options = ["23456", "34567", "45678", "56789"]

class CROI_4436(BaseUserDbAttr):
    """1.a.(1)(b): All other loans secured by real estate"""
    options = ["67890", "78901", "89012", "90123"]

class CROI_4012(BaseUserDbAttr):
    """1.a.(2): Commercial and industrial loans"""
    options = ["11234", "22345", "33456", "44567"]

class CROI_B485(BaseUserDbAttr):
    """1.a.(3)(a): Credit cards"""
    options = ["55678", "66789", "77890", "88901"]

class CROI_4058(BaseUserDbAttr):
    """1.a.(5): All other loans"""
    options = ["99012", "10123", "21234", "32345"]

class CROI_4010(BaseUserDbAttr):
    """1.a.(6): Total interest and fee income on loans"""
    options = ["43456", "54567", "65678", "76789"]

class CROI_4065(BaseUserDbAttr):
    """1.b: Income from lease financing receivables"""
    options = ["87890", "98901", "10912", "21023"]

class CROI_4115(BaseUserDbAttr):
    """1.c: Interest income on balances due from depository institutions"""
    options = ["31134", "42245", "53356", "64467"]

class CROI_B488(BaseUserDbAttr):
    """1.d.(1): U.S. Treasury securities and U.S. Government agency obligations"""
    options = ["75578", "86689", "97790", "10891"]

class CROI_B489(BaseUserDbAttr):
    """1.d.(2): Mortgage-backed securities"""
    options = ["21902", "32013", "42124", "52235"]

class CROI_4020(BaseUserDbAttr):
    """1.f: Interest income on federal funds sold and securities purchased under agreements to resell"""
    options = ["62346", "72457", "82568", "92679"]

class CROI_4518(BaseUserDbAttr):
    """1.g: Other interest income"""
    options = ["10234", "21345", "32456", "43567"]

class CROI_4107(BaseUserDbAttr):
    """1.h: Total interest income"""
    options = ["54678", "65789", "76890", "87901"]

class CROI_4508(BaseUserDbAttr):
    """2.a.(1): Interest on deposits - transaction accounts"""
    options = ["98012", "10123", "21234", "32345"]

class CROI_0093(BaseUserDbAttr):
    """2.a.(2)(a): Savings deposits (includes MMDAs)"""
    options = ["43456", "54567", "65678", "76789"]

class CROI_HK03(BaseUserDbAttr):
    """2.a.(2)(b): Time deposits of $250,000 or less"""
    options = ["87890", "98901", "10912", "21023"]

class CROI_HK04(BaseUserDbAttr):
    """2.a.(2)(c): Time deposits of more than $250,000"""
    options = ["31134", "42245", "53356", "64467"]

class CROI_4180(BaseUserDbAttr):
    """2.b: Expense of federal funds purchased and securities sold under agreements to repurchase"""
    options = ["75578", "86689", "97790", "10891"]

class CROI_4185(BaseUserDbAttr):
    """2.c: Interest on trading liabilities and other borrowed money"""
    options = ["21902", "32013", "42124", "52235"]

