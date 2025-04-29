import user_profile_attributes
from typing import List
from abc import ABC, abstractmethod

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


def get_inputs_inside_field(field, agent_generations):
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


class FormFieldMeta(type):
    """
    Metaclass for possible form fields
    """

    registry = {}

    def __new__(cls, name, bases, attrs):
        new_p_attr = super().__new__(cls, name, bases, attrs)
        base_classes = ["FormBaseField", "FormBaseNumericField", "FormBaseStringField", "FormBaseCheckboxField", "FormAnnotatedField", "FormSignOrInitial", "FormSignature", "FormInitials"]
        if name not in base_classes:
            # check for duplicates
            assert name not in cls.registry, f"Form field {name} already exists"
            cls.registry[name] = new_p_attr
        return new_p_attr


class FormBaseField(metaclass=FormFieldMeta):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @abstractmethod
    def is_correct(self, agent_generation, user_profile):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_profile_info(cls, user_profile):
        raise NotImplementedError


class FormBaseNumericField(FormBaseField):
    # def is_correct(self, agent_generation, user_profile):
    def is_correct(self, agent_generation, user_profile):
        agent_generations_inside = get_inputs_inside_field(self, agent_generation)
        concatted_input = concat_agent_generations(agent_generations_inside)
        profile_info = self.get_profile_info(user_profile)
        return numerize(profile_info) == numerize(concatted_input)


class FormBaseStringField(FormBaseField):
    # def is_correct(self, agent_generation, user_profile):
    def is_correct(self, agent_generation, user_profile):
        agent_generations_inside = get_inputs_inside_field(self, agent_generation)
        concatted_input = concat_agent_generations(agent_generations_inside)
        profile_info = self.get_profile_info(user_profile)
        return remove_punctuation(profile_info) == remove_punctuation(concatted_input)


class FormBaseCheckboxField(FormBaseField):
    # def is_correct(self, agent_generation, user_profile):
    def is_correct(self, agent_generation, user_profile):
        agent_generations_inside = get_inputs_inside_field(self, agent_generation)
        concatted_input = concat_agent_generations(agent_generations_inside)
        profile_info = self.get_profile_info(user_profile)
        assert isinstance(profile_info, bool)
        if profile_info:
            return concatted_input == "x"
        else:
            return concatted_input == ""


class FormAnnotatedField(FormBaseField):
    pass


class FormSignOrInitial(FormBaseField):
    def is_correct(self, agent_generation, user_profile):
        agent_generations_inside = get_inputs_inside_field(self, agent_generation)
        if len(agent_generations_inside) != 1:
            return False
        agent_gen = agent_generations_inside[0]
        if agent_gen["action"] != "Sign":
            return False
        signature_val = agent_gen["value"]
        profile_info = self.get_profile_info(user_profile)
        return profile_info == signature_val


class FormSignature(FormSignOrInitial):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FirstName + " " + user_profile.features.LastName


class FormInitials(FormSignOrInitial):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FirstName[0] + user_profile.features.LastName[0]


class FieldBanners(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldBanners

class FieldCalls(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCalls

class FieldCasesKentGlLtsKS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesKentGlLtsKS

class FieldCasesKentIiiKS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesKentIiiKS

class FieldCasesNewportKS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesNewportKS

class FieldCasesNewportLtsKS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesNewportLtsKS

class FieldOfStoresSupplied(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldOfStoresSupplied

class FieldOpenEnds(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldOpenEnds

class FieldReps(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldReps

class FieldCases(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCases

class FieldCasesKent100(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesKent100

class FieldCasesKentGl100(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesKentGl100

class FieldCasesKentIiKS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesKentIiKS

class FieldCasesKentIii100(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesKentIii100

class FieldCasesKentKS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesKentKS

class FieldCasesNewport100S(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesNewport100S

class FieldCasesNewportLts100(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesNewportLts100

class FieldCasesNewportLtsKs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesNewportLtsKs

class FieldCasesNewportksKS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesNewportksKS

class FieldCasesTrueKS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCasesTrueKS

class FieldDisplaysPlaced(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldDisplaysPlaced

class FieldDisplaysPlacedCounter(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldDisplaysPlacedCounter

class FieldDisplaysPlacedFloor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldDisplaysPlacedFloor

class FieldDisplaysPlacedPosters(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldDisplaysPlacedPosters

class FieldItemsDealsReceived(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldItemsDealsReceived

class Field(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field

class Field150OffCartonCoupon(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field150OffCartonCoupon

class FieldMoistureInTobacco(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldMoistureInTobacco

class FieldMoistureInTow(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldMoistureInTow

class FieldOfDistributionAchievedInRetailOutlets(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldOfDistributionAchievedInRetailOutlets

class FieldOfDistributionAchievedInRetailOutletsAnnualCalls(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldOfDistributionAchievedInRetailOutletsAnnualCalls

class FieldOfDistributionAchievedInRetailOutletsClassifiedCalls(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldOfDistributionAchievedInRetailOutletsClassifiedCalls

class FieldOfRetailCalls(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldOfRetailCalls

class FieldPlasticizer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldPlasticizer

class FieldSolution(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldSolution

class Field59(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field59

class Field6HardPack(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field6HardPack

class FieldBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldBy

class FieldCurrent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCurrent

class FieldDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldDate

class FieldFromCurrentBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldFromCurrentBudget

class FieldFromNextYearSBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldFromNextYearSBudget

class FieldGiveReasonsBelow(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldGiveReasonsBelow

class FieldIncludingThisCoverSheet(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldIncludingThisCoverSheet

class FieldOnlyPartialRegionContinueWithDivisionSScope(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldOnlyPartialRegionContinueWithDivisionSScope

class FieldProductTestAUEtc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldProductTestAUEtc

class FieldRecordsRetention(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldRecordsRetention

class FieldContD(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldContD

class FieldPlease(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldPlease

class FieldPleaseSpecify(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldPleaseSpecify

class FieldS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldS

class FieldTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldTo

class FieldAdvertisingCreativeTitle(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldAdvertisingCreativeTitle

class FieldDirectorGLLittell(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldDirectorGLLittell

class FieldExplanationOfChange(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldExplanationOfChange

class FieldRevisedCompletionDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldRevisedCompletionDate

class FieldSpaceColor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldSpaceColor

class FieldSrManagerBJPowell(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldSrManagerBJPowell

class FieldSrVpTWRobertson(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldSrVpTWRobertson

class FieldDateOfEvent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldDateOfEvent

class FieldExplain(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldExplain

class FieldIssueFrequencyYear(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldIssueFrequencyYear

class Field10ContingencyFinalReportInc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field10ContingencyFinalReportInc

class Field10ContingencyFinalReportIncNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field10ContingencyFinalReportIncNo

class Field10ContingencyFinalReportIncYes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field10ContingencyFinalReportIncYes

class FieldDateInitiated(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldDateInitiated

class FieldBrandSApplicable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldBrandSApplicable

class FieldCirculation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCirculation

class FieldCouponExpirationDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCouponExpirationDate

class FieldCouponIssueDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCouponIssueDate

class FieldCouponValue(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCouponValue

class FieldGeographicalAreaS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldGeographicalAreaS

class FieldMediaName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldMediaName

class FieldMediaType(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldMediaType

class FieldPackAndOrCarton(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldPackAndOrCarton

class FieldSignatureOfInitiator(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldSignatureOfInitiator

class FieldSpeaker(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldSpeaker

class Field12Cigar(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field12Cigar

class Field13Cigar(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field13Cigar

class FieldDec(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldDec

class FieldJun(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldJun

class FieldMar(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldMar

class FieldSep(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldSep

class FieldWentOutImmediately(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldWentOutImmediately

class Field1(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1

class Field1680(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1680

class Field1Enhancement(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1Enhancement

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimant(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimant

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantAddress(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantAddress

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantCity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantCity

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantName

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantState(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantState

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantTelephone(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantTelephone

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantZipCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantZipCode

class Field1ProductivityImprovement(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1ProductivityImprovement

class Field1StatesAndCitiesSelectedToReceiveProduct(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProduct

class Field1StatesAndCitiesSelectedToReceiveProductChicagoIll(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductChicagoIll

class Field1StatesAndCitiesSelectedToReceiveProductNycNY(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductNycNY

class Field1StatesAndCitiesSelectedToReceiveProductAlabama(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductAlabama

class Field1StatesAndCitiesSelectedToReceiveProductAlaska(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductAlaska

class Field1StatesAndCitiesSelectedToReceiveProductArizona(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductArizona

class Field1StatesAndCitiesSelectedToReceiveProductArkansas(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductArkansas

class Field1StatesAndCitiesSelectedToReceiveProductCalifornia(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductCalifornia

class Field1StatesAndCitiesSelectedToReceiveProductColorada(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductColorada

class Field1StatesAndCitiesSelectedToReceiveProductConnecticut(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductConnecticut

class Field1StatesAndCitiesSelectedToReceiveProductDC(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductDC

class Field1StatesAndCitiesSelectedToReceiveProductDelaware(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductDelaware

class Field1StatesAndCitiesSelectedToReceiveProductFlorida(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductFlorida

class Field1StatesAndCitiesSelectedToReceiveProductGeorgia(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductGeorgia

class Field1StatesAndCitiesSelectedToReceiveProductHawaii(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductHawaii

class Field1StatesAndCitiesSelectedToReceiveProductIdaho(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductIdaho

class Field1StatesAndCitiesSelectedToReceiveProductIllinois(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductIllinois

class Field1StatesAndCitiesSelectedToReceiveProductIndiana(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductIndiana

class Field1StatesAndCitiesSelectedToReceiveProductIowa(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductIowa

class Field1StatesAndCitiesSelectedToReceiveProductKansas(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductKansas

class Field1StatesAndCitiesSelectedToReceiveProductKentucky(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductKentucky

class Field1StatesAndCitiesSelectedToReceiveProductLouisiana(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductLouisiana

class Field1StatesAndCitiesSelectedToReceiveProductMaine(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductMaine

class Field1StatesAndCitiesSelectedToReceiveProductMaryland(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductMaryland

class Field1StatesAndCitiesSelectedToReceiveProductMassachusetts(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductMassachusetts

class Field1StatesAndCitiesSelectedToReceiveProductMichigan(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductMichigan

class Field1StatesAndCitiesSelectedToReceiveProductMinnesota(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductMinnesota

class Field1StatesAndCitiesSelectedToReceiveProductMississippi(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductMississippi

class Field1StatesAndCitiesSelectedToReceiveProductMissouri(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductMissouri

class Field1StatesAndCitiesSelectedToReceiveProductMontana(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductMontana

class Field1StatesAndCitiesSelectedToReceiveProductNebraska(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductNebraska

class Field1StatesAndCitiesSelectedToReceiveProductNevada(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductNevada

class Field1StatesAndCitiesSelectedToReceiveProductNewHampshire(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductNewHampshire

class Field1StatesAndCitiesSelectedToReceiveProductNewJersey(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductNewJersey

class Field1StatesAndCitiesSelectedToReceiveProductNewMexico(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductNewMexico

class Field1StatesAndCitiesSelectedToReceiveProductNewYork(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductNewYork

class Field1StatesAndCitiesSelectedToReceiveProductNorthCarolina(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductNorthCarolina

class Field1StatesAndCitiesSelectedToReceiveProductNorthDakota(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductNorthDakota

class Field1StatesAndCitiesSelectedToReceiveProductOhio(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductOhio

class Field1StatesAndCitiesSelectedToReceiveProductOklahoma(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductOklahoma

class Field1StatesAndCitiesSelectedToReceiveProductOregon(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductOregon

class Field1StatesAndCitiesSelectedToReceiveProductPennsylVania(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductPennsylVania

class Field1StatesAndCitiesSelectedToReceiveProductRhodeIsland(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductRhodeIsland

class Field1StatesAndCitiesSelectedToReceiveProductSouthCarolina(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductSouthCarolina

class Field1StatesAndCitiesSelectedToReceiveProductSouthDakota(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductSouthDakota

class Field1StatesAndCitiesSelectedToReceiveProductTennessee(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductTennessee

class Field1StatesAndCitiesSelectedToReceiveProductTexas(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductTexas

class Field1StatesAndCitiesSelectedToReceiveProductUtah(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductUtah

class Field1StatesAndCitiesSelectedToReceiveProductVermont(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductVermont

class Field1StatesAndCitiesSelectedToReceiveProductVirginia(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductVirginia

class Field1StatesAndCitiesSelectedToReceiveProductWashington(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductWashington

class Field1StatesAndCitiesSelectedToReceiveProductWestVirginia(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductWestVirginia

class Field1StatesAndCitiesSelectedToReceiveProductWisconsin(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductWisconsin

class Field1StatesAndCitiesSelectedToReceiveProductWyoming(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1StatesAndCitiesSelectedToReceiveProductWyoming

class Field10(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field10

class Field100S(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field100S

class Field100000(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field100000

class Field12Yr(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field12Yr

class Field1976(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1976

class Field1987(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1987

class Field198(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field198

class Field1990Cost(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field1990Cost

class Field2(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2

class Field2Aminoanthhacene(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2Aminoanthhacene

class Field2Aminoanthracene(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2Aminoanthracene

class Field2EstimatedTestProductQuantitiesPerMarket(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2EstimatedTestProductQuantitiesPerMarket

class Field2EstimatedTestProductQuantitiesPerMarket4S5S20SEtc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2EstimatedTestProductQuantitiesPerMarket4S5S20SEtc

class Field2EstimatedTestProductQuantitiesPerMarketCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2EstimatedTestProductQuantitiesPerMarketCode

class Field2EstimatedTestProductQuantitiesPerMarketProductCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2EstimatedTestProductQuantitiesPerMarketProductCode

class Field2EstimatedTestProductQuantitiesPerMarketQuantity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2EstimatedTestProductQuantitiesPerMarketQuantity

class Field2Maintenance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2Maintenance

class Field2NamesOfFirstNamedPlaintiffAndFirstNamedDefendantOnTheCaptionOfTheComplaint(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2NamesOfFirstNamedPlaintiffAndFirstNamedDefendantOnTheCaptionOfTheComplaint

class Field2NamesOfFirstNamedPlaintiffAndFirstNamedDefendantOnTheCaptionOfTheComplaintDefendant(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2NamesOfFirstNamedPlaintiffAndFirstNamedDefendantOnTheCaptionOfTheComplaintDefendant

class Field2NamesOfFirstNamedPlaintiffAndFirstNamedDefendantOnTheCaptionOfTheComplaintPlaintiff(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2NamesOfFirstNamedPlaintiffAndFirstNamedDefendantOnTheCaptionOfTheComplaintPlaintiff

class Field2ReturnOnInvestment(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2ReturnOnInvestment

class Field202851A1B1Im(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field202851A1B1Im

class Field2134(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2134

class Field213496(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field213496

class Field2134Bright(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2134Bright

class Field2134Kl(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2134Kl

class Field25Yr(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field25Yr

class Field2AEstimatedTotalsByProductAllMarketsCombined(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2AEstimatedTotalsByProductAllMarketsCombined

class Field2AEstimatedTotalsByProductAllMarketsCombined4S5S20SEtc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2AEstimatedTotalsByProductAllMarketsCombined4S5S20SEtc

class Field2AEstimatedTotalsByProductAllMarketsCombinedQuantity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field2AEstimatedTotalsByProductAllMarketsCombinedQuantity

class Field3(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field3

class Field3CustomerImpact(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field3CustomerImpact

class Field3DateOfClaimantSBirth(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field3DateOfClaimantSBirth

class Field3SpecialProcessing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field3SpecialProcessing

class Field30SheetPosters(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field30SheetPosters

class Field35Over(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field35Over

class Field35Under(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field35Under

class Field35(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field35

class Field35109(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field35109

class Field35Bright(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field35Bright

class Field35Kl(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field35Kl

class Field36Over(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field36Over

class Field4(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field4

class Field4AdHoc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field4AdHoc

class Field4CaseInvolvesCheckAppropriateBoxes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field4CaseInvolvesCheckAppropriateBoxes

class Field4CaseInvolvesCheckAppropriateBoxesAInjury(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field4CaseInvolvesCheckAppropriateBoxesAInjury

class Field4CaseInvolvesCheckAppropriateBoxesBWrongfulDeath(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field4CaseInvolvesCheckAppropriateBoxesBWrongfulDeath

class Field4CaseInvolvesCheckAppropriateBoxesCConsortium(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field4CaseInvolvesCheckAppropriateBoxesCConsortium

class Field4GovernmentRequirement(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field4GovernmentRequirement

class Field5(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field5

class Field5BusinessChange(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field5BusinessChange

class Field5Emergency(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field5Emergency

class Field5SpecifyTheNatureOrTypeOfAsbestosRelatedInjuryAllegedByTheClaimantEQAsbestosisLungCancerAdenocarcinomaLungCancerMesotheliomaPleuralThickeningFibrosisEtc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field5SpecifyTheNatureOrTypeOfAsbestosRelatedInjuryAllegedByTheClaimantEQAsbestosisLungCancerAdenocarcinomaLungCancerMesotheliomaPleuralThickeningFibrosisEtc

class Field5TypesOfLocalGovernmentalUnitAflected(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field5TypesOfLocalGovernmentalUnitAflected

class Field5TypesOfLocalGovernmentalUnitAflectedCities(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field5TypesOfLocalGovernmentalUnitAflectedCities

class Field5TypesOfLocalGovernmentalUnitAflectedOthers(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field5TypesOfLocalGovernmentalUnitAflectedOthers

class Field5TypesOfLocalGovernmentalUnitAflectedVillages(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field5TypesOfLocalGovernmentalUnitAflectedVillages

class Field50Yr(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field50Yr

class Field530(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field530

class Field6(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field6

class Field6SystemError(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field6SystemError

class Field6Yr(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field6Yr

class Field7(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field7

class Field7ProceduralError(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Field7ProceduralError

class FieldBeginner(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldBeginner

class FieldExcellent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldExcellent

class FieldFair(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldFair

class FieldGood(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldGood

class A(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.A

class ADM(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ADM

class AJMellman(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AJMellman

class AcceptRejectAsPer58185C(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AcceptRejectAsPer58185C

class Accepted(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Accepted

class AcceptedSymposium(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AcceptedSymposium

class AccountNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AccountNo

class AccountingChargeNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AccountingChargeNo

class AccountingDistribution(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AccountingDistribution

class AccountingDistributionFeb(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AccountingDistributionFeb

class AccountingDistributionJan(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AccountingDistributionJan

class AccountingDistributionMar(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AccountingDistributionMar

class AcctNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AcctNo

class AcuteCadcovascular(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AcuteCadcovascular

class AcuteCardiovascular(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AcuteCardiovascular

class AdminCtrMgmtCtrPurchaseOrderNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdminCtrMgmtCtrPurchaseOrderNo

class AdminCtrMgmtCtrAsRequired(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdminCtrMgmtCtrAsRequired

class AdvertisingCreativeTheme(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdvertisingCreativeTheme

class Affiliation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Affiliation

class Affillation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Affillation

class Aftertaste(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Aftertaste

class Age(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Age

class Age2534(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Age2534

class Age3544(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Age3544

class Age45Over(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Age45Over

class AgeUnder25(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AgeUnder25

class Agency(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Agency

class Age1625(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Age1625

class Age2635(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Age2635

class Age3645(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Age3645

class Age46Over(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Age46Over

class AirTime(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AirTime

class Albert(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Albert

class Alternatives(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Alternatives

class Ame(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ame

class AmountOfChangeIncreaseCircleOne(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AmountOfChangeIncreaseCircleOne

class AmtMenthol7More(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AmtMenthol7More

class Analytical(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Analytical

class AnalyticalMethodS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AnalyticalMethodS

class AnalyticalRequirements(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AnalyticalRequirements

class AnalyticalRequirementsCodeAssigned(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AnalyticalRequirementsCodeAssigned

class AnalyticalRequirementsEstRedemption(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AnalyticalRequirementsEstRedemption

class AnalyticalRequirementsForControlUseOnly(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AnalyticalRequirementsForControlUseOnly

class AnalyticalRequirementsJobNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AnalyticalRequirementsJobNumber

class Annuals(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Annuals

class Approval(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Approval

class ApprovalRouting(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalRouting

class Approvals(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Approvals

class ApprovalsDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsDate

class ApprovalsDirIntAdmin(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsDirIntAdmin

class ApprovalsGroupProdDir(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsGroupProdDir

class ApprovalsRegionalDirVp(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsRegionalDirVp

class ApprovalsSeniorVpIntL(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsSeniorVpIntL

class ApprovalsVpIntLMarketing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsVpIntLMarketing

class ApprovalsVpIntLPlanning(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsVpIntLPlanning

class ApprovalsAccounting(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsAccounting

class ApprovalsAgency(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsAgency

class ApprovalsAuthorizationNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsAuthorizationNo

class ApprovalsBudgetAllocation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsBudgetAllocation

class ApprovalsChairmanCeo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsChairmanCeo

class ApprovalsExecutive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsExecutive

class ApprovalsForecasting(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsForecasting

class ApprovalsMarketing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsMarketing

class ApprovalsMedia(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsMedia

class ApprovalsPresident(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsPresident

class ApprovalsProduct(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsProduct

class ApprovalsSales(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsSales

class ApprovalsVPMarketing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalsVPMarketing

class ApproveInIts(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApproveInIts

class Approved(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Approved

class ApproximateOfRetailCallsSecuredByGlass(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApproximateOfRetailCallsSecuredByGlass

class Apr(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Apr

class Aptertaste7Pleasant(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Aptertaste7Pleasant

class AreaRegionDivision(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AreaRegionDivision

class AreaRegion(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AreaRegion

class ArtWork(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ArtWork

class AssayResult(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AssayResult

class At919AtTheGreensboroBranchAsSoonAsPossible(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.At919AtTheGreensboroBranchAsSoonAsPossible

class AtTheTimeOfReproductionTheFollowingNotattonsWereMade(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AtTheTimeOfReproductionTheFollowingNotattonsWereMade

class AttachmentsCheckIfIncluded(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttachmentsCheckIfIncluded

class AttachmentsCheckIfIncludedBlendFormulae(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttachmentsCheckIfIncludedBlendFormulae

class AttachmentsCheckIfIncludedCasingFlavoringFormulae(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttachmentsCheckIfIncludedCasingFlavoringFormulae

class AttachmentsCheckIfIncludedCostAnalysis(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttachmentsCheckIfIncludedCostAnalysis

class AttachmentsCheckIfIncludedInitialProductionRequirement(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttachmentsCheckIfIncludedInitialProductionRequirement

class AttachmentsCheckIfIncludedPackagingArtStat(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttachmentsCheckIfIncludedPackagingArtStat

class AttachmentsCheckIfIncludedProcessingDetail(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttachmentsCheckIfIncludedProcessingDetail

class AttachmentsCheckIfIncludedProductSpecificationList(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttachmentsCheckIfIncludedProductSpecificationList

class AttachmentsCheckIfIncludedRationale(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttachmentsCheckIfIncludedRationale

class AttachmentsCheckIfIncludedSpecChangeDetail(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttachmentsCheckIfIncludedSpecChangeDetail

class Attributes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Attributes

class AttributesViceroy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttributesViceroy

class AuthorizationNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AuthorizationNo

class AuthorizedCost(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AuthorizedCost

class Authors(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Authors

class AverageDailyEffectiveCirculation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AverageDailyEffectiveCirculation

class AverageWeightRangeGm(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AverageWeightRangeGm

class AvgRate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AvgRate

class AcceptedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AcceptedBy

class Account(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Account

class AccountCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AccountCode

class AccountExecutive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AccountExecutive

class AccountMonth(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AccountMonth

class AccountName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AccountName

class AccountNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AccountNumber

class AccountingFile(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AccountingFile

class AcctName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AcctName

class AdditionalSpray(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdditionalSpray

class Address(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Address

class AddressPostalRequirementsBarcodesDocumentStorageAndBatchNumbersToBeSuppliedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AddressPostalRequirementsBarcodesDocumentStorageAndBatchNumbersToBeSuppliedBy

class AdhesiveCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdhesiveCode

class Adhesive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Adhesive

class AdhesiveSupplierS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdhesiveSupplierS

class AdhesiveSupplierCodeNoS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdhesiveSupplierCodeNoS

class AdhesiveType(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdhesiveType

class AdjustedTotalCostOfProject(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdjustedTotalCostOfProject

class AdjustedTotalCostOfProtect(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdjustedTotalCostOfProtect

class Adjustment(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Adjustment

class AdvanceRegistrationFeePriorToAugust10(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AdvanceRegistrationFeePriorToAugust10

class AffectedCh20Appropriations(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AffectedCh20Appropriations

class AlertNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AlertNumber

class AllowableSubstitutions(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AllowableSubstitutions

class AmendmentAttachAdditionalSheetsAsNecessary(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AmendmentAttachAdditionalSheetsAsNecessary

class AmendmentNoIfApplicable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AmendmentNoIfApplicable

class Amount(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Amount

class AmountEarnedButNotReceived(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AmountEarnedButNotReceived

class AmtOfChange(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AmtOfChange

class AmtOfChangeDecrease(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AmtOfChangeDecrease

class AmtOfChangeIncrease(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AmtOfChangeIncrease

class Analyst(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Analyst

class AnySpecialDietaryMealAndYouOrYourGuestWouldPrefer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AnySpecialDietaryMealAndYouOrYourGuestWouldPrefer

class AppearanceOrAnswerDues(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AppearanceOrAnswerDues

class ApplicationPattern(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApplicationPattern

class ApplicationPatternOverall(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApplicationPatternOverall

class ApplicationPatternSkip(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApplicationPatternSkip

class ApplicationTippingCartonEndFlapsEtc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApplicationTippingCartonEndFlapsEtc

class ApprovalSignatureDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovalSignatureDate

class ApprovedByDirectorForecastingMktTo250000(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovedByDirectorForecastingMktTo250000

class ApprovedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovedBy

class ApprovedByGroupManager(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovedByGroupManager

class ApprovedByGroupProductManager(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovedByGroupProductManager

class ApprovedByMpio(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovedByMpio

class ApprovedByProductManager(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ApprovedByProductManager

class AreaCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AreaCode

class ArrivalDateAndTimeIncludeAirlineAndFlightNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ArrivalDateAndTimeIncludeAirlineAndFlightNo

class Asst(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Asst

class AsumptionsUsedInArrivingAtFiscalEstimate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AsumptionsUsedInArrivingAtFiscalEstimate

class Attendees(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Attendees

class AttendeesCustomersAttended(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttendeesCustomersAttended

class AttendeesCustomersInvited(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttendeesCustomersInvited

class AttendeesLorillardPersonnel(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AttendeesLorillardPersonnel

class Attention(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Attention

class Attn(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Attn

class AudienceConcentration(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AudienceConcentration

class Aug(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Aug

class AuthNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AuthNo

class AuthorizedSignature(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AuthorizedSignature

class AuthorizedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AuthorizedBy

class AuthorizedTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AuthorizedTo

class Average(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Average

class AverageCouponBuydownValueOnTargetedBrandsDoralBasicMonarchCambridgeGpc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AverageCouponBuydownValueOnTargetedBrandsDoralBasicMonarchCambridgeGpc

class AverageCouponBuydownValueOnTargetedBrandsDoralBasicMonarchCambridgeGpcCartons(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AverageCouponBuydownValueOnTargetedBrandsDoralBasicMonarchCambridgeGpcCartons

class AverageCouponBuydownValueOnTargetedBrandsDoralBasicMonarchCambridgeGpcPacks(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AverageCouponBuydownValueOnTargetedBrandsDoralBasicMonarchCambridgeGpcPacks

class BWApprovals(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BWApprovals

class BWApprovalsDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BWApprovalsDate

class BWApprovalsDepartment(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BWApprovalsDepartment

class BWApprovalsSignature(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BWApprovalsSignature

class BWOriginator(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BWOriginator

class B(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.B

class BackCigarettes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BackCigarettes

class BackCigarettesComments(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BackCigarettesComments

class BackCigarettesCratering(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BackCigarettesCratering

class BackCigarettesHoleDepth(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BackCigarettesHoleDepth

class BackCigarettesScorching(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BackCigarettesScorching

class Basic(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Basic

class BatesNumberNotUsed(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BatesNumberNotUsed

class Beatty(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Beatty

class BetweenTheActs25MmButt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BetweenTheActs25MmButt

class BetweenTheActs25MmButtMeanOfLast12Samples(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BetweenTheActs25MmButtMeanOfLast12Samples

class BetweenTheActs25MmButtPresentSample(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BetweenTheActs25MmButtPresentSample

class Blend(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Blend

class BoldSubHead(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BoldSubHead

class BookletCoupon(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BookletCoupon

class Box80S(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Box80S

class Branch(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Branch

class BrandSPromoted(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrandSPromoted

class BrandName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrandName

class BrandSmoked(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrandSmoked

class BrandSmokedAllOtherSmokers(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrandSmokedAllOtherSmokers

class BrandSmokedTestBrandSmokers(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrandSmokedTestBrandSmokers

class BrandSmoker(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrandSmoker

class BrandSmokerAllOtherSmokers(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrandSmokerAllOtherSmokers

class BrandSmokerTestBrandSmokers(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrandSmokerTestBrandSmokers

class BrandProjectName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrandProjectName

class Brands(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Brands

class BrandsSApplicable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrandsSApplicable

class BrcCodesW81CartonOrderForm(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrcCodesW81CartonOrderForm

class BudgetNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BudgetNo

class BudgetYear19(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BudgetYear19

class Buyer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Buyer

class BwitSuggestion(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BwitSuggestion

class By(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.By

class BackgroundProblemDefinition(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BackgroundProblemDefinition

class BalanceToSpend(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BalanceToSpend

class BalanceToSpendCapital(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BalanceToSpendCapital

class BalanceToSpendExpense(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BalanceToSpendExpense

class BaleNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BaleNo

class BatchNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BatchNumber

class BatchSize(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BatchSize

class BeforeMeANotaryPublicPersonallyAppeared(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BeforeMeANotaryPublicPersonallyAppeared

class Binding(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Binding

class Brand(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Brand

class BrandStyle(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrandStyle

class BrandSApplicable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrandSApplicable

class BrandS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrandS

class BriefDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BriefDescription

class BriefNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BriefNumber

class Bright(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Bright

class BrightKsWhiteTipping(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BrightKsWhiteTipping

class BudgetCheck(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BudgetCheck

class BudgetCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BudgetCode

class Budgeted(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Budgeted

class BudgetedNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BudgetedNo

class BudgetedYes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BudgetedYes

class BusinessTelephone(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BusinessTelephone

class BusinessUnit(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BusinessUnit

class ByCity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ByCity

class ByCityBQuilla(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ByCityBQuilla

class ByCityBogot(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ByCityBogot

class ByCityMedellin(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ByCityMedellin

class C(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.C

class Cable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Cable

class CanTimeBeSparedForCompletion(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CanTimeBeSparedForCompletion

class Capital(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Capital

class Capri(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Capri

class CarcinogenOsha(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CarcinogenOsha

class CarcinogenOther(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CarcinogenOther

class CarryoverTo1988(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CarryoverTo1988

class Cartons(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Cartons

class Casing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Casing

class Cf(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Cf

class ChainAcceptance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChainAcceptance

class ChainAcceptanceExcellent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChainAcceptanceExcellent

class ChainAcceptanceFair(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChainAcceptanceFair

class ChainAcceptanceGood(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChainAcceptanceGood

class ChainAcceptancePoor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChainAcceptancePoor

class Chargeback(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Chargeback

class ChemicalDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalDescription

class ChemicalDescriptionCas(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalDescriptionCas

class ChemicalDescriptionChemicalFormula(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalDescriptionChemicalFormula

class ChemicalDescriptionDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalDescriptionDescription

class ChemicalDescriptionManufacturer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalDescriptionManufacturer

class ChemicalDescriptionMsdsOnFileCircleOne(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalDescriptionMsdsOnFileCircleOne

class ChemicalDescriptionPercentActivesNonWater(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalDescriptionPercentActivesNonWater

class ChemicalDescriptionPhone(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalDescriptionPhone

class ChemicalDescriptionProductChemicalName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalDescriptionProductChemicalName

class ChemicalDescriptionProductClassificationCircleDne(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalDescriptionProductClassificationCircleDne

class ChemicalPurity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalPurity

class ChemicalUsage(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalUsage

class ChemicalUsage1993AnnualUsageLbs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalUsage1993AnnualUsageLbs

class ChemicalUsage1993AvgMonthlyUsageLbs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalUsage1993AvgMonthlyUsageLbs

class ChemicalUsageApplicationCircleOneAndBrieflyDescribe(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemicalUsageApplicationCircleOneAndBrieflyDescribe

class CigaretteReportForm(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportForm

class CigaretteReportFormTar(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormTar

class CigaretteReportForm1YearCovered(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportForm1YearCovered

class CigaretteReportForm10VarietyUnitSales(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportForm10VarietyUnitSales

class CigaretteReportForm11VarietyDollarSales(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportForm11VarietyDollarSales

class CigaretteReportForm12FirstSalesDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportForm12FirstSalesDate

class CigaretteReportForm2BrandFamilyName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportForm2BrandFamilyName

class CigaretteReportForm3VarietyDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportForm3VarietyDescription

class CigaretteReportForm4ProductLength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportForm4ProductLength

class CigaretteReportForm5Filter(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportForm5Filter

class CigaretteReportForm7Menthol(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportForm7Menthol

class CigaretteReportForm8PackSizeSold(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportForm8PackSizeSold

class CigaretteReportForm9Tar(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportForm9Tar

class CigaretteReportFormBrandFamilyName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormBrandFamilyName

class CigaretteReportFormFilter(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormFilter

class CigaretteReportFormFirstSalesDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormFirstSalesDate

class CigaretteReportFormHardPack(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormHardPack

class CigaretteReportFormLastSalesDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormLastSalesDate

class CigaretteReportFormMenthol(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormMenthol

class CigaretteReportFormNicotine(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormNicotine

class CigaretteReportFormNonfilter(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormNonfilter

class CigaretteReportFormNonmenthol(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormNonmenthol

class CigaretteReportFormPackSizeSold(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormPackSizeSold

class CigaretteReportFormProductLength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormProductLength

class CigaretteReportFormSoftPack(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormSoftPack

class CigaretteReportFormVarietyDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormVarietyDescription

class CigaretteReportFormVarietyDollarSales(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormVarietyDollarSales

class CigaretteReportFormVarietyUnitSales(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormVarietyUnitSales

class CigaretteReportFormYearCovered(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteReportFormYearCovered

class Cigarettes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Cigarettes

class Cigarettes627647(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Cigarettes627647

class Cigarettes647627(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Cigarettes647627

class Circulation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Circulation

class City(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.City

class CityState(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CityState

class CityStateZip(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CityStateZip

class Class(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Class

class Client(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Client

class ClubCashCarryEtc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ClubCashCarryEtc

class Code(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Code

class CommentOnPlant(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CommentOnPlant

class Comments(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Comments

class CommentsByManagerOrDirector(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CommentsByManagerOrDirector

class Commitments(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Commitments

class Committed(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Committed

class Company(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Company

class CompetitiveActivitiesAndPromotions(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveActivitiesAndPromotions

class CompetitiveActivitiesAndPromotionsBrandSPromoted(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveActivitiesAndPromotionsBrandSPromoted

class CompetitiveActivitiesAndPromotionsCc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveActivitiesAndPromotionsCc

class CompetitiveActivitiesAndPromotionsDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveActivitiesAndPromotionsDate

class CompetitiveActivitiesAndPromotionsHowWidespread(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveActivitiesAndPromotionsHowWidespread

class CompetitiveActivitiesAndPromotionsManufacturer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveActivitiesAndPromotionsManufacturer

class CompetitiveActivitiesAndPromotionsOtherComments(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveActivitiesAndPromotionsOtherComments

class CompetitiveActivitiesAndPromotionsReportedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveActivitiesAndPromotionsReportedBy

class CompetitiveActivitiesAndPromotionsSourceOfInformation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveActivitiesAndPromotionsSourceOfInformation

class CompetitiveActivitiesAndPromotionsTypeOfPromotion(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveActivitiesAndPromotionsTypeOfPromotion

class CompetitivePromotionalActivity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitivePromotionalActivity

class CompleteEitherAOrBBelow(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompleteEitherAOrBBelow

class Completion(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Completion

class Compound(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Compound

class CompoundUsPlate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundUsPlate

class CompoundCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundCode

class CompoundName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundName

class CompoundSensitive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundSensitive

class CompoundSensitiveTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundSensitiveTo

class CompoundSensitiveAir(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundSensitiveAir

class CompoundSensitiveHeat(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundSensitiveHeat

class CompoundSensitiveMoisture(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundSensitiveMoisture

class CompoundSensitiveOther(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundSensitiveOther

class CompoundVehicle(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundVehicle

class CompoundVehicleOther(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundVehicleOther

class CompoundVehicleMethylCellulose(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundVehicleMethylCellulose

class CompoundVehicleCornOil(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundVehicleCornOil

class CompoundVehicleSaline(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundVehicleSaline

class CompoundPlates(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompoundPlates

class Concentration1Mgimit(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Concentration1Mgimit

class ConcentrationMgMl(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConcentrationMgMl

class Conclusion(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Conclusion

class Confidential(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Confidential

class ConsumerAcceptance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConsumerAcceptance

class ConsumerAcceptanceExcellent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConsumerAcceptanceExcellent

class ConsumerAcceptanceFair(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConsumerAcceptanceFair

class ConsumerAcceptanceGood(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConsumerAcceptanceGood

class ConsumerAcceptancePoor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConsumerAcceptancePoor

class ConsumerOffer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConsumerOffer

class Contingency(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Contingency

class Contract(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Contract

class ControlAfvertantsPerPlate005MlSolvent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ControlAfvertantsPerPlate005MlSolvent

class ControlRevertantsPerPlateToonMiSolventi(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ControlRevertantsPerPlateToonMiSolventi

class CostOrRetailPricing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CostOrRetailPricing

class CostSummary(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CostSummary

class CostSummaryEstAnnualProductCostChange(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CostSummaryEstAnnualProductCostChange

class CostSummaryObsoleteMaterialCost(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CostSummaryObsoleteMaterialCost

class CostSummarySpecialEquipmentMaterialCost(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CostSummarySpecialEquipmentMaterialCost

class Cqa(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Cqa

class Cumulative(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Cumulative

class CurrentBalAvailable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CurrentBalAvailable

class CustomerShippingNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CustomerShippingNumber

class CapitalBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CapitalBudget

class CharNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CharNo

class CharacteristicTested(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CharacteristicTested

class ChargeCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChargeCode

class ChargeToSection(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChargeToSection

class CheckColumnsBelowOnlyIfBillMakesARectAppropriationOrAffectASumSufficientAppropriation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CheckColumnsBelowOnlyIfBillMakesARectAppropriationOrAffectASumSufficientAppropriation

class ChemAbstr(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ChemAbstr

class Chicago(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Chicago

class Cicarettes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Cicarettes

class CicarettesAirDilution(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CicarettesAirDilution

class CicarettesCircumference(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CicarettesCircumference

class CicarettesGlueRoller(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CicarettesGlueRoller

class CicarettesLength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CicarettesLength

class CicarettesMaker(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CicarettesMaker

class CicarettesPaper(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CicarettesPaper

class CicarettesTipPaper(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CicarettesTipPaper

class CicarettesTipPaperPor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CicarettesTipPaperPor

class CicarettesWeight(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CicarettesWeight

class Cigarette(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Cigarette

class CigaretteDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigaretteDescription

class CigarettesBrand(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigarettesBrand

class CigarettesCircumference(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigarettesCircumference

class CigarettesDraw(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigarettesDraw

class CigarettesFilterLength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigarettesFilterLength

class CigarettesFirmness(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigarettesFirmness

class CigarettesLength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigarettesLength

class CigarettesPaper(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigarettesPaper

class CigarettesPrint(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigarettesPrint

class CigarettesTippingPaper(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigarettesTippingPaper

class CigarettesWeight(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigarettesWeight

class CigarettesMaker(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CigarettesMaker

class CircOfRod(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CircOfRod

class CirculationQuantity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CirculationQuantity

class Circunference(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Circunference

class CityTown(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CityTown

class ClientContact(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ClientContact

class ClientGroup(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ClientGroup

class ClientName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ClientName

class ClientStudyNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ClientStudyNo

class Color(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Color

class ColumnInches(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ColumnInches

class CombWrap(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CombWrap

class CombWrapPor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CombWrapPor

class Commercial(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Commercial

class CommittedToDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CommittedToDate

class CommittedToDateCurrentYear(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CommittedToDateCurrentYear

class CommitteeMeeting(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CommitteeMeeting

class CompensationReceivedLobbying(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompensationReceivedLobbying

class Competitive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Competitive

class CompetitiveProposalsObtained(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveProposalsObtained

class CompetitiveProposalsObtainedCost(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveProposalsObtainedCost

class CompetitiveProposalsObtainedCostPerInterview(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveProposalsObtainedCostPerInterview

class CompetitiveProposalsObtainedEst(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveProposalsObtainedEst

class CompetitiveProposalsObtainedEstTravel(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveProposalsObtainedEstTravel

class CompetitiveProposalsObtainedSupplier(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveProposalsObtainedSupplier

class CompetitiveProposalsObtainedTotalCost(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveProposalsObtainedTotalCost

class Competitive25PgWSorbitol647627(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Competitive25PgWSorbitol647627

class CompetitiveCurrentViceroy84647647(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitiveCurrentViceroy84647647

class CompetitorsBrandsMild7LightsSmokers(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompetitorsBrandsMild7LightsSmokers

class CompleteWeight(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompleteWeight

class CompletionDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CompletionDate

class Con(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Con

class Confirmation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Confirmation

class ConfirmationName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConfirmationName

class ConfirmationNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConfirmationNo

class ConfirmationYes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConfirmationYes

class ConsiderationDeferredUntil(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConsiderationDeferredUntil

class ConsumerSegmentS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConsumerSegmentS

class ConsumerSegmentSBySel(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConsumerSegmentSBySel

class ConsumerSegmentSByAge(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConsumerSegmentSByAge

class ConsumerSegmentSFemale(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConsumerSegmentSFemale

class ConsumerSegmentSMale(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ConsumerSegmentSMale

class ContactNameTelephone(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ContactNameTelephone

class Contact(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Contact

class ContractNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ContractNo

class ContractSubject(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ContractSubject

class ContractualOrAgreedFee(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ContractualOrAgreedFee

class Contribution(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Contribution

class Copies(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Copies

class CopiesToTheFollowing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CopiesToTheFollowing

class CopiesTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CopiesTo

class Cost(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Cost

class CostEstimate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CostEstimate

class CostPerInterview(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CostPerInterview

class Country(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Country

class CountyOf(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CountyOf

class CouponExpirationDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CouponExpirationDate

class CouponIssueDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CouponIssueDate

class CouponValue(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CouponValue

class Court(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Court

class CurrentBalanceAvailable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CurrentBalanceAvailable

class CurrentBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CurrentBudget

class CurrentYearCost(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CurrentYearCost

class Customer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Customer

class D(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.D

class DM(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DM

class DEC(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DEC

class DailyEffectiveCirculation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DailyEffectiveCirculation

class DateComplete(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateComplete

class DateForwardedPromotionServices(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateForwardedPromotionServices

class DateIssued(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateIssued

class DateOfReport(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateOfReport

class DateOfRequisition(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateOfRequisition

class DatePostersReceivedFromLithographer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DatePostersReceivedFromLithographer

class DatePostingCompleted(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DatePostingCompleted

class DateReceived(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateReceived

class DateRequested(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateRequested

class DateShipped(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateShipped

class DateSubmittedAndDeptManager(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateSubmittedAndDeptManager

class DateToCorp(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateToCorp

class DateToNyo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateToNyo

class DateWanted(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateWanted

class Dates(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Dates

class Ddress(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ddress

class DeFullfillmentVendor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DeFullfillmentVendor

class DeadlineForBidReceipt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DeadlineForBidReceipt

class Dec1987Accrual(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Dec1987Accrual

class DeliveryDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DeliveryDate

class DepartmentCharged(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DepartmentCharged

class Department(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Department

class DeptNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DeptNo

class Description(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Description

class DescriptionOfReactivity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DescriptionOfReactivity

class DescriptionOfReactivityWithHeating80c(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DescriptionOfReactivityWithHeating80c

class DescriptionOfReactivityWithoutHeating(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DescriptionOfReactivityWithoutHeating

class Design(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Design

class DesignNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DesignNo

class DesignOnDisplay(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DesignOnDisplay

class Dessicator(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Dessicator

class DirOfLifeSciencesHealthServicesCompoundPrepToxScientificResTox(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DirOfLifeSciencesHealthServicesCompoundPrepToxScientificResTox

class DirectAccountAndChainVoidsUseXToIndicateAVoid(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DirectAccountAndChainVoidsUseXToIndicateAVoid

class DirectAccountAndChainVoidsUseXToIndicateAVoid100S(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DirectAccountAndChainVoidsUseXToIndicateAVoid100S

class DirectAccountAndChainVoidsUseXToIndicateAVoidAccount(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DirectAccountAndChainVoidsUseXToIndicateAVoidAccount

class DirectAccountAndChainVoidsUseXToIndicateAVoidLts100S(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DirectAccountAndChainVoidsUseXToIndicateAVoidLts100S

class DirectAccountAndChainVoidsUseXToIndicateAVoidNoStores(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DirectAccountAndChainVoidsUseXToIndicateAVoidNoStores

class DirectorOfRaQa(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DirectorOfRaQa

class DirectorOfResearch(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DirectorOfResearch

class DisplayAgreement(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DisplayAgreement

class DisplayBrands(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DisplayBrands

class DisplayMaterial(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DisplayMaterial

class Distribution(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Distribution

class DivNameNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DivNameNo

class Division(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Division

class DivisionName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DivisionName

class DivisionFull(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DivisionFull

class DivisionPartial(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DivisionPartial

class DoesWorkMeritPublication(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DoesWorkMeritPublication

class Doral(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Doral

class DosageMgKgBodyWeight(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DosageMgKgBodyWeight

class DatasetName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DatasetName

class Date(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Date

class DateS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateS

class DateInitiated(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateInitiated

class DateMade(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateMade

class DateRecD(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateRecD

class DateRequired(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateRequired

class DateRouted(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateRouted

class DateSent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateSent

class DateSubmitted(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateSubmitted

class DateAndHourOfService(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateAndHourOfService

class DateOfFinalReportReviewCompletedDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateOfFinalReportReviewCompletedDate

class DateOfRequest(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DateOfRequest

class DatesOfContact(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DatesOfContact

class DeadlineForResponse(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DeadlineForResponse

class Dec(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Dec

class DecisionOfCommitteeOnPresentRequest(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DecisionOfCommitteeOnPresentRequest

class DeclinedSendLetter(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DeclinedSendLetter

class Decrease(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Decrease

class DeliveryRollerOverTape(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DeliveryRollerOverTape

class DeptCodeNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DeptCodeNo

class DescribePossibleSolutionsAndBenefits(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DescribePossibleSolutionsAndBenefits

class DescriptionOfChangeOrder(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DescriptionOfChangeOrder

class DescriptionCapriExpansion(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DescriptionCapriExpansion

class Dimension(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Dimension

class DirectAccount(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DirectAccount

class DirectionalDifference(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DirectionalDifference

class Director(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Director

class DistAsgmtCF(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DistAsgmtCF

class DistanceFromYourHomeToAirport(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DistanceFromYourHomeToAirport

class DistributionDropDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DistributionDropDate

class DistributorNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DistributorNo

class DivisionSToBeContacted(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DivisionSToBeContacted

class DivisionMgr(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DivisionMgr

class DoYouPreferAirlineSeatsInSmokingOrNonSmokingSection(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DoYouPreferAirlineSeatsInSmokingOrNonSmokingSection

class DocumentS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DocumentS

class Domestic(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Domestic

class Draw(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Draw

class DryWeight(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DryWeight

class DryWtWithAdhesive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DryWtWithAdhesive

class DueThe1StMondayOfTheMonthDuringTheLegislativeSessionToReportThePreviousMonthsActivity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DueThe1StMondayOfTheMonthDuringTheLegislativeSessionToReportThePreviousMonthsActivity

class DuringThisReportingPeriodHaveYouMadeAnyExpenditureOrIncurredAnyObligationOf2500OrMorePerOccurenceToPromoteOrOpposeAnyLegislationIncludingButNotLimitedMailingsMealsPrintOrBroadcastAdvertisementsOrGiftsYesOrNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DuringThisReportingPeriodHaveYouMadeAnyExpenditureOrIncurredAnyObligationOf2500OrMorePerOccurenceToPromoteOrOpposeAnyLegislationIncludingButNotLimitedMailingsMealsPrintOrBroadcastAdvertisementsOrGiftsYesOrNo

class E(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.E

class EaseOfDraw17Easier(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EaseOfDraw17Easier

class EffectivenessOfAdvertising(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EffectivenessOfAdvertising

class EffectivenessOf(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EffectivenessOf

class EfficiencyRating(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EfficiencyRating

class EfficiencyRatingExcellent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EfficiencyRatingExcellent

class EfficiencyRatingFair(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EfficiencyRatingFair

class EfficiencyRatingGood(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EfficiencyRatingGood

class EfficiencyRatingPoor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EfficiencyRatingPoor

class Elt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Elt

class Endorsements(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Endorsements

class Epb(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Epb

class EstimateOfTimeNeededToCompleteWork(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimateOfTimeNeededToCompleteWork

class EstimateOfTimeNeededToPrepareManuscriptForPresentation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimateOfTimeNeededToPrepareManuscriptForPresentation

class EstimateOfTimeNeededToPrepareManuscriptForPublication(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimateOfTimeNeededToPrepareManuscriptForPublication

class EstimatedPaybackPeriod(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimatedPaybackPeriod

class EstimatedTargetDateOriginalComments(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimatedTargetDateOriginalComments

class EstimatedToxicityClass(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimatedToxicityClass

class Expense(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Expense

class ExperimentalProcedures(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ExperimentalProcedures

class Explosive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Explosive

class ExtraCopiesTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ExtraCopiesTo

class EnclosedAreCopiesOfLegalProcesServedUponTheStatutoryAgentOfTheAboveCompanyAsFollows(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EnclosedAreCopiesOfLegalProcesServedUponTheStatutoryAgentOfTheAboveCompanyAsFollows

class EstMonthlyOngoing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstMonthlyOngoing

class EstTravel(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstTravel

class EstimateCost(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimateCost

class EstimateCostCapital(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimateCostCapital

class EstimateCostExpense(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimateCostExpense

class EstimateCostTotal(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimateCostTotal

class EstimateNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimateNo

class EstimatedAttendance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimatedAttendance

class EstimatedFreightCharges(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimatedFreightCharges

class EstimatedManHoursForCompletion(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimatedManHoursForCompletion

class EstimatedResponders(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimatedResponders

class EstimatedResponse(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimatedResponse

class EstimatedCostOfTheStudyWillBe(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.EstimatedCostOfTheStudyWillBe

class Excellent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Excellent

class ExclusiveAdvertisingFor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ExclusiveAdvertisingFor

class ExpirationDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ExpirationDate

class Export(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Export

class ExtAuthoDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ExtAuthoDate

class ExtentOfDistribution(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ExtentOfDistribution

class ExtraBanquetTickets4000(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ExtraBanquetTickets4000

class FPMDeliveryRoller(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FPMDeliveryRoller

class FPMNo1Roller(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FPMNo1Roller

class FPMNo2Roller(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FPMNo2Roller

class Fax(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Fax

class FaxMumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FaxMumber

class FaxNumbers(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FaxNumbers

class FdcRepresentatives(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FdcRepresentatives

class FileFileType(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FileFileType

class FinalFlavor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FinalFlavor

class FirmName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FirmName

class FiscalEstimateAdMba23Rev1180(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FiscalEstimateAdMba23Rev1180

class FixedDistribution(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FixedDistribution

class Flammable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Flammable

class Fo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Fo

class FoaControlUseOnly(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FoaControlUseOnly

class FoaControlUseOnlyCodeAssigned(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FoaControlUseOnlyCodeAssigned

class FoaControlUseOnlyEstRedemption(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FoaControlUseOnlyEstRedemption

class FoaControlUseOnlyJoeNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FoaControlUseOnlyJoeNumber

class FollowDepartmentAndCompanySafetyManuals(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FollowDepartmentAndCompanySafetyManuals

class FollowUpDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FollowUpDate

class For(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.For

class ForControlUseOnly(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ForControlUseOnly

class ForControlUseOnlyCodeAssigned(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ForControlUseOnlyCodeAssigned

class ForControlUseOnlyJobNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ForControlUseOnlyJobNumber

class ForPurchasingDepartmentUseOnly(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ForPurchasingDepartmentUseOnly

class Freezer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Freezer

class From(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.From

class FrontCigarettes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FrontCigarettes

class FrontCigarettesComments(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FrontCigarettesComments

class FrontCigarettesCratering(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FrontCigarettesCratering

class FrontCigarettesHoleDepth(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FrontCigarettesHoleDepth

class FrontCigarettesScorching(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FrontCigarettesScorching

class FsMarketing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FsMarketing

class Full(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Full

class FullInspection(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FullInspection

class Funding(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Funding

class Facility(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Facility

class Fair(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Fair

class FaxNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FaxNumber

class FaxNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FaxNo

class Feb(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Feb

class Female(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Female

class Female106(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Female106

class FemaleBright(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FemaleBright

class FemaleKl(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FemaleKl

class FieldComplete(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldComplete

class FieldStart(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldStart

class FieldworkSchedule(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldworkSchedule

class FilmCleared(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FilmCleared

class FilmSEnclosed(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FilmSEnclosed

class Filter(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Filter

class Filters(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Filters

class FiltersCircumference(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FiltersCircumference

class FiltersKind(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FiltersKind

class FiltersPlasticizer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FiltersPlasticizer

class FiltersPlugWrap(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FiltersPlugWrap

class FiltersPressureDrop(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FiltersPressureDrop

class FiltersProcess(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FiltersProcess

class FiltersRodLength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FiltersRodLength

class FiltersWeight(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FiltersWeight

class FinalReportDue(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FinalReportDue

class FinalReportDueSupplierRpt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FinalReportDueSupplierRpt

class FinalRptDue(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FinalRptDue

class FinalSupplierReportDue(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FinalSupplierReportDue

class FinalApprovalIsOfCourseDependentUponTimeAndPlacementOfTheCommercialS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FinalApprovalIsOfCourseDependentUponTimeAndPlacementOfTheCommercialS

class FinalistName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FinalistName

class FirmnessOfRod(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FirmnessOfRod

class First(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.First

class FiscalEffect(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FiscalEffect

class FollowingPhysicalVisualPropertiesOutOfSpecifications(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FollowingPhysicalVisualPropertiesOutOfSpecifications

class ForAmericanBrandsInc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ForAmericanBrandsInc

class FormulaNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FormulaNo

class FromNewspaper(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FromNewspaper

class FromNicotineMgCigt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FromNicotineMgCigt

class FromTarMgCigt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FromTarMgCigt

class FullfillmentDataEntryAt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FullfillmentDataEntryAt

class FundSourceAffected(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FundSourceAffected

class FurtherInformationPleaseAttachAnyRelevantMaterialsPosAdvertisingBrochuresEtc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FurtherInformationPleaseAttachAnyRelevantMaterialsPosAdvertisingBrochuresEtc

class GPC(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GPC

class GLCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GLCode

class GeneralInformation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GeneralInformation

class GeneralInformationEventDates(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GeneralInformationEventDates

class GeneralInformationEventLocation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GeneralInformationEventLocation

class GeneralInformationEventName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GeneralInformationEventName

class GeneralProjectDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GeneralProjectDescription

class GeneralExport(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GeneralExport

class GeogfiaphicalAreaS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GeogfiaphicalAreaS

class Geography(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Geography

class GolfTournament(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GolfTournament

class GroupNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GroupNo

class GeneralManager(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GeneralManager

class GeneticAssayNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GeneticAssayNo

class GeographicalAreaS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GeographicalAreaS

class GluePreeArea(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GluePreeArea

class GroupProduct(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GroupProduct

class Harshness(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Harshness

class HasWorkBeenReportedInManuscript(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HasWorkBeenReportedInManuscript

class HazardousCompound(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HazardousCompound

class HazardousCompoundCarcinogenOsha(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HazardousCompoundCarcinogenOsha

class HazardousCompoundCarcinogenOther(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HazardousCompoundCarcinogenOther

class HazardousCompoundExplosive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HazardousCompoundExplosive

class HazardousCompoundFlammable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HazardousCompoundFlammable

class HazardousCompoundRadioactive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HazardousCompoundRadioactive

class Headline(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Headline

class HkTrial(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HkTrial

class Hours(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Hours

class HoursMondayFriday(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HoursMondayFriday

class HoursSaturdaySunday(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HoursSaturdaySunday

class HowWidespread(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HowWidespread

class HaveYouContactedYourManagerSupervisor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HaveYouContactedYourManagerSupervisor

class HaveYouContactedYourManagerSupervisorNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HaveYouContactedYourManagerSupervisorNo

class HaveYouContactedYourManagerSupervisorYes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HaveYouContactedYourManagerSupervisorYes

class HaveYouPaidAnyTypeOfCompensationOrIncurredAnyObligationForPaymentToTheAboveNamed(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HaveYouPaidAnyTypeOfCompensationOrIncurredAnyObligationForPaymentToTheAboveNamed

class HomeAddress(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HomeAddress

class HomeTelephone(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HomeTelephone

class HotelMotelReservationsNeeded(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HotelMotelReservationsNeeded

class HousekeepingCleaning(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.HousekeepingCleaning

class IWillParticipateInTheGolfTournament(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IWillParticipateInTheGolfTournament

class IWillParticipateInTheTennisTournamentIWouldClassifyMyselfAsPleaseCheckAppropriateBox(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IWillParticipateInTheTennisTournamentIWouldClassifyMyselfAsPleaseCheckAppropriateBox

class Id(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Id

class IfNoExplain(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IfNoExplain

class IfSoGiveDateAndTitle(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IfSoGiveDateAndTitle

class IfYesCanItBeImproved(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IfYesCanItBeImproved

class IfYouDoNotReceiveAnyOfThePagesPleaseCall(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IfYouDoNotReceiveAnyOfThePagesPleaseCall

class IfYouHaveAnyQuestionsPleaseContactTheFollowingPerson(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IfYouHaveAnyQuestionsPleaseContactTheFollowingPerson

class Ii(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ii

class IiiSupplementalLiteratureSearchChemicalAbstractsVol23Vol65ArctanderSPerfumeAndFlavorMaterialsOfNaturalOrigin1960GuentherSMonographsOnFragranceRawMaterials1979TobaccoAbstractsUSDispensatory23RdEdition1943(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IiiSupplementalLiteratureSearchChemicalAbstractsVol23Vol65ArctanderSPerfumeAndFlavorMaterialsOfNaturalOrigin1960GuentherSMonographsOnFragranceRawMaterials1979TobaccoAbstractsUSDispensatory23RdEdition1943

class Illustration(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Illustration

class In(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.In

class InTestimonyWhereofIHaveSetMyHandAndSealTheDayAndYearAforesaid(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InTestimonyWhereofIHaveSetMyHandAndSealTheDayAndYearAforesaid

class InalTitleOfSymposium(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InalTitleOfSymposium

class InbifoInstitutFRBiologischeForschungGmbh(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InbifoInstitutFRBiologischeForschungGmbh

class IndLorVolume(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IndLorVolume

class IndVolume(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IndVolume

class IndependentAcceptance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IndependentAcceptance

class IndependentAcceptanceExcellent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IndependentAcceptanceExcellent

class IndependentAcceptanceFair(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IndependentAcceptanceFair

class IndependentAcceptanceGood(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IndependentAcceptanceGood

class IndependentAcceptancePoor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IndependentAcceptancePoor

class InitialMaterialsRequired(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InitialMaterialsRequired

class InitialMaterialsRequiredCartons(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InitialMaterialsRequiredCartons

class InitialMaterialsRequiredCases(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InitialMaterialsRequiredCases

class InitialMaterialsRequiredDollarCost(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InitialMaterialsRequiredDollarCost

class InitialMaterialsRequiredPackFlatsLabels(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InitialMaterialsRequiredPackFlatsLabels

class InitialMaterialsRequiredQtyInUnits(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InitialMaterialsRequiredQtyInUnits

class Initiated(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Initiated

class InspectionBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InspectionBy

class Instructions(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Instructions

class InventoryDepletionDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InventoryDepletionDate

class InvestigatorS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InvestigatorS

class IssueFrequencyYear(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IssueFrequencyYear

class Issue(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Issue

class IssuedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IssuedBy

class Item(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Item

class ItemBrand(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ItemBrand

class Items(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Items

class ItemsAnyOtherItemsAvailable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ItemsAnyOtherItemsAvailable

class ItemsBannerS4X8(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ItemsBannerS4X8

class ItemsBaseballCap(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ItemsBaseballCap

class ItemsGeneralMarket(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ItemsGeneralMarket

class ItemsSpanishLanguage(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ItemsSpanishLanguage

class ItemsUrban(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ItemsUrban

class ItemsWaterBottles(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ItemsWaterBottles

class IfAMaterialOrDimensionalChangeAlsoInvolved(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IfAMaterialOrDimensionalChangeAlsoInvolved

class IfAnyAddressesOrTelephoneNumbersHaveChangedSinceTheLastReportingPeriodPleaseCheckHereAndNoteTheChangeInTheSpaceProvidedAtTheEndOfThisForm(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IfAnyAddressesOrTelephoneNumbersHaveChangedSinceTheLastReportingPeriodPleaseCheckHereAndNoteTheChangeInTheSpaceProvidedAtTheEndOfThisForm

class IfThereIsATransmissionProblemPleaseCall(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IfThereIsATransmissionProblemPleaseCall

class IfYesSupplyDetails(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IfYesSupplyDetails

class IfYesPleaseCompleteTheFollowing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IfYesPleaseCompleteTheFollowing

class Implement(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Implement

class ImplementNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ImplementNo

class ImplementPending(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ImplementPending

class ImplementYes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ImplementYes

class Incidence(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Incidence

class IncreaseCostsMayBePossibleToAbsorb(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IncreaseCostsMayBePossibleToAbsorb

class InformationAndHearsayFromOutsideContacts(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InformationAndHearsayFromOutsideContacts

class InitiationDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InitiationDate

class Inorganic(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Inorganic

class Institution(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Institution

class Insurance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Insurance

class IntInitDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IntInitDate

class InternalInitDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InternalInitDate

class InterviewLength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InterviewLength

class InterviewsDividedAmong3Gorups(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InterviewsDividedAmong3Gorups

class Invitations(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Invitations

class InvitationsRequested(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InvitationsRequested

class InvitationsDateNotified(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InvitationsDateNotified

class InvitationsDateOrdered(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InvitationsDateOrdered

class InviteesComments(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.InviteesComments

class IsThisACorporation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.IsThisACorporation

class Jan(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Jan

class JobNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JobNo

class Job(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Job

class Jul(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Jul

class JimmyHBellBScScientist(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.JimmyHBellBScScientist

class Jun(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Jun

class KS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.KS

class Kool(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Kool

class KoolLights(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.KoolLights

class KoolLightsKsWhiteTipPingMasked(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.KoolLightsKsWhiteTipPingMasked

class KeyCriteriaForAnalysis(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.KeyCriteriaForAnalysis

class Keywords1993(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Keywords1993

class Kind(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Kind

class LAngeles(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LAngeles

class LRGravely(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LRGravely

class LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCratering(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCratering

class LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringBrand(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringBrand

class LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringModules(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringModules

class LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringPower(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringPower

class LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringPulse(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringPulse

class LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringShiftDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringShiftDate

class Ld5095ConfidenceLimits(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ld5095ConfidenceLimits

class Ld5095Confidence(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ld5095Confidence

class LeadIn(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LeadIn

class LhNumberS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LhNumberS

class ListPrice(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ListPrice

class ListTheInformationBelowAsItPertainsToTheUrbanCenterPortionOfYourAssignmentOnly(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ListTheInformationBelowAsItPertainsToTheUrbanCenterPortionOfYourAssignmentOnly

class LiteratureSurveyed(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LiteratureSurveyed

class LocalApproval(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LocalApproval

class LocalPOreleaseNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LocalPOreleaseNo

class Lorillard(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Lorillard

class LorillardCompoundCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LorillardCompoundCode

class LorillardCompoundCodeNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LorillardCompoundCodeNumber

class LorillardNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LorillardNo

class LorillardResearchCenter(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LorillardResearchCenter

class Lot(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Lot

class LotNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LotNo

class LotNoS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LotNoS

class LotNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LotNumber

class Louisville(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Louisville

class LrbOrBillNoHanAuNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LrbOrBillNoHanAuNo

class LrcCompoundCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LrcCompoundCode

class LrcFileNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LrcFileNumber

class Lt100S(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Lt100S

class LtBox80S(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LtBox80S

class LtKS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LtKS

class LaboratoryAnalysis(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LaboratoryAnalysis

class Last(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Last

class LateRegistrationFeeAfterAugust(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LateRegistrationFeeAfterAugust

class Law(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Law

class LegalApproval(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LegalApproval

class LegalApprovalRecommendedRequired(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LegalApprovalRecommendedRequired

class LegalApprovalRecommendedRequiredNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LegalApprovalRecommendedRequiredNo

class LegalApprovalRecommendedRequiredYes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LegalApprovalRecommendedRequiredYes

class Length(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Length

class LengthInt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LengthInt

class LengthOfCigarettes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LengthOfCigarettes

class LengthOfRod(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LengthOfRod

class LicenseeRefNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LicenseeRefNo

class LobbyistName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LobbyistName

class LocalPurchasing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LocalPurchasing

class Local(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Local

class LocalDecreasCorts(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LocalDecreasCorts

class LocalMandatory(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LocalMandatory

class LocalPermane(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LocalPermane

class LocalIncreaseCosts(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LocalIncreaseCosts

class LocalNoOcaGOvernmentCost(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LocalNoOcaGOvernmentCost

class LocalPermissive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LocalPermissive

class Location(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Location

class LongRangeFiscalImplications(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LongRangeFiscalImplications

class LotOrSample(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LotOrSample

class MBDavis(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MBDavis

class Macon(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Macon

class Madison25MmButt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Madison25MmButt

class Madison25MmButtMeanOfLast12Samples(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Madison25MmButtMeanOfLast12Samples

class Madison25MmButtPresentSample(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Madison25MmButtPresentSample

class MajorMktAndMktResearchSteps(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MajorMktAndMktResearchSteps

class MajorMktAndMktResearchStepsInHomePlacement(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MajorMktAndMktResearchStepsInHomePlacement

class Manufacturer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Manufacturer

class Manufacturers(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Manufacturers

class Market(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Market

class MarketS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MarketS

class MaterialNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MaterialNo

class MaverickHarleyB1G1F(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MaverickHarleyB1G1F

class MechanicalProduction(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MechanicalProduction

class Media(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Media

class MediaMagazines(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MediaMagazines

class MediaNewspaper(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MediaNewspaper

class Medium(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Medium

class Ment(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ment

class Menthol(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Menthol

class MentholFlavor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MentholFlavor

class MentholTaste7Better(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MentholTaste7Better

class Merchandise(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Merchandise

class MerchandiseOrderThroughYourSupplier(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MerchandiseOrderThroughYourSupplier

class MerchandiseWillBeArbitrarilyShippedToStore(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MerchandiseWillBeArbitrarilyShippedToStore

class MethodOfPreparation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MethodOfPreparation

class MilitaryExport(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MilitaryExport

class Moist(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Moist

class MolecularWeight(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MolecularWeight

class MrPersonnel(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MrPersonnel

class Mrd(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Mrd

class MyCommissionExpires(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MyCommissionExpires

class Macket(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Macket

class Magazine(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Magazine

class MaiCheckTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MaiCheckTo

class MailTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MailTo

class Maildate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Maildate

class MailfileCells(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MailfileCells

class MailfileDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MailfileDescription

class MailfileId(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MailfileId

class MajorAirportNearestYourHome(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MajorAirportNearestYourHome

class MakerNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MakerNo

class Male(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Male

class Male99(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Male99

class Manager(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Manager

class ManagerComments(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ManagerComments

class ManufacturerBrand(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ManufacturerBrand

class Mar(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Mar

class MarginalDifference(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MarginalDifference

class MarketSZoneS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MarketSZoneS

class Marketing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Marketing

class MarketingResearch(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MarketingResearch

class MarketingAndOrResearchObjectives(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MarketingAndOrResearchObjectives

class MaterialTested(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MaterialTested

class May(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.May

class MeanDrawOfRod(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MeanDrawOfRod

class MediaName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MediaName

class MediaType(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MediaType

class Message(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Message

class Method(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Method

class MethodOfShipment(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MethodOfShipment

class MethodOfTravel(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MethodOfTravel

class MethodOfTravelAir(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MethodOfTravelAir

class MethodOfTravelAuto(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MethodOfTravelAuto

class MethodOfTravelOther(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MethodOfTravelOther

class MethodOfTravelTrain(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MethodOfTravelTrain

class Mgr(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Mgr

class Middle(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Middle

class Military(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Military

class Mo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Mo

class ModeratorsFee(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ModeratorsFee

class MondayYN(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MondayYN

class MyHandicapIs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MyHandicapIs

class NWKremer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NWKremer

class Name(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Name

class NameOrInitials(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NameOrInitials

class NamesOfOtherPersonsCollaboratingInWork(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NamesOfOtherPersonsCollaboratingInWork

class NatureOfWork(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NatureOfWork

class NewCompetitiveProducts(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewCompetitiveProducts

class NewCompetitiveProductsBrandName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewCompetitiveProductsBrandName

class NewCompetitiveProductsDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewCompetitiveProductsDate

class NewCompetitiveProductsExtentOfDistribution(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewCompetitiveProductsExtentOfDistribution

class NewCompetitiveProductsListPrice(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewCompetitiveProductsListPrice

class NewCompetitiveProductsManufacturer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewCompetitiveProductsManufacturer

class NewCompetitiveProductsOtherInformation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewCompetitiveProductsOtherInformation

class NewCompetitiveProductsReportedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewCompetitiveProductsReportedBy

class NewCompetitiveProductsSizeOrSizes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewCompetitiveProductsSizeOrSizes

class NewCompetitiveProductsTime(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewCompetitiveProductsTime

class NewCompetitiveProductsTypeOfProduct(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewCompetitiveProductsTypeOfProduct

class NewCompetitiveProductsCc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewCompetitiveProductsCc

class NewItem(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewItem

class NewItemBrandS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewItemBrandS

class NewItemDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewItemDescription

class NewItemMaterialNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewItemMaterialNo

class NewItemNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewItemNo

class NewItemUpcNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewItemUpcNo

class NgDocumentsWereFoundWithinTheOriginal(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NgDocumentsWereFoundWithinTheOriginal

class Nic(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Nic

class Nicotine(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Nicotine

class NoOfRotaries(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NoOfRotaries

class NoCartons(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NoCartons

class NoOfStores(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NoOfStores

class NotApproved(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NotApproved

class Note(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Note

class NotebookPage(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NotebookPage

class Notes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Notes

class NumberOfCartons(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NumberOfCartons

class NumberOfCigarettesSmoked(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NumberOfCigarettesSmoked

class NumberOfFollowingPages(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NumberOfFollowingPages

class NumberOfPagesIncludingCoverSheet(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NumberOfPagesIncludingCoverSheet

class NumberOfPanels(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NumberOfPanels

class NumberOfPanelsIlluminated(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NumberOfPanelsIlluminated

class NumberOfPanelsRegular(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NumberOfPanelsRegular

class NumberOfPanelsTotal(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NumberOfPanelsTotal

class NumberOfSamplingPersonnel(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NumberOfSamplingPersonnel

class NumberOfSupervisors(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NumberOfSupervisors

class NumberViewed(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NumberViewed

class Number(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Number

class Numbers(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Numbers

class NyoOnly(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NyoOnly

class NyoOnlyDateForwardedToPromotionServices(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NyoOnlyDateForwardedToPromotionServices

class NysawmdInc211East43rdStreetNewYorkNy100174707(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NysawmdInc211East43rdStreetNewYorkNy100174707

class NamePhoneExt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NamePhoneExt

class NameOfAccount(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NameOfAccount

class NameOfEvent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NameOfEvent

class NameOfGuests(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NameOfGuests

class NameOfSpouseParticipatingInTheGuestPrograms(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NameOfSpouseParticipatingInTheGuestPrograms

class NatureOfAction(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NatureOfAction

class NewBalance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewBalance

class NewspaperDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NewspaperDate

class No(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.No

class NoPreference(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NoPreference

class No1RollerOverTape(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.No1RollerOverTape

class NoOfCartons(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NoOfCartons

class Nov(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Nov

class NumberOfStores(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.NumberOfStores

class OOrganizerIfApplicable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OOrganizerIfApplicable

class Objective(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Objective

class Oct(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Oct

class Of(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Of

class Operator(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Operator

class Option(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Option

class Or(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Or

class Oral(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Oral

class OrderNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OrderNo

class OrientationMeeting(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OrientationMeeting

class OrientationMeetingDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OrientationMeetingDate

class OrientationMeetingPlace(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OrientationMeetingPlace

class OrientationMeetingTime(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OrientationMeetingTime

class OriginalCompletionDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OriginalCompletionDate

class OriginalCompletionDate1St(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OriginalCompletionDate1St

class OriginalCompletionDate79(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OriginalCompletionDate79

class OriginalCompletionDateQtr(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OriginalCompletionDateQtr

class OriginalSignedProjectSheetsToPso(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OriginalSignedProjectSheetsToPso

class OtherComments(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OtherComments

class OtherInformation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OtherInformation

class OtherInformationDateRequested(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OtherInformationDateRequested

class OtherInformationDeadlineForBidReceipt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OtherInformationDeadlineForBidReceipt

class OtherPersonnelAssigned(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OtherPersonnelAssigned

class OttApprovals(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OttApprovals

class OttApprovalsDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OttApprovalsDate

class OttApprovalsDepartment(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OttApprovalsDepartment

class OttApprovalsSignature(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OttApprovalsSignature

class OurFaxNumberIs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OurFaxNumberIs

class Overall(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Overall

class OfferDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OfferDescription

class OnWhomProcessWasServed(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OnWhomProcessWasServed

class OperatorInitials(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OperatorInitials

class OrganizationEmployerName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OrganizationEmployerName

class Original(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Original

class OriginalBudgetedAmount(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OriginalBudgetedAmount

class OriginalRequestMadeBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OriginalRequestMadeBy

class Originator(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Originator

class Other(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Other

class OtherSpecifications(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OtherSpecifications

class OwnBrandDunhillSmokers(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OwnBrandDunhillSmokers

class POBox(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.POBox

class PS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PS

class PackAndOrCartocarton(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PackAndOrCartocarton

class PackAndOrCarton(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PackAndOrCarton

class Packing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Packing

class PackingBox80SWhereAvailable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PackingBox80SWhereAvailable

class PackingFilter100S(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PackingFilter100S

class PackingFilterKS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PackingFilterKS

class Packs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Packs

class Page(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Page

class PageNumberSWereMissingInTheOriginal(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PageNumberSWereMissingInTheOriginal

class PageS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PageS

class Paid1987(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Paid1987

class PaidOutOf1987Budget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PaidOutOf1987Budget

class PaidOutOf1989Budget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PaidOutOf1989Budget

class PaidOutOf1989BudgetDec(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PaidOutOf1989BudgetDec

class PaidOutOf1989BudgetFeb(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PaidOutOf1989BudgetFeb

class Partial(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Partial

class Payroll(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Payroll

class Pdc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Pdc

class PerformingDepartments(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PerformingDepartments

class PeriodFrom(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PeriodFrom

class Permanent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Permanent

class Petersburg(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Petersburg

class PhCalculated50(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhCalculated50

class Ph(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ph

class PhysicalAppearance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalAppearance

class PhysicalDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalDescription

class PhysicalDescriptionColor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalDescriptionColor

class PhysicalDescriptionLiquid(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalDescriptionLiquid

class PhysicalDescriptionPressurized(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalDescriptionPressurized

class PhysicalDescriptionSolid(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalDescriptionSolid

class PhysicalState(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalState

class Place(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Place

class PlantAverage(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PlantAverage

class PlantOperator(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PlantOperator

class PleaseDeliverTransmissionTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseDeliverTransmissionTo

class PleaseDeliverTransmissionToFaxPhoneNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseDeliverTransmissionToFaxPhoneNumber

class PleaseDeliverTransmissionToName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseDeliverTransmissionToName

class PleaseDeliverTransmissionToOffice(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseDeliverTransmissionToOffice

class PleaseNotifyThisDepartmentOfAnyChangesInTheCodeNumberS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseNotifyThisDepartmentOfAnyChangesInTheCodeNumberS

class PleaseTransmitThisDocumentTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseTransmitThisDocumentTo

class PleaseTransmitThisDocumentToFaxPhoneNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseTransmitThisDocumentToFaxPhoneNumber

class PleaseTransmitThisDocumentToName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseTransmitThisDocumentToName

class PleaseTransmitThisDocumentToOffice(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseTransmitThisDocumentToOffice

class Pm6(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Pm6

class Pm6Base(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Pm6Base

class Pm6Scores(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Pm6Scores

class Pm6Score(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Pm6Score

class Population(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Population

class PopulationComposition(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PopulationComposition

class PopulationCompositionBlack(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PopulationCompositionBlack

class PopulationCompositionHispanic(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PopulationCompositionHispanic

class PopulationCompositionOther(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PopulationCompositionOther

class PopulationCompositionTotal(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PopulationCompositionTotal

class PopulationCompositionWhite(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PopulationCompositionWhite

class PosterDesign(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PosterDesign

class PostiveControlUgPlate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PostiveControlUgPlate

class PpsProgram(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PpsProgram

class PreSell(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreSell

class PredominantBuydownValueOfTargetedBrandsDoralGPCBasic(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PredominantBuydownValueOfTargetedBrandsDoralGPCBasic

class Preference(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Preference

class PresentForm(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PresentForm

class PresentStatusOfWorkCiteProgressReportsWhereAppropriate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PresentStatusOfWorkCiteProgressReportsWhereAppropriate

class Present(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Present

class PressQuery(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PressQuery

class PressQueryDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PressQueryDate

class PressQueryDescribeTheStorylineListTheQuestionsAndProposedAnswersAndSummarizeHandlingIncludingClearances(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PressQueryDescribeTheStorylineListTheQuestionsAndProposedAnswersAndSummarizeHandlingIncludingClearances

class PressQueryPublication(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PressQueryPublication

class PressQueryReceivedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PressQueryReceivedBy

class PressQueryReporterEditor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PressQueryReporterEditor

class PressQueryTime(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PressQueryTime

class Pressurized(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Pressurized

class Previous(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Previous

class Price(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Price

class PrimaryClassOfTrade(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PrimaryClassOfTrade

class PrimaryDistributionChannelEGJobberSubJobberMembership(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PrimaryDistributionChannelEGJobberSubJobberMembership

class Priority(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Priority

class PriorityDefer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PriorityDefer

class PriorityHigh(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PriorityHigh

class PriorityImmediate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PriorityImmediate

class PriorityLow(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PriorityLow

class PriorityMedium(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PriorityMedium

class ProblemDefinition(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProblemDefinition

class ProblemDefinitionDescriptionOfRequest(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProblemDefinitionDescriptionOfRequest

class ProblemDefinitionReasonForRequest(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProblemDefinitionReasonForRequest

class ProblemDefinitionRequestAuthorizedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProblemDefinitionRequestAuthorizedBy

class Product(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Product

class ProductCade639(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProductCade639

class ProductCode519(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProductCode519

class ProductCode327(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProductCode327

class ProductCode462(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProductCode462

class ProductCode741(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProductCode741

class ProductCode753(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProductCode753

class ProductCode934(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProductCode934

class ProfitImprovement(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProfitImprovement

class Program(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Program

class Projeci(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Projeci

class Project(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Project

class ProjectCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectCode

class ProjectCoordinator(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectCoordinator

class ProjectDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectDescription

class ProjectLeader(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectLeader

class ProjectName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectName

class ProjectNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectNumber

class ProjectObjective(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectObjective

class ProjectOriginatedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectOriginatedBy

class ProjectSheetNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectSheetNo

class ProjectTitle(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectTitle

class ProjectedCurrentYearExpenses19(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedCurrentYearExpenses19

class ProjectedCurrentYearExpenses19Actual8Months(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedCurrentYearExpenses19Actual8Months

class ProjectedCurrentYearExpenses19Projected4Months(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedCurrentYearExpenses19Projected4Months

class ProjectedCurrentYearExpenses19TotalYear(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedCurrentYearExpenses19TotalYear

class Projected(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Projected

class ProjectedExtAuthDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedExtAuthDate

class ProjectedExtAuthDateWaveS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedExtAuthDateWaveS

class ProjectedFieldComplete(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedFieldComplete

class ProjectedFieldCompleteWaveS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedFieldCompleteWaveS

class ProjectedFinalReportDueSupplierRpt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedFinalReportDueSupplierRpt

class ProjectedFinalReportDueSupplierRptWaveS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedFinalReportDueSupplierRptWaveS

class ProjectedInternalInitDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedInternalInitDate

class Promo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Promo

class PromotionalImpact(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionalImpact

class PromotionalImpact50OffPack(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionalImpact50OffPack

class PromotionalImpact500OffCarton(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionalImpact500OffCarton

class PromotionalImpact20CentsOffPackCouponSticker(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionalImpact20CentsOffPackCouponSticker

class PromotionalImpactSalesForce20S(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionalImpactSalesForce20S

class PromotionalPeriod(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionalPeriod

class ProtectivePrecautionsRequired(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProtectivePrecautionsRequired

class ProvedRecall(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProvedRecall

class ProvedRecallBase(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProvedRecallBase

class ProvedRecallScore(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProvedRecallScore

class Publication(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Publication

class Purchasing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Purchasing

class PackingAndDistribution(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PackingAndDistribution

class PaperAndMaterials(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PaperAndMaterials

class PartOfFinalReportToBeAmendedExactLocation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PartOfFinalReportToBeAmendedExactLocation

class PartOfSalaryReceivedForLobbying(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PartOfSalaryReceivedForLobbying

class Pay(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Pay

class PayMethod(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PayMethod

class PayTerms(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PayTerms

class PayTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PayTo

class Payment(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Payment

class Per(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Per

class Permit(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Permit

class PhoneNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhoneNumber

class PhysicalCharacteristics(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristics

class PhysicalCharacteristicsCigaretteCircumference(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristicsCigaretteCircumference

class PhysicalCharacteristicsFilterPlugLength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristicsFilterPlugLength

class PhysicalCharacteristicsFilterPlugPressureDropEncap(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristicsFilterPlugPressureDropEncap

class PhysicalCharacteristicsFilterPlugPressureDropUnencap(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristicsFilterPlugPressureDropUnencap

class PhysicalCharacteristicsFilterVentilationRate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristicsFilterVentilationRate

class PhysicalCharacteristicsMoistureContentPacking(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristicsMoistureContentPacking

class PhysicalCharacteristicsMoistureContentExCatcher(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristicsMoistureContentExCatcher

class PhysicalCharacteristicsOverallCigaretteLength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristicsOverallCigaretteLength

class PhysicalCharacteristicsPrintPositionFromFilterEnd(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristicsPrintPositionFromFilterEnd

class PhysicalCharacteristicsTippingLength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristicsTippingLength

class PhysicalCharacteristicsTobaccoRodLength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristicsTobaccoRodLength

class PhysicalCharacteristicsTotalPressureDropEncap(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristicsTotalPressureDropEncap

class PhysicalCharacteristicsTotalPressureDropUnencap(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PhysicalCharacteristicsTotalPressureDropUnencap

class PlaceOfManufacture(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PlaceOfManufacture

class PlaintiffSAttorneyS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PlaintiffSAttorneyS

class PlantManagerPostingSupt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PlantManagerPostingSupt

class Plast(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Plast

class PleaseDeliverAsSoonPossibleTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseDeliverAsSoonPossibleTo

class PleaseDeliverAsSoonPossibleToCompany(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseDeliverAsSoonPossibleToCompany

class PleaseDeliverAsSoonPossibleToFax(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseDeliverAsSoonPossibleToFax

class PleaseDeliverAsSoonPossibleToNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseDeliverAsSoonPossibleToNo

class PleaseDeliverAsSoonPossibleToPhoneNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseDeliverAsSoonPossibleToPhoneNo

class PleaseDeliverAsSoonPossibleToRecipient(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseDeliverAsSoonPossibleToRecipient

class PleaseShipTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseShipTo

class PleaseCompleteTheFollowingIfCheckedNoForCorporationAbove(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseCompleteTheFollowingIfCheckedNoForCorporationAbove

class PleaseIndicateTheCapacityInWhichYouAreExecutingThisDocument(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseIndicateTheCapacityInWhichYouAreExecutingThisDocument

class PleaseMakeTheNecessaryFieldTripArrangementsFor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleaseMakeTheNecessaryFieldTripArrangementsFor

class PleasePlaceTheFollowingOrderForKoolAndOrGpcGolfBagsForMySection(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PleasePlaceTheFollowingOrderForKoolAndOrGpcGolfBagsForMySection

class PlugWrap(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PlugWrap

class PlugWrapPor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PlugWrapPor

class Position(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Position

class Positioning(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Positioning

class PreparationAndComposition(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreparationAndComposition

class PreparedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreparedBy

class President(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.President

class PressureDrop(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PressureDrop

class PressureOnAirJet(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PressureOnAirJet

class PrevOrRecommendedSupplier(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PrevOrRecommendedSupplier

class PreviousCommitmentsThisProject(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PreviousCommitmentsThisProject

class PricesAndSchedule(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PricesAndSchedule

class ProcessAndColors(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProcessAndColors

class ProducionProcess(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProducionProcess

class ProductManager(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProductManager

class ProductionSupervisedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProductionSupervisedBy

class Products(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Products

class ProgramBudgetCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProgramBudgetCode

class ProgramGroup(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProgramGroup

class ProiectedExternalAuthorizationDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProiectedExternalAuthorizationDate

class ProjectNameDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectNameDescription

class ProjectNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectNo

class ProjectType(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectType

class ProjectTypeProductTestAUEtc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectTypeProductTestAUEtc

class ProjectedFieldStart(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedFieldStart

class ProjectedFinalReportDue(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedFinalReportDue

class ProjectedInitiationDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProjectedInitiationDate

class PromoDates(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromoDates

class PromotionCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionCode

class PromotionName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionName

class PromotionNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionNumber

class PromotionQuantity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionQuantity

class PromotionQuantityDisplays8(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionQuantityDisplays8

class PromotionQuantityFloor40(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionQuantityFloor40

class PromotionQuantityMugs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionQuantityMugs

class PromotionQuantityPosters(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PromotionQuantityPosters

class ProposalNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ProposalNo

class PumpPressCardRoller(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PumpPressCardRoller

class Purpose(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Purpose

class PurposeOfSample(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PurposeOfSample

class PurposeOfTrip(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PurposeOfTrip

class PurposeCompanyImprovementsAdministrativeRequirements(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PurposeCompanyImprovementsAdministrativeRequirements

class PurposeComplianceWithOutsideRequirements(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PurposeComplianceWithOutsideRequirements

class PurposeCostReduction(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PurposeCostReduction

class PurposeExpansionOfExistingBusiness(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PurposeExpansionOfExistingBusiness

class PurposeMaintenanceOfExistingBusiness(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PurposeMaintenanceOfExistingBusiness

class PurposeNewProducts(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PurposeNewProducts

class PurposeQualityImprovement(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PurposeQualityImprovement

class QipLog1(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QipLog1

class Qned(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Qned

class QualityAssuranceAssoc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QualityAssuranceAssoc

class Quantities(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Quantities

class Quantity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Quantity

class QuantityRequired(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QuantityRequired

class Qty(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Qty

class QualitativeResearchProductTestAUEtc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QualitativeResearchProductTestAUEtc

class QualitativeResearchProductTestAUEtcRecommendedSupplier(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QualitativeResearchProductTestAUEtcRecommendedSupplier

class QualityControl(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QualityControl

class QualityOfBloom(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QualityOfBloom

class QualityOfHospitalityTent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QualityOfHospitalityTent

class QualityOfHospitalityTentCleanliness(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QualityOfHospitalityTentCleanliness

class QualityOfHospitalityTentFood(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QualityOfHospitalityTentFood

class QualityOfHospitalityTentService(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QualityOfHospitalityTentService

class QuanOfTraysProduced(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QuanOfTraysProduced

class QuantitiesAndDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QuantitiesAndDescription

class QuantityReceived(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QuantityReceived

class QuantityCartonsOf200Each(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QuantityCartonsOf200Each

class QuotationTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.QuotationTo

class RDComments(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RDComments

class RDGroup(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RDGroup

class Radioactive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Radioactive

class RdEProcess(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RdEProcess

class RdEProduct(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RdEProduct

class Re(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Re

class Reactivity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reactivity

class Reactivity1WaterOrBrine(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reactivity1WaterOrBrine

class Reactivity25Hcl(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reactivity25Hcl

class Reactivity35Naoh(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reactivity35Naoh

class Reactivity4Alcohols(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reactivity4Alcohols

class Reactivity5Oxygen(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reactivity5Oxygen

class Reactivity6Light(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reactivity6Light

class ReasonCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReasonCode

class ReasonCode1ProductivityImprovement(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReasonCode1ProductivityImprovement

class ReasonCode2ReturnOnInvestment(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReasonCode2ReturnOnInvestment

class ReasonCode3CustomerImpact(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReasonCode3CustomerImpact

class ReasonCode4GovernmentRequirement(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReasonCode4GovernmentRequirement

class ReasonCode5BusinessChange(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReasonCode5BusinessChange

class ReasonCode6SystemError(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReasonCode6SystemError

class ReasonCode7ProceduralError(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReasonCode7ProceduralError

class Recasing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Recasing

class ReceiptDateS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReceiptDateS

class Received(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Received

class ReceivedAndForwardedOn(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReceivedAndForwardedOn

class Recommendation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Recommendation

class ReducedToMaterial(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReducedToMaterial

class Reference(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reference

class ReferenceForCalculation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferenceForCalculation

class Region(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Region

class RegionFull(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RegionFull

class RegionPartial(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RegionPartial

class RegistryNumberIfApplicable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RegistryNumberIfApplicable

class RegulatoryAffairs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RegulatoryAffairs

class RegulatoryStatus(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RegulatoryStatus

class Rejected(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Rejected

class ReleasedToAcctg(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReleasedToAcctg

class Remarks(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Remarks

class RemarksTheseCostsWillIncludeButAreNotExclusiveToTheTheFollowingMaterials(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RemarksTheseCostsWillIncludeButAreNotExclusiveToTheTheFollowingMaterials

class RemarksToCoverTheCostOfCollateralMerchandisingMaterialsToBeUsedIn1991InConnectionWithTheMerchandisingAndPromotionOfBullDurham(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RemarksToCoverTheCostOfCollateralMerchandisingMaterialsToBeUsedIn1991InConnectionWithTheMerchandisingAndPromotionOfBullDurham

class ReportableExpenditures(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures

class ReportableExpendituresInThousands(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousands

class ReportableExpendituresInThousandsCatExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsCatExpenses

class ReportableExpendituresInThousandsCatCExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsCatCExpenses

class ReportableExpendituresInThousandsCatDExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsCatDExpenses

class ReportableExpendituresInThousandsCatFExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsCatFExpenses

class ReportableExpendituresInThousandsCatGExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsCatGExpenses

class ReportableExpendituresInThousandsCatJExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsCatJExpenses

class ReportableExpendituresInThousandsCatKExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsCatKExpenses

class ReportableExpendituresInThousandsCatLExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsCatLExpenses

class ReportableExpendituresInThousandsCatMExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsCatMExpenses

class ReportableExpendituresInThousandsCatEExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsCatEExpenses

class ReportableExpendituresInThousandsCatHExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsCatHExpenses

class ReportableExpendituresInThousandsCatIExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsCatIExpenses

class ReportableExpendituresInThousandsCatAExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsCatAExpenses

class ReportableExpendituresInThousandsTotalReportableExpendituresForVarietyi(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpendituresInThousandsTotalReportableExpendituresForVarietyi

class ReportableExpenditures13CatAExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures13CatAExpenses

class ReportableExpenditures14CatBExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures14CatBExpenses

class ReportableExpenditures15CatCExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures15CatCExpenses

class ReportableExpenditures16CatDExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures16CatDExpenses

class ReportableExpenditures17CatEExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures17CatEExpenses

class ReportableExpenditures18CatFExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures18CatFExpenses

class ReportableExpenditures19CatGExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures19CatGExpenses

class ReportableExpenditures20CatHExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures20CatHExpenses

class ReportableExpenditures21CatIExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures21CatIExpenses

class ReportableExpenditures22CatJExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures22CatJExpenses

class ReportableExpenditures23CatKExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures23CatKExpenses

class ReportableExpenditures24CatLExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures24CatLExpenses

class ReportableExpenditures25CatMExpenses(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures25CatMExpenses

class ReportableExpenditures26TotalReportableExpendituresForVariety(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportableExpenditures26TotalReportableExpendituresForVariety

class Reported(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reported

class RequestAuthorizedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequestAuthorizedBy

class RequestNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequestNo

class RequestType(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequestType

class RequestType1Enhancement(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequestType1Enhancement

class RequestType2Maintenance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequestType2Maintenance

class RequestType3SpecialProcessing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequestType3SpecialProcessing

class RequestType4AdHoc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequestType4AdHoc

class RequestType5Emergency(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequestType5Emergency

class RequestedImplementationDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequestedImplementationDate

class RequirementsMp(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequirementsMp

class RequisitionNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequisitionNo

class Requisitioner(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Requisitioner

class RespondHere(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RespondHere

class ResultsNoDeadNoTested(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResultsNoDeadNoTested

class ResultsNoTested(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResultsNoTested

class RetailCallFrequency(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RetailCallFrequency

class ReversionRateTestReversantsControlRevertantsPerPlate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReversionRateTestReversantsControlRevertantsPerPlate

class ReversionRateTestRevertantsControlRevertantsPerPlate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReversionRateTestRevertantsControlRevertantsPerPlate

class ReviewCompleted(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReviewCompleted

class ReviewRouting(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReviewRouting

class Reviewed(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reviewed

class RevisedContractTotals(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RevisedContractTotals

class RevisedTargetDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RevisedTargetDate

class Revision(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Revision

class Revisions(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Revisions

class RevisionsApproved(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RevisionsApproved

class RevisionsToShellOtherThanTermCompensationOrJob(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RevisionsToShellOtherThanTermCompensationOrJob

class RincipalOrganizerWhoWillReceiveCorrespondence(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RincipalOrganizerWhoWillReceiveCorrespondence

class RoomTemperature(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RoomTemperature

class RouteOfCompoundAdministration(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RouteOfCompoundAdministration

class RaceDayInfo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RaceDayInfo

class RaceDayInfoEventAttendance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RaceDayInfoEventAttendance

class RaceDayInfoHospitalityTentAttendance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RaceDayInfoHospitalityTentAttendance

class ReasonSForRecommendation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReasonSForRecommendation

class ReasonForTheAmendment(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReasonForTheAmendment

class Reason(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reason

class Reasons(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reasons

class RecD(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RecD

class RecearchEngineer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RecearchEngineer

class ReceivedByRegulatoryAffatrs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReceivedByRegulatoryAffatrs

class RecentActionsRegardingAboveSolicitor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RecentActionsRegardingAboveSolicitor

class RecommemdedSupplier(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RecommemdedSupplier

class RecommendedBrandSAndPromotionalActivity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RecommendedBrandSAndPromotionalActivity

class RecommendedSupplier(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RecommendedSupplier

class Ref(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ref

class RefPaper(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RefPaper

class ReferentBrand(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferentBrand

class ReferentBrandS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReferentBrandS

class RegistrationNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RegistrationNo

class RegistryOfTheToxicEffectsOfChemicals(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RegistryOfTheToxicEffectsOfChemicals

class ReimbursementsForExpensesPleaseItemize(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReimbursementsForExpensesPleaseItemize

class RelationshipToFinalist(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RelationshipToFinalist

class Replaces(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Replaces

class Report(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Report

class ReportedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportedBy

class ReportingPeriod(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportingPeriod

class ReportingSchedule(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportingSchedule

class Reports(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Reports

class ReportsCopiesTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportsCopiesTo

class ReportsOriginalTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportsOriginalTo

class ReportsWrittenBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReportsWrittenBy

class Requested(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Requested

class RequestedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequestedBy

class Requirements(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Requirements

class RequirementsLaboratory(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequirementsLaboratory

class RequirementsOthers(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequirementsOthers

class RequirementsOther(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RequirementsOther

class Res(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Res

class ResearchDesign(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResearchDesign

class ResearchDesignNCellsElegibilityDesignKeyBannerBreaksMethodologyCities(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResearchDesignNCellsElegibilityDesignKeyBannerBreaksMethodologyCities

class ResearchFirm(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResearchFirm

class ResearchLiaison(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResearchLiaison

class ResearchLimitations(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResearchLimitations

class ResearchReqAttached(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResearchReqAttached

class ResearchReqAttachedNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResearchReqAttachedNo

class ResearchReqAttachedYes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResearchReqAttachedYes

class ResearchRequestAttached(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResearchRequestAttached

class ResearchRequestAttachedNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResearchRequestAttachedNo

class ResearchRequestAttachedYes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResearchRequestAttachedYes

class ReservationsMadeAt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReservationsMadeAt

class RespondentIncidence(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RespondentIncidence

class ResponderDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResponderDate

class ResponseCodeAssigned(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResponseCodeAssigned

class Responsibility(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Responsibility

class ResponsibilityFilterProduction(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResponsibilityFilterProduction

class ResponsibilityMakingPacking(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResponsibilityMakingPacking

class ResponsibilityShipping(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResponsibilityShipping

class ResponsibilityTobaccoBlend(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResponsibilityTobaccoBlend

class ResponsibilitySampleRequisitionForm020206(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResponsibilitySampleRequisitionForm020206

class ResponsibilitySampleRequistion(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ResponsibilitySampleRequistion

class Retainer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Retainer

class ReturnTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReturnTo

class ReturnThisFormTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ReturnThisFormTo

class RevisedBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RevisedBudget

class RevisedCostsIfAny(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RevisedCostsIfAny

class RevisedFrom(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RevisedFrom

class RevisionDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RevisionDate

class Rod(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Rod

class RodsPerMin(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.RodsPerMin

class Room(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Room

class STyphimurium(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.STyphimurium

class SPV(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SPV

class Sales(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Sales

class SalesObjective(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SalesObjective

class SampleWeight(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SampleWeight

class Sample(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Sample

class SamplesItemsRequired(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SamplesItemsRequired

class SamplingDates(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SamplingDates

class SamplingHours(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SamplingHours

class Satisfying7More(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Satisfying7More

class Schedule(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Schedule

class ScheduleDateOrInventoryDepletion(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ScheduleDateOrInventoryDepletion

class ScheduledPostingDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ScheduledPostingDate

class ScientificJournalOfChoice(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ScientificJournalOfChoice

class ScientificMetingOfChoice(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ScientificMetingOfChoice

class Scope(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Scope

class ScopeArea(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ScopeArea

class ScopeDivision(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ScopeDivision

class ScopeOther(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ScopeOther

class ScopeRegion(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ScopeRegion

class SecondaryClassOfTrade(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SecondaryClassOfTrade

class SectionOne(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SectionOne

class SectionTwo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SectionTwo

class SectionS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SectionS

class SectionsRevised(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SectionsRevised

class Sensitive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Sensitive

class Sex(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Sex

class SexFemale(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SexFemale

class SexMale(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SexMale

class ShipTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ShipTo

class ShipToDeptBranch(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ShipToDeptBranch

class ShipToCustomerShippingNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ShipToCustomerShippingNumber

class ShipmentToArriveNotLaterThan(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ShipmentToArriveNotLaterThan

class Shipment(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Shipment

class ShippedTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ShippedTo

class ShippedVia(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ShippedVia

class ShouldPromotionBeRepeated(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ShouldPromotionBeRepeated

class ShouldPromotionBeRepeatedNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ShouldPromotionBeRepeatedNo

class ShouldPromotionBeRepeatedYes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ShouldPromotionBeRepeatedYes

class Signature(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Signature

class SignatureS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SignatureS

class Signatures(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Signatures

class SignaturesGroupProductDirector(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SignaturesGroupProductDirector

class SignaturesMerchandisingManager(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SignaturesMerchandisingManager

class SignaturesPurchasingDepartment(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SignaturesPurchasingDepartment

class SignaturesRequestingManager(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SignaturesRequestingManager

class SignaturesReturnTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SignaturesReturnTo

class SizeOrSizes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SizeOrSizes

class SizeShowing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SizeShowing

class Smoker(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Smoker

class Smoothness75Moother(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Smoothness75Moother

class Solubility(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Solubility

class Solvent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Solvent

class Source(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Source

class SourceOfBusiness(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SourceOfBusiness

class SourceOfBusinessMajorCompetitiveBrands(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SourceOfBusinessMajorCompetitiveBrands

class SourceOfBusinessTargetAudience(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SourceOfBusinessTargetAudience

class SourceOfInformation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SourceOfInformation

class Space(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Space

class SpaceColor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpaceColor

class SpaceColorMagazines(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpaceColorMagazines

class SpaceColorNewspapers(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpaceColorNewspapers

class SpecialEventRequestForm(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpecialEventRequestForm

class SpecialEventRequestFormDateOfEvent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpecialEventRequestFormDateOfEvent

class SpecialEventRequestFormNameOfEvent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpecialEventRequestFormNameOfEvent

class SpecialEventRequestFormSamplesItemsRequired(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpecialEventRequestFormSamplesItemsRequired

class SpecialInstructionsWhileDosing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpecialInstructionsWhileDosing

class SpecialSampleManufacture(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpecialSampleManufacture

class SpecificationChangeNumber8479(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpecificationChangeNumber8479

class Specifics(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Specifics

class SpotCheck(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpotCheck

class Sprouge(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Sprouge

class SqInchesFeet(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SqInchesFeet

class Sqc21(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Sqc21

class Ss(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ss

class StateTaxStatus(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StateTaxStatus

class Stationary(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Stationary

class Stations(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Stations

class StorageConditions(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StorageConditions

class StorageRecommendations(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StorageRecommendations

class StoreInDark(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StoreInDark

class StoresParticipating(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StoresParticipating

class StrainOfMice(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StrainOfMice

class Strength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Strength

class Strength7Stronger(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Strength7Stronger

class Structure(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Structure

class StudyDirector(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StudyDirector

class StudyTitleProposalNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StudyTitleProposalNumber

class SubjectToTheFollowingSuggestedRevisionsItemizeBelow(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubjectToTheFollowingSuggestedRevisionsItemizeBelow

class Subject(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Subject

class SubmissionDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDate

class SubmissionDateDec26(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateDec26

class SubmissionDateJan23(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateJan23

class SubmissionDateJan231995(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateJan231995

class SubmissionDateOct3(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateOct3

class SubmissionDateOct31(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateOct31

class SubmissionDateAug10(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateAug10

class SubmissionDateAug26(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateAug26

class SubmissionDateDec8(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateDec8

class SubmissionDateFeb23(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateFeb23

class SubmissionDateJan19(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateJan19

class SubmissionDateJun24(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateJun24

class SubmissionDateJune29(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateJune29

class SubmissionDateMay27(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateMay27

class SubmissionDateNov9(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateNov9

class SubmissionDateOct07(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateOct07

class SubmissionDateSept21(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmissionDateSept21

class SubmittedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmittedBy

class SubmitterSSs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SubmitterSSs

class SuggestionDescribeCurrentSituationAndIdea(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SuggestionDescribeCurrentSituationAndIdea

class Summary(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Summary

class SupervisorInformation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SupervisorInformation

class SupervisorInformationBeeperNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SupervisorInformationBeeperNumber

class SupervisorInformationNameOfAllwaysSupervisor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SupervisorInformationNameOfAllwaysSupervisor

class SupervisorInformationPhoneNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SupervisorInformationPhoneNumber

class SuppliedUntil(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SuppliedUntil

class Supplier(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Supplier

class SuppliersBeingConsidered(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SuppliersBeingConsidered

class SalesAnalysis(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SalesAnalysis

class SalesPersonnelToBeContacted(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SalesPersonnelToBeContacted

class SalesPersonnelToBeWorkedWith(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SalesPersonnelToBeWorkedWith

class SalesRepresentative(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SalesRepresentative

class SampleDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SampleDescription

class SampleDisposition(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SampleDisposition

class SampleNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SampleNo

class SampleSize(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SampleSize

class SampleSpecificationsWrittenBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SampleSpecificationsWrittenBy

class ScreenerQuestionnaire(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ScreenerQuestionnaire

class ScriptSAndOrStoryBoardSCleared(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ScriptSAndOrStoryBoardSCleared

class ScriptSAndOrStoryBoardSClearedEcu(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ScriptSAndOrStoryBoardSClearedEcu

class ScriptSAndOrStoryBoardSClearedPhoneBooth(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ScriptSAndOrStoryBoardSClearedPhoneBooth

class SectionA(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SectionA

class SectionB(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SectionB

class SectionIiiA2NdParagraphTheFirstSentenceIsToBeChangedToReadAsFollows(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SectionIiiA2NdParagraphTheFirstSentenceIsToBeChangedToReadAsFollows

class SectionNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SectionNumber

class SectionSalesManagerSName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SectionSalesManagerSName

class Seeds(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Seeds

class SeniorVpMarketingTo1000000(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SeniorVpMarketingTo1000000

class Sep(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Sep

class SeparatePay(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SeparatePay

class Served(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Served

class SignPrintNamesSeeInstructionsOnBack(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SignPrintNamesSeeInstructionsOnBack

class SignatureEmployerOrDesignee(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SignatureEmployerOrDesignee

class SignatureOfHetailPurchaser(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SignatureOfHetailPurchaser

class SignatureOfInitiator(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SignatureOfInitiator

class Signed(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Signed

class SignificantDifference(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SignificantDifference

class Size(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Size

class Sizes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Sizes

class SmokingResults(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SmokingResults

class SolidsComposit(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SolidsComposit

class SourceOfBusinessLocalPremiumKsSmokers(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SourceOfBusinessLocalPremiumKsSmokers

class SourceOfBusinessThis(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SourceOfBusinessThis

class SpecialInstructionsComments(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpecialInstructionsComments

class SpecialRequirements(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpecialRequirements

class Species(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Species

class SpentPriorTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SpentPriorTo

class StandardGradeMark(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StandardGradeMark

class Start(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Start

class StartPleteFr(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StartPleteFr

class State(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.State

class StateOf(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StateOf

class StateCreateNewAppropriation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StateCreateNewAppropriation

class StateDecreaseExistingAppropriation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StateDecreaseExistingAppropriation

class StateDecreaseExistingRevenues(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StateDecreaseExistingRevenues

class StateIncreaseExistingAppropriation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StateIncreaseExistingAppropriation

class StateIncreaseExistingRevenues(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StateIncreaseExistingRevenues

class StateNoStateFiscalEffect(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StateNoStateFiscalEffect

class StaticCompleteCigar(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StaticCompleteCigar

class Status(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Status

class Status1993(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Status1993

class StatusApproved(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StatusApproved

class StatusProposed(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StatusProposed

class Street(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Street

class Streptozotocin(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Streptozotocin

class Strokes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Strokes

class StudyName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StudyName

class StudyNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StudyNumber

class StudyTitle(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.StudyTitle

class Style(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Style

class Submission(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Submission

class SuggestedSolutionsS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SuggestedSolutionsS

class Suggestion(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Suggestion

class SuggestionsRecommendations(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SuggestionsRecommendations

class SumaryOfImrdBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SumaryOfImrdBudget

class SumaryOfImrdBudgetCommittedToDateCurrentYear(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SumaryOfImrdBudgetCommittedToDateCurrentYear

class SumaryOfImrdBudgetCurrentBalAvailable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SumaryOfImrdBudgetCurrentBalAvailable

class SumaryOfImrdBudgetNewBalance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SumaryOfImrdBudgetNewBalance

class SumaryOfImrdBudgetThisAmountFromNextYearSBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SumaryOfImrdBudgetThisAmountFromNextYearSBudget

class SumaryOfImrdBudgetThisChangeFromCurrentBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SumaryOfImrdBudgetThisChangeFromCurrentBudget

class SumaryOfImrdBudgetTotalAreaBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SumaryOfImrdBudgetTotalAreaBudget

class SummaryOfMrdBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SummaryOfMrdBudget

class SummaryOfMrdBudgetCommitedToDateCurrentYear(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SummaryOfMrdBudgetCommitedToDateCurrentYear

class SummaryOfMrdBudgetCurrentBalAvailable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SummaryOfMrdBudgetCurrentBalAvailable

class SummaryOfMrdBudgetNewBalance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SummaryOfMrdBudgetNewBalance

class SummaryOfMrdBudgetThisAmount(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SummaryOfMrdBudgetThisAmount

class SummaryOfMrdBudgetThisChangeFromCurrentBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SummaryOfMrdBudgetThisChangeFromCurrentBudget

class SummaryOfMrdBudgetTotalAreaBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SummaryOfMrdBudgetTotalAreaBudget

class SummaryOfResearchBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SummaryOfResearchBudget

class SummaryOfResearchBudgetCurrentBalAvailable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SummaryOfResearchBudgetCurrentBalAvailable

class SummaryOfResearchBudgetCurrentBalanceAvailable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SummaryOfResearchBudgetCurrentBalanceAvailable

class SummaryOfResearchBudgetThisAmount(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SummaryOfResearchBudgetThisAmount

class SummaryOfResearchBudgetThisChangeFromCurrentBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SummaryOfResearchBudgetThisChangeFromCurrentBudget

class SummaryOfResearchBudgetTotalAreaBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SummaryOfResearchBudgetTotalAreaBudget

class SupervisorManager(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SupervisorManager

class SupplierRabidResearch(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SupplierRabidResearch

class Suppression(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Suppression

class SwornToAndSubscribedBeforeMeThis(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.SwornToAndSubscribedBeforeMeThis

class System(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.System

class T(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.T

class TCodesNa(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TCodesNa

class TN(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TN

class Ta100(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ta100

class Ta10059(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ta10059

class Ta1535(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ta1535

class Ta153559(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ta153559

class Ta15359(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ta15359

class Ta98(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ta98

class Ta9859(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Ta9859

class Tar(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Tar

class Target(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Target

class TargetDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TargetDate

class TelNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TelNo

class Tel(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Tel

class TelecopierTransmittalCoverSheet(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TelecopierTransmittalCoverSheet

class TelecopierTransmittalCoverSheetDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TelecopierTransmittalCoverSheetDate

class TelecopierTransmittalCoverSheetFrom(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TelecopierTransmittalCoverSheetFrom

class TelecopierTransmittalCoverSheetPages(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TelecopierTransmittalCoverSheetPages

class TelecopierTransmittalCoverSheetRe(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TelecopierTransmittalCoverSheetRe

class TelecopierTransmittalCoverSheetTo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TelecopierTransmittalCoverSheetTo

class TelefaxMessageNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TelefaxMessageNo

class Telex(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Telex

class TennisTournament(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TennisTournament

class Terms(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Terms

class TermsFOB(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TermsFOB

class TermsNet(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TermsNet

class TermsVia(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TermsVia

class TestDates(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TestDates

class TestMaterialS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TestMaterialS

class Tested(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Tested

class TextOver500PrizesToBeAwarded(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TextOver500PrizesToBeAwarded

class TheFollowingInformationMustBeFurnished(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TheFollowingInformationMustBeFurnished

class TheFollowingInformationMustBeFurnishedDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TheFollowingInformationMustBeFurnishedDate

class TheFollowingInformationMustBeFurnishedSignature(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TheFollowingInformationMustBeFurnishedSignature

class TheFollowingInformationMustBeFurnished1FullName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TheFollowingInformationMustBeFurnished1FullName

class TheFollowingInformationMustBeFurnished2ResidenceAddress(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TheFollowingInformationMustBeFurnished2ResidenceAddress

class TheFollowingInformationMustBeFurnished3BusinessAddress(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TheFollowingInformationMustBeFurnished3BusinessAddress

class TheFollowingInformationMustBeFurnished4Occupation(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TheFollowingInformationMustBeFurnished4Occupation

class This(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.This

class ThisAmount(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ThisAmount

class ThisChangeFromCurrentBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ThisChangeFromCurrentBudget

class ThisDocumentIsFrom(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ThisDocumentIsFrom

class ThisDocumentIsFromComments(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ThisDocumentIsFromComments

class ThisDocumentIsFromFaxPhoneNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ThisDocumentIsFromFaxPhoneNumber

class ThisDocumentIsFromFaxTelephoneNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ThisDocumentIsFromFaxTelephoneNumber

class ThisDocumentIsFromName(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ThisDocumentIsFromName

class ThisDocumentIsFromOffice(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ThisDocumentIsFromOffice

class Time(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Time

class Timetable(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Timetable

class TimetableInMarketArrivalDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimetableInMarketArrivalDate

class TimetableLaunchDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimetableLaunchDate

class TimetableManufacturing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimetableManufacturing

class TimetableProductSpecsDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimetableProductSpecsDate

class TimetableShipping(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimetableShipping

class TimetableStartManufactureDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TimetableStartManufactureDate

class To(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.To

class TotalOfIndependentNewport1ClubOutlets(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalOfIndependentNewport1ClubOutlets

class TotalOfIndependentSpecialEmphasisOutlets(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalOfIndependentSpecialEmphasisOutlets

class TotalOfNumberOneClubOutletsWithDistribution(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalOfNumberOneClubOutletsWithDistribution

class TotalOfSpEmphasisOutleisWithDistribution(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalOfSpEmphasisOutleisWithDistribution

class TotalAreaBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalAreaBudget

class TotalBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalBudget

class TotalPages(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalPages

class Total(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Total

class Totals(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Totals

class ToxicitySurvival(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ToxicitySurvival

class ToxicitySurvival100(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ToxicitySurvival100

class ToxicitySurvival50(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ToxicitySurvival50

class ToxicitySurvival80(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ToxicitySurvival80

class Transfer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Transfer

class TrimSize(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TrimSize

class FieldTrue(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldTrue

class TrueCoreAreas(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TrueCoreAreas

class TypeChange(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeChange

class TypeDisplay(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeDisplay

class TypeDisplayCounter(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeDisplayCounter

class TypeDisplayFloor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeDisplayFloor

class TypeDisplayPoster(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeDisplayPoster

class TypeOfProduct(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfProduct

class TypeOfPromotion(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfPromotion

class TypeOfSpecificationChangeCheckAllThatApply(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfSpecificationChangeCheckAllThatApply

class TypeOfSpecificationChangeCheckAllThatApplyCigaretteDesignPermanent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfSpecificationChangeCheckAllThatApplyCigaretteDesignPermanent

class TypeOfSpecificationChangeCheckAllThatApplyCigaretteDesignTrial(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfSpecificationChangeCheckAllThatApplyCigaretteDesignTrial

class TypeOfSpecificationChangeCheckAllThatApplyDiscontinueProduct(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfSpecificationChangeCheckAllThatApplyDiscontinueProduct

class TypeOfSpecificationChangeCheckAllThatApplyEquivalentAdditive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfSpecificationChangeCheckAllThatApplyEquivalentAdditive

class TypeOfSpecificationChangeCheckAllThatApplyEquivalentFilterPaperTipping(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfSpecificationChangeCheckAllThatApplyEquivalentFilterPaperTipping

class TypeOfSpecificationChangeCheckAllThatApplyEquivalentPackagingMaterial(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfSpecificationChangeCheckAllThatApplyEquivalentPackagingMaterial

class TypeOfSpecificationChangeCheckAllThatApplyNewProduct(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfSpecificationChangeCheckAllThatApplyNewProduct

class TypeOfSpecificationChangeCheckAllThatApplyPackagingPermanent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfSpecificationChangeCheckAllThatApplyPackagingPermanent

class TypeOfSpecificationChangeCheckAllThatApplyPackagingTemporary(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfSpecificationChangeCheckAllThatApplyPackagingTemporary

class TypeOfSpecificationChangeCheckAllThatApplyProcessing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfSpecificationChangeCheckAllThatApplyProcessing

class TypeOfSpecificationChangeCheckAllThatApplyTarAdjustment1Mg(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfSpecificationChangeCheckAllThatApplyTarAdjustment1Mg

class TypeBiological(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeBiological

class TypeChemical(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeChemical

class TypeCombined(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeCombined

class TapeSpeed(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TapeSpeed

class TarNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TarNumber

class Tars(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Tars

class TaxStatusPaidOrFree(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TaxStatusPaidOrFree

class Technician(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Technician

class Telefax(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Telefax

class Telephone(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Telephone

class TestArticle(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TestArticle

class TestPeriod(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TestPeriod

class Tester(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Tester

class TheFollowingDocumentIncludingCoverPageIs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TheFollowingDocumentIncludingCoverPageIs

class ThisAmountFromNextYearSBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ThisAmountFromNextYearSBudget

class ThisChange(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ThisChange

class ThisProjectIs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ThisProjectIs

class ThisFormWasPlacedBeforeBatesId(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ThisFormWasPlacedBeforeBatesId

class TippingPaper(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TippingPaper

class TippingPaperBobbinWidth(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TippingPaperBobbinWidth

class TippingPaperColor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TippingPaperColor

class TippingPaperDobbinLength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TippingPaperDobbinLength

class TippingPaperPerforationTypeNoOfLines(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TippingPaperPerforationTypeNoOfLines

class TippingPaperPerforationTypeAndNoOfLines(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TippingPaperPerforationTypeAndNoOfLines

class TippingPaperPorosity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TippingPaperPorosity

class TippingPaperPrintDescription(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TippingPaperPrintDescription

class TippingPaperRobbinLength(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TippingPaperRobbinLength

class TippingPaperSupplierCodeNoS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TippingPaperSupplierCodeNoS

class TippingPaperSupplierS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TippingPaperSupplierS

class TippingPaperSubstance(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TippingPaperSubstance

class TippingAndTippingApplication(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TippingAndTippingApplication

class Title(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Title

class TitleOfAction(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TitleOfAction

class ToBeDeductedFrom1998Budget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ToBeDeductedFrom1998Budget

class ToBeDeductedFrom1999Budget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ToBeDeductedFrom1999Budget

class ToSampleStock(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ToSampleStock

class ToSampleStockMR(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ToSampleStockMR

class ToSampleStockRD(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ToSampleStockRD

class ToNicotineMgCigt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ToNicotineMgCigt

class ToTarMgCigt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ToTarMgCigt

class TobaccoNumber(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TobaccoNumber

class TobaccoUsed(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TobaccoUsed

class TodaySDate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TodaySDate

class Topic(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Topic

class Total205(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Total205

class TotalAreaAuthorized(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalAreaAuthorized

class TotalAuthorizedProjectAmount(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalAuthorizedProjectAmount

class TotalContractCost(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalContractCost

class TotalCost(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalCost

class TotalDenierAsMarked(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalDenierAsMarked

class TotalDenierAsTested(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalDenierAsTested

class TotalSample(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalSample

class TotalSolids(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalSolids

class TotalVOCS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalVOCS

class TotalNumberOfPagesIncludingThisPage(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalNumberOfPagesIncludingThisPage

class TotalBright(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalBright

class TotalKl(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TotalKl

class Toxline(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Toxline

class TradeRegister(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TradeRegister

class TuesdayYN(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TuesdayYN

class Type(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Type

class TypeOfAd(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfAd

class TypeOfCigarette(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfCigarette

class TypeOfEvent(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfEvent

class TypeOfMaker(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfMaker

class TypeOfRod(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfRod

class TypeOfTipper(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfTipper

class TypeOfProductSizeSListPrice(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TypeOfProductSizeSListPrice

class TPic(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TPic

class Unit(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Unit

class UnitPrice(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.UnitPrice

class Units(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Units

class UpcNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.UpcNo

class Use(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Use

class Under35(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Under35

class Under3535Over(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Under3535Over

class Up(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Up

class Vendor(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Vendor

class Via(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Via

class ViaCertifiedMail(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ViaCertifiedMail

class ViaCertifiedAirMail(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ViaCertifiedAirMail

class Viceroy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Viceroy

class Volume(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Volume

class VsCurrentYearIncrDecr(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.VsCurrentYearIncrDecr

class Verification(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Verification

class VickiClark(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.VickiClark

class VoucherApproval(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.VoucherApproval

class Warning(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Warning

class WereQuantitiesAppropriate(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WereQuantitiesAppropriate

class WereQuantitiesAppropriateNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WereQuantitiesAppropriateNo

class WereQuantitiesAppropriateYes(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WereQuantitiesAppropriateYes

class WinstonSalem(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WinstonSalem

class WorkRequestedBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WorkRequestedBy

class Writer(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Writer

class WaterTreatment(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WaterTreatment

class Wave(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Wave

class WaveS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WaveS

class WavesS(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WavesS

class WeHerebyCertifyChargesShownAboveOnDatesPerAttachedBillAreTrueAndCorrectAsBilledToTheAccountInUpperRightHandCornerOfTheAffidavitAndAreExclusive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WeHerebyCertifyChargesShownAboveOnDatesPerAttachedBillAreTrueAndCorrectAsBilledToTheAccountInUpperRightHandCornerOfTheAffidavitAndAreExclusive

class WeekOf(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WeekOf

class Weight(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Weight

class Weights(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Weights

class WeightsNetNetTobacco(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WeightsNetNetTobacco

class WeightsNetTobRodDensity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WeightsNetTobRodDensity

class WeightsTobaccoRodDensity(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WeightsTobaccoRodDensity

class WeightsTotalCigaretteWeight(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WeightsTotalCigaretteWeight

class WeightsTotalCigtWt(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WeightsTotalCigtWt

class WetWeight(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WetWeight

class WidthOfBand(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WidthOfBand

class WithinAgencySBudget(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WithinAgencySBudget

class Wrapping(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Wrapping

class WrappingCartons(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WrappingCartons

class WrappingClosures(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WrappingClosures

class WrappingLabels(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WrappingLabels

class WrappingMarkings(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WrappingMarkings

class WrappingTearTape(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WrappingTearTape

class Wrappings(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Wrappings

class WrappingsCartons(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WrappingsCartons

class WrappingsClosures(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WrappingsClosures

class WrappingsLabels(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WrappingsLabels

class WrappingsMarkings(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WrappingsMarkings

class WrappingsTearTape(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WrappingsTearTape

class WrittenBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WrittenBy

class WtOfCigarettes4Oz(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WtOfCigarettes4Oz

class Yea(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Yea

class Year(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Year

class YearFive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.YearFive

class YearFour(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.YearFour

class YearOne(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.YearOne

class YearThree(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.YearThree

class Yr(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Yr

class Zip(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Zip

class ZipCode(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ZipCode

class Advertisements(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Advertisements

class apping(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.apping

class AppingCartons(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AppingCartons

class AppingClosures(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AppingClosures

class AppingLabels(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AppingLabels

class AppingMarkings(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AppingMarkings

class AppingTearRape(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AppingTearRape

class AsFollows(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.AsFollows

class BpMp(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.BpMp

class by(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.by

class Cc(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Cc

class CheckApplicableBoxEs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CheckApplicableBoxEs

class CtionToLitmus(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.CtionToLitmus

class DayOf(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.DayOf

class Dimensions(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Dimensions

class Explain(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.Explain

class GinalRequestMadeBy(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.GinalRequestMadeBy

class LobbyistForLobbyingYesOrNo(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.LobbyistForLobbyingYesOrNo

class MmHg(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.MmHg

class OfTheAbovementionedNewspaperAndThatDisplayAdsForTheAboveAccountWereMadeThroughTheAforesaidNewspaperDuring(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.OfTheAbovementionedNewspaperAndThatDisplayAdsForTheAboveAccountWereMadeThroughTheAforesaidNewspaperDuring

class on(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.on

class pH(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.pH

class PagesLong(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.PagesLong

class resider(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.resider

class TheMonthOf(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.TheMonthOf

class ToBePerformedInAcuteDermalToxicologyBuilding18(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.ToBePerformedInAcuteDermalToxicologyBuilding18

class WeightedAsFollows(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WeightedAsFollows

class WhoBeingDulySwornSaysThatHeSheIs(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.WhoBeingDulySwornSaysThatHeSheIs

class YesPleaseDetailIncludingTheNamesOfThePersonsReceivingAndInWhoseBehalfSuchExpendituresHaveBeenMadeTheAmountDatePlaceAndReasonForTheExpenditure(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.YesPleaseDetailIncludingTheNamesOfThePersonsReceivingAndInWhoseBehalfSuchExpendituresHaveBeenMadeTheAmountDatePlaceAndReasonForTheExpenditure

class FieldCorrected(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCorrected

class FieldDecreaseRevenues(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldDecreaseRevenues

class FieldIncreaseRevenues(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldIncreaseRevenues

class FieldMandatory(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldMandatory

class FieldMembership(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldMembership

class FieldPurchasing(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldPurchasing

class FieldPermissive(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldPermissive

class FieldStationary(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldStationary

class FieldSupplemental(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldSupplemental

class FieldUpdated(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldUpdated

class FieldCombined(FormBaseStringField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return user_profile.features.FieldCombined

class RouteOfCompoundAdministrationP(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.RouteOfCompoundAdministration
            == user_profile_attributes.RouteOfCompoundAdministrationEnum.P.value
        )

class RouteOfCompoundAdministrationPO(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.RouteOfCompoundAdministration
            == user_profile_attributes.RouteOfCompoundAdministrationEnum.PO.value
        )

class RouteOfCompoundAdministrationIP(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.RouteOfCompoundAdministration
            == user_profile_attributes.RouteOfCompoundAdministrationEnum.FieldIP.value
        )

class RouteOfCompoundAdministrationIV(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.RouteOfCompoundAdministration
            == user_profile_attributes.RouteOfCompoundAdministrationEnum.FieldIV.value
        )

class RouteOfCompoundAdministrationInhalation(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.RouteOfCompoundAdministration
            == user_profile_attributes.RouteOfCompoundAdministrationEnum.FieldInhalation.value
        )

class Compound5MethylCelulose(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Compound
            == user_profile_attributes.CompoundEnum.Field5MethylCelulose.value
        )

class CompoundCornOil(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Compound
            == user_profile_attributes.CompoundEnum.FieldCornOil.value
        )

class CompoundOther(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Compound
            == user_profile_attributes.CompoundEnum.FieldOther.value
        )

class CompoundSaline(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Compound
            == user_profile_attributes.CompoundEnum.FieldSaline.value
        )

class StateTaxStatusNotToBeChargedBySupplier(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.StateTaxStatus
            == user_profile_attributes.StateTaxStatusEnum.NotToBeChargedBySupplier.value
        )

class StateTaxStatusToBeCharged(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.StateTaxStatus
            == user_profile_attributes.StateTaxStatusEnum.FieldToBeCharged.value
        )

class SolventDmsc(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Solvent
            == user_profile_attributes.SolventEnum.Dmsc.value
        )

class SolventOmso(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Solvent
            == user_profile_attributes.SolventEnum.Omso.value
        )

class SolventOther(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Solvent
            == user_profile_attributes.SolventEnum.FieldOther.value
        )

class SolventWater(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Solvent
            == user_profile_attributes.SolventEnum.FieldWater.value
        )

class EstimatedCostOfTheStudyWillBeDecreased(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.EstimatedCostOfTheStudyWillBe
            == user_profile_attributes.EstimatedCostOfTheStudyWillBeEnum.decreased.value
        )

class EstimatedCostOfTheStudyWillBeIncreased(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.EstimatedCostOfTheStudyWillBe
            == user_profile_attributes.EstimatedCostOfTheStudyWillBeEnum.increased.value
        )

class EstimatedCostOfTheStudyWillBeNotAffected(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.EstimatedCostOfTheStudyWillBe
            == user_profile_attributes.EstimatedCostOfTheStudyWillBeEnum.NotAffected.value
        )

class StorageConditionsDessicator(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.StorageConditions
            == user_profile_attributes.StorageConditionsEnum.Dessicator.value
        )

class StorageConditionsFreezer(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.StorageConditions
            == user_profile_attributes.StorageConditionsEnum.Freezer.value
        )

class StorageConditionsOther(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.StorageConditions
            == user_profile_attributes.StorageConditionsEnum.Other.value
        )

class StorageConditionsRefrigerator8C(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.StorageConditions
            == user_profile_attributes.StorageConditionsEnum.Refrigerator8C.value
        )

class StorageConditionsRoomTemperature(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.StorageConditions
            == user_profile_attributes.StorageConditionsEnum.RoomTemperature.value
        )

class StorageConditionsSpecialInstructionsWhileDosing(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.StorageConditions
            == user_profile_attributes.StorageConditionsEnum.SpecialInstructionsWhileDosing.value
        )

class StorageConditionsStoreInDark(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.StorageConditions
            == user_profile_attributes.StorageConditionsEnum.StoreInDark.value
        )

class PermanentBulletin(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Permanent
            == user_profile_attributes.PermanentEnum.Bulletin.value
        )

class PermanentRotary(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Permanent
            == user_profile_attributes.PermanentEnum.Rotary.value
        )

class PermanentWall(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Permanent
            == user_profile_attributes.PermanentEnum.Wall.value
        )

class WithinAgencySBudgetYes(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.WithinAgencySBudget
            == user_profile_attributes.WithinAgencySBudgetEnum.Yes.value
        )

class WithinAgencySBudgetDecreaseCosts(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.WithinAgencySBudget
            == user_profile_attributes.WithinAgencySBudgetEnum.FieldDecreaseCosts.value
        )

class WithinAgencySBudgetNo(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.WithinAgencySBudget
            == user_profile_attributes.WithinAgencySBudgetEnum.FieldNo.value
        )

class FundSourceAffectedGpr(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.FundSourceAffected
            == user_profile_attributes.FundSourceAffectedEnum.Gpr.value
        )

class FundSourceAffectedPro(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.FundSourceAffected
            == user_profile_attributes.FundSourceAffectedEnum.Pro.value
        )

class FundSourceAffectedFed(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.FundSourceAffected
            == user_profile_attributes.FundSourceAffectedEnum.FieldFed.value
        )

class FundSourceAffectedPrs(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.FundSourceAffected
            == user_profile_attributes.FundSourceAffectedEnum.FieldPrs.value
        )

class FundSourceAffectedSeg(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.FundSourceAffected
            == user_profile_attributes.FundSourceAffectedEnum.FieldSeg.value
        )

class FundSourceAffectedSegS(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.FundSourceAffected
            == user_profile_attributes.FundSourceAffectedEnum.FieldSegS.value
        )

class TypeChangeOfficial(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.TypeChange
            == user_profile_attributes.TypeChangeEnum.Official.value
        )

class TypeChangeTemporary(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.TypeChange
            == user_profile_attributes.TypeChangeEnum.FieldTemporary.value
        )

class IfAMaterialOrDimensionalChangeAlsoInvolvedNo(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.IfAMaterialOrDimensionalChangeAlsoInvolved
            == user_profile_attributes.IfAMaterialOrDimensionalChangeAlsoInvolvedEnum.No.value
        )

class IfAMaterialOrDimensionalChangeAlsoInvolvedYes(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.IfAMaterialOrDimensionalChangeAlsoInvolved
            == user_profile_attributes.IfAMaterialOrDimensionalChangeAlsoInvolvedEnum.FieldYes.value
        )

class SubmissionDateAug11(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.SubmissionDate
            == user_profile_attributes.SubmissionDateEnum.Aug11.value
        )

class SubmissionDateJun30(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.SubmissionDate
            == user_profile_attributes.SubmissionDateEnum.Jun30.value
        )

class SubmissionDateMay19(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.SubmissionDate
            == user_profile_attributes.SubmissionDateEnum.May19.value
        )

class SubmissionDateSep22(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.SubmissionDate
            == user_profile_attributes.SubmissionDateEnum.Sep22.value
        )

class SubmissionDateFeb17(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.SubmissionDate
            == user_profile_attributes.SubmissionDateEnum.Feb17.value
        )

class SubmissionDateJuly6(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.SubmissionDate
            == user_profile_attributes.SubmissionDateEnum.July6.value
        )

class SubmissionDateMar16(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.SubmissionDate
            == user_profile_attributes.SubmissionDateEnum.Mar16.value
        )

class SubmissionDateMay11(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.SubmissionDate
            == user_profile_attributes.SubmissionDateEnum.May11.value
        )

class SpecificsOfBooth(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Specifics
            == user_profile_attributes.SpecificsEnum.FieldOfBooth.value
        )

class SpecificsOfBoothS(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Specifics
            == user_profile_attributes.SpecificsEnum.FieldOfBoothS.value
        )

class SpecificsPremiumsOnly(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Specifics
            == user_profile_attributes.SpecificsEnum.PremiumsOnly.value
        )

class SpecificsMusicVan(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Specifics
            == user_profile_attributes.SpecificsEnum.FieldMusicVan.value
        )

class SpecificsRacingCar(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Specifics
            == user_profile_attributes.SpecificsEnum.FieldRacingCar.value
        )

class SpecificsSamplingPremiums(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Specifics
            == user_profile_attributes.SpecificsEnum.FieldSamplingPremiums.value
        )

class SpecificsSignage(FormBaseCheckboxField):
    @classmethod
    def get_profile_info(cls, user_profile):
        return (
            user_profile.features.Specifics
            == user_profile_attributes.SpecificsEnum.FieldSignage.value
        )

