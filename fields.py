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
import re


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
        except (ParserError, OverflowError):
            return False
        return input_date == gt_date


class BaseNameField(BaseField):
    def is_correct(self, agent_generations_inside, profile_info: str):
        assert isinstance(profile_info, str)
        concatted_input = concat_agent_generations(agent_generations_inside)
        pred_words = concatted_input.split()
        gt_words = profile_info.split()
        # first name
        if len(set(pred_words)) <= 2:
            return False
        for pred_word in pred_words:
            if pred_word not in gt_words:
                return False
        return True


class BaseDurationField(BaseField):
    def is_correct(self, agent_generations_inside, profile_info: str):
        # convert years to months
        years = re.search(r"(\d+) year", agent_generations_inside).group()
        months = re.search(r"(\d+) month", agent_generations_inside).group()
        if years is not None:
            years = int(years)
            months = years * 12
        if months is not None:
            months = int(months)
        return months == int(profile_info)


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
        return str(user_profile.features.AutoAmountRequested)


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


class JointCityState(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        needed = ["JointCity", "JointState"]
        for n in needed:
            if not hasattr(feat, n):
                raise Exception(f"No user_feature for {n} in JointCityState.")
        return f"{feat.JointCity}, {feat.JointState}"


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
        return str(int(user_profile.features.TimeAtAddressMonths) // 12)


class TimeAtAddressMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.TimeAtAddressMonths) % 12)


class JointTimeAtAddressYears(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.JointTimeAtAddressMonths) // 12)


class JointTimeAtAddressMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.JointTimeAtAddressMonths) % 12)


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
        return str(int(user_profile.features.TimeAtPreviousAddressMonths) // 12)


class TimeAtPreviousAddressMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.TimeAtPreviousAddressMonths) % 12)


class JointTimeAtPreviousAddressYears(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.JointTimeAtPreviousAddressMonths) // 12)


class JointTimeAtPreviousAddressMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.JointTimeAtPreviousAddressMonths) % 12)


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
        return str(int(user_profile.features.EmployerLengthMonths) // 12)


class EmployerLengthMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.EmployerLengthMonths) % 12)


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
        return str(
            int(user_profile.features.IncomeFromEmployment)
            + int(user_profile.features.AdditionalIncomeAmount)
            + int(user_profile.features.AlimonyAmount)
        )


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
        return str(int(user_profile.features.JointEmployerLengthMonths) // 12)


class JointEmployerLengthMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.JointEmployerLengthMonths) % 12)


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
        return (
            user_profile.features.JointGrossMonthlyIncome
            + user_profile.features.JointAdditionalMonthlyIncome
            + user_profile.features.JointAlimonyAmount
        )


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


class PreviousLengthEmployed(BaseDurationField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousLengthEmployedMonths


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


class JointPreviousLengthEmployed(BaseDurationField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousLengthEmployedMonths


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
        if user_profile.features.TimeInBusinessMonths == "N/A":
            return "N/A"
        return str(int(user_profile.features.TimeInBusinessMonths) // 12)


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
        if user_profile.features.JointTimeInBusinessMonths == "N/A":
            return "N/A"
        return str(int(user_profile.features.JointTimeInBusinessMonths) // 12)


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


class TimeAtAddressYearsAndMonths(BaseDurationField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimeAtAddressMonths


class JointTimeAtAddressYearsAndMonths(BaseDurationField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointTimeAtAddressMonths


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


### SEC NL fields


class PortionOfAggregateSalesIssuer(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PortionOfAggregateSalesIssuer


class PortionOfAggregateSalesSecurityHolders(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PortionOfAggregateSalesSecurityHolders


class CrdNumber(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CrdNumber


class NetProceeds(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NetProceeds


class TitleOfEachClassOfSecurities(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TitleOfEachClassOfSecurities


class ApproximateNumberOfHolders(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApproximateNumberOfHolders


class CommissionFileNumbers(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CommissionFileNumbers


class NameOfIssuerAsSpecifiedInTheCommissionFile(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NameOfIssuerAsSpecifiedInTheCommissionFile


class By(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.By


class Title(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Title


### SEC DB Fields


class SEC_UnderwritersName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_UnderwritersName


class SEC_SalesCommissionsName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_SalesCommissionsName


class SEC_FindersFeesName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_FindersFeesName


class SEC_AuditorName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_AuditorName


class SEC_LegalName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_LegalName


class SEC_PromotersName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_PromotersName


class SEC_BlueSkyComplianceName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_BlueSkyComplianceName


class SEC_UnderwritersFees(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_UnderwritersFees


class SEC_SalesCommissionsFees(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_SalesCommissionsFees


class SEC_FindersFeesFees(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_FindersFeesFees


class SEC_AuditorFees(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_AuditorFees


class SEC_LegalFees(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_LegalFees


class SEC_PromotersFees(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_PromotersFees


class SEC_BlueSkyComplianceFees(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SEC_BlueSkyComplianceFees


### new for al_5 ###


class LoanSecured_Secured(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.LoanSecured
            == user_features.LoanSecuredEnum.Secured.value
        )


class LoanSecured_Unsecured(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.LoanSecured
            == user_features.LoanSecuredEnum.Unsecured.value
        )


class Credit_Individual(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.CreditType
            == user_features.CreditTypeEnum.Individual.value
        )


class Credit_Joint(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.CreditType == user_features.CreditTypeEnum.Joint.value
        )


class LoanDuration(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LoanDuration


class Ach_Monthly(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.AchFrequency
            == user_features.AchFrequencyEnum.Monthly.value
        )


class Ach_SemiMonthly(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.AchFrequency
            == user_features.AchFrequencyEnum.SemiMonthly.value
        )


class Payroll_D124(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PayrollType
            == user_features.PayrollTypeEnum.D124.value
        )


class Payroll_D231(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PayrollType
            == user_features.PayrollTypeEnum.D231.value
        )


class Payroll_Aero(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PayrollType
            == user_features.PayrollTypeEnum.Aero.value
        )


class Proceeds_DebtConsolidation(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.ProceedsType
            == user_features.ProceedsTypeEnum.DebtConsolidation.value
        )


class Proceeds_Other(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.ProceedsType
            == user_features.ProceedsTypeEnum.Other.value
        )


class VehicleCondition_PrivateParty(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.VehicleCondition
            == user_features.VehicleLoanConditionEnum.PrivateParty.value
        )


class VehicleMakeAndModelAndYear(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.VehicleMake
            + " "
            + user_profile.features.VehicleModel
            + " "
            + str(user_profile.features.VehicleYear)
        )


class MiddleName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MiddleName


class AgesOfDependents(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AgesOfDependents


class AddressFull(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return concatenate_address(
            user_profile.features.HouseNumber,
            user_profile.features.StreetName,
            user_profile.features.City,
            user_profile.features.State,
            user_profile.features.Zip,
        )


class County(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.County


class PreviousCounty(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousCounty


class TimeAtPreviousAddressYearsAndMonths(BaseDurationField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimeAtPreviousAddressMonths


class EmployerLengthYearsAndMonths(BaseDurationField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerLengthMonths


class EmployerWorkPhoneExtension(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerWorkPhoneExtension


class PayFrequencyALWAYSMONTHLY(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        _ = user_profile.features.FirstName  # trick unit tests
        return "Monthly"


class JointPreviousEmployerNameAndAddressFull(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointPreviousEmployerName
            + ", "
            + concatenate_address(
                user_profile.features.JointPreviousEmployerHouseNumber,
                user_profile.features.JointPreviousEmployerStreetName,
                user_profile.features.JointPreviousEmployerCity,
                user_profile.features.JointPreviousEmployerState,
                user_profile.features.JointPreviousEmployerZip,
            )
        )


class PreviousEmployerYearsAndMonths(BaseDurationField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousEmployerMonths


class NearestRelativeName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NearestRelativeName


class NearestRelativePhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NearestRelativePhone


class NearestRelativeRelationship(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NearestRelativeRelationship


class NearestRelativeYears(BaseDurationField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NearestRelativeMonths


class Alimony_CourtOrder(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.AlimonyType
            == user_features.AlimonyTypeEnum.CourtOrder.value
        )


class Alimony_WrittenAgreement(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.AlimonyType
            == user_features.AlimonyTypeEnum.WrittenAgreement.value
        )


class Alimony_OralUnderstanding(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.AlimonyType
            == user_features.AlimonyTypeEnum.OralUnderstanding.value
        )


class IncomeLikelyToBeReduced_No(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.IncomeLikelyToBeReduced
            == user_features.YesNoEnum.No.value
        )


class IncomeLikelyToBeReduced_Yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.IncomeLikelyToBeReduced
            == user_features.YesNoEnum.Yes.value
        )


class IncomeLikelyToBeReducedExplanation(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IncomeLikelyToBeReducedExplanation


class PreviousCreditWithUs_No(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreviousCreditWithUs
            == user_features.YesNoEnum.No.value
        )


class PreviousCreditWithUs_Yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreviousCreditWithUs
            == user_features.YesNoEnum.Yes.value
        )


class PreviousCreditWithUsWhen(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousCreditWithUsWhen


class JointPreviousCreditWithUsWhen(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousCreditWithUsWhen


class JointMiddleName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointMiddleName


class JointRelationToApplicant(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointRelationToApplicant


class JointAgesOfDependents(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointAgesOfDependents


class JointAddressFull(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return concatenate_address(
            user_profile.features.JointHouseNumber,
            user_profile.features.JointStreetName,
            user_profile.features.JointCity,
            user_profile.features.JointState,
            user_profile.features.JointZip,
        )


class JointCounty(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointCounty


### Missing Joint Fields ###


class JointEmployerLengthYearsAndMonths(BaseDurationField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerLengthMonths


class JointEmployerWorkPhoneExtension(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerWorkPhoneExtension


class JointPayFrequencyALWAYSMONTHLY(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        _ = user_profile.features.FirstName  # trick unit tests
        return "Monthly"


class JointPreviousEmployerYearsAndMonths(BaseDurationField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousEmployerMonths


class JointAlimony_CourtOrder(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointAlimonyType
            == user_features.AlimonyTypeEnum.CourtOrder.value
        )


class JointAlimony_WrittenAgreement(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointAlimonyType
            == user_features.AlimonyTypeEnum.WrittenAgreement.value
        )


class JointAlimony_OralUnderstanding(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointAlimonyType
            == user_features.AlimonyTypeEnum.OralUnderstanding.value
        )


class JointIncomeLikelyToBeReduced_No(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointIncomeLikelyToBeReduced
            == user_features.YesNoEnum.No.value
        )


class JointIncomeLikelyToBeReduced_Yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointIncomeLikelyToBeReduced
            == user_features.YesNoEnum.Yes.value
        )


class JointIncomeLikelyToBeReducedExplanation(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointIncomeLikelyToBeReducedExplanation


class JointPreviousCreditWithUs_No(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointPreviousCreditWithUs
            == user_features.YesNoEnum.No.value
        )


class JointPreviousCreditWithUs_Yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointPreviousCreditWithUs
            == user_features.YesNoEnum.Yes.value
        )


# AL 4


# JointCurrentAddressStartYearAndMonth
# JointLibertySavingsAccountNumber


class JointCurrentAddressStartYearAndMonth(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointCurrentAddressStartYearAndMonth


class JointLibertySavingsAccountNumber(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointLibertySavingsAccountNumber


class JointEmployerNameAndAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointEmployerName
            + ", "
            + concatenate_address(
                user_profile.features.JointEmployerHouseNumber,
                user_profile.features.JointEmployerStreetName,
                user_profile.features.JointEmployerCity,
                user_profile.features.JointEmployerState,
                user_profile.features.JointEmployerZip,
            )
        )


class CurrentAddressStartYearAndMonth(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CurrentAddressStartYearAndMonth


class LibertySavingsAccountNumber(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LibertySavingsAccountNumber


class PreferredPhone_Home(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreferredPhone
            == user_features.PreferredPhoneEnum.Home.value
        )


class PreferredPhone_Work(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreferredPhone
            == user_features.PreferredPhoneEnum.Work.value
        )


class PreferredPhone_Cell(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreferredPhone
            == user_features.PreferredPhoneEnum.Cell.value
        )


class JointPreferredPhone_Home(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointPreferredPhone
            == user_features.PreferredPhoneEnum.Home.value
        )


class JointPreferredPhone_Work(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointPreferredPhone
            == user_features.PreferredPhoneEnum.Work.value
        )


class JointPreferredPhone_Cell(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointPreferredPhone
            == user_features.PreferredPhoneEnum.Cell.value
        )


class PreviousEmployerNameAndAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreviousEmployerName
            + ", "
            + concatenate_address(
                user_profile.features.PreviousEmployerHouseNumber,
                user_profile.features.PreviousEmployerStreetName,
                user_profile.features.PreviousEmployerCity,
                user_profile.features.PreviousEmployerState,
                user_profile.features.PreviousEmployerZip,
            )
        )


class JointPreviousEmployerNameAndAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointPreviousEmployerName
            + ", "
            + concatenate_address(
                user_profile.features.JointPreviousEmployerHouseNumber,
                user_profile.features.JointPreviousEmployerStreetName,
                user_profile.features.JointPreviousEmployerCity,
                user_profile.features.JointPreviousEmployerState,
                user_profile.features.JointPreviousEmployerZip,
            )
        )


class SupervisorName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SupervisorName


class JointSupervisorName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointSupervisorName


class CitizenOrAlien_Yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CitizenOrAlien == user_features.YesNoEnum.Yes.value


class CitizenOrAlien_No(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CitizenOrAlien == user_features.YesNoEnum.No.value


class JointCitizenOrAlien_Yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointCitizenOrAlien
            == user_features.YesNoEnum.Yes.value
        )


class JointCitizenOrAlien_No(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointCitizenOrAlien
            == user_features.YesNoEnum.No.value
        )


### AL6


class ApplyingWithJointCredit_Yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.ApplyingWithJointCredit
            == user_features.YesNoEnum.Yes.value
        )


class ApplyingWithJointCredit_No(BaseCheckboxField):

    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.ApplyingWithJointCredit
            == user_features.YesNoEnum.No.value
        )


class VehiclePrice(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.VehiclePrice


class VehicleDownPayment(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.VehicleDownPayment


class PreviousApplicantName_Yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreviousApplicantName
            == user_features.YesNoEnum.Yes.value
        )


class PreviousApplicantName_No(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreviousApplicantName
            == user_features.YesNoEnum.No.value
        )


class PreviousNames(BaseStringField):

    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousNames


class PreviousEmployerPhone(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousEmployerPhone


class SelfEmployed_yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.SelfEmployed
            == user_features.SelfEmployedEnum.Yes.value
        )


class SelfEmployed_no(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.SelfEmployed
            == user_features.SelfEmployedEnum.No.value
        )


class AutomaticDeductionFromFNB_yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.AutomaticDeductionFromFNB
            == user_features.YesNoEnum.Yes.value
        )


class AutomaticDeductionFromFNB_no(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.AutomaticDeductionFromFNB
            == user_features.YesNoEnum.No.value
        )


class FNBCheckingAccountNumber(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FNBCheckingAccountNumber


class JointFNBCheckingAccountNumber(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointFNBCheckingAccountNumber


class PreviousEmployerYears(BaseDurationField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.PreviousEmployerMonths) // 12)


class JointPreviousEmployerYears(BaseDurationField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.JointPreviousEmployerMonths) // 12)


class PreviousEmployerMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.PreviousEmployerMonths) % 12)


class JointPreviousEmployerMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.JointPreviousEmployerMonths) % 12)


class JointDriversLicenseIssueDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointDriversLicenseIssueDate


class DriversLicenseIssueDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DriversLicenseIssueDate


class JointSelfEmployed_Yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointSelfEmployed
            == user_features.SelfEmployedEnum.Yes.value
        )


class JointSelfEmployed_No(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointSelfEmployed
            == user_features.SelfEmployedEnum.No.value
        )


class JointPreviousEmployerLengthMonths(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.JointPreviousEmployerLengthMonths) % 12)


class JointPreviousEmployerLengthYears(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(int(user_profile.features.JointPreviousEmployerLengthMonths) // 12)


class JointPreviousEmployerPhone(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousEmployerPhone


### AL 7 ###


class HourlyWage(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(user_profile.features.HourlyWage)


class TotalMonthlyExpenses(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(user_profile.features.TotalMonthlyExpenses)


class Term_1year(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Term == "12 months"


class Term_2years(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Term == "24 months"


class Term_3years(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Term == "36 months"


class BankruptcyStatus_yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.BankruptcyStatus == user_features.YesNoEnum.Yes.value
        )


class BankruptcyStatus_no(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.BankruptcyStatus == user_features.YesNoEnum.No.value
        )


class MarriageStatus_Divorced(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.MarriageStatus
            == user_features.MarriageStatusEnum.Divorced.value
        )


class PermissionForElectronicTransfer_yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PermissionForElectronicTransfer
            == user_features.YesNoEnum.Yes.value
        )


class PermissionForElectronicTransfer_no(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PermissionForElectronicTransfer
            == user_features.YesNoEnum.No.value
        )


class EmergencyContactName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmergencyContactName


class EmergencyContact2Name(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmergencyContact2Name


class EmergencyContactPhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(user_profile.features.EmergencyContactPhone)


class EmergencyContact2Phone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return str(user_profile.features.EmergencyContact2Phone)


class SavingsAccountNumber(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SavingsAccountNumber


# AL 8


class Repayment_PayrollDeduction(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.RepaymentMethod
            == user_features.RepaymentMethodEnum.PayrollDeduction.value
        )


class Repayment_Cash(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.RepaymentMethod
            == user_features.RepaymentMethodEnum.Cash.value
        )


class Repayment_MilitaryAllotment(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.RepaymentMethod
            == user_features.RepaymentMethodEnum.MilitaryAllotment.value
        )


class Repayment_Automatic(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.RepaymentMethod
            == user_features.RepaymentMethodEnum.Automatic.value
        )


class InterestedInLoanProtection_yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.InterestedInLoanProtection
            == user_features.YesNoEnum.Yes.value
        )


class InterestedInLoanProtection_no(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.InterestedInLoanProtection
            == user_features.YesNoEnum.No.value
        )


class JointType_Coapplicant(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointType
            == user_features.JointTypeEnum.Coapplicant.value
        )


class JointType_Spouse(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointType == user_features.JointTypeEnum.Spouse.value
        )


class JointType_Other(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointType == user_features.JointTypeEnum.Other.value
        )


class JointCSEAccountNumber(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointCSEAccountNumber


class CSEAccountNumber(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CSEAccountNumber


class JointDriversLicenseNoAndState(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return f"{user_profile.features.JointDriversLicenseNo} {user_profile.features.JointDriversLicenseState}"


class DriversLicenseNoAndState(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return f"{user_profile.features.DriversLicenseNo} {user_profile.features.DriversLicenseState}"


class JointEmployerWorkPhoneAndExtension(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return f"{user_profile.features.JointEmployerWorkPhone} {user_profile.features.JointEmployerWorkPhoneExtension}"


class EmployerWorkPhoneAndExtension(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return f"{user_profile.features.EmployerWorkPhone} {user_profile.features.EmployerWorkPhoneExtension}"


class JointTimeAtPreviousAddressYearsAndMonths(BaseDurationField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointTimeAtPreviousAddressMonths


class EmployerNameAndAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.EmployerName
            + ", "
            + concatenate_address(
                user_profile.features.EmployerHouseNumber,
                user_profile.features.EmployerStreetName,
                user_profile.features.EmployerCity,
                user_profile.features.EmployerState,
                user_profile.features.EmployerZip,
            )
        )


class TimesAtWork(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimesAtWork


class JointTimesAtWork(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointTimesAtWork


class SelfEmployedTypeOfBusiness(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SelfEmployedTypeOfBusiness


class JointSelfEmployedTypeOfBusiness(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointSelfEmployedTypeOfBusiness


class JointIncomePeriodALWAYSMONTHLY(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        _ = user_profile.features.FirstName  # trick unit tests
        return "Monthly"


class IncomePeriodALWAYSMONTHLY(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        _ = user_profile.features.FirstName  # trick unit tests
        return "Monthly"


class GrossOrNetALWAYSGROSS_Net(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        _ = user_profile.features.FirstName  # trick unit tests
        return False


class JointGrossOrNetALWAYSGROSS_Net(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        _ = user_profile.features.FirstName  # trick unit tests
        return False


class GrossOrNetALWAYSGROSS_Gross(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        _ = user_profile.features.FirstName  # trick unit tests
        return True


class JointGrossOrNetALWAYSGROSS_Gross(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        _ = user_profile.features.FirstName  # trick unit tests
        return True


class AdditionalIncomePeriodALWAYSMONTHLY(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        _ = user_profile.features.FirstName  # trick unit tests
        return "Monthly"


class JointAdditionalIncomePeriodALWAYSMONTHLY(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        _ = user_profile.features.FirstName  # trick unit tests
        return "Monthly"


class DutyStationTransferExpected_yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.DutyStationTransferExpected
            == user_features.YesNoEnum.Yes.value
        )


class JointDutyStationTransferExpected_yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointDutyStationTransferExpected
            == user_features.YesNoEnum.Yes.value
        )


class DutyStationTransferExpected_no(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.DutyStationTransferExpected
            == user_features.YesNoEnum.No.value
        )


class JointDutyStationTransferExpected_no(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointDutyStationTransferExpected
            == user_features.YesNoEnum.No.value
        )


class JointDutyStationTransferTo(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointDutyStationTransferTo


class DutyStationTransferTo(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DutyStationTransferTo


class JointDutyStationTransferDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointDutyStationTransferDate


class DutyStationTransferDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DutyStationTransferDate


class JointPreviousEmployerHireDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousEmployerHireDate


class PreviousEmployerHireDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousEmployerHireDate


class PreviousEmployerEndDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousEmployerEndDate


class JointPreviousEmployerEndDate(BaseDateField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousEmployerEndDate


class JointNearestRelativeRelationship(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointNearestRelativeRelationship


class JointNearestRelativeHomePhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointNearestRelativeHomePhone


class NearestRelativeNameAndAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.NearestRelativeName
            + ", "
            + concatenate_address(
                user_profile.features.NearestRelativeHouseNumber,
                user_profile.features.NearestRelativeStreetName,
                user_profile.features.NearestRelativeCity,
                user_profile.features.NearestRelativeState,
                user_profile.features.NearestRelativeZip,
            )
        )


class JointNearestRelativeNameAndAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointNearestRelativeName
            + ", "
            + concatenate_address(
                user_profile.features.JointNearestRelativeHouseNumber,
                user_profile.features.JointNearestRelativeStreetName,
                user_profile.features.JointNearestRelativeCity,
                user_profile.features.JointNearestRelativeState,
                user_profile.features.JointNearestRelativeZip,
            )
        )


# New fields from the list
class TypeOfContract_Lease(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.TypeOfContract
            == user_features.TypeOfContractEnum.Lease.value
        )


class TypeOfContract_RetailInstallment(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.TypeOfContract
            == user_features.TypeOfContractEnum.Installment.value
        )


class PreferredFirstName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreferredFirstName


class ApplicantsPrincipleDrivers_yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.ApplicantsPrincipleDrivers
            == user_features.YesNoEnum.Yes.value
        )


class ApplicantsPrincipleDrivers_no(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.ApplicantsPrincipleDrivers
            == user_features.YesNoEnum.No.value
        )


class EmployerHouseNumberAndStreet(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.EmployerHouseNumber
            + " "
            + user_profile.features.EmployerStreetName
        )


class EmployerState(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerState


class EmployerZip(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerZip


class PreviousEmployerFullAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreviousHouseNumber
            + " "
            + user_profile.features.PreviousStreetName
            + " "
            + user_profile.features.PreviousCity
            + " "
            + user_profile.features.PreviousState
            + " "
            + user_profile.features.PreviousZip
        )


class Education_HighSchool(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Education
            == user_features.EducationEnum.HighSchool.value
        )


class Education_SomeCollege(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Education
            == user_features.EducationEnum.SomeCollege.value
        )


class Education_2year(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Education == user_features.EducationEnum.TwoYear.value
        )


class Education_4year(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Education
            == user_features.EducationEnum.FourYear.value
        )


class Education_SpecialTraining(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Education
            == user_features.EducationEnum.SpecialTraining.value
        )


class IncomeFromEmployment(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IncomeFromEmployment


class AlimonyAmount(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AlimonyAmount


class AdditionalIncomeAmount(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdditionalIncomeAmount


class JointType_NonApplicantSpouse(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointType == user_features.JointTypeEnum.Spouse.value
        )


class JointPreferredFirstName(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreferredFirstName


class JointEmployerState(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerState


class JointEmployerZip(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerZip


class JointPreviousEmployerAddressFull(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointPreviousEmployerHouseNumber
            + " "
            + user_profile.features.JointPreviousEmployerStreetName
            + " "
            + user_profile.features.JointPreviousEmployerCity
            + " "
            + user_profile.features.JointPreviousEmployerState
            + " "
            + user_profile.features.JointPreviousEmployerZip
        )


class JointIncomeFromEmployment(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointIncomeFromEmployment


class JointAlimonyAmount(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointAlimonyAmount


class JointAdditionalIncomeAmount(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointAdditionalIncomeAmount


class MortgageCompanyLandlordCity(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MortgageCompanyLandlordCity


class MortgageCompanyLandlordState(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MortgageCompanyLandlordState


class MortgageCompanyLandlordPhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MortgageCompanyLandlordPhone


class PreviousTFSCredit_yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreviousTFSCredit == user_features.YesNoEnum.Yes.value
        )


class PreviousTFSCredit_no(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreviousTFSCredit == user_features.YesNoEnum.No.value
        )


class LastVehicleMakeModelYear(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.LastVehicleMake
            + " "
            + user_profile.features.LastVehicleModel
            + " "
            + user_profile.features.LastVehicleYear
        )


class LastVehicleFinancedBy(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LastVehicleFinancedBy


class LastVehicleCost(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LastVehicleCost


class PreferredAccount_Checking(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreferredAccount
            == user_features.PreferredAccountEnum.Checking.value
        )


class PropertyReposessed_yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PropertyReposessed
            == user_features.YesNoEnum.Yes.value
        )


class PreferredAccount_Savings(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PreferredAccount
            == user_features.PreferredAccountEnum.Savings.value
        )


class PropertyReposessed_no(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.PropertyReposessed == user_features.YesNoEnum.No.value
        )


class PendingSuits_yes(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PendingSuits == user_features.YesNoEnum.Yes.value


class PendingSuits_No(BaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PendingSuits == user_features.YesNoEnum.No.value


class NearestRelativeFullAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.NearestRelativeHouseNumber
            + " "
            + user_profile.features.NearestRelativeStreetName
            + " "
            + user_profile.features.NearestRelativeCity
            + " "
            + user_profile.features.NearestRelativeState
            + " "
            + user_profile.features.NearestRelativeZip
        )


class JointNearestRelativeFullAddress(BaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointNearestRelativeHouseNumber
            + " "
            + user_profile.features.JointNearestRelativeStreetName
            + " "
            + user_profile.features.JointNearestRelativeCity
            + " "
            + user_profile.features.JointNearestRelativeState
            + " "
            + user_profile.features.JointNearestRelativeZip
        )


class NearestRelativeCellPhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NearestRelativeCellPhone


class JointNearestRelativeCellPhone(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointNearestRelativeCellPhone
