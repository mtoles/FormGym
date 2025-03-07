"""
File defining fields APPEARING in a form

Types of fields:
- Text
- Checkbox
"""

from typing import List
from abc import ABC, abstractmethod
import user_features


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


def concat_agent_inputs(agent_inputs):
    return " ".join(
        [
            x["value"]
            for x in sorted(agent_inputs, key=lambda item: (item["y"], item["x"]))
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
    def is_correct(self, agent_input, user_profile):
        raise NotImplemented

    @abstractmethod
    def get_profile_info(self, user_profile):
        raise NotImplemented


class BaseNumericField(BaseField):
    def is_correct(self, agent_input, user_profile):
        agent_inputs_inside = get_inputs_inside_field(self, agent_input)
        concatted_input = concat_agent_inputs(agent_inputs_inside)
        profile_info = self.get_profile_info(user_profile)
        return numerize(profile_info) == numerize(concatted_input)


class BaseStringField(BaseField):
    def is_correct(self, agent_input, user_profile):
        agent_inputs_inside = get_inputs_inside_field(self, agent_input)
        concatted_input = concat_agent_inputs(agent_inputs_inside)
        profile_info = self.get_profile_info(user_profile)
        return remove_punctuation(profile_info) == remove_punctuation(concatted_input)


class BaseCheckboxField(BaseField):
    def is_correct(self, agent_input, user_profile):
        # ignoring underscore-based fields for now, so skip
        raise NotImplementedError(
            "Checkbox logic is not updated yet (fields with underscores are ignored)."
        )


def get_inputs_inside_field(field: BaseField, agent_inputs: List):
    return [
        ai
        for ai in agent_inputs
        if (
            ai["x"] >= field.x
            and ai["x"] <= field.x + field.w
            and ai["y"] >= field.y
            and ai["y"] <= field.y + field.h
        )
    ]


class Doc:
    def __init__(self, fields: List[BaseField]):
        self.fields = fields


# -----------------------------------------
# LOAN / VEHICLE FIELDS
# -----------------------------------------
class AutoAmountRequested(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AutoAmountRequested


class Term(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Term


class Vin(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Vin


class VehicleYear(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.VehicleYear


class VehicleMakeAndModel(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.VehicleMake + " " + user_profile.features.VehicleModel
        )


class VehicleMiles(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.VehicleMiles


# -----------------------------------------
# APPLICANT PERSONAL INFORMATION
# -----------------------------------------
class ApplyingWithJointCredit(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApplyingWithJointCredit


class FullName(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        if (
            not hasattr(user_profile.features, "FirstName")
            or not hasattr(user_profile.features, "MiddleName")
            or not hasattr(user_profile.features, "LastName")
        ):
            raise Exception(
                "No user_feature for FullName. Expected FirstName, MiddleName, LastName."
            )
        return f"{user_profile.features.FirstName} {user_profile.features.MiddleName} {user_profile.features.LastName}"


class Age(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Age


class HomePhoneNumber(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HomePhoneNumber


class EmailAddress(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmailAddress


class CellPhoneNumber(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CellPhoneNumber


class FullAddress(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        return cls.concatenate_address(
            feat.HouseNumber, feat.StreetName, feat.City, feat.State, feat.Zip
        )


class HouseNumberAndStreetAddress(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        return feat.HouseNumber + " " + feat.StreetName


class CityState(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        needed = ["City", "State"]
        for n in needed:
            if not hasattr(feat, n):
                raise Exception(f"No user_feature for {n} in CityState.")
        return f"{feat.City}, {feat.State}"


class Zip(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Zip


class SocialSecurityNumber(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SocialSecurityNumber


class FullBirthDate(BaseField):
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
class JointFullName(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        # user_features do not provide separate joint first/middle/last name attributes
        # raise Exception("No user_feature for JointFullName.")
        return " ".join(
            [
                user_profile.features.JointFirstName,
                user_profile.features.JointMiddleName,
                user_profile.features.JointLastName,
            ]
        )


class JointAge(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointAge


class JointHomePhoneNumber(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointHomePhoneNumber


class JointEmailAddress(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmailAddress


class JointCellPhoneNumber(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointCellPhoneNumber


class JointFullAddress(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return concatenate_address(
            user_profile.features.JointHouseNumber,
            user_profile.features.JointStreetName,
            user_profile.features.JointCity,
            user_profile.features.JointState,
            user_profile.features.JointZip,
        )


class JointHouseNumberAndStreetAddress(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.JointHouseNumber
            + " "
            + user_profile.features.JointStreetName
        )


class JointCity(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointCity


class JointZip(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointZip


class JointSocialSecurityNumber(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointSocialSecurityNumber


class JointFullBirthDate(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return f"{user_profile.features.JointBirthMonth}/{user_profile.features.JointBirthDay}/{user_profile.features.JointBirthYear}"


# -----------------------------------------
# FIELDS WITH UNDERSCORES - IGNORE FOR NOW
# (including checkboxes/residence status)
# -----------------------------------------
# Skipped as per instructions.


# -----------------------------------------
# TIME AT ADDRESS (no underscore)
# -----------------------------------------
class TimeAtAddressYears(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimeAtAddressYears


class TimeAtAddressMonths(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimeAtAddressMonths


class JointTimeAtAddressYears(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointTimeAtAddressYears


class JointTimeAtAddressMonths(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointTimeAtAddressMonths


class MortgageCompanyLandlord(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MortgageCompanyLandlord


class JointMortgageCompanyLandlord(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointMortgageCompanyLandlord


class MonthlyMortgageOrRent(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MonthlyMortgageOrRent


class JointMortgageRent(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointMortgageRent


# -----------------------------------------
# PREVIOUS RESIDENCE
# -----------------------------------------
class PreviousFullAddress(BaseField):
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


class JointPreviousFullAddress(BaseField):
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


class TimeAtPreviousAddressYears(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimeAtPreviousAddressYears


class TimeAtPreviousAddressMonths(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimeAtPreviousAddressMonths


class JointTimeAtPreviousAddressYears(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointTimeAtPreviousAddressYears


class JointTimeAtPreviousAddressMonths(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointTimeAtPreviousAddressMonths


# -----------------------------------------
# REFERENCES
# -----------------------------------------
class ReferenceName(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferenceName


class ReferenceRelationship(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferenceRelationship


class ReferenceFullAddress(BaseField):
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


class ReferenceCellPhone(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferenceCellPhone


class ReferenceHomePhone(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferenceHomePhone


class JointReferenceName(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        return f"{feat.JointReferenceFirstName} {feat.JointReferenceLastName}"


class JointReferenceRelationship(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReferenceRelationship


class JointReferenceFullAddress(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        return f"{feat.JointReferenceHouseNumber} {feat.JointReferenceStreetName}, {feat.JointReferenceCity}, {feat.JointReferenceState}, {feat.JointReferenceZip}"


class JointReferenceCellPhone(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReferenceCellPhone


class JointReferenceHomePhone(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReferenceHomePhone


# -----------------------------------------
# SECOND REFERENCE
# -----------------------------------------
class Reference2Name(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reference2Name


class Reference2FullAddress(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        feat = user_profile.features
        return f"{feat.Reference2HouseNumber} {feat.Reference2StreetName}, {feat.Reference2City}, {feat.Reference2State}, {feat.Reference2Zip}"


class Reference2CellPhone(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reference2CellPhone


class Reference2HomePhone(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reference2HomePhone


class JointReference2Name(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReference2Name


class JointReference2FullAddress(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        # This is provided as one string in user_features
        return user_profile.features.JointReference2FullAddress


class JointReference2CellPhone(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReference2CellPhone


class JointReference2HomePhone(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointReference2HomePhone


# -----------------------------------------
# EMPLOYMENT
# -----------------------------------------
class EmployerName(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerName


class EmployerCity(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerCity


class EmployerLengthYears(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerLengthYears


class EmployerPosition(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerPosition


class EmployerWorkPhone(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EmployerWorkPhone


class GrossMonthlyIncome(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GrossMonthlyIncome


class JointEmployerName(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerName


class JointEmployerCity(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerCity


class JointEmployerLengthYears(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerLengthYears


class JointEmployerPosition(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerPosition


class JointEmployerWorkPhone(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointEmployerWorkPhone


class JointGrossMonthlyIncome(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointGrossMonthlyIncome


# -----------------------------------------
# ADDITIONAL INCOME
# -----------------------------------------
class AdditionalIncomeSource(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdditionalIncomeSource


class AdditionalMonthlyIncome(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdditionalMonthlyIncome


class JointAdditionalIncomeSource(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointAdditionalIncomeSource


class JointAdditionalMonthlyIncome(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointAdditionalMonthlyIncome


# -----------------------------------------
# PREVIOUS EMPLOYER
# -----------------------------------------
class PreviousEmployerName(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousEmployerName


class PreviousEmployerCity(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousEmployerCity


class PreviousEmployerPosition(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousEmployerPosition


class PreviousLengthEmployed(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousLengthEmployed


class JointPreviousEmployerName(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousEmployerName


class JointPreviousEmployerCity(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousEmployerCity


class JointPreviousEmployerPosition(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousEmployerPosition


class JointPreviousLengthEmployed(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousLengthEmployed


# -----------------------------------------
# BANK INFORMATION
# -----------------------------------------
class BankName(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BankName


class BankAddress(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BankAddress


class BankAccountNumber(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BankAccountNumber


class JointBankName(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointBankName


class JointBankAddress(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointBankAddress


class JointBankAccountNumber(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointBankAccountNumber


# -----------------------------------------
# BANKRUPTCY
# -----------------------------------------
class BankruptcyStatus(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BankruptcyStatus


class BankruptcyYear(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BankruptcyYear


class JointBankruptcyStatus(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointBankruptcyStatus


class JointBankruptcyYear(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointBankruptcyYear


# -----------------------------------------
# AUTO TRADE-IN
# -----------------------------------------
class TradingInCar(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TradingInCar


class AutoBalanceDue(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AutoBalanceDue


class AutoCreditReference(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AutoCreditReference


class RegisteredCarOwner(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RegisteredCarOwner


# -----------------------------------------
# DATE FIELDS
# -----------------------------------------
class TodaysDate(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TodaysDate


# -----------------------------------------
# CHECKBOX FIELDS
# -----------------------------------------

# Additional classes with underscores that raise exceptions:

class ResidenceStatus_Buying(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResidenceStatus == user_features.ResidenceStatusEnum.Buying.value

class ResidenceStatus_Renting(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResidenceStatus == user_features.ResidenceStatusEnum.Renting.value

class ResidenceStatus_Relatives(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResidenceStatus == user_features.ResidenceStatusEnum.LivingWithRelatives.value

class JointResidenceStatus_Buying(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointResidenceStatus == user_features.ResidenceStatusEnum.Buying.value

class JointResidenceStatus_Renting(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointResidenceStatus == user_features.ResidenceStatusEnum.Renting.value

class JointResidenceStatus_Relatives(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointResidenceStatus == user_features.ResidenceStatusEnum.LivingWithRelatives.value

class PreviousResidenceStatus_Buying(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousResidenceStatus == user_features.ResidenceStatusEnum.Buying.value

class PreviousResidenceStatus_Renting(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousResidenceStatus == user_features.ResidenceStatusEnum.Renting.value

class PreviousResidenceStatus_Relatives(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousResidenceStatus == user_features.ResidenceStatusEnum.LivingWithRelatives.value

class JointPreviousResidenceStatus_Buying(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousResidenceStatus == user_features.ResidenceStatusEnum.Buying.value

class JointPreviousResidenceStatus_Renting(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousResidenceStatus == user_features.ResidenceStatusEnum.Renting.value

class JointPreviousResidenceStatus_Relatives(BaseField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointPreviousResidenceStatus == user_features.ResidenceStatusEnum.LivingWithRelatives.value

