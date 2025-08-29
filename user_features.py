from enum import Enum
from utils import *

### ENUMS ###


class TypeOfContractEnum(Enum):
    Lease = "Lease"
    Installment = "Installment"


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
    PrivateParty = "Private Party"


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
    Divorced = "Divorced"  # don't give profiles divorced (form logic clash)


class EnterpriseTypeEnum(Enum):
    Corporation = "Corporation"
    Partnership = "Partnership"
    Proprietorship = "Proprietorship"
    NoEnterprise = "No Enterprise Type"
    LLC = "LLC"


class GrossIncomePeriodEnum(Enum):
    Monthly = "Monthly"
    Yearly = "Yearly"


class ProceedsTypeEnum(Enum):
    DebtConsolidation = "Debt Consolidation"
    Other = "Other"


class PreferredPhoneEnum(Enum):
    Home = "Home"
    Work = "Work"
    Cell = "Cell"


class YesNoEnum(Enum):
    Yes = "Yes"
    No = "No"


class JointTypeEnum(Enum):
    Coapplicant = "Coapplicant"
    Spouse = "Spouse"
    Other = "Other"


### AL_5 ###


class LoanSecuredEnum(Enum):
    Secured = "Secured"
    Unsecured = "Unsecured"


class CreditTypeEnum(Enum):
    Individual = "Individual"
    Joint = "Joint"


class AchFrequencyEnum(Enum):
    Monthly = "Monthly"
    SemiMonthly = "Semi-Monthly"


class PayrollTypeEnum(Enum):
    D124 = "D124"
    D231 = "D231"
    Aero = "Aero"
    DebtConsolidation = "Debt Consolidation"


class AlimonyTypeEnum(Enum):
    CourtOrder = "Court Order"
    WrittenAgreement = "Written Agreement"
    OralUnderstanding = "Oral Understanding"
    NA = "NA"


class PreferredAccountEnum(Enum):
    Checking = "Checking"
    Savings = "Savings"


class EducationEnum(Enum):
    HighSchool = "High School"
    SomeCollege = "Some College"
    TwoYear = "2 Year"
    FourYear = "4 Year"
    SpecialTraining = "Special Training"


## USER ATTRIBUTES ###


class UserAttributeMeta(type):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_p_attr = super().__new__(cls, name, bases, attrs)
        if name not in ["BaseUserAttr", "BaseUserDbAttr"]:
            assert name not in cls.registry, f"User attribute {name} already exists"
            cls.registry[name] = new_p_attr
        return new_p_attr


class UserProfile:
    # This variable is dedicated to my mom, Charleen
    def __init__(self, idx, relevant_features: set):
        self.relevant_features = relevant_features

        class Features:
            pass

        self.features = Features()
        # for name, attr_class in UserAttributeMeta.registry.items():
        missing_user_attributes = []
        for name in self.relevant_features:
            if name not in UserAttributeMeta.registry:
                missing_user_attributes.append(name)
                continue

            attr_class = UserAttributeMeta.registry[name]
            if name in relevant_features:
                if hasattr(attr_class, "options") and isinstance(
                    attr_class.options, list
                ):
                    # Use modulo to handle cases where there are fewer options than user indices
                    safe_idx = idx % len(attr_class.options)
                    setattr(self.features, name, attr_class.options[safe_idx])
                else:
                    raise AttributeError(f"Class {name} must have an 'options' list.")
        if missing_user_attributes:
            missing_str = "\n".join(missing_user_attributes)
            raise ValueError(f"Missing user attributes: {missing_str}")

    def get_nl_profile(self):
        nl_profile = []
        for name, attr_class in UserAttributeMeta.registry.items():
            if name in self.relevant_features:
                nl_profile.append(attr_class.nl_desc(getattr(self.features, name)))
        return nl_profile


# metaclass
# abstract class
# rattan's abstract class rattans(options, nl_desc)
# classes
# rattans class                                         <- product


class BaseUserAttr(metaclass=UserAttributeMeta):
    pass


class BaseUserDbAttr(metaclass=UserAttributeMeta):
    form_name, cell_id = __name__.split("_")

    @staticmethod
    def nl_desc(option):
        # form_name, cell_id = __class__.__name__.split("_")
        # return f"The user's value for form {__class__.form_name} in cell {__class__.cell_id} ({__class__.__doc__}) is: {option}"
        return None


### AUTO LOAN FEATURES ###


class FirstName(BaseUserAttr):
    options = ["Lucas", "Ava", "Ethan", "Mia"]

    @staticmethod
    def nl_desc(option):
        return f"The user's first name is: {option}"


# class xyz(BaseUserAttr):


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
        return f"The user's residence status ({', '.join([e.value for e in ResidenceStatusEnum])}) is: {option}"


class JointResidenceStatus(BaseUserAttr):
    options = [
        ResidenceStatusEnum.Renting.value,
        ResidenceStatusEnum.Other.value,
        ResidenceStatusEnum.Own.value,
        ResidenceStatusEnum.LivingWithRelatives.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's residence status ({', '.join([e.value for e in ResidenceStatusEnum])}) is: {option}"


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
    options = ["1200", "1450", "1750", "2100"]

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
    options = [
        f"{25*12} months",
        f"{24*12} months",
        f"{23*12} months",
        f"{22*12} months",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user has been employed at their current job for: {option}"


class AdditionalIncome(BaseUserAttr):
    options = ["400", "900", "1100", "600"]

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
        return f"The user's checking account number is: {option}"


class BankruptcyStatus(BaseUserAttr):
    options = ["Yes", "No", "Yes", "No"]

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
    options = ["5200", "9700", "14300", "6600"]

    @staticmethod
    def nl_desc(option):
        return f"The user's remaining auto balance is: {option}"


class TradingInCar(BaseUserAttr):
    options = ["Yes", "No", "Yes", "No"]

    @staticmethod
    def nl_desc(option):
        return f"The user is trading in a car: {option}"


class RegisteredCarOwner(BaseUserAttr):
    options = ["Self", "Spouse", "Self", "Spouse"]

    @staticmethod
    def nl_desc(option):
        opt = "the user" if option == "Self" else "the user's spouse"
        return f"The new car will be registered with: {opt}"


class AutoAmountRequested(BaseUserAttr):
    options = ["8000", "12000", "18500", "7300"]

    @staticmethod
    def nl_desc(option):
        return f"The auto amount requested by the user is: {option}"


class Term(BaseUserAttr):
    options = ["12 months", "12 months", "24 months", "36 months"]

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


class LastVehicleMake(BaseUserAttr):
    options = ["Ford", "Chevrolet", "Toyota", "Honda"]

    @staticmethod
    def nl_desc(option):
        return f"The user's last vehicle was a: {option}"


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
    options = ["Yes", "Yes", "Yes", "Yes"]

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
        return f"The user's home phone (evening) number is: {option}"


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
        return f"The joint filer's home phone (evening) number is: {option}"


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


# class TimeAtAddressYears(BaseUserAttr):
#     options = ["1", "3", "4", "7"]

#     @staticmethod
#     def nl_desc(option):
#         return f"The years the user has been at this address: {option}"


class TimeAtAddressMonths(BaseUserAttr):
    options = ["12", "36", "48", "84"]

    @staticmethod
    def nl_desc(option):
        return f"The months the user has been at this address: {option}"


# class JointTimeAtAddressYears(BaseUserAttr):
#     options = ["2", "4", "6", "9"]

#     @staticmethod
#     def nl_desc(option):
#         return f"The years the joint filer has been at this address: {option}"


class JointTimeAtAddressMonths(BaseUserAttr):
    options = ["24", "48", "72", "96"]

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
    options = ["900", "1100", "1400", "2000"]

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
        return f"The user's most recent previous residence status ({', '.join([e.value for e in ResidenceStatusEnum])}) is: {option}"


class JointPreviousResidenceStatus(BaseUserAttr):
    options = [
        ResidenceStatusEnum.LivingWithRelatives.value,
        ResidenceStatusEnum.Other.value,
        ResidenceStatusEnum.Buying.value,
        ResidenceStatusEnum.Renting.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's most recent previous residence status ({', '.join([e.value for e in ResidenceStatusEnum])}) is: {option}"


# class TimeAtPreviousAddressYears(BaseUserAttr):
#     options = ["1", "2", "4", "6"]

#     @staticmethod
#     def nl_desc(option):
#         return f"The user's time at previous address in years is: {option}"


class TimeAtPreviousAddressMonths(BaseUserAttr):
    options = ["12", "48", "84", "120"]

    @staticmethod
    def nl_desc(option):
        return f"The user's time at previous address in months is: {option}"


# class JointTimeAtPreviousAddressYears(BaseUserAttr):
#     options = [12, 36, 60, 84]

#     @staticmethod
#     def nl_desc(option):
#         return f"The joint filer's time at previous address in years is: {option}"


class JointTimeAtPreviousAddressMonths(BaseUserAttr):
    options = ["24", "60", "96", "120"]

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
    options = ["Springfield", "H Davenport", "Lakeshire", "Brightvale"]

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


# class EmployerLengthYears(BaseUserAttr):
#     options = ["1", "3", "5", "9"]

#     @staticmethod
#     def nl_desc(option):
#         return f"The user's years at their current employer is: {option}"


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
        return f"The user's work (daytime) phone is: {option}"


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


# class JointEmployerLengthYears(BaseUserAttr):
#     options = ["2", "4", "6", "10"]

#     @staticmethod
#     def nl_desc(option):
#         return f"The joint filer's years at their current employer is: {option}"


class JointEmployerPosition(BaseUserAttr):
    options = ["Supervisor", "Manager", "Analyst", "Director"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's current job title is: {option}"


class JointEmployerWorkPhone(BaseUserAttr):
    options = ["310-555-5559", "415-555-6667", "202-555-7774", "646-555-8883"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's work (daytime) phone is: {option}"


class JointGrossMonthlyIncome(BaseUserAttr):
    options = ["2800", "4200", "5000", "5900"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's gross monthly income is: {option}"


class AdditionalIncomeSource(BaseUserAttr):
    options = ["Freelancing", "Part-time Tutoring", "Investments", "Online Business"]

    @staticmethod
    def nl_desc(option):
        return f"The user's additional monthly income source is: {option}"


class AdditionalMonthlyIncome(BaseUserAttr):
    options = ["300", "600", "1200", "900"]

    @staticmethod
    def nl_desc(option):
        return f"The user's additional monthly income is: {option}"


class JointAdditionalIncomeSource(BaseUserAttr):
    options = ["Bank Robbery", "Small Business", "Online Sales", "Stocks/Dividends"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's additional income source is: {option}"


class JointAdditionalMonthlyIncome(BaseUserAttr):
    options = ["400", "800", "1300", "700"]

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


class PreviousEmployerStreetName(BaseUserAttr):
    options = ["8th Ave", "5th St", "3rd St", "1st St"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous employer street name is: {option}"


class PreviousEmployerHouseNumber(BaseUserAttr):
    options = ["87", "76", "65", "54"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous employer house number is: {option}"


class PreviousEmployerState(BaseUserAttr):
    options = ["NJ", "CA", "NY", "TX"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous employer state is: {option}"


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


# class PreviousLengthEmployed(BaseUserAttr):
#     options = ["8 months", "1 year", "2 years", "4 years"]

#     @staticmethod
#     def nl_desc(option):
#         # return f"The user's : {option}"
#         return f"The user was employed at their previous position for: {option}"


class PreviousLengthEmployedMonths(BaseUserAttr):
    options = ["8", "12", "24", "48"]

    @staticmethod
    def nl_desc(option):
        return f"The user was employed at their previous position for: {option} months"


class JointPreviousLengthEmployedMonths(BaseUserAttr):
    options = ["48", "60", "72", "84"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer was employed at their previous position for: {option} months"


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


# class JointPreviousLengthEmployed(BaseUserAttr):
#     options = ["8 months", "1 year", "2 years", "4 years"]

#     @staticmethod
#     def nl_desc(option):
#         return f"The joint filer was previously employed for: {option}"


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
    options = ["Yes", "No", "Yes", "No"]

    @staticmethod
    def nl_desc(option):
        return f"Has the joint filer previously gone bankrupt: {option}"


class JointBankruptcyYear(BaseUserAttr):
    options = ["N/A", "2018", "2020", "2022"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer went bankrupt in: {option}"


class TodaysDate(BaseUserAttr):
    options = ["2/15/2025"] * 4

    @staticmethod
    def nl_desc(option):
        return f"Today's date is (MM/DD/YYYY): {option}"


class LoanType(BaseUserAttr):
    options = ([o.value for o in LoanTypeEnum] * 4)[:4]

    @staticmethod
    def nl_desc(option):
        return f"The user's loan type is: {option}"


class VehicleLoanCondition(BaseUserAttr):
    options = ([o.value for o in VehicleLoanConditionEnum] * 4)[:4]

    @staticmethod
    def nl_desc(option):
        return f"The condition of the user's trade-in vehicle is: {option}"


class VehicleLoanType(BaseUserAttr):
    options = ([o.value for o in VehicleLoanTypeEnum] * 4)[:4]

    @staticmethod
    def nl_desc(option):
        return f"The user is applying for a loan to buy a: {option}"


class PersonalAmountRequested(BaseUserAttr):
    options = ["N/A", "N/A", "N/A", "N/A"]

    @staticmethod
    def nl_desc(option):
        return f"The amount the user is requesting for a personal loan is: {option}"


class CreditAmountRequested(BaseUserAttr):
    options = ["N/A", "N/A", "N/A", "N/A"]

    @staticmethod
    def nl_desc(option):
        return f"The amount the user is requesting for a line of credit is: {option}"


class CreditLoanPurpose(BaseUserAttr):
    options = ["N/A", "", "N/A", "N/A"]

    @staticmethod
    def nl_desc(option):
        return f"The purpose the user is requesting for a line of credit is: {option}"


class PersonalLoanPurpose(BaseUserAttr):
    options = ["N/A", "N/A", "N/A", "N/A"]

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
    options = ["Cox Rd", "Woodlands Cv", "Patterson Dr", "12th st"]

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


class PreviousEmployerZip(BaseUserAttr):
    options = ["08873", "90001", "10001", "70001"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous employer's zip is: {option}"


class JointEmployerZip(BaseUserAttr):
    options = ["36832", "35671", "35080", "36040"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's employer's zip is: {option}"


class EmployerHireDate(BaseUserAttr):
    options = ["1/1/2000", "1/1/2001", "1/1/2002", "1/1/2003"]

    @staticmethod
    def nl_desc(option):
        return f"The user's hire date at their current employer is: {option}"


class JointEmployerHireDate(BaseUserAttr):
    options = ["2/2/2000", "2/2/2001", "2/2/2002", "2/2/2003"]

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
    options = ["1/1/2030", "1/1/2031", "1/1/2032", "1/1/2033"]

    @staticmethod
    def nl_desc(option):
        return f"The user's driver license expiration date is: {option}"


class JointDriversLicenseExpirationDate(BaseUserAttr):
    options = ["2/2/2030", "2/2/2031", "2/2/2032", "2/2/2033"]

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
    options = ([o.value for o in MarriageStatusEnum] * 4)[:4]

    @staticmethod
    def nl_desc(option):
        return f"The user's marriage status is: {option}"


class JointMarriageStatus(BaseUserAttr):
    options = ([o.value for o in MarriageStatusEnum] * 4)[:4]

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

    db = "cr"
    options = ["23456", "34567", "45678", "56789"]


class CROI_4436(BaseUserDbAttr):
    """1.a.(1)(b): All other loans secured by real estate"""

    db = "cr"
    options = ["67890", "78901", "89012", "90123"]


class CROI_4012(BaseUserDbAttr):
    """1.a.(2): Commercial and industrial loans"""

    db = "cr"
    options = ["11234", "22345", "33456", "44567"]


class CROI_B485(BaseUserDbAttr):
    """1.a.(3)(a): Credit cards"""

    db = "cr"
    options = ["55678", "66789", "77890", "88901"]


class CROI_B486(BaseUserDbAttr):
    """1.a.(3)(b): Other"""

    db = "cr"
    options = ["40112", "51223", "62334", "73445"]


class CROI_4058(BaseUserDbAttr):
    """1.a.(5): All other loans"""

    db = "cr"
    options = ["99012", "10123", "21234", "32345"]


# Calculated with math, so no user profile info
# class CROI_4010(BaseUserDbAttr):
#     """1.a.(6): Total interest and fee income on loans"""
#     options = ["43456", "54567", "65678", "76789"]


class CROI_4065(BaseUserDbAttr):
    """1.b: Income from lease financing receivables"""

    db = "cr"
    options = ["87890", "98901", "10912", "21023"]


class CROI_4115(BaseUserDbAttr):
    """1.c: Interest income on balances due from depository institutions"""

    db = "cr"
    options = ["31134", "42245", "53356", "64467"]


class CROI_B488(BaseUserDbAttr):
    """1.d.(1): U.S. Treasury securities and U.S. Government agency obligations"""

    db = "cr"
    options = ["75578", "86689", "97790", "10891"]


class CROI_B489(BaseUserDbAttr):
    """1.d.(2): Mortgage-backed securities"""

    db = "cr"
    options = ["21902", "32013", "42124", "52235"]


class CROI_4060(BaseUserDbAttr):
    """1.d.(3): (3) All other securities (includes securities issued by states and political subdivisions in the U.S.)"""

    db = "cr"
    options = ["11365", "22476", "33587", "44698"]


class CROI_4020(BaseUserDbAttr):
    """1.f: Interest income on federal funds sold and securities purchased under agreements to resell"""

    db = "cr"
    options = ["62346", "72457", "82568", "92679"]


class CROI_4518(BaseUserDbAttr):
    """1.g: Other interest income"""

    db = "cr"
    options = ["10234", "21345", "32456", "43567"]


# calculated with math
# class CROI_4107(BaseUserDbAttr):
#     """1.h: Total interest income"""
#     options = ["54678", "65789", "76890", "87901"]


class CROI_4508(BaseUserDbAttr):
    """2.a.(1): Interest on deposits - transaction accounts"""

    db = "cr"
    options = ["98012", "10123", "21234", "32345"]


class CROI_0093(BaseUserDbAttr):
    """2.a.(2)(a): Savings deposits (includes MMDAs)"""

    db = "cr"
    options = ["43456", "54567", "65678", "76789"]


class CROI_HK03(BaseUserDbAttr):
    """2.a.(2)(b): Time deposits of $250,000 or less"""

    db = "cr"
    options = ["87890", "98901", "10912", "21023"]


class CROI_HK04(BaseUserDbAttr):
    """2.a.(2)(c): Time deposits of more than $250,000"""

    db = "cr"
    options = ["31134", "42245", "53356", "64467"]


class CROI_4180(BaseUserDbAttr):
    """2.b: Expense of federal funds purchased and securities sold under agreements to repurchase"""

    db = "cr"
    options = ["75578", "86689", "97790", "10891"]


class CROI_4185(BaseUserDbAttr):
    """2.c: Interest on trading liabilities and other borrowed money"""

    db = "cr"
    options = ["21902", "32013", "42124", "52235"]


class CROI_4200(BaseUserDbAttr):
    """2.d: Interest on subordinated notes and debentures"""

    db = "cr"
    options = ["11365", "22476", "33587", "44698"]


class CROI_JJ33(BaseUserDbAttr):
    """4: Provisions for credit losses"""

    db = "cr"
    options = ["62346", "72457", "82568", "92679"]


### SEC FEATURES ###

### SEC NL fields

# class PortionOfAggregateSalesIssuer(BaseNumericField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.PortionOfAggregateSales


class PortionOfAggregateSalesIssuer(BaseUserAttr):
    """The portion of aggregate sales attributable to securities sold on behalf of the issuer"""

    options = ["1000000", "2000000", "3000000", "4000000"]

    @staticmethod
    def nl_desc(option):
        return f"The portion of aggregate sales attributable to securities sold on behalf of the issuer is: {option}"


# class PortionOfAggregateSalesSecurityHolders(BaseNumericField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.PortionOfAggregateSalesSecurityHolders
class PortionOfAggregateSalesSecurityHolders(BaseUserAttr):
    """The portion of aggregate sales attributable to securities sold on behalf of selling securityholders"""

    options = ["500000", "600000", "700000", "800000"]

    @staticmethod
    def nl_desc(option):
        return f"The portion of aggregate sales attributable to securities sold on behalf of selling securityholders is: {option}"


# class CrdNumber(BaseNumericField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.CrdNumber
class CrdNumber(BaseUserAttr):
    """CRD Number of any broker or dealer listed"""

    options = ["1234567890", "1234567891", "1234567892", "1234567893"]

    @staticmethod
    def nl_desc(option):
        return f"The CRD Number of any broker or dealer listed is: {option}"


class ApproximateNumberOfHolders(BaseUserAttr):
    """Approximate number of holders"""

    options = ["1000000", "2000000", "3000000", "4000000"]

    @staticmethod
    def nl_desc(option):
        return f"The approximate number of holders is: {option}"


# class NetProceeds(BaseNumericField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.NetProceeds
class NetProceeds(BaseUserAttr):
    """Net proceeds from the sale of the security"""

    options = ["37492837492837", "37492837492838", "37492837492839", "37492837492840"]

    @staticmethod
    def nl_desc(option):
        return f"The net proceeds from the sale of the security is: {option}"


# class TitleOfEachClassOfSecurities(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.TitleOfEachClassOfSecurities


class TitleOfEachClassOfSecurities(BaseUserAttr):
    """Title of each class of securities"""

    options = [
        "Common Stock",
        "Preferred Stock",
        "Convertible Preferred Stock",
        "Warrant",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The title of each class of securities is: {option}"


# class CommissionFileNumbers(BaseNumericField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.CommissionFileNumbers
class CommissionFileNumbers(BaseUserAttr):
    """Commission file numbers"""

    options = ["1234567890", "1234567891", "1234567892", "1234567893"]

    @staticmethod
    def nl_desc(option):
        return f"The commission file numbers are: {option}"


# class NameOfIssuerAsSpecifiedInTheCommissionFile(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.NameOfIssuerAsSpecifiedInTheCommissionFile
class NameOfIssuerAsSpecifiedInTheCommissionFile(BaseUserAttr):
    """Name of issuer as specified in the commission file"""

    options = ["Soda Corp", "Popcorn Inc", "Corn Co", "Cheese Co"]

    @staticmethod
    def nl_desc(option):
        return f"The name of issuer as specified in the commission file is: {option}"


# class By(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.By


class By(BaseUserAttr):
    """By"""

    options = ["Joseph Lee", "John Smith", "Jane Doe", "Jim Beam"]

    @staticmethod
    def nl_desc(option):
        return f"The name of the person signing is: {option}"


# class Title(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.Title


class Title(BaseUserAttr):
    """Title"""

    options = ["CFO", "CEO", "CTO", "COO"]

    @staticmethod
    def nl_desc(option):
        return f"The title of the person signing is: {option}"


# ### SEC DB Fields


# class SEC_UnderwritersName(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_UnderwritersName
class SEC_UnderwritersName(BaseUserDbAttr):
    """Name of the underwriters"""

    db = "sec"
    col = "name"
    row = "Underwriters"
    options = [
        "First Underwriter Co.",
        "Second Underwriter Co.",
        "Third Underwriter Co.",
        "Fourth Underwriter Co.",
    ]


# class SEC_SalesCommissionsName(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_SalesCommissionsName
class SEC_SalesCommissionsName(BaseUserDbAttr):
    """Name of the sales commissions"""

    db = "sec"
    col = "name"
    row = "SalesCommissions"
    options = [
        "First Sales Commission Co.",
        "Second Sales Commission Co.",
        "Third Sales Commission Co.",
        "Fourth Sales Commission Co.",
    ]


# class SEC_FindersFeesName(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_FindersFeesName
class SEC_FindersFeesName(BaseUserDbAttr):
    """Name of the finders fees"""

    db = "sec"
    col = "name"
    row = "FindersFees"
    options = [
        "First Finders Fee Co.",
        "Second Finders Fee Co.",
        "Third Finders Fee Co.",
        "Fourth Finders Fee Co.",
    ]


# class SEC_AuditorName(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_AuditorName
class SEC_AuditorName(BaseUserDbAttr):
    """Name of the auditor"""

    db = "sec"
    col = "name"
    row = "Auditor"
    options = [
        "First Auditor Co.",
        "Second Auditor Co.",
        "Third Auditor Co.",
        "Fourth Auditor Co.",
    ]


# class SEC_LegalName(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_LegalName
class SEC_LegalName(BaseUserDbAttr):
    """Name of the legal"""

    db = "sec"
    col = "name"
    row = "Legal"
    options = [
        "First Legal Co.",
        "Second Legal Co.",
        "Third Legal Co.",
        "Fourth Legal Co.",
    ]


# class SEC_PromotersName(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_PromotersName
class SEC_PromotersName(BaseUserDbAttr):
    """Name of the promoters"""

    db = "sec"
    col = "name"
    row = "Promoters"
    options = [
        "First Promoter Co.",
        "Second Promoter Co.",
        "Third Promoter Co.",
        "Fourth Promoter Co.",
    ]


# class SEC_BlueSkyComplianceName(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_BlueSkyComplianceName
class SEC_BlueSkyComplianceName(BaseUserDbAttr):
    """Name of the blue sky compliance"""

    db = "sec"
    col = "name"
    row = "BlueSkyCompliance"
    options = [
        "First Blue Sky Compliance Co.",
        "Second Blue Sky Compliance Co.",
        "Third Blue Sky Compliance Co.",
        "Fourth Blue Sky Compliance Co.",
    ]


# class SEC_UnderwritersFees(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_UnderwritersFees
class SEC_UnderwritersFees(BaseUserDbAttr):
    """Fees of the underwriters"""

    db = "sec"
    col = "fees"
    row = "Underwriters"
    options = ["100000", "200000", "300000", "400000"]


# class SEC_SalesCommissionsFees(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_SalesCommissionsFees
class SEC_SalesCommissionsFees(BaseUserDbAttr):
    """Fees of the sales commissions"""

    db = "sec"
    col = "fees"
    row = "SalesCommissions"
    options = ["330000", "331000", "332000", "333000"]


# class SEC_FindersFeesFees(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_FindersFeesFees
class SEC_FindersFeesFees(BaseUserDbAttr):
    """Fees of the finders fees"""

    db = "sec"
    col = "fees"
    row = "FindersFees"
    options = ["111000", "112000", "113000", "114000"]


# class SEC_AuditorFees(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_AuditorFees
class SEC_AuditorFees(BaseUserDbAttr):
    """Fees of the auditor"""

    db = "sec"
    col = "fees"
    row = "Auditor"
    options = ["111100", "111200", "111300", "111400"]


# class SEC_LegalFees(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_LegalFees
class SEC_LegalFees(BaseUserDbAttr):
    """Fees of the legal"""

    db = "sec"
    col = "fees"
    row = "Legal"
    options = ["111110", "111120", "111130", "111140"]


# class SEC_PromotersFees(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_PromotersFees
class SEC_PromotersFees(BaseUserDbAttr):
    """Fees of the promoters"""

    db = "sec"
    col = "fees"
    row = "Promoters"
    options = ["111111", "111112", "111113", "111114"]


# class SEC_BlueSkyComplianceFees(BaseStringField):
#     @classmethod
#     def get_profile_info(cls, user_profile):
#         return user_profile.features.SEC_BlueSkyComplianceFees
class SEC_BlueSkyComplianceFees(BaseUserDbAttr):
    """Fees of the blue sky compliance"""

    db = "sec"
    col = "fees"
    row = "BlueSkyCompliance"
    options = ["222222", "222223", "222224", "222225"]


# AL 5


class JointEmployerWorkPhoneExtension(BaseUserAttr):
    options = ["N/A", "N/A", "N/A", "N/A"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's employer work phone extension is: {option}"


class PreviousEmployerMonths(BaseUserAttr):
    options = ["6", "12", "18", "24"]

    @staticmethod
    def nl_desc(option):
        return f"The user was at their previous employer for: {option} months"


class AchFrequency(BaseUserAttr):
    options = [AchFrequencyEnum.Monthly.value, AchFrequencyEnum.SemiMonthly.value] * 2

    @staticmethod
    def nl_desc(option):
        return f"The user's ACH repayment frequency is: {option}"


class NearestRelativeMonths(BaseUserAttr):
    options = ["240", "360", "480", "600"]

    @staticmethod
    def nl_desc(option):
        return f"The user's nearest relative has been a relative for: {option} months"


class JointRelationToApplicant(BaseUserAttr):
    options = ["Spouse", "Parent", "Sibling", "Child"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's relation to the applicant is: {option}"


class County(BaseUserAttr):
    options = ["Dallas County", "Los Angeles County", "Hudson County", "Fulton County"]

    @staticmethod
    def nl_desc(option):
        return f"The user's county is: {option}"


class JointCounty(BaseUserAttr):
    options = ["Pinellas County", "King County", "New York County", "Jefferson County"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's county is: {option}"


class JointPreviousEmployerState(BaseUserAttr):
    options = ["TX", "CA", "NY", "FL"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous employer state is: {option}"


class JointPreviousEmployerZip(BaseUserAttr):
    options = ["75001", "90210", "10001", "33101"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous employer zip is: {option}"


class JointAgesOfDependents(BaseUserAttr):
    options = ["5, 8", "12, 15", "3, 6, 9", "10, 13, 16"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's ages of dependents are: {option}"


class AgesOfDependents(BaseUserAttr):
    options = ["4, 7", "11, 14", "2, 5, 8", "9, 12, 15"]

    @staticmethod
    def nl_desc(option):
        return f"The user's ages of dependents are: {option}"


class JointPreviousEmployerHouseNumber(BaseUserAttr):
    options = ["100", "200", "300", "400"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous employer house number is: {option}"


class JointPreviousEmployerStreetName(BaseUserAttr):
    options = ["Main Street", "Oak Avenue", "Pine Road", "Elm Drive"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous employer street name is: {option}"


class NearestRelativeRelationship(BaseUserAttr):
    options = ["Mother", "Father", "Sister", "Brother"]

    @staticmethod
    def nl_desc(option):
        return f"The user's nearest relative relationship is: {option}"


class LoanSecured(BaseUserAttr):
    options = [LoanSecuredEnum.Secured.value, LoanSecuredEnum.Unsecured.value] * 2

    @staticmethod
    def nl_desc(option):
        return f"The loan is: {option}"


class JointPreviousCreditWithUsWhen(BaseUserAttr):
    options = ["2018", "2019", "2020", "2021"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous credit with us was in: {option}"


class JointPreviousCreditWithUs(BaseUserAttr):
    options = ["Yes", "No", "Yes", "No"]

    @staticmethod
    def nl_desc(option):
        return f"Has the joint filer had previous credit with us: {option}"


class EmployerWorkPhoneExtension(BaseUserAttr):
    options = ["N/A", "N/A", "N/A", "N/A"]

    @staticmethod
    def nl_desc(option):
        return f"The user's employer work phone extension is: {option}"


class NearestRelativeName(BaseUserAttr):
    options = ["John Smithy", "Jane Doey", "Robert Johnsony", "Mary Wilsony"]

    @staticmethod
    def nl_desc(option):
        return f"The user's nearest relative name is: {option}"


class PayrollType(BaseUserAttr):
    options = [
        PayrollTypeEnum.D124.value,
        PayrollTypeEnum.D231.value,
        PayrollTypeEnum.Aero.value,
        PayrollTypeEnum.DebtConsolidation.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's payroll type is: {option}"


class PreviousCounty(BaseUserAttr):
    options = [
        "Denver County",
        "Wake County",
        "Philadelphia County",
        "Cumberland County",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous county is: {option}"


class NearestRelativePhone(BaseUserAttr):
    options = ["(555) 111-1111", "(555) 222-2222", "(555) 333-3333", "(555) 444-4444"]

    @staticmethod
    def nl_desc(option):
        return f"The user's nearest relative phone is: {option}"


class NearestRelativeCellPhone(BaseUserAttr):
    options = ["(555) 111-2222", "(555) 222-3333", "(555) 333-4444", "(555) 444-5555"]

    @staticmethod
    def nl_desc(option):
        return f"The user's nearest relative cell phone is: {option}"


class PreviousCreditWithUs(BaseUserAttr):
    options = ["Yes", "No", "Yes", "No"]

    @staticmethod
    def nl_desc(option):
        return f"Has the user had previous credit with us: {option}"


class AlimonyType(BaseUserAttr):
    options = [
        AlimonyTypeEnum.CourtOrder.value,
        AlimonyTypeEnum.WrittenAgreement.value,
        AlimonyTypeEnum.OralUnderstanding.value,
        AlimonyTypeEnum.NA.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's alimony type is: {option}"


class LoanDuration(BaseUserAttr):
    options = ["24 months", "36 months", "48 months", "60 months"]

    @staticmethod
    def nl_desc(option):
        return f"The loan duration is: {option}"


# class PreviousEmployerYears(BaseUserAttr):
#     options = ["1", "2", "3", "4"]

#     @staticmethod
#     def nl_desc(option):
#         return f"The user was at their previous employer for: {option} years"


class JointIncomeLikelyToBeReducedExplanation(BaseUserAttr):
    options = [
        "N/A",
        "Reduced hours",
        "N/A",
        "Retirement",
    ]  # must match JointIncomeLikelyToBeReduced_Yes/No

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's income likely to be reduced explanation is: {option}"


class JointAlimonyType(BaseUserAttr):
    options = [
        AlimonyTypeEnum.CourtOrder.value,
        AlimonyTypeEnum.WrittenAgreement.value,
        AlimonyTypeEnum.OralUnderstanding.value,
        AlimonyTypeEnum.NA.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's alimony type is: {option}"


class JointIncomeLikelyToBeReduced(BaseUserAttr):
    options = [YesNoEnum.No.value, YesNoEnum.Yes.value] * 2

    @staticmethod
    def nl_desc(option):
        return f"Is the joint filer's income likely to be reduced: {option}"


class JointPreviousEmployerMonths(BaseUserAttr):
    options = ["6", "12", "18", "24"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer was at their previous employer for: {option} months"


class PreviousCreditWithUsWhen(BaseUserAttr):
    options = ["2017", "2018", "2019", "2020"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous credit with us was in: {option}"


class IncomeLikelyToBeReduced(BaseUserAttr):
    options = [YesNoEnum.No.value, YesNoEnum.Yes.value] * 2

    @staticmethod
    def nl_desc(option):
        return f"Is the user's income likely to be reduced: {option}"


class CreditType(BaseUserAttr):
    options = [CreditTypeEnum.Individual.value, CreditTypeEnum.Joint.value] * 2

    @staticmethod
    def nl_desc(option):
        return f"The credit type is: {option}"


class IncomeLikelyToBeReducedExplanation(BaseUserAttr):
    options = [
        "N/A",
        "Reduced hours",
        "N/A",
        "Retirement",
    ]  # must match IncomeLikelyToBeReduced_Yes/No

    @staticmethod
    def nl_desc(option):
        return f"The user's income likely to be reduced explanation is: {option}"


class VehicleCondition(BaseUserAttr):
    options = [
        VehicleLoanConditionEnum.New.value,
        VehicleLoanConditionEnum.Used.value,
        VehicleLoanConditionEnum.Refinance.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The vehicle condition is: {option}"


class ProceedsType(BaseUserAttr):
    options = [
        ProceedsTypeEnum.DebtConsolidation.value,
        ProceedsTypeEnum.Other.value,
    ] * 2

    @staticmethod
    def nl_desc(option):
        return f"The proceeds of unsecured loan will be used for: {option}"


### AL 4 ###


class CurrentAddressStartYearAndMonth(BaseUserAttr):
    # must match TimeAtAddressMonths ["12", "36", "48", "84"]
    options = ["02/2024", "02/2022", "02/2021", "02/2018"]

    @staticmethod
    def nl_desc(option):
        return f"The user moved into their current address in {option}"


class JointCurrentAddressStartYearAndMonth(BaseUserAttr):
    # must match class JointTimeAtAddressMonths options = ["24", "48", "72", "96"]
    options = ["02/2023", "02/2021", "02/2019", "02/2017"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer moved into their current address in {option}"


class LibertySavingsAccountNumber(BaseUserAttr):
    options = ["1234567890", "0987654321", "1234567890", "0987654321"]

    @staticmethod
    def nl_desc(option):
        return f"The user's Liberty Savings Account number is: {option}"


class JointLibertySavingsAccountNumber(BaseUserAttr):
    options = ["234567890", "987654329", "234567890", "987654329"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's Liberty Savings Account number is: {option}"


class PreferredPhone(BaseUserAttr):
    options = [
        PreferredPhoneEnum.Home.value,
        PreferredPhoneEnum.Work.value,
        PreferredPhoneEnum.Cell.value,
    ] * 2

    @staticmethod
    def nl_desc(option):
        return f"The user's preferred phone is: {option}"


class JointPreferredPhone(BaseUserAttr):
    options = [
        PreferredPhoneEnum.Home.value,
        PreferredPhoneEnum.Work.value,
        PreferredPhoneEnum.Cell.value,
    ] * 2

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's preferred phone is: {option}"


class SupervisorName(BaseUserAttr):
    options = ["AA Smith", "BB Jones", "CC Brown", "DD Davis"]

    @staticmethod
    def nl_desc(option):
        return f"The user's supervisor name is: {option}"


class JointSupervisorName(BaseUserAttr):
    options = ["EE Callahan", "FF Chan", "GG Lee", "HH McCay"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's supervisor name is: {option}"


class CitizenOrAlien(BaseUserAttr):
    options = [YesNoEnum.Yes.value, YesNoEnum.No.value] * 2

    @staticmethod
    def nl_desc(option):
        return f"The user's citizenship status is: {option}"


class JointCitizenOrAlien(BaseUserAttr):
    options = [YesNoEnum.Yes.value, YesNoEnum.No.value] * 2

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's citizenship status is: {option}"


### AL 6 ###


class AutomaticDeductionEnum(Enum):
    Yes = "Yes"
    No = "No"


class SelfEmployedEnum(Enum):
    Yes = "Yes"
    No = "No"


class AutomaticDeductionFromFNB(BaseUserAttr):
    options = [
        AutomaticDeductionEnum.Yes.value,
        AutomaticDeductionEnum.No.value,
    ] * 2

    @staticmethod
    def nl_desc(option):
        return (
            f"Does the user want automatic deductions from their FNB account: {option}"
        )


class DriversLicenseIssueDate(BaseUserAttr):
    options = ["03/2008", "11/2010", "07/2005", "09/2012"]

    @staticmethod
    def nl_desc(option):
        return f"The user's driver's license issue date is: {option}"


class FNBCheckingAccountNumber(BaseUserAttr):
    options = ["9876543210", "1122334455", "5566778899", "9988776655"]

    @staticmethod
    def nl_desc(option):
        return f"The user's FNB checking account number is: {option}"


class JointPreviousEmployerLengthMonths(BaseUserAttr):
    options = ["18", "36", "48", "60"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous employer length in months is: {option}"


class PreviousApplicantName(BaseUserAttr):
    options = [
        YesNoEnum.Yes.value,
        YesNoEnum.No.value,
    ] * 2

    @staticmethod
    def nl_desc(option):
        return f"The previous applicant's name is: {option}"


class JointPreviousEmployerPhone(BaseUserAttr):
    options = ["555-123-4567", "555-987-6543", "555-456-7890", "555-321-0987"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous employer phone number is: {option}"


class VehiclePrice(BaseUserAttr):
    options = ["25000", "32500", "18750", "41200"]

    @staticmethod
    def nl_desc(option):
        return f"The vehicle price is: {option}"


class JointSelfEmployed(BaseUserAttr):
    options = [
        SelfEmployedEnum.Yes.value,
        SelfEmployedEnum.No.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's self-employed status is: {option}"


class VehicleDownPayment(BaseUserAttr):
    options = ["5000", "7500", "3200", "9800"]

    @staticmethod
    def nl_desc(option):
        return f"The vehicle down payment is: {option}"


class PreviousEmployerPhone(BaseUserAttr):
    options = ["555-111-2222", "555-333-4444", "555-555-6666", "555-777-8888"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous employer phone number is: {option}"


class JointDriversLicenseIssueDate(BaseUserAttr):
    options = ["05/2009", "12/2011", "08/2006", "01/2013"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's driver's license issue date is: {option}"


class PreviousNames(BaseUserAttr):
    options = ["Elizabeth Thompson", "N/A", "Lisa Garcia", "N/A"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous name was: {option}"


class SelfEmployed(BaseUserAttr):
    options = [
        SelfEmployedEnum.Yes.value,
        SelfEmployedEnum.No.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's self-employed status is: {option}"


# EmergencyContactPhone
# SavingsAccountNumber
# SavingsAccountBankName
# TotalMonthlyExpenses
# EmergencyContact2Phone
# HourlyWage
# CheckingAccountBankName
# PermissionForElectronicTransfer
# EmergencyContactName
# EmergencyContact2Name


class EmergencyContactPhone(BaseUserAttr):
    options = ["(555) 123-4567", "(555) 987-6543", "(555) 456-7890", "(555) 321-0987"]

    @staticmethod
    def nl_desc(option):
        return f"The emergency contact phone number is: {option}"


class SavingsAccountNumber(BaseUserAttr):
    options = ["123456789012", "987654321098", "456789123456", "789123456789"]

    @staticmethod
    def nl_desc(option):
        return f"The savings account number is: {option}"


class SavingsAccountBankName(BaseUserAttr):
    options = ["Chase Bank", "Wells Fargo", "Bank of America", "Citibank"]

    @staticmethod
    def nl_desc(option):
        return f"The savings account bank name is: {option}"


class TotalMonthlyExpenses(BaseUserAttr):
    options = ["2450", "3120", "1890", "4750"]

    @staticmethod
    def nl_desc(option):
        return f"The total monthly expenses are: {option}"


class EmergencyContact2Phone(BaseUserAttr):
    options = ["(555) 555-1234", "(555) 666-5678", "(555) 777-9012", "(555) 888-3456"]

    @staticmethod
    def nl_desc(option):
        return f"The second emergency contact phone number is: {option}"


class HourlyWage(BaseUserAttr):
    options = ["$18.50", "$22.75", "$15.25", "$28.90"]

    @staticmethod
    def nl_desc(option):
        return f"The hourly wage is: {option}"


class PermissionForElectronicTransfer(BaseUserAttr):
    options = ["Yes", "No", "Pending", "Limited"]

    @staticmethod
    def nl_desc(option):
        return f"The permission for electronic transfer is: {option}"


class EmergencyContactName(BaseUserAttr):
    options = ["Sarah Johnson", "Michael Chen", "Emily Rodriguez", "David Thompson"]

    @staticmethod
    def nl_desc(option):
        return f"The emergency contact name is: {option}"


class EmergencyContact2Name(BaseUserAttr):
    options = ["Jennifer Smith", "Robert Wilson", "Lisa Garcia", "Thomas Brown"]

    @staticmethod
    def nl_desc(option):
        return f"The second emergency contact name is: {option}"


### NEW ENUMS ###


class RepaymentMethodEnum(Enum):
    PayrollDeduction = "Payroll Deduction"
    Cash = "Cash"
    MilitaryAllotment = "Military Allotment"
    Automatic = "Automatic"


### NEW CLASSES ###


class PreviousEmployerEndDate(BaseUserAttr):
    options = ["12/2022", "06/2023", "09/2021", "03/2023"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous employer end date is: {option}"


class PreviousEmployerHireDate(BaseUserAttr):
    options = ["01/2020", "03/2019", "06/2020", "09/2018"]

    @staticmethod
    def nl_desc(option):
        return f"The user's previous employer hire date is: {option}"


class JointNearestRelativeZip(BaseUserAttr):
    options = ["90210", "10001", "60601", "77001"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's nearest relative zip code is: {option}"


class NearestRelativeHouseNumber(BaseUserAttr):
    options = ["123", "456", "789", "654"]

    @staticmethod
    def nl_desc(option):
        return f"The user's nearest relative house number is: {option}"


class NearestRelativeStreetName(BaseUserAttr):
    options = ["Main Street", "Oak Avenue", "Pine Road", "Washington Boulevard"]

    @staticmethod
    def nl_desc(option):
        return f"The user's nearest relative street name is: {option}"


class TimesAtWork(BaseUserAttr):
    options = [
        "8:00 AM - 5:00 PM",
        "9:00 AM - 6:00 PM",
        "7:00 AM - 4:00 PM",
        "10:00 AM - 7:00 PM",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's work hours are: {option}"


class SelfEmployedTypeOfBusiness(BaseUserAttr):
    options = [
        "Plumbing",
        "Hacking",
        "Construction",
        "Consulting",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's self-employed type of business is: {option}"


class NearestRelativeState(BaseUserAttr):
    options = ["CA", "NY", "TX", "IL"]

    @staticmethod
    def nl_desc(option):
        return f"The user's nearest relative state is: {option}"


class JointNearestRelativeStreetName(BaseUserAttr):
    options = ["Maple Lane", "Cedar Boulevard", "Birch Court", "Willow Way"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's nearest relative street name is: {option}"


class JointNearestRelativeHouseNumber(BaseUserAttr):
    options = ["567", "890", "234", "678"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's nearest relative house number is: {option}"


class JointDutyStationTransferDate(BaseUserAttr):
    options = ["01/2026", "06/2026", "12/2026", "03/2026"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's duty station transfer date is: {option}"


class JointNearestRelativeCity(BaseUserAttr):
    options = ["Phoenix", "Philadelphia", "San Antonio", "San Diego"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's nearest relative city is: {option}"


class NearestRelativeCity(BaseUserAttr):
    options = ["New York", "Los Angeles", "Chicago", "Miami"]

    @staticmethod
    def nl_desc(option):
        return f"The user's nearest relative city is: {option}"


class DutyStationTransferExpected(BaseUserAttr):
    options = [
        YesNoEnum.Yes.value,
    ] * 4

    @staticmethod
    def nl_desc(option):
        return f"The user's duty station transfer is expected: {option}"


class JointTimesAtWork(BaseUserAttr):
    options = [
        "8:30 AM - 5:30 PM",
        "9:30 AM - 6:30 PM",
        "7:30 AM - 4:30 PM",
        "10:30 AM - 7:30 PM",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's work hours are: {option}"


class DutyStationTransferDate(BaseUserAttr):
    options = ["01/2027", "06/2027", "12/2027", "03/2027"]

    @staticmethod
    def nl_desc(option):
        return f"The user's duty station transfer date is: {option}"


class InterestedInLoanProtection(BaseUserAttr):
    options = [
        YesNoEnum.Yes.value,
        YesNoEnum.No.value,
    ] * 2

    @staticmethod
    def nl_desc(option):
        return f"The user is interested in loan protection: {option}"


class JointType(BaseUserAttr):
    options = [
        JointTypeEnum.Coapplicant.value,
        JointTypeEnum.Spouse.value,
        JointTypeEnum.Other.value,
    ] * 4

    @staticmethod
    def nl_desc(option):
        return f"The joint type is: {option}"


class JointNearestRelativeState(BaseUserAttr):
    options = ["AZ", "PA", "OH", "NC"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's nearest relative state is: {option}"


class JointSelfEmployedTypeOfBusiness(BaseUserAttr):
    options = [
        "Juggling",
        "Clowning",
        "Medicine",
        "PhD stipend",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's self-employed type of business is: {option}"


class JointDutyStationTransferTo(BaseUserAttr):
    options = ["Fort Hood", "Camp Pendleton", "Fort Bragg", "Naval Base San Diego"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's duty station transfer to is: {option}"


class JointDutyStationTransferExpected(BaseUserAttr):
    options = [
        YesNoEnum.Yes.value,
    ] * 4

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's duty station transfer is expected: {option}"


class DutyStationTransferTo(BaseUserAttr):
    options = ["Fort Campbell", "Fort Benning", "Fort Stewart", "Fort Carson"]

    @staticmethod
    def nl_desc(option):
        return f"The user's duty station transfer to is: {option}"


class JointNearestRelativeRelationship(BaseUserAttr):
    options = ["Sibling", "Child", "Cousin", "Neighbor"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's nearest relative relationship is: {option}"


class JointCSEAccountNumber(BaseUserAttr):
    options = ["CSE654321", "CSE098765", "CSE456789", "CSE210987"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's CSE account number is: {option}"


class CSEAccountNumber(BaseUserAttr):
    options = ["CSE111111", "CSE222222", "CSE333333", "CSE444444"]

    @staticmethod
    def nl_desc(option):
        return f"The user's CSE account number is: {option}"


class JointNearestRelativeName(BaseUserAttr):
    options = ["Michael Brown", "Sarah Davis", "David Miller", "Lisa Garcia"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's nearest relative name is: {option}"


class NearestRelativeZip(BaseUserAttr):
    options = ["10001", "90210", "60601", "77001"]

    @staticmethod
    def nl_desc(option):
        return f"The user's nearest relative zip code is: {option}"


class RepaymentMethod(BaseUserAttr):
    options = [
        RepaymentMethodEnum.Automatic.value,
        RepaymentMethodEnum.Cash.value,
        RepaymentMethodEnum.PayrollDeduction.value,
        RepaymentMethodEnum.MilitaryAllotment.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The repayment method is: {option}"


class JointPreviousEmployerEndDate(BaseUserAttr):
    options = ["11/2022", "05/2023", "08/2021", "02/2023"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous employer end date is: {option}"


class JointNearestRelativeHomePhone(BaseUserAttr):
    options = ["(555) 123-4567", "(555) 234-5678", "(555) 345-6789", "(555) 456-7890"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's nearest relative home phone is: {option}"


class JointNearestRelativeCellPhone(BaseUserAttr):
    options = ["(555) 123-5678", "(555) 234-6789", "(555) 345-7890", "(555) 456-8901"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's nearest relative cell phone is: {option}"


class JointPreviousEmployerHireDate(BaseUserAttr):
    options = ["02/2020", "07/2019", "10/2021", "04/2018"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's previous employer hire date is: {option}"


class PropertyReposessed(BaseUserAttr):
    options = [
        YesNoEnum.Yes.value,
        YesNoEnum.No.value,
        YesNoEnum.Yes.value,
        YesNoEnum.No.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's property has been repossessed: {option}"


class IncomeFromEmployment(BaseUserAttr):
    options = ["3500", "4200", "2800", "5100"]

    @staticmethod
    def nl_desc(option):
        return f"The user's income from employment is: {option}"


class PreferredAccount(BaseUserAttr):
    options = [
        PreferredAccountEnum.Checking.value,
    ] * 4

    @staticmethod
    def nl_desc(option):
        return f"The user's preferred account type is: {option}"


class LastVehicleFinancedBy(BaseUserAttr):
    options = [
        "ABC Credit Union",
        "XYZ Bank",
        "Local Finance Co.",
        "National Auto Loans",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's last vehicle was financed by: {option}"


class ApplicantsPrincipleDrivers(BaseUserAttr):
    options = [
        YesNoEnum.Yes.value,
        YesNoEnum.No.value,
        YesNoEnum.Yes.value,
        YesNoEnum.No.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The applicants are the principle drivers: {option}"


class AlimonyAmount(BaseUserAttr):
    options = ["500", "750", "300", "1000"]

    @staticmethod
    def nl_desc(option):
        return f"The user receives in alimony per month: {option}"


class JointIncomeFromEmployment(BaseUserAttr):
    options = ["4200", "3800", "5500", "2900"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's income from employment is: {option}"


class MortgageCompanyLandlordState(BaseUserAttr):
    options = ["TX", "CA", "NY", "FL"]

    @staticmethod
    def nl_desc(option):
        return f"The mortgage company/landlord state is: {option}"


class MortgageCompanyLandlordCity(BaseUserAttr):
    options = ["Austin", "Los Angeles", "New York", "Miami"]

    @staticmethod
    def nl_desc(option):
        return f"The mortgage company/landlord city is: {option}"


class Education(BaseUserAttr):
    options = [
        EducationEnum.HighSchool.value,
        EducationEnum.SomeCollege.value,
        EducationEnum.TwoYear.value,
        EducationEnum.FourYear.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user's education level is: {option}"


class MortgageCompanyLandlordPhone(BaseUserAttr):
    options = [
        "(512) 555-1234",
        "(213) 555-5678",
        "(212) 555-9012",
        "(305) 555-3456",
    ]

    @staticmethod
    def nl_desc(option):
        return f"The mortgage company/landlord phone number is: {option}"


class LastVehicleCost(BaseUserAttr):
    options = ["25000", "32000", "18500", "45000"]

    @staticmethod
    def nl_desc(option):
        return f"The user's last vehicle cost was: {option}"


class LastVehicleModel(BaseUserAttr):
    options = ["Toyota Camry", "Honda Civic", "Ford Focus", "Chevrolet Malibu"]

    @staticmethod
    def nl_desc(option):
        return f"The user's last vehicle model was: {option}"


class TypeOfContract(BaseUserAttr):
    options = [
        TypeOfContractEnum.Lease.value,
        TypeOfContractEnum.Installment.value,
        TypeOfContractEnum.Lease.value,
        TypeOfContractEnum.Installment.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The type of contract is: {option}"


class JointPreferredFirstName(BaseUserAttr):
    options = ["Sarah", "Michael", "Emily", "David"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's preferred first name is: {option}"


class PreviousTFSCredit(BaseUserAttr):
    options = [
        YesNoEnum.Yes.value,
        YesNoEnum.No.value,
        YesNoEnum.Yes.value,
        YesNoEnum.No.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user has previous TFS credit: {option}"


class LastVehicleYear(BaseUserAttr):
    options = ["2020", "2019", "2021", "2018"]

    @staticmethod
    def nl_desc(option):
        return f"The user's last vehicle year was: {option}"


class PendingSuits(BaseUserAttr):
    options = [
        YesNoEnum.Yes.value,
        YesNoEnum.No.value,
        YesNoEnum.Yes.value,
        YesNoEnum.No.value,
    ]

    @staticmethod
    def nl_desc(option):
        return f"The user has pending suits: {option}"


class PreferredFirstName(BaseUserAttr):
    options = ["Lucas", "Ava", "Ethan", "Syke"]

    @staticmethod
    def nl_desc(option):
        return f"The user's preferred first name is: {option}"


class JointAlimonyAmount(BaseUserAttr):
    options = ["600", "850", "400", "1200"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's alimony amount is: {option}"


class JointAdditionalIncomeAmount(BaseUserAttr):
    options = ["800", "1200", "600", "950"]

    @staticmethod
    def nl_desc(option):
        return f"The joint filer's additional income amount is: {option}"


class AdditionalIncomeAmount(BaseUserAttr):
    options = ["600", "900", "400", "1100"]

    @staticmethod
    def nl_desc(option):
        return f"The user's additional income amount is: {option}"
