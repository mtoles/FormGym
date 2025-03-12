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


def concat_agent_generations(agent_generations):
    return " ".join(
        [
            x["value"]
            for x in sorted(agent_generations, key=lambda item: (item["y"], item["x"]))
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
        return remove_punctuation(profile_info) == remove_punctuation(concatted_input)


class BaseCheckboxField(BaseField):
    # def is_correct(self, agent_generation, user_profile):
    def is_correct(self, agent_generations_inside, profile_info: bool):
        assert isinstance(profile_info, bool)
        # ignoring underscore-based fields for now, so skip
        # agent_generations_inside = get_inputs_inside_field(self, agent_generation)
        concatted_input = concat_agent_generations(agent_generations_inside)
        # profile_info_bool = self.get_profile_info(user_profile)

        # replace `True`` with 'x'
        # for i, ai in enumerate(concatted_input):
        #     if ai["value"] == True:
        #         # agent_generations_inside[i]["value"] = "x"
        #         concatted_input[i]["value"] = "x"
        #     elif ai["value"] == False:
        #         concatted_input[i]["value"] = ""
        #     else:
        #         pass

        if profile_info:
            return concatted_input == "x"
        else:
            return concatted_input == ""


def get_inputs_inside_field(field: BaseField, agent_generations: List):
    return [
        ag
        for ag in agent_generations
        if (
            ag["x"] >= field.x
            and ag["x"] <= field.x + field.w
            and ag["y"] >= field.y
            and ag["y"] <= field.y + field.h
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


class FullName(BaseStringField):
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
        return cls.concatenate_address(
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


class Zip(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Zip


class SocialSecurityNumber(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SocialSecurityNumber


class FullBirthDate(BaseNumericField):
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
class JointFullName(BaseStringField):
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


class JointZip(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointZip


class JointSocialSecurityNumber(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JointSocialSecurityNumber


class JointFullBirthDate(BaseNumericField):
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


class JointMortgageRent(BaseNumericField):
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
class TodaysDate(BaseNumericField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TodaysDate


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
