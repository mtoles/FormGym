from enum import Enum


class UserAttributeMeta(type):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_p_attr = super().__new__(cls, name, bases, attrs)
        if name != "BaseUserAttr":
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


class BaseUserAttr(metaclass=UserAttributeMeta):
    pass


class FirstName(BaseUserAttr):
    options = ["Lucas", "Ava", "Ethan", "Mia"]


class LastName(BaseUserAttr):
    options = ["Reynolds", "Chen", "Patel", "Nguyen"]


class MiddleName(BaseUserAttr):
    options = ["James", "Marie", "Olivia", "Daniel"]


class SocialSecurityNumber(BaseUserAttr):
    options = ["314-22-5612", "562-78-4132", "901-45-2796", "274-63-9185"]


class BirthYear(BaseUserAttr):
    options = ["1979", "1992", "1988", "2000"]


class BirthMonth(BaseUserAttr):
    options = ["2", "9", "12", "5"]


class BirthDay(BaseUserAttr):
    options = ["7", "19", "23", "30"]


class JointBirthYear(BaseUserAttr):
    options = ["1979", "1992", "1988", "2000"]


class JointBirthMonth(BaseUserAttr):
    options = ["02", "09", "12", "05"]


class JointBirthDay(BaseUserAttr):
    options = ["07", "19", "23", "30"]


class PhoneNumber(BaseUserAttr):
    options = ["310-555-7891", "415-555-2034", "202-555-6970", "646-555-0311"]


class CellPhone(BaseUserAttr):
    options = ["310-555-1499", "415-555-8282", "202-555-7788", "646-555-9666"]


class EmailAddress(BaseUserAttr):
    options = [
        "lucas.work@example.com",
        "ava.personal@example.net",
        "ethan.home@example.org",
        "mia.contact@example.com",
    ]


class HouseNumber(BaseUserAttr):
    options = ["742", "315", "89", "251"]


class StreetName(BaseUserAttr):
    options = ["Park Boulevard", "Heather Lane", "Cedar Court", "Magnolia Circle"]


class City(BaseUserAttr):
    options = ["Brookhaven", "Fairview", "Hillside", "Willowdale"]


class State(BaseUserAttr):
    options = ["TX", "CA", "NJ", "GA"]


class Zip(BaseUserAttr):
    options = ["73301", "90007", "07030", "30301"]


class Country(BaseUserAttr):
    options = ["US"]


class ResidenceStatusEnum(Enum):
    Buying = "Buying"
    Renting = "Renting"
    LivingWithRelatives = "Living with relatives"
    Other = "Other"


class ResidenceStatus(BaseUserAttr):
    options = [
        ResidenceStatusEnum.Buying.value,
        ResidenceStatusEnum.Renting.value,
        ResidenceStatusEnum.LivingWithRelatives.value,
        ResidenceStatusEnum.Other.value,
    ]


class MortgageCompany(BaseUserAttr):
    options = [
        "Sunrise Mortgage LLC",
        "Oakwood Home Loans",
        "Guardian Mortgage Co.",
        "Stonegate Lending",
    ]


class MonthlyMortgageOrRent(BaseUserAttr):
    options = ["$1,200", "$1,450", "$1,750", "$2,100"]


class PreviousHouseNumber(BaseUserAttr):
    options = ["560", "912", "47", "893"]


class PreviousStreetName(BaseUserAttr):
    options = ["Mulberry Rd", "Orchard St", "Pinecrest Dr", "Willow Way"]


class PreviousCity(BaseUserAttr):
    options = ["Northfield", "Springview", "Lakeport", "Bayview"]


class PreviousState(BaseUserAttr):
    options = ["CO", "NC", "PA", "ME"]


class PreviousZip(BaseUserAttr):
    options = ["80203", "27601", "19019", "04401"]


class JointPreviousHouseNumber(BaseUserAttr):
    options = ["560", "912", "47", "893"]


class JointPreviousStreetName(BaseUserAttr):
    options = ["Mulberry Rd", "Orchard St", "Pinecrest Dr", "Willow Way"]


class JointPreviousCity(BaseUserAttr):
    options = ["Northfield", "Springview", "Lakeport", "Bayview"]


class JointPreviousState(BaseUserAttr):
    options = ["CO", "NC", "PA", "ME"]


class JointPreviousZip(BaseUserAttr):
    options = ["80203", "27601", "19019", "04401"]


class ReferenceName(BaseUserAttr):
    options = ["Cynthia Park", "Malik Evans", "Serena Lewis", "Diego Ramirez"]


class ReferenceRelationship(BaseUserAttr):
    options = ["Sister", "Uncle", "Friend", "Cousin"]


class ReferenceHouseNumber(BaseUserAttr):
    options = ["4502", "128", "67", "999"]


class ReferenceStreetName(BaseUserAttr):
    options = ["Sunset Blvd", "Highland Ave", "Rivergate Ln", "Oak Terrace"]


class ReferenceCity(BaseUserAttr):
    options = ["Brighton", "Fairmont", "Riverside", "Rosewood"]


class ReferenceState(BaseUserAttr):
    options = ["AZ", "KY", "OH", "ND"]


class ReferenceZip(BaseUserAttr):
    options = ["85001", "40202", "43210", "58201"]


class ReferencePhone(BaseUserAttr):
    options = ["310-555-0101", "415-555-2020", "202-555-3300", "646-555-4040"]


class Employment(BaseUserAttr):
    options = ["Data Scientist", "HR Manager", "Graphic Designer", "Account Executive"]


class EmployeNamer(BaseUserAttr):
    options = [
        "Atlas Corp.",
        "Meridian Solutions",
        "NextGen Innovations",
        "Skyline Ventures",
    ]


class EmployerCity(BaseUserAttr):
    options = ["Newton", "Parkside", "Glendale", "Brookline"]


class LengthEmployed(BaseUserAttr):
    options = ["1 year", "3 years", "6 months", "9 years"]


class GrossMonthlyIncome(BaseUserAttr):
    options = ["$3,800", "$5,200", "$6,400", "$4,100"]


class AdditionalIncome(BaseUserAttr):
    options = ["$400", "$900", "$1,100", "$600"]


class IncomeSource(BaseUserAttr):
    options = ["Tutoring", "Online Sales", "Consulting", "Stock Dividends"]


class BankName(BaseUserAttr):
    options = ["MidFirst Bank", "KeyBank", "Fifth Third Bank", "PNC Bank"]


class BankAccountNumber(BaseUserAttr):
    options = ["787412345", "341278945", "512709384", "109857236"]


class BankruptcyStatus(BaseUserAttr):
    options = ["Never", "2014", "2017", "2021"]


class AutoCreditReference(BaseUserAttr):
    options = [
        "Ally Financial",
        "PNC Auto Loans",
        "TD Auto Finance",
        "USAA Auto Loans",
    ]


class AutoBalanceDue(BaseUserAttr):
    options = ["$5,200", "$9,700", "$14,300", "$6,600"]


class TradingInCar(BaseUserAttr):
    options = ["Yes", "No"]


class RegisteredCarOwner(BaseUserAttr):
    options = ["Self", "Spouse"]


class AutoAmountRequested(BaseUserAttr):
    options = ["$8,000", "$12,000", "$18,500", "$7,300"]


class Term(BaseUserAttr):
    options = ["24 months", "36 months", "48 months", "60 months"]


class Vin(BaseUserAttr):
    options = [
        "1GCHK292X1E123456",
        "WBA3B5G59FNR12345",
        "JM1BK343211234567",
        "2HKYF18794H123456",
    ]


class VehicleYear(BaseUserAttr):
    options = ["2019", "2020", "2021", "2022"]


class VehicleMake(BaseUserAttr):
    options = ["Hyundai", "Subaru", "Volkswagen", "Nissan"]


class VehicleModel(BaseUserAttr):
    options = ["Elantra", "Outback", "Golf", "Sentra"]


class VehicleMiles(BaseUserAttr):
    options = ["12,345", "22,678", "35,890", "9,450"]


class ApplyingWithJointCredit(BaseUserAttr):
    options = ["Yes", "No"]


class Age(BaseUserAttr):
    options = ["22", "34", "41", "57"]


class HomePhoneNumber(BaseUserAttr):
    options = ["209-555-1112", "307-555-3344", "469-555-5566", "762-555-7788"]


class CellPhoneNumber(BaseUserAttr):
    options = ["209-555-9922", "307-555-8734", "469-555-1133", "762-555-8877"]


class JointFirstName(BaseUserAttr):
    options = ["Mary", "Peter", "Emily", "Adam"]


class JointMiddleName(BaseUserAttr):
    options = ["Elara", "Kaia", "Niamh", "Sage"]


class JointLastName(BaseUserAttr):
    options = ["Connors", "Smith", "Mills", "Jones"]


class JointAge(BaseUserAttr):
    options = ["29", "36", "50", "61"]


class JointHomePhoneNumber(BaseUserAttr):
    options = ["208-555-1234", "308-555-5678", "469-555-9012", "763-555-3456"]


class JointEmailAddress(BaseUserAttr):
    options = [
        "maryconnors@example.com",
        "petersmith@example.com",
        "emilymills@example.com",
        "adamjones@example.com",
    ]


class JointCellPhoneNumber(BaseUserAttr):
    options = ["208-555-8888", "308-555-5670", "469-555-9010", "763-555-3400"]


class JointCity(BaseUserAttr):
    options = ["Clearwater", "Riverton", "Maplewood", "Eastfield"]


class JointHouseNumber(BaseUserAttr):
    options = ["123", "456", "789", "101"]


class JointStreetName(BaseUserAttr):
    options = ["Main st.", "Second st.", "Third ave.", "Fourth ave."]


class JointState(BaseUserAttr):
    options = ["FL", "WA", "NY", "CA"]


class JointZip(BaseUserAttr):
    options = ["60608", "98008", "10029", "35006"]


class JointSocialSecurityNumber(BaseUserAttr):
    options = ["111-22-3344", "445-66-7788", "221-33-4455", "778-89-9900"]


class JointResidenceStatus(BaseUserAttr):
    options = [
        ResidenceStatusEnum.Buying.value,
        ResidenceStatusEnum.Renting.value,
        ResidenceStatusEnum.LivingWithRelatives.value,
        ResidenceStatusEnum.Other.value,
    ]


class TimeAtAddressYears(BaseUserAttr):
    options = ["1", "3", "4", "7"]


class TimeAtAddressMonths(BaseUserAttr):
    options = ["2", "5", "8", "10"]


class JointTimeAtAddressYears(BaseUserAttr):
    options = ["2", "4", "6", "9"]


class JointTimeAtAddressMonths(BaseUserAttr):
    options = ["3", "6", "9", "11"]


class MortgageCompanyLandlord(BaseUserAttr):
    options = [
        "BrightStar Mortgage",
        "BlueRiver Realty",
        "Prime Homes Rentals",
        "Heritage Lending",
    ]


class JointMortgageCompanyLandlord(BaseUserAttr):
    options = [
        "Pinecone Mortgage",
        "Horizon Realty",
        "Metro Homes Rentals",
        "Summit Lending",
    ]


class JointMortgageRent(BaseUserAttr):
    options = ["$900", "$1,100", "$1,400", "$2,000"]


class PreviousResidenceStatus(BaseUserAttr):
    options = [
        ResidenceStatusEnum.Other.value,
        ResidenceStatusEnum.Buying.value,
        ResidenceStatusEnum.Renting.value,
        ResidenceStatusEnum.LivingWithRelatives.value,
    ]


class JointPreviousResidenceStatus(BaseUserAttr):
    options = [
        ResidenceStatusEnum.LivingWithRelatives.value,
        ResidenceStatusEnum.Other.value,
        ResidenceStatusEnum.Buying.value,
        ResidenceStatusEnum.Renting.value,
    ]

class TimeAtPreviousAddressYears(BaseUserAttr):
    options = ["1", "2", "4", "6"]


class TimeAtPreviousAddressMonths(BaseUserAttr):
    options = ["1", "4", "7", "11"]


class JointTimeAtPreviousAddressYears(BaseUserAttr):
    options = ["1", "3", "5", "7"]


class JointTimeAtPreviousAddressMonths(BaseUserAttr):
    options = ["2", "5", "8", "12"]


class ReferenceCellPhone(BaseUserAttr):
    options = ["310-555-0000", "415-555-1111", "202-555-2222", "646-555-3333"]


class ReferenceHomePhone(BaseUserAttr):
    options = ["310-555-4444", "415-555-5555", "202-555-6666", "646-555-7777"]


class JointReferenceFirstName(BaseUserAttr):
    options = ["Derek", "Hannah", "Gabriel", "Nina"]


class JointReferenceLastName(BaseUserAttr):
    options = ["Bennett", "Peterson", "Martinez", "Foster"]


class JointReferenceRelationship(BaseUserAttr):
    options = ["Father", "Sister", "Friend", "Cousin"]


class JointReferenceHouseNumber(BaseUserAttr):
    options = ["510", "808", "72", "43"]


class JointReferenceStreetName(BaseUserAttr):
    options = ["Evergreen Rd", "Silver Lake Dr", "Crescent Ave", "Sunrise Blvd"]


class JointReferenceCity(BaseUserAttr):
    options = ["Springfield", "Havenport", "Lakeshire", "Brightvale"]


class JointReferenceState(BaseUserAttr):
    options = ["SC", "UT", "AK", "LA"]


class JointReferenceZip(BaseUserAttr):
    options = ["29201", "84321", "99501", "70112"]


class JointReferenceCellPhone(BaseUserAttr):
    options = ["210-555-8888", "414-555-9999", "203-555-1010", "641-555-1111"]


class JointReferenceHomePhone(BaseUserAttr):
    options = ["210-555-1212", "414-555-3434", "203-555-5656", "641-555-7878"]


class Reference2Name(BaseUserAttr):
    options = ["Ana Wilson", "Corey Bell", "Tanya Singh", "Oscar Phillips"]


class Reference2HouseNumber(BaseUserAttr):
    options = ["2211", "654", "899", "1420"]


class Reference2StreetName(BaseUserAttr):
    options = ["Lakewood Dr", "Vine St", "Forest Ave", "Kingston Rd"]


class Reference2City(BaseUserAttr):
    options = ["Madison", "Rockford", "Bloomfield", "Lincoln Park"]


class Reference2State(BaseUserAttr):
    options = ["WI", "IL", "MI", "NJ"]


class Reference2Zip(BaseUserAttr):
    options = ["53703", "61107", "48302", "07052"]


class Reference2CellPhone(BaseUserAttr):
    options = ["240-333-3333", "241-444-4444", "242-555-5555", "243-666-6666"]


class Reference2HomePhone(BaseUserAttr):
    options = ["240-111-1111", "241-222-2222", "242-777-7777", "243-888-8888"]


class JointReference2Name(BaseUserAttr):
    options = ["Lucille Gray", "Tyler Morgan", "Fiona Cruz", "Adrian Lopez"]


class JointReference2FullAddress(BaseUserAttr):
    options = [
        "988 South Oak Dr, Glendale, CA, 91204",
        "530 West Pine Ln, Troy, MI, 48083",
        "234 Maple Circle, Bentonville, AR, 72712",
        "1608 Birch Ave, Orlando, FL, 32801",
    ]


class JointReference2CellPhone(BaseUserAttr):
    options = ["270-999-9999", "271-123-1234", "272-456-4567", "273-789-7890"]


class JointReference2HomePhone(BaseUserAttr):
    options = ["274-234-2345", "275-345-3456", "276-567-5678", "277-678-6789"]


class EmployerName(BaseUserAttr):
    options = [
        "BrightTech Solutions",
        "Crest Marketing",
        "Secure Finances",
        "Transit Logistics",
    ]


class EmployerLengthYears(BaseUserAttr):
    options = ["1", "3", "5", "9"]


class EmployerPosition(BaseUserAttr):
    options = [
        "Software Engineer",
        "Marketing Manager",
        "Financial Analyst",
        "Project Coordinator",
    ]


class EmployerWorkPhone(BaseUserAttr):
    options = ["310-555-7211", "415-555-9222", "202-555-7333", "646-555-8444"]


class JointEmployerName(BaseUserAttr):
    options = ["DeltaTech Corp", "Zenith Consulting", "Lunar Finance", "Apex Partners"]


class JointEmployerCity(BaseUserAttr):
    options = ["Weston", "Bridgeport", "Fairford", "Millcreek"]


class JointEmployerLengthYears(BaseUserAttr):
    options = ["2", "4", "6", "10"]


class JointEmployerPosition(BaseUserAttr):
    options = ["Supervisor", "Manager", "Analyst", "Director"]


class JointEmployerWorkPhone(BaseUserAttr):
    options = ["310-555-5559", "415-555-6667", "202-555-7774", "646-555-8883"]


class JointGrossMonthlyIncome(BaseUserAttr):
    options = ["$2,800", "$4,200", "$5,000", "$5,900"]


class AdditionalIncomeSource(BaseUserAttr):
    options = ["Freelancing", "Part-time Tutoring", "Investments", "Online Business"]


class AdditionalMonthlyIncome(BaseUserAttr):
    options = ["$300", "$600", "$1,200", "$900"]


class JointAdditionalIncomeSource(BaseUserAttr):
    options = ["Child Support", "Small Business", "Online Sales", "Stocks/Dividends"]


class JointAdditionalMonthlyIncome(BaseUserAttr):
    options = ["$400", "$800", "$1,300", "$700"]


class PreviousEmployerName(BaseUserAttr):
    options = [
        "Sunrise Tech",
        "Green Leaf Marketing",
        "Balanced Finance Group",
        "LogiPlus",
    ]


class PreviousEmployerCity(BaseUserAttr):
    options = ["Somerset", "Eagleton", "Ridgeville", "Clayton"]


class PreviousEmployerPosition(BaseUserAttr):
    options = ["Clerk", "Analyst", "Manager", "Supervisor"]


class PreviousLengthEmployed(BaseUserAttr):
    options = ["8 months", "1 year", "2 years", "4 years"]


class JointPreviousEmployerName(BaseUserAttr):
    options = [
        "Moonlight Software",
        "Terrace Marketing",
        "New Age Finance",
        "Global Express",
    ]


class JointPreviousEmployerCity(BaseUserAttr):
    options = ["Bartlett", "Waterford", "Sanford", "Coralview"]


class JointPreviousEmployerPosition(BaseUserAttr):
    options = ["Clerk", "Analyst", "Manager", "Supervisor"]


class JointPreviousLengthEmployed(BaseUserAttr):
    options = ["8 months", "1 year", "2 years", "4 years"]


class BankAddress(BaseUserAttr):
    options = [
        "430 Mason St, Dallas, TX, 75202",
        "902 Redwood Ave, Seattle, WA, 98109",
        "123 Pine Circle, Denver, CO, 80202",
        "567 Oak Blvd, Miami, FL, 33131",
    ]


class JointBankName(BaseUserAttr):
    options = ["Union Bank", "HSBC", "BB&T", "SunTrust"]


class JointBankAddress(BaseUserAttr):
    options = [
        "210 Elm St, Boston, MA, 02108",
        "781 Maple Ln, Portland, OR, 97205",
        "345 Alder Ave, Chicago, IL, 60611",
        "190 Redwood Dr, Phoenix, AZ, 85004",
    ]


class JointBankAccountNumber(BaseUserAttr):
    options = ["511111111", "522222222", "533333333", "544444444"]


class BankruptcyYear(BaseUserAttr):
    options = ["2015", "2018", "2020", "2022"]


class JointBankruptcyStatus(BaseUserAttr):
    options = ["Never", "2015", "2018", "2020"]


class JointBankruptcyYear(BaseUserAttr):
    options = ["None", "2018", "2020", "2022"]


class TodaysDate(BaseUserAttr):
    options = ["02/17/2023", "07/10/2023", "11/28/2024", "03/06/2025"]
