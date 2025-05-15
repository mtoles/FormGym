"""
File defining fields APPEARING in a form

Types of fields:
- Text
- Checkbox

NOTE TO EDITORS:
"""

from typing import List
from abc import ABC, abstractmethod
import user_features
from dateutil.parser import parse, ParserError


# -----------------------------------------
# Utility Functions
# -----------------------------------------
def numerize(s):
    ls = list(s)
    valid = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
    return str([x for x in ls if x in valid])


def remove_punctuation(s):
    # replace punctuation with space
    s = "".join(
        " " if c in "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c" else c
        for c in s
    )
    # replace all whitespace with spaces
    s = " ".join(s.split())
    return s


def concat_agent_generations(agent_generations):
    return " ".join(
        [
            x["value"]
            for x in sorted(
                agent_generations, key=lambda item: (item["cy"], item["cx"])
            )
        ]
    )


def concatenate_address(house_number, street_name, city, state, zipcode):
    return f"{house_number} {street_name}, {city}, {state}, {zipcode}"


# -----------------------------------------
# Metaclass and BaseField
# -----------------------------------------
class FieldMeta(type):
    """
    Metaclass for possible form fields
    """

    registry = {}

    def __new__(cls, name, bases, attrs):
        new_p_attr = super().__new__(cls, name, bases, attrs)
        if name != "BaseField":
            # check for duplicates
            assert name not in cls.registry, f"User attribute {name} already exists"
            cls.registry[name] = new_p_attr
        return new_p_attr


class BaseField(metaclass=FieldMeta):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @abstractmethod
    def is_correct(self, agent_generation, user_profile):
        raise NotImplemented

    @abstractmethod
    def get_profile_info(self, user_profile):
        raise NotImplemented


class BaseNumericField(BaseField):
    # def is_correct(self, agent_generation, user_profile):
    def is_correct(self, agent_generations_inside, profile_info: str):
        # agent_generations_inside = get_inputs_inside_field(self, agent_generation)
        concatted_input = concat_agent_generations(agent_generations_inside)
        # profile_info = self.get_profile_info(user_profile)
        return numerize(profile_info) == numerize(concatted_input)


class BaseStringField(BaseField):
    # def is_correct(self, agent_generation, user_profile):
    def is_correct(self, agent_generations_inside, profile_info: str):
        # agent_generations_inside = get_inputs_inside_field(self, agent_generation)
        concatted_input = concat_agent_generations(agent_generations_inside)
        # profile_info = self.get_profile_info(user_profile)
        return (
            remove_punctuation(profile_info).lower()
            == remove_punctuation(concatted_input).lower()
        )


class BaseCheckboxField(BaseField):
    # def is_correct(self, agent_generation, user_profile):
    def is_correct(self, agent_generations_inside, profile_info: bool):
        assert isinstance(profile_info, bool)
        concatted_input = concat_agent_generations(agent_generations_inside).lower()
        if profile_info:
            return concatted_input == "x"
        else:
            return concatted_input == ""


class BaseDateField(BaseField):
    def is_correct(self, agent_generations_inside, profile_info: str):
        assert isinstance(profile_info, str)
        concatted_input = concat_agent_generations(agent_generations_inside)
        gt_date = parse(profile_info).date()
        try:
            input_date = parse(concatted_input).date()
        except ParserError:
            return False
        return input_date == gt_date

class BaseNameField(BaseField):
    def is_correct(self, agent_generations_inside, profile_info: str):
        assert isinstance(profile_info, str)
        concatted_input = concat_agent_generations(agent_generations_inside)
        pred_words = concatted_input.split()
        gt_words = profile_info.split()
        # first name
        if len(set(pred_words)) <=2:
            return False
        for pred_word in pred_words:
            if pred_word not in gt_words:
                return False
        return True
        
class AnnotatedField(BaseField):
    pass


class SignOrInitial(BaseField):
    def is_correct(self, agent_generations_inside, profile_info: bool):
        if len(agent_generations_inside) != 1:
            return False
        agent_gen = agent_generations_inside[0]
        if agent_gen["action"] != "Sign":
            return False
        signature_val = agent_gen["value"]

        return profile_info == signature_val


class Signature(SignOrInitial):
    @classmethod
    def get_profile_info(self, user_profile: bool):
        return user_profile.features.FirstName + " " + user_profile.features.LastName


class Initials(SignOrInitial):
    @classmethod
    def get_profile_info(self, user_profile):
        return user_profile.features.FirstName[0] + user_profile.features.LastName[0]


class JointSignature(SignOrInitial):
    @classmethod
    def get_profile_info(self, user_profile):
        return (
            user_profile.features.JointFirstName
            + " "
            + user_profile.features.JointLastName
        )


class JointInitials(SignOrInitial):
    @classmethod
    def get_profile_info(self, user_profile):
        return (
            user_profile.features.JointFirstName[0]
            + user_profile.features.JointLastName[0]
        )


def get_inputs_inside_field(field: BaseField, agent_generations: List):
    return [
        ag
        for ag in agent_generations
        if (
            ag["cx"] >= field.x
            and ag["cx"] <= field.x + field.w
            and ag["cy"] >= field.y
            and ag["cy"] <= field.y + field.h
        )
    ]


# -----------------------------------------
# LOAN / VEHICLE FIELDS
# -----------------------------------------
class AutoAmountRequested(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AutoAmountRequested


class Term(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Term


class Vin(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Vin


class VehicleYear(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.VehicleYear


class VehicleMakeAndModel(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.VehicleMake + " " + user_profile.features.VehicleModel
        )


class VehicleMiles(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.VehicleMiles


# -----------------------------------------
# APPLICANT PERSONAL INFORMATION
# -----------------------------------------
class ApplyingWithJointCredit(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApplyingWithJointCredit


class FullName(BaseNameField):
    @classmethod
    def get_profile_info(cls, user_profile):
        if (
            not hasattr(user_profile.features, "FirstName")
            or not hasattr(user_profile.features, "MiddleName")
            or not hasattr(user_profile.features, "LastName")
            or not hasattr(user_profile.features, "Suffix")
        ):
            raise Exception(
                "No user_feature for FullName. Expected FirstName, MiddleName, LastName."
            )
        return f"{user_profile.features.FirstName} {user_profile.features.MiddleName} {user_profile.features.LastName} {user_profile.features.Suffix}"


class LastName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LastName


class MiddleInitial(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MiddleName[0]


class JointMiddleInitial(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointMiddleName[0]


class JointLastName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointLastName


class FirstName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FirstName


class JointFirstName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointFirstName


class Suffix(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Suffix


class JointSuffix(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointSuffix


class Age(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Age


class HomePhoneNumber(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HomePhoneNumber


class EmailAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmailAddress


class CellPhoneNumber(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CellPhoneNumber


class FullAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        return concatenate_address(
            feat.HouseNumber, feat.StreetName, feat.City, feat.State, feat.Zip
        )


class HouseNumberAndStreetAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        return feat.HouseNumber + " " + feat.StreetName


class CityState(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        needed = ["City", "State"]
        for n in needed:
            if not hasattr(feat, n):
                raise Exception(f"No user_feature for {n} in CityState.")
        return f"{feat.City}, {feat.State}"


class City(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.City


class State(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.State


class Zip(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Zip


class SocialSecurityNumber(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SocialSecurityNumber


class FullBirthDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        needed = ["BirthMonth", "BirthDay", "BirthYear"]
        for n in needed:
            if not hasattr(feat, n):
                raise Exception(f"No user_feature for {n} in FullBirthDate.")
        return f"{feat.BirthMonth}/{feat.BirthDay}/{feat.BirthYear}"


# -----------------------------------------
# JOINT APPLICANT PERSONAL INFORMATION
# -----------------------------------------
class JointFullName(BaseNameField):
    @classmethod
    def get_profile_info(cls, user_profile):
        # user_features do not provide separate joint first/middle/last name attributes
        # raise Exception("No user_feature for JointFullName.")
        return " ".join(
            [
                user_profile.features.JointFirstName,
                user_profile.features.JointMiddleName,
                user_profile.features.JointLastName,
                user_profile.features.JointSuffix,
            ]
        )


class JointAge(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointAge


class JointHomePhoneNumber(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointHomePhoneNumber


class JointEmailAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmailAddress


class JointCellPhoneNumber(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointCellPhoneNumber


class JointFullAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return concatenate_address(
            user_profile.features.JointHouseNumber,
            user_profile.features.JointStreetName,
            user_profile.features.JointCity,
            user_profile.features.JointState,
            user_profile.features.JointZip,
        )


class JointHouseNumberAndStreetAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointHouseNumber
            + " "
            + user_profile.features.JointStreetName
        )


class JointCity(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointCity


class JointState(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointState


class JointZip(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointZip


class JointSocialSecurityNumber(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointSocialSecurityNumber


class JointFullBirthDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return f"{user_profile.features.JointBirthMonth}/{user_profile.features.JointBirthDay}/{user_profile.features.JointBirthYear}"


class NumDependents(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NumDependents


class JointNumDependents(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointNumDependents


# -----------------------------------------
# FIELDS WITH UNDERSCORES - IGNORE FOR NOW
# (including checkboxes/residence status)
# -----------------------------------------
# Skipped as per instructions.


# -----------------------------------------
# TIME AT ADDRESS (no underscore)
# -----------------------------------------
class TimeAtAddressYears(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimeAtAddressYears


class TimeAtAddressMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimeAtAddressMonths


class JointTimeAtAddressYears(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointTimeAtAddressYears


class JointTimeAtAddressMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointTimeAtAddressMonths


class MortgageCompanyLandlord(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MortgageCompanyLandlord


class JointMortgageCompanyLandlord(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointMortgageCompanyLandlord


class MonthlyMortgageOrRent(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MonthlyMortgageOrRent


class JointMonthlyMortgageOrRent(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointMortgageRent


# -----------------------------------------
# PREVIOUS RESIDENCE
# -----------------------------------------
class PreviousFullAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        needed = [
            "PreviousHouseNumber",
            "PreviousStreetName",
            "PreviousCity",
            "PreviousState",
            "PreviousZip",
        ]
        for n in needed:
            if not hasattr(feat, n):
                raise Exception(f"No user_feature for {n} in PreviousFullAddress.")
        return f"{feat.PreviousHouseNumber} {feat.PreviousStreetName}, {feat.PreviousCity}, {feat.PreviousState}, {feat.PreviousZip}"


class JointPreviousFullAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        needed = [
            "JointPreviousHouseNumber",
            "JointPreviousStreetName",
            "JointPreviousCity",
            "JointPreviousState",
            "JointPreviousZip",
        ]
        for n in needed:
            if not hasattr(feat, n):
                raise Exception(f"No user_feature for {n} in JointPreviousFullAddress.")
        return f"{feat.JointPreviousHouseNumber} {feat.JointPreviousStreetName}, {feat.JointPreviousCity}, {feat.JointPreviousState}, {feat.JointPreviousZip}"


class TimeAtPreviousAddressYears(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimeAtPreviousAddressYears


class TimeAtPreviousAddressMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimeAtPreviousAddressMonths


class JointTimeAtPreviousAddressYears(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointTimeAtPreviousAddressYears


class JointTimeAtPreviousAddressMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointTimeAtPreviousAddressMonths


# -----------------------------------------
# REFERENCES
# -----------------------------------------
class ReferenceName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferenceName


class ReferenceRelationship(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferenceRelationship


class ReferenceFullAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        needed = [
            "ReferenceHouseNumber",
            "ReferenceStreetName",
            "ReferenceCity",
            "ReferenceState",
            "ReferenceZip",
        ]
        for n in needed:
            if not hasattr(feat, n):
                raise Exception(f"No user_feature for {n} in ReferenceFullAddress.")
        return f"{feat.ReferenceHouseNumber} {feat.ReferenceStreetName}, {feat.ReferenceCity}, {feat.ReferenceState}, {feat.ReferenceZip}"


class ReferenceCellPhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferenceCellPhone


class ReferenceHomePhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferenceHomePhone


class JointReferenceName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        return f"{feat.JointReferenceFirstName} {feat.JointReferenceLastName}"


class JointReferenceRelationship(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReferenceRelationship


class JointReferenceFullAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        return f"{feat.JointReferenceHouseNumber} {feat.JointReferenceStreetName}, {feat.JointReferenceCity}, {feat.JointReferenceState}, {feat.JointReferenceZip}"


class JointReferenceCellPhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReferenceCellPhone


class JointReferenceHomePhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReferenceHomePhone


# -----------------------------------------
# SECOND REFERENCE
# -----------------------------------------
class Reference2Name(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reference2Name


class Reference2FullAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        return f"{feat.Reference2HouseNumber} {feat.Reference2StreetName}, {feat.Reference2City}, {feat.Reference2State}, {feat.Reference2Zip}"


class Reference2CellPhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reference2CellPhone


class Reference2Relationship(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reference2Relationship


class Reference2HomePhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reference2HomePhone


class JointReference2Name(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReference2Name


class JointReference2FullAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        # This is provided as one string in user_features
        return user_profile.features.JointReference2FullAddress


class JointReference2CellPhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReference2CellPhone


class JointReference2HomePhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReference2HomePhone


# -----------------------------------------
# EMPLOYMENT
# -----------------------------------------
class EmployerName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerName


class EmployerCity(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerCity


class EmployerLengthYears(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerLengthYears


class EmployerLengthMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerLengthMonths


class EmployerPosition(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerPosition


class EmployerWorkPhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerWorkPhone


class GrossMonthlyIncome(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GrossMonthlyIncome


class JointEmployerName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerName


class JointEmployerCity(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerCity


class JointEmployerLengthYears(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerLengthYears


class JointEmployerLengthMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerLengthMonths


class JointEmployerPosition(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerPosition


class JointEmployerWorkPhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerWorkPhone


class JointGrossMonthlyIncome(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointGrossMonthlyIncome


# -----------------------------------------
# ADDITIONAL INCOME
# -----------------------------------------
class AdditionalIncomeSource(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdditionalIncomeSource


class AdditionalMonthlyIncome(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdditionalMonthlyIncome


class JointAdditionalIncomeSource(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointAdditionalIncomeSource


class JointAdditionalMonthlyIncome(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointAdditionalMonthlyIncome


# -----------------------------------------
# PREVIOUS EMPLOYER
# -----------------------------------------
class PreviousEmployerName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousEmployerName


class PreviousEmployerCity(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousEmployerCity


class PreviousEmployerPosition(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousEmployerPosition


class PreviousLengthEmployed(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousLengthEmployed


class JointPreviousEmployerName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousEmployerName


class JointPreviousEmployerCity(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousEmployerCity


class JointPreviousEmployerPosition(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousEmployerPosition


class JointPreviousLengthEmployed(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousLengthEmployed


# -----------------------------------------
# BANK INFORMATION
# -----------------------------------------
class BankName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BankName


class BankAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BankAddress


class BankAccountNumber(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BankAccountNumber


class JointBankName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointBankName


class JointBankAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointBankAddress


class JointBankAccountNumber(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointBankAccountNumber


# -----------------------------------------
# BANKRUPTCY
# -----------------------------------------
class BankruptcyStatus(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BankruptcyStatus


class BankruptcyYear(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BankruptcyYear


class JointBankruptcyStatus(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointBankruptcyStatus


class JointBankruptcyYear(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointBankruptcyYear


# -----------------------------------------
# AUTO TRADE-IN
# -----------------------------------------
class TradingInCar(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TradingInCar


class AutoBalanceDue(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AutoBalanceDue


class AutoCreditReference(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AutoCreditReference


class RegisteredCarOwner(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RegisteredCarOwner


# -----------------------------------------
# DATE FIELDS
# -----------------------------------------
class TodaysDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TodaysDate


# -----------------------------------------
# Business FIELDS
# -----------------------------------------


class BusinessType(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BusinessType


class TimeInBusinessYears(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimeInBusinessYears


class TimeInBusinessMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimeInBusinessMonths


class JointBusinessType(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointBusinessType


class JointTimeInBusinessYears(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointTimeInBusinessYears


class JointTimeInBusinessMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointTimeInBusinessMonths


# -----------------------------------------
# CHECKBOX FIELDS
# -----------------------------------------

# Additional classes with underscores that raise exceptions:


class ResidenceStatus_Buying(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.ResidenceStatus
            == user_features.ResidenceStatusEnum.Buying.value
        )


class ResidenceStatus_Renting(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.ResidenceStatus
            == user_features.ResidenceStatusEnum.Renting.value
        )


class ResidenceStatus_Relatives(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.ResidenceStatus
            == user_features.ResidenceStatusEnum.LivingWithRelatives.value
        )


class ResidenceStatus_Own(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.ResidenceStatus
            == user_features.ResidenceStatusEnum.Own.value
        )


class ResidenceStatus_Other(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.ResidenceStatus
            == user_features.ResidenceStatusEnum.Other.value
        )


class JointResidenceStatus_Buying(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointResidenceStatus
            == user_features.ResidenceStatusEnum.Buying.value
        )


class JointResidenceStatus_Renting(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointResidenceStatus
            == user_features.ResidenceStatusEnum.Renting.value
        )


class JointResidenceStatus_Relatives(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointResidenceStatus
            == user_features.ResidenceStatusEnum.LivingWithRelatives.value
        )


class JointResidenceStatus_Own(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointResidenceStatus
            == user_features.ResidenceStatusEnum.Own.value
        )


class JointResidenceStatus_Other(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointResidenceStatus
            == user_features.ResidenceStatusEnum.Other.value
        )


class PreviousResidenceStatus_Buying(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreviousResidenceStatus
            == user_features.ResidenceStatusEnum.Buying.value
        )


class PreviousResidenceStatus_Renting(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreviousResidenceStatus
            == user_features.ResidenceStatusEnum.Renting.value
        )


class PreviousResidenceStatus_Relatives(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreviousResidenceStatus
            == user_features.ResidenceStatusEnum.LivingWithRelatives.value
        )


class JointPreviousResidenceStatus_Buying(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointPreviousResidenceStatus
            == user_features.ResidenceStatusEnum.Buying.value
        )


class JointPreviousResidenceStatus_Renting(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointPreviousResidenceStatus
            == user_features.ResidenceStatusEnum.Renting.value
        )


class JointPreviousResidenceStatus_Relatives(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointPreviousResidenceStatus
            == user_features.ResidenceStatusEnum.LivingWithRelatives.value
        )


class EnterpriseType_Corporation(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.EnterpriseType
            == user_features.EnterpriseTypeEnum.Corporation.value
        )


class EnterpriseType_LLC(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.EnterpriseType
            == user_features.EnterpriseTypeEnum.LLC.value
        )


class EnterpriseType_Proprietorship(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.EnterpriseType
            == user_features.EnterpriseTypeEnum.Proprietorship.value
        )


class EnterpriseType_Partnership(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.EnterpriseType
            == user_features.EnterpriseTypeEnum.Partnership.value
        )


class JointEnterpriseType_Corporation(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.EnterpriseType
            == user_features.EnterpriseTypeEnum.Corporation.value
        )


class JointEnterpriseType_LLC(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.EnterpriseType
            == user_features.EnterpriseTypeEnum.LLC.value
        )


class JointEnterpriseType_Proprietorship(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.EnterpriseType
            == user_features.EnterpriseTypeEnum.Proprietorship.value
        )


class JointEnterpriseType_Partnership(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.EnterpriseType
            == user_features.EnterpriseTypeEnum.Partnership.value
        )


class GrossIncomePeriod_Monthly(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.GrossIncomePeriod
            == user_features.GrossIncomePeriodEnum.Monthly.value
        )


class JointGrossIncomePeriod_Monthly(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointGrossIncomePeriod
            == user_features.GrossIncomePeriodEnum.Monthly.value
        )


class GrossIncomePeriod_Yearly(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.GrossIncomePeriod
            == user_features.GrossIncomePeriodEnum.Yearly.value
        )


class JointGrossIncomePeriod_Yearly(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointGrossIncomePeriod
            == user_features.GrossIncomePeriodEnum.Yearly.value
        )


# -----------------------------------------
# SORT LATER
# -----------------------------------------


class TimeAtAddressYearsAndMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.TimeAtAddressYears
            + " years "
            + user_profile.features.TimeAtAddressMonths
            + " months"
        )


class JointTimeAtAddressYearsAndMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointTimeAtAddressYears
            + " years "
            + user_profile.features.JointTimeAtAddressMonths
            + " months"
        )


class ResidenceStatus(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResidenceStatus


class JointResidenceStatus(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointResidenceStatus


class PreviousAddressFull(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return concatenate_address(
            user_profile.features.PreviousHouseNumber,
            user_profile.features.PreviousStreetName,
            user_profile.features.PreviousCity,
            user_profile.features.PreviousState,
            user_profile.features.PreviousZip,
        )


class JointPreviousAddressFull(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return concatenate_address(
            user_profile.features.JointPreviousHouseNumber,
            user_profile.features.JointPreviousStreetName,
            user_profile.features.JointPreviousCity,
            user_profile.features.JointPreviousState,
            user_profile.features.JointPreviousZip,
        )


class EmployerAddressFull(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return concatenate_address(
            user_profile.features.EmployerHouseNumber,
            user_profile.features.EmployerStreetName,
            user_profile.features.EmployerCity,
            user_profile.features.EmployerState,
            user_profile.features.EmployerZip,
        )


class JointEmployerAddressFull(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return concatenate_address(
            user_profile.features.JointEmployerHouseNumber,
            user_profile.features.JointEmployerStreetName,
            user_profile.features.JointEmployerCity,
            user_profile.features.JointEmployerState,
            user_profile.features.JointEmployerZip,
        )


class DriversLicenseNo(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DriversLicenseNo


class JointDriversLicenseNo(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointDriversLicenseNo


class LoanType_Vehicle(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.LoanType == user_features.LoanTypeEnum.Vehicle.value
        )


class LoanType_Personal(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.LoanType == user_features.LoanTypeEnum.Personal.value
        )


class LoanType_Credit(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LoanType == user_features.LoanTypeEnum.Credit.value


class VehicleLoanCondition_New(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.VehicleLoanCondition
            == user_features.VehicleLoanConditionEnum.New.value
        )


class VehicleLoanCondition_Used(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.VehicleLoanCondition
            == user_features.VehicleLoanConditionEnum.Used.value
        )


class VehicleLoanCondition_Refinance(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.VehicleLoanCondition
            == user_features.VehicleLoanConditionEnum.Refinance.value
        )


class VehicleLoanType_Auto(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.VehicleLoanType
            == user_features.VehicleLoanTypeEnum.Auto.value
        )


class VehicleLoanType_TruckOrSUV(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.VehicleLoanType
            == user_features.VehicleLoanTypeEnum.TruckOrSUV.value
        )


class VehicleLoanType_RV(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.VehicleLoanType
            == user_features.VehicleLoanTypeEnum.RV.value
        )


class VehicleLoanType_Motorcyle(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.VehicleLoanType
            == user_features.VehicleLoanTypeEnum.Motorcycle.value
        )


class VehicleLoanType_Boat(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.VehicleLoanType
            == user_features.VehicleLoanTypeEnum.Boat.value
        )


class VehicleLoanType_Watercraft(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.VehicleLoanType
            == user_features.VehicleLoanTypeEnum.Watercraft.value
        )


class PersonalAmountRequested(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PersonalAmountRequested


class PersonalLoanPurpose(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PersonalLoanPurpose


class CreditAmountRequested(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CreditAmountRequested


class CreditLoanPurpose(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CreditLoanPurpose


class AfcuAccountNo(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AfcuAccountNo


class JointAfcuAccountNo(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointAfcuAccountNo


class EmployerHireDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerHireDate


class JointEmployerHireDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerHireDate


class DriversLicenseExpirationDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DriversLicenseExpirationDate


class JointDriversLicenseExperationDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointDriversLicenseExpirationDate


class DriversLicenseState(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DriversLicenseState


class JointDriversLicenseState(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointDriversLicenseState


class MarriageStatus_Married(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.MarriageStatus
            == user_features.MarriageStatusEnum.Married.value
        )


class MarriageStatus_Separated(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.MarriageStatus
            == user_features.MarriageStatusEnum.Separated.value
        )


class MarriageStatus_Single(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.MarriageStatus
            == user_features.MarriageStatusEnum.Single.value
        )


class JointMarriageStatus_Married(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointMarriageStatus
            == user_features.MarriageStatusEnum.Married.value
        )


class JointMarriageStatus_Separated(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointMarriageStatus
            == user_features.MarriageStatusEnum.Separated.value
        )


class JointMarriageStatus_Single(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointMarriageStatus
            == user_features.MarriageStatusEnum.Single.value
        )


class JointReferencePhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReferencePhone


class ReferencePhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferencePhone


class JointReferenceCity(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReferenceCity


class JointReferenceState(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReferenceState


class JointReferenceZip(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReferenceZip


class ReferenceCity(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferenceCity


class ReferenceState(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferenceState


class ReferenceZip(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferenceZip


### CROI classes ###


class CROI_4435(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_4435


class CROI_4436(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_4436


class CROI_4012(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_4012


class CROI_B485(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_B485


class CROI_B486(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_B486


class CROI_4058(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_4058


class CROI_4010(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(
            int(user_profile.features.CROI_4435)
            + int(user_profile.features.CROI_4436)
            + int(user_profile.features.CROI_4012)
            + int(user_profile.features.CROI_B485)
            + int(user_profile.features.CROI_B486)
            + int(user_profile.features.CROI_4058)
        )


class CROI_4065(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_4065


class CROI_4115(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_4115


class CROI_B488(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_B488


class CROI_B489(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_B489


class CROI_4060(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_4060


class CROI_4020(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_4020


class CROI_4518(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_4518


class CROI_4107(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(
            int(CROI_4010.get_profile_info(user_profile))
            + int(user_profile.features.CROI_4065)
            + int(user_profile.features.CROI_4115)
            + int(user_profile.features.CROI_B488)
            + int(user_profile.features.CROI_B489)
            + int(user_profile.features.CROI_4060)
            + int(user_profile.features.CROI_4020)
            + int(user_profile.features.CROI_4518)
        )


class CROI_4508(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_4508


class CROI_0093(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_0093


class CROI_HK03(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_HK03


class CROI_HK04(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_HK04


class CROI_4180(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_4180


class CROI_4185(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_4185


class CROI_4200(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_4200


class CROI_4073(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(
            int(user_profile.features.CROI_4508)
            + int(user_profile.features.CROI_0093)
            + int(user_profile.features.CROI_HK03)
            + int(user_profile.features.CROI_HK04)
            + int(user_profile.features.CROI_4180)
            + int(user_profile.features.CROI_4185)
            + int(user_profile.features.CROI_4200)
        )


class CROI_4074(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(
            int(CROI_4107.get_profile_info(user_profile))
            - int(CROI_4073.get_profile_info(user_profile))
        )


class CROI_JJ33(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CROI_JJ33
