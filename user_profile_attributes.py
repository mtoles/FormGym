from enum import Enum

class FormUserAttributeMeta(type):
    registry = {}

    def __new__(cls, name, bases, attrs):
        new_p_attr = super().__new__(cls, name, bases, attrs)
        if name not in ["FormUserAttr"]:
            assert name not in cls.registry, f"User attribute {name} already exists"
            cls.registry[name] = new_p_attr
        return new_p_attr


class FormUserProfile:
    def __init__(self, form_name=None, idx=None):
        class Features:
            pass

        self.features = Features()
        
        # If form_name is provided, use it directly
        if form_name is not None:
            self.form_name = form_name
        # Otherwise, use the index to find the form name
        elif idx is not None and idx < len(self.all_form_names):
            self.form_name = self.all_form_names[idx]
        else:
            # Default to first form if invalid index
            self.form_name = self.all_form_names[0] if self.all_form_names else "unknown"
        
        for name, attr_class in FormUserAttributeMeta.registry.items():
            if hasattr(attr_class, "values") and isinstance(attr_class.values, dict):
                # Get the value for this form, or empty string if not found
                value = attr_class.values.get(self.form_name, "")
                setattr(self.features, name, value)
            else:
                raise AttributeError(f"Class {name} must have a 'values' dictionary.")

    def get_nl_profile(self):
        nl_profile = []
        for name, attr_class in FormUserAttributeMeta.registry.items():
            nl_profile.append(attr_class.nl_desc(getattr(self.features, name)))
        return nl_profile
    
    # Store all form names for reference
    all_form_names = ['0000971160_processed', '0000989556_processed', '0000990274_processed', '0000999294_processed', '0001118259_processed', '0001123541_processed', '0001129658_processed', '0001209043_processed', '0001239897_processed', '0001438955_processed', '0001456787_processed', '0001463282_processed', '0001463448_processed', '0001476912_processed', '0001477983_processed', '0001485288_processed', '00040534_processed', '00070353_processed', '00093726_processed', '0011505151_processed', '0011838621_processed', '0011845203_processed', '0011856542_processed', '0011859695_processed', '0011899960_processed', '0011906503_processed', '0011973451_processed', '0011974919_processed', '0011976929_processed', '0012178355_processed', '0012199830_processed', '0012529284_processed', '0012529295_processed', '0012602424_processed', '0012947358_processed', '0013255595_processed', '00283813_processed', '0030031163_processed', '0030041455_processed', '0060000813_processed', '0060007216_processed', '0060024314_processed', '0060025670_processed', '0060029036_processed', '0060036622_processed', '0060068489_processed', '0060077689_processed', '0060080406_processed', '0060091229_processed', '0060094595_processed', '0060136394_processed', '0060165115_processed', '0060173256_processed', '0060207528_processed', '0060214859_processed', '0060255888_processed', '0060262650_processed', '0060270727_processed', '0060302201_processed', '0060308251_processed', '0060308461_processed', '0071032790_processed', '0071032807_processed', '00836244_processed', '00836816_processed', '00837285_processed', '00838511_00838525_processed', '00851772_1780_processed', '00851879_processed', '00860012_00860014_processed', '00865872_processed', '00866042_processed', '00920222_processed', '00920294_processed', '00922237_processed', '01073843_processed', '01122115_processed', '01150773_01150774_processed', '01191071_1072_processed', '01197604_processed', '01408099_01408101_processed', '11508234_processed', '11875011_processed', '12052385_processed', '12603270_processed', '12825369_processed', '13149651_processed', '660978_processed', '71108371_processed', '71190280_processed', '71202511_processed', '71206427_processed', '71341634_processed', '71366499_processed', '71563825_processed', '71601299_processed', '716552_processed', '80310840a_processed', '80707440_7443_processed', '80718412_8413_processed', '80728670_processed', '81186212_processed', '81310636_processed', '81574683_processed', '81619486_9488_processed', '81619511_9513_processed', '81749056_9057_processed', '82254638_processed', '87533049_processed', '87672097_processed', '87682908_processed', '88057519_processed', '88547278_88547279_processed', '89368010_processed', '89386032_processed', '89817999_8002_processed', '89867723_processed', '91104867_processed', '91161344_91161347_processed', '91315069_91315070_processed', '91355841_processed', '91356315_processed', '91361993_processed', '91372360_processed', '91391286_processed', '91391310_processed', '91581919_processed', '91856041_6049_processed', '91903177_processed', '91914407_processed', '91939637_processed', '91974562_processed', '92039708_9710_processed', '92081358_1359_processed', '92091873_processed', '92094746_processed', '92094751_processed', '92298125_processed', '92314414_processed', '92327794_processed', '92433599_92433601_processed', '92586242_processed', '92657311_7313_processed', '92657391_processed', '93213298_processed', '93329540_processed', '93351929_93351931_processed', '93380187_processed', '93455715_processed']


class FormUserAttr(metaclass=FormUserAttributeMeta):
    pass

class RouteOfCompoundAdministrationEnum(Enum):
    P = "P."
    PO = "P.O."
    FieldIP = "☐ I.P."
    FieldIV = "☐ I.V."
    FieldInhalation = "☐ INHALATION"
    FieldPO = "☐ P. O."

class CompoundEnum(Enum):
    Field5MethylCelulose = ".5 % METHYL CELULOSE"
    FieldCornOil = "☐ CORN OIL"
    FieldOther = "☐ OTHER"
    FieldSaline = "☐ SALINE"

class StateTaxStatusEnum(Enum):
    NotToBeChargedBySupplier = "NOT TO BE CHARGED BY SUPPLIER"
    FieldToBeCharged = "☐ TO BE CHARGED"

class SolventEnum(Enum):
    Dmsc = "DMSC"
    Omso = "OMSO"
    FieldOther = "☐ OTHER"
    FieldWater = "☐ WATER"

class EstimatedCostOfTheStudyWillBeEnum(Enum):
    decreased = "decreased"
    increased = "increased"
    NotAffected = "not affected"

class StorageConditionsEnum(Enum):
    Dessicator = "DESSICATOR"
    Freezer = "FREEZER"
    Other = "OTHER"
    Refrigerator8C = "REFRIGERATOR 8 C"
    RoomTemperature = "ROOM TEMPERATURE"
    SpecialInstructionsWhileDosing = "SPECIAL INSTRUCTIONS WHILE DOSING"
    StoreInDark = "STORE IN DARK"

class PermanentEnum(Enum):
    Bulletin = "BULLETIN ☐"
    Rotary = "ROTARY"
    Wall = "WALL ☐"

class WithinAgencySBudgetEnum(Enum):
    Yes = "Yes"
    FieldDecreaseCosts = "☐ Decrease Costs"
    FieldNo = "☐ No"

class FundSourceAffectedEnum(Enum):
    Gpr = "GPR"
    Pro = "PRO"
    FieldFed = "☐ FED"
    FieldPrs = "☐ PRS"
    FieldSeg = "☐ SEG"
    FieldSegS = "☐ SEG-S"

class TypeChangeEnum(Enum):
    Official = "OFFICIAL"
    FieldTemporary = "☐ TEMPORARY"

class IfAMaterialOrDimensionalChangeAlsoInvolvedEnum(Enum):
    No = "NO"
    FieldYes = "☐ YES"

class SubmissionDateEnum(Enum):
    Aug11 = "AUG 11"
    Jun30 = "JUN 30"
    May19 = "MAY 19"
    Sep22 = "SEP 22"

class SpecificsEnum(Enum):
    FieldOfBooth = "# OF BOOTH"
    FieldOfBoothS = "# OF BOOTH(S)"
    PremiumsOnly = "PREMIUMS ONLY"
    FieldMusicVan = "☐ MUSIC VAN"
    FieldRacingCar = "☐ RACING CAR"
    FieldSamplingPremiums = "☐ SAMPLING & PREMIUMS"
    FieldSignage = "☐ SIGNAGE"

class FieldBanners(FormUserAttr):
    values = {'89867723_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's # Banners: {option}"

class FieldCalls(FormUserAttr):
    values = {'92081358_1359_processed': '0 8 162 76 57 303'}

    @staticmethod
    def nl_desc(option):
        return f"The user's # CALLS: {option}"

class FieldCasesKentGlLtsKS(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's # CASES_KENT GL LTS K S.: {option}"

class FieldCasesKentIiiKS(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's # CASES_KENT III K. S.: {option}"

class FieldCasesNewportKS(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's # CASES_NEWPORT K. S.: {option}"

class FieldCasesNewportLtsKS(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's # CASES_NEWPORT LTS K. S.: {option}"

class FieldOfStoresSupplied(FormUserAttr):
    values = {'81749056_9057_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's # OF STORES SUPPLIED: {option}"

class FieldOpenEnds(FormUserAttr):
    values = {'89867723_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's # Open Ends: {option}"

class FieldReps(FormUserAttr):
    values = {'81619511_9513_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's # REPS: {option}"

class FieldCases(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's #CASES: {option}"

class FieldCasesKent100(FormUserAttr):
    values = {'82254638_processed': '', '91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's #CASES_KENT 100: {option}"

class FieldCasesKentGl100(FormUserAttr):
    values = {'82254638_processed': '', '91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's #CASES_KENT GL 100: {option}"

class FieldCasesKentIiKS(FormUserAttr):
    values = {'82254638_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's #CASES_KENT II K.S.: {option}"

class FieldCasesKentIii100(FormUserAttr):
    values = {'82254638_processed': '1', '91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's #CASES_KENT III 100: {option}"

class FieldCasesKentKS(FormUserAttr):
    values = {'82254638_processed': '1', '91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's #CASES_KENT K.S.: {option}"

class FieldCasesNewport100S(FormUserAttr):
    values = {'82254638_processed': '', '91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's #CASES_NEWPORT 100'S: {option}"

class FieldCasesNewportLts100(FormUserAttr):
    values = {'82254638_processed': '', '91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's #CASES_NEWPORT LTS. 100: {option}"

class FieldCasesNewportLtsKs(FormUserAttr):
    values = {'82254638_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's #CASES_NEWPORT LTS. KS.: {option}"

class FieldCasesNewportksKS(FormUserAttr):
    values = {'82254638_processed': '1'}

    @staticmethod
    def nl_desc(option):
        return f"The user's #CASES_NEWPORTKS K.S.: {option}"

class FieldCasesTrueKS(FormUserAttr):
    values = {'82254638_processed': '', '91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's #CASES_TRUE K.S.: {option}"

class FieldDisplaysPlaced(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's #Displays Placed:: {option}"

class FieldDisplaysPlacedCounter(FormUserAttr):
    values = {'92091873_processed': '15', '93213298_processed': '0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's #Displays Placed:_Counter: {option}"

class FieldDisplaysPlacedFloor(FormUserAttr):
    values = {'92091873_processed': '9', '93213298_processed': '0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's #Displays Placed:_Floor: {option}"

class FieldDisplaysPlacedPosters(FormUserAttr):
    values = {'92091873_processed': '100', '93213298_processed': '0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's #Displays Placed:_Posters: {option}"

class FieldItemsDealsReceived(FormUserAttr):
    values = {'92094746_processed': '28728', '92094751_processed': '22, 320 (Indy East & West) NO SHOW SAMPLES'}

    @staticmethod
    def nl_desc(option):
        return f"The user's #ITEMS/ DEALS RECEIVED:: {option}"

class Field(FormUserAttr):
    values = {'0012602424_processed': '', '11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's $: {option}"

class Field150OffCartonCoupon(FormUserAttr):
    values = {'89817999_8002_processed': 'CARTON MOVEMENT SPOTTY AT THIS POINT. SUPPLIES ARE MORE THAN ADEQUATE AND THE NEED IS MOSTLY PACKAGE SUPPORT AT THIS TIME.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's $1.50 OFF CARTON COUPON:: {option}"

class FieldMoistureInTobacco(FormUserAttr):
    values = {'01122115_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's % Moisture in Tobacco: {option}"

class FieldMoistureInTow(FormUserAttr):
    values = {'01122115_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's % Moisture in Tow: {option}"

class FieldOfDistributionAchievedInRetailOutlets(FormUserAttr):
    values = {'89817999_8002_processed': '62%\uf702 CLASSIFIED CALLS 10% ANNUAL CALLS', '92657311_7313_processed': '9 0 % CLASSIFIED CALLS 2 % ANNUAL CALLS'}

    @staticmethod
    def nl_desc(option):
        return f"The user's % OF DISTRIBUTION ACHIEVED IN RETAIL OUTLETS:: {option}"

class FieldOfDistributionAchievedInRetailOutletsAnnualCalls(FormUserAttr):
    values = {'91315069_91315070_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's % OF DISTRIBUTION ACHIEVED IN RETAIL OUTLETS:_% ANNUAL CALLS: {option}"

class FieldOfDistributionAchievedInRetailOutletsClassifiedCalls(FormUserAttr):
    values = {'91315069_91315070_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's % OF DISTRIBUTION ACHIEVED IN RETAIL OUTLETS:_% CLASSIFIED CALLS: {option}"

class FieldOfRetailCalls(FormUserAttr):
    values = {'92081358_1359_processed': '247- classifIed 57- annual'}

    @staticmethod
    def nl_desc(option):
        return f"The user's % OF RETAIL CALLS:: {option}"

class FieldPlasticizer(FormUserAttr):
    values = {'01122115_processed': '6 .0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's % Plasticizer: {option}"

class FieldSolution(FormUserAttr):
    values = {'00040534_processed': '5 10 10 10 10', '87672097_processed': '100 100 100 100 100'}

    @staticmethod
    def nl_desc(option):
        return f"The user's % SOLUTION: {option}"

class Field59(FormUserAttr):
    values = {'01073843_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (+) 5-9: {option}"

class Field6HardPack(FormUserAttr):
    values = {'0060308461_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's (6) HARD PACK: {option}"

class FieldBy(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (BY: {option}"

class FieldCurrent(FormUserAttr):
    values = {'0012602424_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (Current: {option}"

class FieldDate(FormUserAttr):
    values = {'71190280_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (Date): {option}"

class FieldFromCurrentBudget(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (From Current Budget): {option}"

class FieldFromNextYearSBudget(FormUserAttr):
    values = {'0012529284_processed': '', '0012602424_processed': '', '12603270_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (From Next Year' s Budget): {option}"

class FieldGiveReasonsBelow(FormUserAttr):
    values = {'00070353_processed': 'APPROVE TENTATIVELY'}

    @staticmethod
    def nl_desc(option):
        return f"The user's (Give reasons below):: {option}"

class FieldIncludingThisCoverSheet(FormUserAttr):
    values = {'92298125_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (Including this cover sheet): {option}"

class FieldOnlyPartialRegionContinueWithDivisionSScope(FormUserAttr):
    values = {'81619511_9513_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (ONLY PARTIAL REGION CONTINUE WITH DIVISION(S) SCOPE): {option}"

class FieldProductTestAUEtc(FormUserAttr):
    values = {'0001463282_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (Product Test, A&U, etc.): {option}"

class FieldRecordsRetention(FormUserAttr):
    values = {'71341634_processed': '30 days)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's (Records Retention:: {option}"

class FieldContD(FormUserAttr):
    values = {'00851772_1780_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (cont'd): {option}"

class FieldPlease(FormUserAttr):
    values = {'0001477983_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (please: {option}"

class FieldPleaseSpecify(FormUserAttr):
    values = {'92314414_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (please specify): {option}"

class FieldS(FormUserAttr):
    values = {'71202511_processed': '', '71601299_processed': '', '92586242_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (s): {option}"

class FieldTo(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's (to: {option}"

class FieldAdvertisingCreativeTitle(FormUserAttr):
    values = {'87533049_processed': 'True Filter King Carton'}

    @staticmethod
    def nl_desc(option):
        return f"The user's * Advertising Creative Title: {option}"

class FieldDirectorGLLittell(FormUserAttr):
    values = {'0060029036_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's * Director - (G. L. Littell): {option}"

class FieldExplanationOfChange(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's * EXPLANATION OF CHANGE: {option}"

class FieldRevisedCompletionDate(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's * REVISED COMPLETION DATE: {option}"

class FieldSpaceColor(FormUserAttr):
    values = {'87533049_processed': 'N/A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's * Space / Color: {option}"

class FieldSrManagerBJPowell(FormUserAttr):
    values = {'0060029036_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's * Sr. Manager (B. J. Powell): {option}"

class FieldSrVpTWRobertson(FormUserAttr):
    values = {'0060029036_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ** Sr. VP T. W. Robertson: {option}"

class FieldDateOfEvent(FormUserAttr):
    values = {'82254638_processed': 'September 10, 1997 Marcus Hellenic Spirit Charities Golf Classic September 18, 1997'}

    @staticmethod
    def nl_desc(option):
        return f"The user's *DATE OF EVENT:: {option}"

class FieldExplain(FormUserAttr):
    values = {'92094746_processed': 'Special Emphasis Calls', '92094751_processed': 'Chain stores will not accept multiple Newport Promotions (Tier system) at the same time.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's *EXPLAIN:: {option}"

class FieldIssueFrequencyYear(FormUserAttr):
    values = {'87533049_processed': 'N/A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's *Issue Frequency / Year: {option}"

class Field10ContingencyFinalReportInc(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's + - 10% Contingency Final Report Inc.: {option}"

class Field10ContingencyFinalReportIncNo(FormUserAttr):
    values = {'89867723_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's + - 10% Contingency Final Report Inc._no: {option}"

class Field10ContingencyFinalReportIncYes(FormUserAttr):
    values = {'89867723_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's + - 10% Contingency Final Report Inc._yes: {option}"

class FieldDateInitiated(FormUserAttr):
    values = {'93380187_processed': 'JANUARY 8, 1992'}

    @staticmethod
    def nl_desc(option):
        return f"The user's - -DATE INITIATED: {option}"

class FieldBrandSApplicable(FormUserAttr):
    values = {'93380187_processed': 'TRUE'}

    @staticmethod
    def nl_desc(option):
        return f"The user's - BRAND(S) APPLICABLE: {option}"

class FieldCirculation(FormUserAttr):
    values = {'93380187_processed': '560,000'}

    @staticmethod
    def nl_desc(option):
        return f"The user's - CIRCULATION: {option}"

class FieldCouponExpirationDate(FormUserAttr):
    values = {'93380187_processed': '8 /31 /92'}

    @staticmethod
    def nl_desc(option):
        return f"The user's - COUPON EXPIRATION DATE: {option}"

class FieldCouponIssueDate(FormUserAttr):
    values = {'93380187_processed': 'MAY 1992'}

    @staticmethod
    def nl_desc(option):
        return f"The user's - COUPON ISSUE DATE: {option}"

class FieldCouponValue(FormUserAttr):
    values = {'93380187_processed': '50c'}

    @staticmethod
    def nl_desc(option):
        return f"The user's - COUPON VALUE: {option}"

class FieldGeographicalAreaS(FormUserAttr):
    values = {'93380187_processed': 'TRUE CORE MARKETS *'}

    @staticmethod
    def nl_desc(option):
        return f"The user's - GEOGRAPHICAL AREA(S): {option}"

class FieldMediaName(FormUserAttr):
    values = {'93380187_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's - MEDIA NAME: {option}"

class FieldMediaType(FormUserAttr):
    values = {'93380187_processed': 'SALES FORCE APPLIED - IRC'}

    @staticmethod
    def nl_desc(option):
        return f"The user's - MEDIA TYPE: {option}"

class FieldPackAndOrCarton(FormUserAttr):
    values = {'93380187_processed': 'PACK'}

    @staticmethod
    def nl_desc(option):
        return f"The user's - PACK AND/OR CARTON: {option}"

class FieldSignatureOfInitiator(FormUserAttr):
    values = {'93380187_processed': 'Michell '}

    @staticmethod
    def nl_desc(option):
        return f"The user's - SIGNATURE OF INITIATOR: {option}"

class FieldSpeaker(FormUserAttr):
    values = {'0060262650_processed': 'Dr. Michael A. Bender'}

    @staticmethod
    def nl_desc(option):
        return f"The user's - Speaker: {option}"

class Field12Cigar(FormUserAttr):
    values = {'0060094595_processed': '5 0 5 0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's -1 /2 Cigar: {option}"

class Field13Cigar(FormUserAttr):
    values = {'0060094595_processed': '7 1 4 1'}

    @staticmethod
    def nl_desc(option):
        return f"The user's -1 /3 Cigar: {option}"

class FieldDec(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's -DEC: {option}"

class FieldJun(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's -JUN.: {option}"

class FieldMar(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's -MAR.: {option}"

class FieldSep(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's -SEP: {option}"

class FieldWentOutImmediately(FormUserAttr):
    values = {'0060094595_processed': '12 0 4 0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's -Went out immediately: {option}"

class Field1(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1: {option}"

class Field1680(FormUserAttr):
    values = {'0060068489_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1,680: {option}"

class Field1Enhancement(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. Enhancement: {option}"

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimant(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. Name, address and telephone number of law firm representing claimant:: {option}"

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantAddress(FormUserAttr):
    values = {'92433599_92433601_processed': '999 Grant Avenue, P. O. Box 2109'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. Name, address and telephone number of law firm representing claimant:_Address: {option}"

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantCity(FormUserAttr):
    values = {'92433599_92433601_processed': 'Novato'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. Name, address and telephone number of law firm representing claimant:_City: {option}"

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantName(FormUserAttr):
    values = {'92433599_92433601_processed': 'BRAYTON, GISVOLD. & HARLEY'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. Name, address and telephone number of law firm representing claimant:_Name: {option}"

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantState(FormUserAttr):
    values = {'92433599_92433601_processed': 'CA'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. Name, address and telephone number of law firm representing claimant:_State: {option}"

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantTelephone(FormUserAttr):
    values = {'92433599_92433601_processed': '(415) 898- 1555'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. Name, address and telephone number of law firm representing claimant:_Telephone: {option}"

class Field1NameAddressAndTelephoneNumberOfLawFirmRepresentingClaimantZipCode(FormUserAttr):
    values = {'92433599_92433601_processed': '94948'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. Name, address and telephone number of law firm representing claimant:_Zip Code: {option}"

class Field1ProductivityImprovement(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. Productivity Improvement: {option}"

class Field1StatesAndCitiesSelectedToReceiveProduct(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductChicagoIll(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_*Chicago, Ill.: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductNycNY(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_*NYC, N. Y.: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductAlabama(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Alabama: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductAlaska(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Alaska: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductArizona(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Arizona: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductArkansas(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Arkansas: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductCalifornia(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_California: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductColorada(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Colorada: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductConnecticut(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Connecticut: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductDC(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_D. C.: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductDelaware(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Delaware: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductFlorida(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Florida: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductGeorgia(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Georgia: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductHawaii(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Hawaii: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductIdaho(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Idaho: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductIllinois(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Illinois: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductIndiana(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Indiana: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductIowa(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Iowa: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductKansas(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Kansas: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductKentucky(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Kentucky: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductLouisiana(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Louisiana: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductMaine(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Maine: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductMaryland(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Maryland: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductMassachusetts(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Massachusetts: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductMichigan(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Michigan: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductMinnesota(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Minnesota: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductMississippi(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Mississippi: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductMissouri(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Missouri: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductMontana(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Montana: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductNebraska(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Nebraska: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductNevada(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Nevada: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductNewHampshire(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_New Hampshire: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductNewJersey(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_New Jersey: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductNewMexico(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_New Mexico: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductNewYork(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_New York: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductNorthCarolina(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_North Carolina: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductNorthDakota(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_North Dakota: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductOhio(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Ohio: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductOklahoma(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Oklahoma: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductOregon(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Oregon: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductPennsylVania(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Pennsyl vania: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductRhodeIsland(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Rhode Island: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductSouthCarolina(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_South Carolina: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductSouthDakota(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_South Dakota: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductTennessee(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Tennessee: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductTexas(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Texas: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductUtah(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Utah: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductVermont(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Vermont: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductVirginia(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Virginia: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductWashington(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Washington: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductWestVirginia(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_West Virginia: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductWisconsin(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Wisconsin: {option}"

class Field1StatesAndCitiesSelectedToReceiveProductWyoming(FormUserAttr):
    values = {'91161344_91161347_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1. STATES AND CITIES* SELECTED TO RECEIVE PRODUCT:_Wyoming: {option}"

class Field10(FormUserAttr):
    values = {'87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 10): {option}"

class Field100S(FormUserAttr):
    values = {'81749056_9057_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 100's: {option}"

class Field100000(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 100,000): {option}"

class Field12Yr(FormUserAttr):
    values = {'92081358_1359_processed': '162 53%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 12/ YR: {option}"

class Field1976(FormUserAttr):
    values = {'0060036622_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1976: {option}"

class Field1987(FormUserAttr):
    values = {'0012529284_processed': ' (886, 220. 53) +14, 165. 00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1987: {option}"

class Field198(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 198–: {option}"

class Field1990Cost(FormUserAttr):
    values = {'0011838621_processed': '$ 0.00 .08 .08'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 1990 Cost: {option}"

class Field2(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2: {option}"

class Field2Aminoanthhacene(FormUserAttr):
    values = {'00836244_processed': '4 2'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2- AMINOANTHHACENE: {option}"

class Field2Aminoanthracene(FormUserAttr):
    values = {'01073843_processed': '4.0 2.0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2. AMINOANTHRACENE: {option}"

class Field2EstimatedTestProductQuantitiesPerMarket(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2. ESTIMATED TEST PRODUCT QUANTITIES (PER MARKET): {option}"

class Field2EstimatedTestProductQuantitiesPerMarket4S5S20SEtc(FormUserAttr):
    values = {'91161344_91161347_processed': "All are 20's"}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2. ESTIMATED TEST PRODUCT QUANTITIES (PER MARKET)_(4's, 5's, 20's etc.): {option}"

class Field2EstimatedTestProductQuantitiesPerMarketCode(FormUserAttr):
    values = {'91161344_91161347_processed': "['519', '934', '639']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2. ESTIMATED TEST PRODUCT QUANTITIES (PER MARKET)_Code #: {option}"

class Field2EstimatedTestProductQuantitiesPerMarketProductCode(FormUserAttr):
    values = {'91161344_91161347_processed': "['741', '753', '827', '462']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2. ESTIMATED TEST PRODUCT QUANTITIES (PER MARKET)_PRODUCT Code #: {option}"

class Field2EstimatedTestProductQuantitiesPerMarketQuantity(FormUserAttr):
    values = {'91161344_91161347_processed': 'Varies by market, see attached list. Approx. 20% of the total # by state will receive product'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2. ESTIMATED TEST PRODUCT QUANTITIES (PER MARKET)_QUANTITY: {option}"

class Field2Maintenance(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2. Maintenance-: {option}"

class Field2NamesOfFirstNamedPlaintiffAndFirstNamedDefendantOnTheCaptionOfTheComplaint(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2. Names of first named plaintiff and first named defendant on the caption of the complaint:: {option}"

class Field2NamesOfFirstNamedPlaintiffAndFirstNamedDefendantOnTheCaptionOfTheComplaintDefendant(FormUserAttr):
    values = {'92433599_92433601_processed': 'ABEX CORPORATION, et al.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2. Names of first named plaintiff and first named defendant on the caption of the complaint:_Defendant: {option}"

class Field2NamesOfFirstNamedPlaintiffAndFirstNamedDefendantOnTheCaptionOfTheComplaintPlaintiff(FormUserAttr):
    values = {'92433599_92433601_processed': 'CHARLES WOODWARD'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2. Names of first named plaintiff and first named defendant on the caption of the complaint:_Plaintiff: {option}"

class Field2ReturnOnInvestment(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2. Return on Investment-: {option}"

class Field202851A1B1Im(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 20. 285 1 (a), 1 (b), 1 (im): {option}"

class Field2134(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's 21- 34: {option}"

class Field213496(FormUserAttr):
    values = {'0000999294_processed': '56+++ 35 9 100'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 21- 34 (96): {option}"

class Field2134Bright(FormUserAttr):
    values = {'0000999294_processed': "['4.74', '3.38', '5.31', '2.99', '2.74', '3.07', '3.92']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's 21- 34_Bright: {option}"

class Field2134Kl(FormUserAttr):
    values = {'0000999294_processed': "['4.35**', '3.61*', '3.63***', '3.45***', '3.17***', '3.52***', '4.07**']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's 21- 34_KL: {option}"

class Field25Yr(FormUserAttr):
    values = {'92081358_1359_processed': '8 3%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 25/ YR: {option}"

class Field2AEstimatedTotalsByProductAllMarketsCombined(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2a. ESTIMATED TOTALS BY PRODUCT ALL MARKETS COMBINED: {option}"

class Field2AEstimatedTotalsByProductAllMarketsCombined4S5S20SEtc(FormUserAttr):
    values = {'91161344_91161347_processed': "All are 20's"}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2a. ESTIMATED TOTALS BY PRODUCT ALL MARKETS COMBINED_(4's, 5's, 20's etc.): {option}"

class Field2AEstimatedTotalsByProductAllMarketsCombinedQuantity(FormUserAttr):
    values = {'91161344_91161347_processed': "['1920 Packs', '1920 Packs', '960 Packs', '960 Packs', '1920 Packs', '1920 Packs', '1920 Packs']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's 2a. ESTIMATED TOTALS BY PRODUCT ALL MARKETS COMBINED_QUANTITY: {option}"

class Field3(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 3: {option}"

class Field3CustomerImpact(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 3. Customer Impact: {option}"

class Field3DateOfClaimantSBirth(FormUserAttr):
    values = {'92433599_92433601_processed': 'June 19, 1921'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 3. Date of claimant's birth:: {option}"

class Field3SpecialProcessing(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 3. Special Processing: {option}"

class Field30SheetPosters(FormUserAttr):
    values = {'0060068489_processed': '$ 26,880,00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 30 Sheet Posters : {option}"

class Field35Over(FormUserAttr):
    values = {'0001209043_processed': '0.0 (55) 29 (86)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 35 & Over: {option}"

class Field35Under(FormUserAttr):
    values = {'0001476912_processed': '0.0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 35 & Under: {option}"

class Field35(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's 35+: {option}"

class Field35109(FormUserAttr):
    values = {'0000999294_processed': '50 42 8 100'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 35+ 109: {option}"

class Field35Bright(FormUserAttr):
    values = {'0000999294_processed': "['4.45', '3.46', '4.61', '2.08', '2.82', '3.39', '3.99']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's 35+_Bright: {option}"

class Field35Kl(FormUserAttr):
    values = {'0000999294_processed': "['4.27', '3.58', '3.65***', '2.34**', '3.08**', '3.60*', '3.94']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's 35+_KL: {option}"

class Field36Over(FormUserAttr):
    values = {'0001476912_processed': '5.0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 36 & Over: {option}"

class Field4(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 4: {option}"

class Field4AdHoc(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 4. Ad Hoc-: {option}"

class Field4CaseInvolvesCheckAppropriateBoxes(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's 4. Case involves (check appropriate boxes):: {option}"

class Field4CaseInvolvesCheckAppropriateBoxesAInjury(FormUserAttr):
    values = {'92433599_92433601_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 4. Case involves (check appropriate boxes):_(a) Injury: {option}"

class Field4CaseInvolvesCheckAppropriateBoxesBWrongfulDeath(FormUserAttr):
    values = {'92433599_92433601_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 4. Case involves (check appropriate boxes):_(b) Wrongful death: {option}"

class Field4CaseInvolvesCheckAppropriateBoxesCConsortium(FormUserAttr):
    values = {'92433599_92433601_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 4. Case involves (check appropriate boxes):_(c) Consortium: {option}"

class Field4GovernmentRequirement(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 4. Government Requirement: {option}"

class Field5(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 5: {option}"

class Field5BusinessChange(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 5. Business Change: {option}"

class Field5Emergency(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 5. Emergency-: {option}"

class Field5SpecifyTheNatureOrTypeOfAsbestosRelatedInjuryAllegedByTheClaimantEQAsbestosisLungCancerAdenocarcinomaLungCancerMesotheliomaPleuralThickeningFibrosisEtc(FormUserAttr):
    values = {'92433599_92433601_processed': 'Mesothelioma and other asbestos- related lung disease'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 5. Specify the nature or type of asbestos- related injury alleged by the claimant. (E. q., Asbestosis; Lung Cancer- adenocarcinoma Lung Cancer- Mesothelioma; Pleural Thickening; Fibrosis; etc.): {option}"

class Field5TypesOfLocalGovernmentalUnitAflected(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's 5. Types of Local Governmental Unit Aflected:: {option}"

class Field5TypesOfLocalGovernmentalUnitAflectedCities(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 5. Types of Local Governmental Unit Aflected:_☐ Cities: {option}"

class Field5TypesOfLocalGovernmentalUnitAflectedOthers(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 5. Types of Local Governmental Unit Aflected:_☐ Others: {option}"

class Field5TypesOfLocalGovernmentalUnitAflectedVillages(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 5. Types of Local Governmental Unit Aflected:_☐ Villages: {option}"

class Field50Yr(FormUserAttr):
    values = {'92081358_1359_processed': '0 0%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 50/ YR: {option}"

class Field530(FormUserAttr):
    values = {'92314414_processed': '274- 38- 3042'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 530:: {option}"

class Field6(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 6: {option}"

class Field6SystemError(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 6. System Error-: {option}"

class Field6Yr(FormUserAttr):
    values = {'92081358_1359_processed': '76 25%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's 6/ YR: {option}"

class Field7(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 7: {option}"

class Field7ProceduralError(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's 7. Procedural Error: {option}"

class FieldBeginner(FormUserAttr):
    values = {'0030031163_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's <> Beginner: {option}"

class FieldExcellent(FormUserAttr):
    values = {'0030031163_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's <> Excellent: {option}"

class FieldFair(FormUserAttr):
    values = {'0030031163_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's <> Fair: {option}"

class FieldGood(FormUserAttr):
    values = {'0030031163_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's <> Good: {option}"

class A(FormUserAttr):
    values = {'0012602424_processed': '', '01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's A.: {option}"

class ADM(FormUserAttr):
    values = {'80728670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's A. D. M.: {option}"

class AJMellman(FormUserAttr):
    values = {'0012602424_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's A. J. MELLMAN: {option}"

class AcceptRejectAsPer58185C(FormUserAttr):
    values = {'89368010_processed': 'Accept Accept Accept   '}

    @staticmethod
    def nl_desc(option):
        return f"The user's ACCEPT/ REJECT (as per 58.185 (c)): {option}"

class Accepted(FormUserAttr):
    values = {'0060214859_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ACCEPTED: {option}"

class AcceptedSymposium(FormUserAttr):
    values = {'0060262650_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ACCEPTED SYMPOSIUM: {option}"

class AccountNo(FormUserAttr):
    values = {'91104867_processed': '6450 6460 6470 6560'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ACCOUNT NO.: {option}"

class AccountingChargeNo(FormUserAttr):
    values = {'0060077689_processed': 'Adv. Expense'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ACCOUNTING CHARGE NO.: {option}"

class AccountingDistribution(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's ACCOUNTING DISTRIBUTION: {option}"

class AccountingDistributionFeb(FormUserAttr):
    values = {'0060080406_processed': '$ 10.000.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ACCOUNTING DISTRIBUTION_FEB: {option}"

class AccountingDistributionJan(FormUserAttr):
    values = {'0060080406_processed': '$ 10.000.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ACCOUNTING DISTRIBUTION_JAN: {option}"

class AccountingDistributionMar(FormUserAttr):
    values = {'0060080406_processed': '$ 15,000.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ACCOUNTING DISTRIBUTION_MAR: {option}"

class AcctNo(FormUserAttr):
    values = {'00922237_processed': '4111'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ACCT NO.: {option}"

class AcuteCadcovascular(FormUserAttr):
    values = {'00865872_processed': '(See SOP for Determination of Solubility of Materials for Acute Cardiovascular and Respiratory Effects Study Beagle Dogs) B164 is insoluble according to this procedure'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ACUTE CADCOVASCULAR: {option}"

class AcuteCardiovascular(FormUserAttr):
    values = {'00836816_processed': '(See SOP for Determination of Solubility of Materials for Acute Cardiovascular and Respiratory Effects Study in Beagle Dogs) Reference OR 100- 32 .2 mg A30 soluble in .5 mL 10 % propylene glycol solution at 38 C. Add A30 to warm (38 C) propylene glycol; add warm water to make 10 % propylene glycol solution.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ACUTE CARDIOVASCULAR: {option}"

class AdminCtrMgmtCtrPurchaseOrderNo(FormUserAttr):
    values = {'0060077689_processed': 'M14789'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ADMIN CTR/MGMT CTR PURCHASE ORDER NO.: {option}"

class AdminCtrMgmtCtrAsRequired(FormUserAttr):
    values = {'0060077689_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ADMIN CTR/MGMT CTR. (AS REQUIRED): {option}"

class AdvertisingCreativeTheme(FormUserAttr):
    values = {'91391286_processed': 'BLUE SKY', '91391310_processed': '', '91974562_processed': '', '93351929_93351931_processed': 'Rebecca'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ADVERTISING CREATIVE THEME: {option}"

class Affiliation(FormUserAttr):
    values = {'0060262650_processed': 'University of Utah'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AFFILIATION: {option}"

class Affillation(FormUserAttr):
    values = {'0060262650_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's AFFILLATION: {option}"

class Aftertaste(FormUserAttr):
    values = {'0001239897_processed': '+22 +21'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AFTERTASTE: {option}"

class Age(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's AGE: {option}"

class Age2534(FormUserAttr):
    values = {'0001209043_processed': '', '0001438955_processed': "['3.0', '(66)']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's AGE:_25- 34: {option}"

class Age3544(FormUserAttr):
    values = {'0001209043_processed': '', '0001438955_processed': "['4.4', '(46)']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's AGE:_35- 44: {option}"

class Age45Over(FormUserAttr):
    values = {'0001209043_processed': '', '0001438955_processed': "['4.0', '(49)']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's AGE:_45 & Over: {option}"

class AgeUnder25(FormUserAttr):
    values = {'0001209043_processed': '', '0001438955_processed': "['3.2', '(63)']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's AGE:_Under 25: {option}"

class Agency(FormUserAttr):
    values = {'0060068489_processed': 'corporate Media Department', '13149651_processed': 'University of Wisconsin System', '91581919_processed': 'Lorillard Media Service'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AGENCY: {option}"

class Age1625(FormUserAttr):
    values = {'0001476912_processed': '0.0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AGE_16-25: {option}"

class Age2635(FormUserAttr):
    values = {'0001476912_processed': '0.0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AGE_26-35: {option}"

class Age3645(FormUserAttr):
    values = {'0001476912_processed': '0.0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AGE_36-45: {option}"

class Age46Over(FormUserAttr):
    values = {'0001476912_processed': '9.3'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AGE_46 & Over: {option}"

class AirTime(FormUserAttr):
    values = {'0060068489_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's AIR TIME: {option}"

class Albert(FormUserAttr):
    values = {'0012602424_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ALBERT: {option}"

class Alternatives(FormUserAttr):
    values = {'80707440_7443_processed': 'Los Angeles Football Fans Chicago Football Fans'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ALTERNATIVES:: {option}"

class Ame(FormUserAttr):
    values = {'0060262650_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's AME: {option}"

class AmountOfChangeIncreaseCircleOne(FormUserAttr):
    values = {'0012602424_processed': '+1 ,000 (0 .5% CHANGE)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AMOUNT OF CHANGE INCREASE ): (CIRCLE ONE): {option}"

class AmtMenthol7More(FormUserAttr):
    values = {'0000999294_processed': '3.64*** 4.94 3.58*** 4.85 3.70*** 5.02 3.63*** 5.31 3.65*** 4.61'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AMT MENTHOL (7= More): {option}"

class Analytical(FormUserAttr):
    values = {'87533049_processed': 'Break - out separately byl packing as indicated'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ANALYTICAL: {option}"

class AnalyticalMethodS(FormUserAttr):
    values = {'00837285_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ANALYTICAL METHOD(S): {option}"

class AnalyticalRequirements(FormUserAttr):
    values = {'93380187_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ANALYTICAL REQUIREMENTS:: {option}"

class AnalyticalRequirementsCodeAssigned(FormUserAttr):
    values = {'91391286_processed': '8482', '91391310_processed': '8470', '91974562_processed': '00862', '93351929_93351931_processed': '221782'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ANALYTICAL REQUIREMENTS:_CODE ASSIGNED:: {option}"

class AnalyticalRequirementsEstRedemption(FormUserAttr):
    values = {'91391310_processed': '80%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ANALYTICAL REQUIREMENTS:_EST, REDEMPTION:: {option}"

class AnalyticalRequirementsForControlUseOnly(FormUserAttr):
    values = {'91391286_processed': '93- 056', '91391310_processed': '', '91974562_processed': '', '93351929_93351931_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ANALYTICAL REQUIREMENTS:_FOR CONTROL USE ONLY:: {option}"

class AnalyticalRequirementsJobNumber(FormUserAttr):
    values = {'91391286_processed': '9076', '91391310_processed': '916', '91974562_processed': '490', '93351929_93351931_processed': '414'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ANALYTICAL REQUIREMENTS:_JOB NUMBER:: {option}"

class Annuals(FormUserAttr):
    values = {'92081358_1359_processed': '57 19%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ANNUALS: {option}"

class Approval(FormUserAttr):
    values = {'0012178355_processed': '', '91104867_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVAL: {option}"

class ApprovalRouting(FormUserAttr):
    values = {'0060029036_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVAL ROUTING: {option}"

class Approvals(FormUserAttr):
    values = {'89368010_processed': '03 June 1982 3 June 1982 3 June 1982'}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS: {option}"

class ApprovalsDate(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS:_Date: {option}"

class ApprovalsDirIntAdmin(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS:_Dir. Int' Admin: {option}"

class ApprovalsGroupProdDir(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS:_Group Prod Dir: {option}"

class ApprovalsRegionalDirVp(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS:_Regional Dir/ VP: {option}"

class ApprovalsSeniorVpIntL(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS:_Senior VP Int'l: {option}"

class ApprovalsVpIntLMarketing(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS:_VP Int'l Marketing: {option}"

class ApprovalsVpIntLPlanning(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS:_VP Int'l Planning: {option}"

class ApprovalsAccounting(FormUserAttr):
    values = {'0060068489_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS_Accounting: {option}"

class ApprovalsAgency(FormUserAttr):
    values = {'0060068489_processed': '', '0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS_Agency: {option}"

class ApprovalsAuthorizationNo(FormUserAttr):
    values = {'0060068489_processed': 'M- 49'}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS_Authorization No.: {option}"

class ApprovalsBudgetAllocation(FormUserAttr):
    values = {'0060068489_processed': 'L- 3a'}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS_Budget Allocation: {option}"

class ApprovalsChairmanCeo(FormUserAttr):
    values = {'0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS_Chairman/ CEO: {option}"

class ApprovalsExecutive(FormUserAttr):
    values = {'0060068489_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS_Executive: {option}"

class ApprovalsForecasting(FormUserAttr):
    values = {'0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS_Forecasting: {option}"

class ApprovalsMarketing(FormUserAttr):
    values = {'0060068489_processed': '', '0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS_Marketing: {option}"

class ApprovalsMedia(FormUserAttr):
    values = {'0060068489_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS_Media: {option}"

class ApprovalsPresident(FormUserAttr):
    values = {'0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS_President: {option}"

class ApprovalsProduct(FormUserAttr):
    values = {'0060068489_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS_Product: {option}"

class ApprovalsSales(FormUserAttr):
    values = {'0060068489_processed': '', '0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS_Sales: {option}"

class ApprovalsVPMarketing(FormUserAttr):
    values = {'0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVALS_V. P. - Marketing: {option}"

class ApproveInIts(FormUserAttr):
    values = {'00070353_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVE IN ITS: {option}"

class Approved(FormUserAttr):
    values = {'0060025670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROVED: {option}"

class ApproximateOfRetailCallsSecuredByGlass(FormUserAttr):
    values = {'92081358_1359_processed': '45% (136 calls)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's APPROXIMATE % OF RETAIL CALLS SECURED BY GLASS:: {option}"

class Apr(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's APR.: {option}"

class Aptertaste7Pleasant(FormUserAttr):
    values = {'0000999294_processed': '3.56*** 3.24 3.69*** 3.21 3.44 3.26 3.52*** 3.07 3.60* 3.39'}

    @staticmethod
    def nl_desc(option):
        return f"The user's APTERTASTE (7= Pleasant): {option}"

class AreaRegionDivision(FormUserAttr):
    values = {'92094751_processed': '03/ 07/ 415415 & 418418'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AREA REGION DIVISION: {option}"

class AreaRegion(FormUserAttr):
    values = {'81749056_9057_processed': '1/ 20'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AREA REGION:: {option}"

class ArtWork(FormUserAttr):
    values = {'0060068489_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ART WORK: {option}"

class AssayResult(FormUserAttr):
    values = {'81310636_processed': 'M. Lymph: negative with S9 activation, positive without S9 activation; Rerun: negative without S9 activation, border- line positive with S9 activation -Technical problems with the'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ASSAY RESULT: {option}"

class At919AtTheGreensboroBranchAsSoonAsPossible(FormUserAttr):
    values = {'92327794_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's AT (919) AT THE GREENSBORO BRANCH AS SOON AS POSSIBLE.: {option}"

class AtTheTimeOfReproductionTheFollowingNotattonsWereMade(FormUserAttr):
    values = {'0001463448_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's AT THE TIME OF REPRODUCTION, THE FOLLOWING NOTATTONS WERE MADE:: {option}"

class AttachmentsCheckIfIncluded(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's ATTACHMENTS (Check if Included): {option}"

class AttachmentsCheckIfIncludedBlendFormulae(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ATTACHMENTS (Check if Included)_Blend Formulae: {option}"

class AttachmentsCheckIfIncludedCasingFlavoringFormulae(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ATTACHMENTS (Check if Included)_Casing Flavoring Formulae: {option}"

class AttachmentsCheckIfIncludedCostAnalysis(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ATTACHMENTS (Check if Included)_Cost Analysis: {option}"

class AttachmentsCheckIfIncludedInitialProductionRequirement(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ATTACHMENTS (Check if Included)_Initial Production Requirement: {option}"

class AttachmentsCheckIfIncludedPackagingArtStat(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ATTACHMENTS (Check if Included)_Packaging Art Stat.: {option}"

class AttachmentsCheckIfIncludedProcessingDetail(FormUserAttr):
    values = {'0012178355_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ATTACHMENTS (Check if Included)_Processing Detail: {option}"

class AttachmentsCheckIfIncludedProductSpecificationList(FormUserAttr):
    values = {'0012178355_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ATTACHMENTS (Check if Included)_Product Specification List: {option}"

class AttachmentsCheckIfIncludedRationale(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ATTACHMENTS (Check if Included)_Rationale: {option}"

class AttachmentsCheckIfIncludedSpecChangeDetail(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ATTACHMENTS (Check if Included)_Spec. Change Detail: {option}"

class Attributes(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's ATTRIBUTES: {option}"

class AttributesViceroy(FormUserAttr):
    values = {'0001239897_processed': "['Current VICEROY 84 (#627/ 647)', '25% PG w/ SORBITOL #647/ 627']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's ATTRIBUTES_VICEROY: {option}"

class AuthorizationNo(FormUserAttr):
    values = {'0060077689_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's AUTHORIZATION NO.: {option}"

class AuthorizedCost(FormUserAttr):
    values = {'0011505151_processed': '70,825 + +10 % (TOTAL 1987) +7.075 (2 -23 -88 77,900 TOTAL', '12052385_processed': '12, 500 (10- 15- 87)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AUTHORIZED COST:: {option}"

class Authors(FormUserAttr):
    values = {'00070353_processed': 'Andrew G. Kallianos, Richard K. Means, James D. Mold'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AUTHORS: {option}"

class AverageDailyEffectiveCirculation(FormUserAttr):
    values = {'12825369_processed': '218, 499'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AVERAGE DAILY EFFECTIVE CIRCULATION: {option}"

class AverageWeightRangeGm(FormUserAttr):
    values = {'00040534_processed': '', '87672097_processed': '16- 30'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AVERAGE WEIGHT RANGE (GM): {option}"

class AvgRate(FormUserAttr):
    values = {'71341634_processed': '$2 84 $2 00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's AVG Rate: {option}"

class AcceptedBy(FormUserAttr):
    values = {'88547278_88547279_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Accepted by:: {option}"

class Account(FormUserAttr):
    values = {'91581919_processed': 'Harley Davidson Cigarettes'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Account: {option}"

class AccountCode(FormUserAttr):
    values = {'0060080406_processed': '10- 320'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Account Code: {option}"

class AccountExecutive(FormUserAttr):
    values = {'88547278_88547279_processed': 'Peter Faucetta Jr.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Account Executive:: {option}"

class AccountMonth(FormUserAttr):
    values = {'71341634_processed': 'Pay Handling'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Account Month: {option}"

class AccountName(FormUserAttr):
    values = {'0001463282_processed': 'BARCLAY', '0011838621_processed': 'International.', '0012529284_processed': '', '0012529295_processed': 'CAPRI', '0012602424_processed': 'New Products', '12603270_processed': 'PRODUCT TESTING', '71341634_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Account Name: {option}"

class AccountNumber(FormUserAttr):
    values = {'0001485288_processed': '22 244 00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Account Number: {option}"

class AccountingFile(FormUserAttr):
    values = {'0060173256_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Accounting File: {option}"

class AcctName(FormUserAttr):
    values = {'11508234_processed': '', '71202511_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Acct. Name:: {option}"

class AdditionalSpray(FormUserAttr):
    values = {'00093726_processed': '3. 4% PMO in EtoH'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Additional Spray: {option}"

class Address(FormUserAttr):
    values = {'88057519_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Address: {option}"

class AddressPostalRequirementsBarcodesDocumentStorageAndBatchNumbersToBeSuppliedBy(FormUserAttr):
    values = {'0011974919_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Address, postal requirements, barcodes, document storage, and batch numbers to be supplied by:: {option}"

class AdhesiveCode(FormUserAttr):
    values = {'0060025670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Adhesive Code:: {option}"

class Adhesive(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Adhesive:: {option}"

class AdhesiveSupplierS(FormUserAttr):
    values = {'0000989556_processed': 'Swift'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Adhesive:_Supplier (s): {option}"

class AdhesiveSupplierCodeNoS(FormUserAttr):
    values = {'0000989556_processed': 'T.K. 9220'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Adhesive:_Supplier Code No (s): {option}"

class AdhesiveType(FormUserAttr):
    values = {'0000989556_processed': 'Printed Imitation cork'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Adhesive:_Type: {option}"

class AdjustedTotalCostOfProject(FormUserAttr):
    values = {'0011838621_processed': '$ 47.711.47 .08', '0012529284_processed': '$ 212, 475 + 10%', '0012602424_processed': '221, 000'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Adjusted Total Cost of Project:: {option}"

class AdjustedTotalCostOfProtect(FormUserAttr):
    values = {'12603270_processed': '$ -0-'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Adjusted Total Cost of Protect:: {option}"

class Adjustment(FormUserAttr):
    values = {'0060173256_processed': '$ 0.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Adjustment: {option}"

class AdvanceRegistrationFeePriorToAugust10(FormUserAttr):
    values = {'87682908_processed': '$ 170.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Advance Registration Fee: (prior to August 10): {option}"

class AffectedCh20Appropriations(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Affected Ch. 20 Appropriations: {option}"

class AlertNumber(FormUserAttr):
    values = {'00920294_processed': '970220'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Alert Number: {option}"

class AllowableSubstitutions(FormUserAttr):
    values = {'0001118259_processed': 'RPCFS or RPCFS-O  RPCBS OT RPCBS- O WCC MC -4 -S MC -4 -PH MC -4 -RC MC -4 -W MC -1 C Stem RRXF or RRXF -O RRXM -B RRXM -T RRBF or RRBF -O RRB -B RRB -L RRB -T'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Allowable Substitutions: {option}"

class AmendmentAttachAdditionalSheetsAsNecessary(FormUserAttr):
    values = {'89368010_processed': 'The report of the results of A 14 Day Repeated Dose Assay for Reference Cigarette Smoke in Mice (I- 1725.001- M1 is attached.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Amendment (Attach additional sheets as necessary): {option}"

class AmendmentNoIfApplicable(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Amendment No. if Applicable: {option}"

class Amount(FormUserAttr):
    values = {'0060173256_processed': '31,000.00 (31,000.00)', '00837285_processed': 'g100ml', '71341634_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Amount: {option}"

class AmountEarnedButNotReceived(FormUserAttr):
    values = {'0001477983_processed': '$'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Amount earned but not received:: {option}"

class AmtOfChange(FormUserAttr):
    values = {'0011838621_processed': 'Increase X', '12603270_processed': 'Increase Decrease X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Amt. of Change:: {option}"

class AmtOfChangeDecrease(FormUserAttr):
    values = {'0012529284_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Amt. of Change:_Decrease: {option}"

class AmtOfChangeIncrease(FormUserAttr):
    values = {'0012529284_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Amt. of Change:_Increase: {option}"

class Analyst(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Analyst: {option}"

class AnySpecialDietaryMealAndYouOrYourGuestWouldPrefer(FormUserAttr):
    values = {'0060091229_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Any special dietary meal and/ you or your guest would prefer: {option}"

class AppearanceOrAnswerDues(FormUserAttr):
    values = {'0012947358_processed': 'Within 20 days after service, exclusive of day of service.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Appearance or Answer Dues: {option}"

class ApplicationPattern(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Application Pattern:: {option}"

class ApplicationPatternOverall(FormUserAttr):
    values = {'0000989556_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Application Pattern:_Overall: {option}"

class ApplicationPatternSkip(FormUserAttr):
    values = {'0000989556_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Application Pattern:_skip: {option}"

class ApplicationTippingCartonEndFlapsEtc(FormUserAttr):
    values = {'0060025670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Application: tipping, carton end flaps, etc.): {option}"

class ApprovalSignatureDate(FormUserAttr):
    values = {'0001123541_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Approval Signature/ Date: {option}"

class ApprovedByDirectorForecastingMktTo250000(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Approved By:_Director Forecasting Mkt (to $ 250,000): {option}"

class ApprovedBy(FormUserAttr):
    values = {'0011856542_processed': '', '0011906503_processed': '', '0060007216_processed': 'R. S. Sprinkle III', '00920222_processed': '', '00922237_processed': 'H.J. Minnemeyer', '89867723_processed': '  '}

    @staticmethod
    def nl_desc(option):
        return f"The user's Approved by: {option}"

class ApprovedByGroupManager(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Approved by:_Group Manager: {option}"

class ApprovedByGroupProductManager(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Approved by:_Group Product Manager: {option}"

class ApprovedByMpio(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Approved by:_MPIO: {option}"

class ApprovedByProductManager(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Approved by:_Product Manager: {option}"

class AreaCode(FormUserAttr):
    values = {'87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Area Code:: {option}"

class ArrivalDateAndTimeIncludeAirlineAndFlightNo(FormUserAttr):
    values = {'80728670_processed': 'Monday, 3 /12 Evening Shuttle'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Arrival date and time (include airline and flight no.): {option}"

class Asst(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Asst: {option}"

class AsumptionsUsedInArrivingAtFiscalEstimate(FormUserAttr):
    values = {'13149651_processed': 'This bill regulates smoking in university buildings which house educational programs and in inpatient health care facilities. Smoking within these or rooms, provided buildings would be allowed only specified facilities designate these "smoking permitted" areas. that signs are posted to university buildings would each It is estimated that, on the average, The per "smoking signs. sign cost is require about three permitted" This estimate is based on the estimated at $4 50 in 1982-83 dollars. 1981 increased to reflect Inflation from 1981 to 1983. per sign cost, and Thus, the expected one-time cost for the University Systet to implement no be about There are significant the provisions of the bill would $8,000. with the bill\'s provisions. continuing annual costs associated'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Asumptions Used in Arriving at Fiscal Estimate: {option}"

class Attendees(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Attendees:: {option}"

class AttendeesCustomersAttended(FormUserAttr):
    values = {'92091873_processed': '35', '93213298_processed': '8'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Attendees:_#Customers Attended: {option}"

class AttendeesCustomersInvited(FormUserAttr):
    values = {'92091873_processed': '40', '93213298_processed': '8'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Attendees:_#Customers Invited: {option}"

class AttendeesLorillardPersonnel(FormUserAttr):
    values = {'92091873_processed': '10', '93213298_processed': '2'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Attendees:_#Lorillard Personnel: {option}"

class Attention(FormUserAttr):
    values = {'0011899960_processed': 'DR. HUGHES, MESSRS. ALAR, SANDEFUR, BLOTT, BUTLER, MIDDLETON, CHRISTENSEN, PEPPLES, SACHS FREEDMAN'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Attention: {option}"

class Attn(FormUserAttr):
    values = {'0060077689_processed': 'Mr. Steven Katz Route 4 and Adams Station North Brunswick, NJ 08901- 0623', '00920222_processed': 'Dr. Connie Stone', '00922237_processed': 'Dr. Harry Minnemeyer'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Attn:: {option}"

class AudienceConcentration(FormUserAttr):
    values = {'0011976929_processed': '90 % White - 10 % Black Age category 21 yrs. to 45 yrs.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Audience Concentration: {option}"

class Aug(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Aug: {option}"

class AuthNo(FormUserAttr):
    values = {'0060080406_processed': '5060'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Auth No.: {option}"

class AuthorizedSignature(FormUserAttr):
    values = {'88547278_88547279_processed': 'Applied Graphics Technologies 50 West 23rd Street, N.Y.C. 10010'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Authorized Signature:: {option}"

class AuthorizedBy(FormUserAttr):
    values = {'00851879_processed': 'Dr. Connie Stone'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Authorized by: {option}"

class AuthorizedTo(FormUserAttr):
    values = {'00851879_processed': 'Mr. Charles Burns'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Authorized to: {option}"

class Average(FormUserAttr):
    values = {'93213298_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Average: {option}"

class AverageCouponBuydownValueOnTargetedBrandsDoralBasicMonarchCambridgeGpc(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Average Coupon Buydown Value On Targeted Brands (Doral/ Basic/ Monarch/ Cambridge/ GPC: {option}"

class AverageCouponBuydownValueOnTargetedBrandsDoralBasicMonarchCambridgeGpcCartons(FormUserAttr):
    values = {'92039708_9710_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Average Coupon Buydown Value On Targeted Brands (Doral/ Basic/ Monarch/ Cambridge/ GPC_CARTONS ☐: {option}"

class AverageCouponBuydownValueOnTargetedBrandsDoralBasicMonarchCambridgeGpcPacks(FormUserAttr):
    values = {'92039708_9710_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Average Coupon Buydown Value On Targeted Brands (Doral/ Basic/ Monarch/ Cambridge/ GPC_PACKS ☐: {option}"

class BWApprovals(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's B&W APPROVALS: {option}"

class BWApprovalsDate(FormUserAttr):
    values = {'71190280_processed': '', '71366499_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's B&W APPROVALS_Date: {option}"

class BWApprovalsDepartment(FormUserAttr):
    values = {'71190280_processed': '', '71366499_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's B&W APPROVALS_Department: {option}"

class BWApprovalsSignature(FormUserAttr):
    values = {'71190280_processed': '', '71366499_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's B&W APPROVALS_Signature: {option}"

class BWOriginator(FormUserAttr):
    values = {'0011845203_processed': 'Mary D. Davis', '11875011_processed': 'H.L. Williams'}

    @staticmethod
    def nl_desc(option):
        return f"The user's B&W ORIGINATOR:: {option}"

class B(FormUserAttr):
    values = {'0012602424_processed': '', '01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's B.: {option}"

class BackCigarettes(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's BACK CIGARETTES: {option}"

class BackCigarettesComments(FormUserAttr):
    values = {'0060000813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's BACK CIGARETTES_Comments:: {option}"

class BackCigarettesCratering(FormUserAttr):
    values = {'0060000813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's BACK CIGARETTES_Cratering:: {option}"

class BackCigarettesHoleDepth(FormUserAttr):
    values = {'0060000813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's BACK CIGARETTES_Hole Depth:: {option}"

class BackCigarettesScorching(FormUserAttr):
    values = {'0060000813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's BACK CIGARETTES_Scorching:: {option}"

class Basic(FormUserAttr):
    values = {'81749056_9057_processed': '20 $ 2.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's BASIC: {option}"

class BatesNumberNotUsed(FormUserAttr):
    values = {'0001463448_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's BATES NUMBER NOT USED.: {option}"

class Beatty(FormUserAttr):
    values = {'0012602424_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's BEATTY: {option}"

class BetweenTheActs25MmButt(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's BETWEEN THE ACTS 25 %% mm. Butt: {option}"

class BetweenTheActs25MmButtMeanOfLast12Samples(FormUserAttr):
    values = {'0060094595_processed': "['1 .106', '0 .37', '35 .6', '3 .83', 'Basic', '23', '0', '1', '0']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's BETWEEN THE ACTS 25 %% mm. Butt_Mean of Last 12 Samples: {option}"

class BetweenTheActs25MmButtPresentSample(FormUserAttr):
    values = {'0060094595_processed': "['1 .089', '0. .34', '39. .7', '4 .26', 'Basic', '0', '5', '7', '12']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's BETWEEN THE ACTS 25 %% mm. Butt_Present Sample: {option}"

class Blend(FormUserAttr):
    values = {'00093726_processed': 'OGS', '00283813_processed': '', '81574683_processed': '1077-84'}

    @staticmethod
    def nl_desc(option):
        return f"The user's BLEND: {option}"

class BoldSubHead(FormUserAttr):
    values = {'80707440_7443_processed': '1st Prize $ 5,000 2nd Prize 2,000 3rd Prize 1,000 4th Prizes 500 fans will receive copies of "The Golden Anniversary of Pro- Football"'}

    @staticmethod
    def nl_desc(option):
        return f"The user's BOLD SUB- HEAD:: {option}"

class BookletCoupon(FormUserAttr):
    values = {'92039708_9710_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's BOOKLET/ COUPON: {option}"

class Box80S(FormUserAttr):
    values = {'81749056_9057_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's BOX 80's: {option}"

class Branch(FormUserAttr):
    values = {'716552_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's BRANCH: {option}"

class BrandSPromoted(FormUserAttr):
    values = {'91355841_processed': 'KOOL CIGARETTES'}

    @staticmethod
    def nl_desc(option):
        return f"The user's BRAND (S) PROMOTED:: {option}"

class BrandName(FormUserAttr):
    values = {'0060207528_processed': 'PALL MALL RED LIGHTS', '12603270_processed': "RICHLAND 100's", '93329540_processed': "SPECIAL 10' s"}

    @staticmethod
    def nl_desc(option):
        return f"The user's BRAND NAME:: {option}"

class BrandSmoked(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's BRAND SMOKED:: {option}"

class BrandSmokedAllOtherSmokers(FormUserAttr):
    values = {'0001209043_processed': "['30', '(125)']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's BRAND SMOKED:_All Other Smokers: {option}"

class BrandSmokedTestBrandSmokers(FormUserAttr):
    values = {'0001209043_processed': "['33', '(42)']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's BRAND SMOKED:_Test Brand Smokers: {option}"

class BrandSmoker(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's BRAND SMOKER: {option}"

class BrandSmokerAllOtherSmokers(FormUserAttr):
    values = {'0001438955_processed': "['7', '(205)']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's BRAND SMOKER_All Other Smokers: {option}"

class BrandSmokerTestBrandSmokers(FormUserAttr):
    values = {'0001438955_processed': "['6', '(17)']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's BRAND SMOKER_Test Brand Smokers: {option}"

class BrandProjectName(FormUserAttr):
    values = {'0011973451_processed': 'RICHLAND Kings (Soft Pack) -Duty Free (Phoenix)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's BRAND/PROJECT NAME:: {option}"

class Brands(FormUserAttr):
    values = {'0060173256_processed': 'Private Stock Carlton'}

    @staticmethod
    def nl_desc(option):
        return f"The user's BRANDS: {option}"

class BrandsSApplicable(FormUserAttr):
    values = {'91391286_processed': 'HARLEY- DAVIDSON', '91391310_processed': 'HARLEY- DAVIDSON', '91974562_processed': 'KENT', '93351929_93351931_processed': 'All Kent Family Packings'}

    @staticmethod
    def nl_desc(option):
        return f"The user's BRANDS(S) APPLICABLE: {option}"

class BrcCodesW81CartonOrderForm(FormUserAttr):
    values = {'00920294_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's BRC Codes w81 carton order form: {option}"

class BudgetNo(FormUserAttr):
    values = {'0060077689_processed': '', '00920222_processed': '', '00922237_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's BUDGET NO.: {option}"

class BudgetYear19(FormUserAttr):
    values = {'91104867_processed': '30,000 28,000 20,000 120,000'}

    @staticmethod
    def nl_desc(option):
        return f"The user's BUDGET YEAR 19: {option}"

class Buyer(FormUserAttr):
    values = {'0060077689_processed': 'M. Stock/ smm '}

    @staticmethod
    def nl_desc(option):
        return f"The user's BUYER: {option}"

class BwitSuggestion(FormUserAttr):
    values = {'0001456787_processed': '99 mm 72 mm 27 mm mm 58.5 mm 24.8 mm mm 32 mm 35 mm 13 % mg 858 mg 243.6 mg/ '}

    @staticmethod
    def nl_desc(option):
        return f"The user's BWIT Suggestion: {option}"

class By(FormUserAttr):
    values = {'0000990274_processed': '', '0012947358_processed': 'THE CORPORATION TRUST COMPANY'}

    @staticmethod
    def nl_desc(option):
        return f"The user's BY:: {option}"

class BackgroundProblemDefinition(FormUserAttr):
    values = {'71601299_processed': "1999 showed that imported cigarettes are recovering from the 1997 / 1998 economic crisis and we forecasted continuos growth over the company's plan period. BAT objective is to substantially increase its market share with growth coming primarily from its first priority brand: Dunhill Lights To achieve growth we consider fundamental to have a superior product in terms of acceptability among potential source of business as well as for our current franchise"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Background / Problem Definition: {option}"

class BalanceToSpend(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Balance to Spend: {option}"

class BalanceToSpendCapital(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Balance to Spend_CAPITAL: {option}"

class BalanceToSpendExpense(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Balance to Spend_EXPENSE: {option}"

class BaleNo(FormUserAttr):
    values = {'01122115_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Bale No.: {option}"

class BatchNumber(FormUserAttr):
    values = {'01197604_processed': 'II'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Batch Number:: {option}"

class BatchSize(FormUserAttr):
    values = {'00093726_processed': '50 lbs.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Batch Size: {option}"

class BeforeMeANotaryPublicPersonallyAppeared(FormUserAttr):
    values = {'91581919_processed': 'Holly Inzer'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Before me a Notary Public, personally appeared: {option}"

class Binding(FormUserAttr):
    values = {'88547278_88547279_processed': 'Leave in Full Sheets'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Binding: {option}"

class Brand(FormUserAttr):
    values = {'0001209043_processed': 'SALEM (RJR)', '0001438955_processed': 'BELAIR', '0012178355_processed': 'ELI CUTTER KS', '0060068489_processed': 'LUCKY STRIKE LOW Tar Filters Box- 100%', '0060080406_processed': 'BULL DURHAM Filter Box BULL DURHAM Lights BOX', '01408099_01408101_processed': '', '12825369_processed': 'Misty', '71190280_processed': 'KOOL Natural', '71366499_processed': 'BKOOL', '88057519_processed': "Satin Filter 100's Satin Menthol 100's"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Brand: {option}"

class BrandStyle(FormUserAttr):
    values = {'0060308251_processed': "CARLTON 100's FMSP"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Brand & Style: {option}"

class BrandSApplicable(FormUserAttr):
    values = {'87533049_processed': 'TRUE'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Brand (s) Applicable: {option}"

class BrandS(FormUserAttr):
    values = {'0060029036_processed': 'Camel/ Winston'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Brand(s): {option}"

class BriefDescription(FormUserAttr):
    values = {'0060029036_processed': "2 Joe's Place Exhibits for use at Winston Cup, Winston Drag and Camel Super Bike Events."}

    @staticmethod
    def nl_desc(option):
        return f"The user's Brief Description: {option}"

class BriefNumber(FormUserAttr):
    values = {'71563825_processed': '#'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Brief Number: {option}"

class Bright(FormUserAttr):
    values = {'0000999294_processed': '4.45 3.43 4.85 3.02 2.78 3.21 3.95'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Bright: {option}"

class BrightKsWhiteTipping(FormUserAttr):
    values = {'0000999294_processed': '5. 5 .55 13. 5 .841'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Bright KS white tipping-: {option}"

class BudgetCheck(FormUserAttr):
    values = {'0012529284_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Budget Check: {option}"

class BudgetCode(FormUserAttr):
    values = {'0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Budget Code: {option}"

class Budgeted(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Budgeted:: {option}"

class BudgetedNo(FormUserAttr):
    values = {'0001463282_processed': '', '11508234_processed': 'X', '71202511_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Budgeted:_No: {option}"

class BudgetedYes(FormUserAttr):
    values = {'0001463282_processed': 'x', '11508234_processed': '', '71202511_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Budgeted:_Yes: {option}"

class BusinessTelephone(FormUserAttr):
    values = {'0060091229_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Business Telephone:: {option}"

class BusinessUnit(FormUserAttr):
    values = {'71341634_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Business Unit: {option}"

class ByCity(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's By City:: {option}"

class ByCityBQuilla(FormUserAttr):
    values = {'71563825_processed': 'KOOL Parent regular smokers 50% -alternate smokers 50%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's By City:_B/ quilla:: {option}"

class ByCityBogot(FormUserAttr):
    values = {'71563825_processed': 'KOOL Parent regular smokers 50% -alternate smokers 50%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's By City:_Bogotá:: {option}"

class ByCityMedellin(FormUserAttr):
    values = {'71563825_processed': 'KOOL Parent regular smokers 50% -alternate smokers 50%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's By City:_Medellin:: {option}"

class C(FormUserAttr):
    values = {'81310636_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's C @: {option}"

class Cable(FormUserAttr):
    values = {'01150773_01150774_processed': 'COVLING'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CABLE: {option}"

class CanTimeBeSparedForCompletion(FormUserAttr):
    values = {'0060302201_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CAN TIME BE SPARED FOR COMPLETION?: {option}"

class Capital(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CAPITAL: {option}"

class Capri(FormUserAttr):
    values = {'0011505151_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CAPRI: {option}"

class CarcinogenOsha(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CARCINOGEN (OSHA): {option}"

class CarcinogenOther(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CARCINOGEN (OTHER): {option}"

class CarryoverTo1988(FormUserAttr):
    values = {'0011505151_processed': '14,165'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CARRYOVER TO 1988: {option}"

class Cartons(FormUserAttr):
    values = {'81749056_9057_processed': '3.00 $ 2.00 $ 3.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CARTONS: {option}"

class Casing(FormUserAttr):
    values = {'00093726_processed': 'OGS', '00283813_processed': '', '81574683_processed': '7773'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CASING: {option}"

class Cf(FormUserAttr):
    values = {'0011859695_processed': 'cb'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CF:: {option}"

class ChainAcceptance(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHAIN ACCEPTANCE:: {option}"

class ChainAcceptanceExcellent(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHAIN ACCEPTANCE:_EXCELLENT: {option}"

class ChainAcceptanceFair(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHAIN ACCEPTANCE:_FAIR: {option}"

class ChainAcceptanceGood(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHAIN ACCEPTANCE:_GOOD: {option}"

class ChainAcceptancePoor(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHAIN ACCEPTANCE:_POOR: {option}"

class Chargeback(FormUserAttr):
    values = {'0001129658_processed': '4162/ 158'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHARGEBACK:: {option}"

class ChemicalDescription(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL DESCRIPTION: {option}"

class ChemicalDescriptionCas(FormUserAttr):
    values = {'0060024314_processed': '108 -05 -4'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL DESCRIPTION_CAS#: {option}"

class ChemicalDescriptionChemicalFormula(FormUserAttr):
    values = {'0060024314_processed': 'Vinyl Acetate'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL DESCRIPTION_CHEMICAL FORMULA:: {option}"

class ChemicalDescriptionDescription(FormUserAttr):
    values = {'0060024314_processed': 'Liquid Adhesive'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL DESCRIPTION_DESCRIPTION:: {option}"

class ChemicalDescriptionManufacturer(FormUserAttr):
    values = {'0060024314_processed': 'H. B. Fuller Company'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL DESCRIPTION_MANUFACTURER:: {option}"

class ChemicalDescriptionMsdsOnFileCircleOne(FormUserAttr):
    values = {'0060024314_processed': 'Yes'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL DESCRIPTION_MSDS ON FILE? (Circle One):: {option}"

class ChemicalDescriptionPercentActivesNonWater(FormUserAttr):
    values = {'0060024314_processed': '.5%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL DESCRIPTION_PERCENT ACTIVES (Non -water):: {option}"

class ChemicalDescriptionPhone(FormUserAttr):
    values = {'0060024314_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL DESCRIPTION_PHONE: {option}"

class ChemicalDescriptionProductChemicalName(FormUserAttr):
    values = {'0060024314_processed': 'Fuller G2315 DC'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL DESCRIPTION_PRODUCT (CHEMICAL) NAME:: {option}"

class ChemicalDescriptionProductClassificationCircleDne(FormUserAttr):
    values = {'0060024314_processed': 'Organic'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL DESCRIPTION_PRODUCT CLASSIFICATION (Circle Dne):: {option}"

class ChemicalPurity(FormUserAttr):
    values = {'00837285_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL PURITY: {option}"

class ChemicalUsage(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL USAGE: {option}"

class ChemicalUsage1993AnnualUsageLbs(FormUserAttr):
    values = {'0060024314_processed': '74880'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL USAGE_1993 ANNUAL USAGE (LBS.):: {option}"

class ChemicalUsage1993AvgMonthlyUsageLbs(FormUserAttr):
    values = {'0060024314_processed': '6240'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL USAGE_1993 AVG. MONTHLY USAGE (LBS.): {option}"

class ChemicalUsageApplicationCircleOneAndBrieflyDescribe(FormUserAttr):
    values = {'0060024314_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CHEMICAL USAGE_APPLICATION (Circle One and Briefly Describe):: {option}"

class CigaretteReportForm(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM: {option}"

class CigaretteReportFormTar(FormUserAttr):
    values = {'0060270727_processed': '16 mg'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_\"TAR\":: {option}"

class CigaretteReportForm1YearCovered(FormUserAttr):
    values = {'0060308461_processed': '1985'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_(1) YEAR COVERED:: {option}"

class CigaretteReportForm10VarietyUnitSales(FormUserAttr):
    values = {'0060308461_processed': '238,282'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_(10) VARIETY UNIT SALES:: {option}"

class CigaretteReportForm11VarietyDollarSales(FormUserAttr):
    values = {'0060308461_processed': '6,117,778'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_(11) VARIETY DOLLAR SALES:: {option}"

class CigaretteReportForm12FirstSalesDate(FormUserAttr):
    values = {'0060308461_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_(12) FIRST SALES DATE:: {option}"

class CigaretteReportForm2BrandFamilyName(FormUserAttr):
    values = {'0060308461_processed': 'LUCKY STRIKE'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_(2) BRAND FAMILY NAME:: {option}"

class CigaretteReportForm3VarietyDescription(FormUserAttr):
    values = {'0060308461_processed': 'Low tar, king size, filter, hard pack'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_(3) VARIETY DESCRIPTION: {option}"

class CigaretteReportForm4ProductLength(FormUserAttr):
    values = {'0060308461_processed': 'King'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_(4) PRODUCT LENGTH:: {option}"

class CigaretteReportForm5Filter(FormUserAttr):
    values = {'0060308461_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_(5) FILTER:: {option}"

class CigaretteReportForm7Menthol(FormUserAttr):
    values = {'0060308461_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_(7) MENTHOL:: {option}"

class CigaretteReportForm8PackSizeSold(FormUserAttr):
    values = {'0060308461_processed': "20's"}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_(8) PACK SIZE SOLD:: {option}"

class CigaretteReportForm9Tar(FormUserAttr):
    values = {'0060308461_processed': '11 mg'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_(9) \"TAR\":: {option}"

class CigaretteReportFormBrandFamilyName(FormUserAttr):
    values = {'0060270727_processed': 'MALIBU'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_BRAND FAMILY NAME:: {option}"

class CigaretteReportFormFilter(FormUserAttr):
    values = {'0060270727_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_FILTER: {option}"

class CigaretteReportFormFirstSalesDate(FormUserAttr):
    values = {'0060270727_processed': '10/ 26/ 87'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_FIRST SALES DATE:: {option}"

class CigaretteReportFormHardPack(FormUserAttr):
    values = {'0060270727_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_HARD PACK:: {option}"

class CigaretteReportFormLastSalesDate(FormUserAttr):
    values = {'0060270727_processed': '', '0060308461_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_LAST SALES DATE:: {option}"

class CigaretteReportFormMenthol(FormUserAttr):
    values = {'0060270727_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_MENTHOL:: {option}"

class CigaretteReportFormNicotine(FormUserAttr):
    values = {'0060270727_processed': '1. 3 mg (Appendix C)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_NICOTINE:: {option}"

class CigaretteReportFormNonfilter(FormUserAttr):
    values = {'0060308461_processed': '(check one)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_NONFILTER:: {option}"

class CigaretteReportFormNonmenthol(FormUserAttr):
    values = {'0060270727_processed': 'X (check one)', '0060308461_processed': 'X (check one)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_NONMENTHOL:: {option}"

class CigaretteReportFormPackSizeSold(FormUserAttr):
    values = {'0060270727_processed': "20' s"}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_PACK SIZE SOLD:: {option}"

class CigaretteReportFormProductLength(FormUserAttr):
    values = {'0060270727_processed': 'King Size'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_PRODUCT LENGTH:: {option}"

class CigaretteReportFormSoftPack(FormUserAttr):
    values = {'0060270727_processed': 'X (check one)', '0060308461_processed': '(check one)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_SOFT PACK:: {option}"

class CigaretteReportFormVarietyDescription(FormUserAttr):
    values = {'0060270727_processed': 'King Size, Filter'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_VARIETY DESCRIPTION:: {option}"

class CigaretteReportFormVarietyDollarSales(FormUserAttr):
    values = {'0060270727_processed': '59, 791'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_VARIETY DOLLAR SALES:: {option}"

class CigaretteReportFormVarietyUnitSales(FormUserAttr):
    values = {'0060270727_processed': '1, 800'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_VARIETY UNIT SALES:: {option}"

class CigaretteReportFormYearCovered(FormUserAttr):
    values = {'0060270727_processed': '1987'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTE REPORT FORM_YEAR COVERED:: {option}"

class Cigarettes(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTES: {option}"

class Cigarettes627647(FormUserAttr):
    values = {'0001239897_processed': 'Current VICEROY B4'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTES_#627/ 647 -: {option}"

class Cigarettes647627(FormUserAttr):
    values = {'0001239897_processed': 'Current VICEROY 84 except with 25% of the propylene glycol replaced with SORBITOL.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIGARETTES_#647/ #627 -: {option}"

class Circulation(FormUserAttr):
    values = {'91391286_processed': '25,461', '91391310_processed': '2,852,100 - 47.200', '91974562_processed': '', '93351929_93351931_processed': '1, 221, 000'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CIRCULATION: {option}"

class City(FormUserAttr):
    values = {'0001476912_processed': 'Los  Chicago 0.0 3.3', '71341634_processed': '', '87682908_processed': '', '88057519_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CITY: {option}"

class CityState(FormUserAttr):
    values = {'0060262650_processed': 'Washington DC 20006'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CITY STATE, : {option}"

class CityStateZip(FormUserAttr):
    values = {'0060262650_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CITY, STATE, ZIP: {option}"

class Class(FormUserAttr):
    values = {'00837285_processed': 'ACID BASE SALT OTHER'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CLASS: {option}"

class Client(FormUserAttr):
    values = {'0060136394_processed': 'THE AMERICAN TOBACCO COMPANY (LUCKY STRIKE)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CLIENT: {option}"

class ClubCashCarryEtc(FormUserAttr):
    values = {'92081358_1359_processed': '*Jobber/ Membership'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CLUB, CASH & CARRY, ETC...):: {option}"

class Code(FormUserAttr):
    values = {'00920222_processed': '', '00922237_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CODE: {option}"

class CommentOnPlant(FormUserAttr):
    values = {'12825369_processed': '(Condition, Structures, Painting Ability, Lighting, Cooperation, etc.) The plant is well maintained and covers all parts of the market. Lamar looks like a good citizen here, keeping a good- looking public and carrying lot operation. doing service, a of local advertisers.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMMENT ON PLANT:: {option}"

class Comments(FormUserAttr):
    values = {'0001129658_processed': '', '0001209043_processed': 'Tested among a half sample of smokers. Sub- group scores subject to wide variation because of small sample size and should be averaged across several ads for meaningful infor- mation.', '0001476912_processed': 'This commercial was tested in color.', '0060302201_processed': 'been with applicability may provide a technique.', '00837285_processed': 'pH- The pH of a 50% concentration of A32 in a 52.6% dioxane/water solution was calculated to be 2.92 at 22°C according to the extra- polation procedures by Dr. P. D. Schickedantz, Lorillard Research Center Accession No. 1662, Reference OR 83- 125. Solubility (See SOP for Biological Solutions) Oral- 5g A32 forms a suspension with stirring in 10 ml 1% Tween 80 at room temperature. Reference OR 72- 151. Acute Cardiovascular- Mix 2 mg A32 with 0.2 ml 80% propylene glycol and grind lightly. Add 0.8 ml saline solution. A32 is a suspension in this mixture at room temperature. Reference OR 72- 152.', '00838511_00838525_processed': 'This carbocyclic keto alcohol was placed in estimated toxicity class II due to the direct attachment of the ketone to the cyclic nucleus.', '01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMMENTS: {option}"

class CommentsByManagerOrDirector(FormUserAttr):
    values = {'0060302201_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMMENTS BY MANAGER OR DIRECTOR: {option}"

class Commitments(FormUserAttr):
    values = {'0012602424_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMMITMENTS: {option}"

class Committed(FormUserAttr):
    values = {'0012602424_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMMITTED: {option}"

class Company(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPANY): {option}"

class CompetitiveActivitiesAndPromotions(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPETITIVE ACTIVITIES AND PROMOTIONS: {option}"

class CompetitiveActivitiesAndPromotionsBrandSPromoted(FormUserAttr):
    values = {'91356315_processed': 'MARLBORO CIGARETTES'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPETITIVE ACTIVITIES AND PROMOTIONS_BRAND (S) PROMOTED:: {option}"

class CompetitiveActivitiesAndPromotionsCc(FormUserAttr):
    values = {'91356315_processed': "['A. H. TISCH', 'M. A. PETERSON', 'R. H. ORCUTT', 'M. L. ORLOWSKY', 'L. GORDON', 'J. P. MASTANDREA', 'G. R. TELFORD', 'N. P. RUFFALO', 'R. G. RYAN', 'P. J. McCANN', 'P. J. McCANN', 'T. L. ACHEY', 'A. J. GIACOIO', 'J. J. TATULLI', 'L. H. LAKERSH', 'J. R. SLATER', 'S. T. JONES', 'R. S. GOLDBRENNER', 'S. F. SMITH']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPETITIVE ACTIVITIES AND PROMOTIONS_CC:: {option}"

class CompetitiveActivitiesAndPromotionsDate(FormUserAttr):
    values = {'91356315_processed': '4/ 26/ 91'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPETITIVE ACTIVITIES AND PROMOTIONS_DATE:: {option}"

class CompetitiveActivitiesAndPromotionsHowWidespread(FormUserAttr):
    values = {'91356315_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPETITIVE ACTIVITIES AND PROMOTIONS_HOW WIDESPREAD?: {option}"

class CompetitiveActivitiesAndPromotionsManufacturer(FormUserAttr):
    values = {'91356315_processed': 'PHILIP MORRIS'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPETITIVE ACTIVITIES AND PROMOTIONS_MANUFACTURER:: {option}"

class CompetitiveActivitiesAndPromotionsOtherComments(FormUserAttr):
    values = {'91356315_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPETITIVE ACTIVITIES AND PROMOTIONS_OTHER COMMENTS:: {option}"

class CompetitiveActivitiesAndPromotionsReportedBy(FormUserAttr):
    values = {'91356315_processed': 'VAL THURMAN, DIVISION MANAGER, LOUISVILLE, KY'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPETITIVE ACTIVITIES AND PROMOTIONS_REPORTED BY:: {option}"

class CompetitiveActivitiesAndPromotionsSourceOfInformation(FormUserAttr):
    values = {'91356315_processed': 'SHORT STOP FOOD MARTS. LOUISVILLE, KY'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPETITIVE ACTIVITIES AND PROMOTIONS_SOURCE OF INFORMATION:: {option}"

class CompetitiveActivitiesAndPromotionsTypeOfPromotion(FormUserAttr):
    values = {'91356315_processed': 'CARTON PROMOTION SWEEPSTAKES (SEE ATTACHMENTS)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPETITIVE ACTIVITIES AND PROMOTIONS_TYPE OF PROMOTION:: {option}"

class CompetitivePromotionalActivity(FormUserAttr):
    values = {'92039708_9710_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPETITIVE PROMOTIONAL ACTIVITY: {option}"

class CompleteEitherAOrBBelow(FormUserAttr):
    values = {'92314414_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPLETE EITHER A OR B BELOW:: {option}"

class Completion(FormUserAttr):
    values = {'0000990274_processed': '', '0011906503_processed': '11 88'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPLETION: {option}"

class Compound(FormUserAttr):
    values = {'00040534_processed': '3-Hydroxy-3-methylbutanoic acid (Tur 13)', '00836244_processed': '2, 4- Dihydroxypyridine', '00851772_1780_processed': 'Valerian Fluid Extract', '00865872_processed': '[] HEAT [MOISTURE] [] OTHER', '01073843_processed': 'Diethyl 3, 3-Dimethyl-2-oxo-1, 4-cyclopentanedicarboxylate', '87672097_processed': 'Mapleine'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND: {option}"

class CompoundUsPlate(FormUserAttr):
    values = {'00836244_processed': '500 250 125'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND (US plate): {option}"

class CompoundCode(FormUserAttr):
    values = {'81310636_processed': 'B83'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND CODE: {option}"

class CompoundName(FormUserAttr):
    values = {'00838511_00838525_processed': '2-Hydroxycyclododecanone', '81310636_processed': 'Proprietary Mixture'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND NAME: {option}"

class CompoundSensitive(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND SENSITIVE: {option}"

class CompoundSensitiveTo(FormUserAttr):
    values = {'00837285_processed': 'AIR HEAT LIGHT MOISTURE OTHER'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND SENSITIVE TO: {option}"

class CompoundSensitiveAir(FormUserAttr):
    values = {'00836816_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND SENSITIVE_☐ AIR: {option}"

class CompoundSensitiveHeat(FormUserAttr):
    values = {'00836816_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND SENSITIVE_☐ HEAT: {option}"

class CompoundSensitiveMoisture(FormUserAttr):
    values = {'00836816_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND SENSITIVE_☐ MOISTURE: {option}"

class CompoundSensitiveOther(FormUserAttr):
    values = {'00836816_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND SENSITIVE_☐ OTHER: {option}"

class CompoundVehicle(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND VEHICLE: {option}"

class CompoundVehicleOther(FormUserAttr):
    values = {'87672097_processed': "['☑', 'pure solution']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND VEHICLE_OTHER: {option}"

class CompoundVehicleMethylCellulose(FormUserAttr):
    values = {'87672097_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND VEHICLE_☐ % METHYL CELLULOSE: {option}"

class CompoundVehicleCornOil(FormUserAttr):
    values = {'87672097_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND VEHICLE_☐ CORN OIL: {option}"

class CompoundVehicleSaline(FormUserAttr):
    values = {'87672097_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND VEHICLE_☐ SALINE: {option}"

class CompoundPlates(FormUserAttr):
    values = {'01073843_processed': '25 12.5 6.25'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COMPOUND plates: {option}"

class Concentration1Mgimit(FormUserAttr):
    values = {'00836244_processed': '.5'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONCENTRATION 1mgimit: {option}"

class ConcentrationMgMl(FormUserAttr):
    values = {'01073843_processed': '.025'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONCENTRATION mg/ml: {option}"

class Conclusion(FormUserAttr):
    values = {'00040534_processed': 'This compound appears to act as a CNS depressant with symptons of respiratory depression, constriction of blood vessels, and in- activity. Survivors recovered in 48 hours. The recommended safe dose for a single trial by inhalation in man is 0.3 mg.', '00836244_processed': 'This compound is judged non mutagenic in this test system.', '01073843_processed': 'This compound is judged non - mutagenic in this test system.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONCLUSION: {option}"

class Confidential(FormUserAttr):
    values = {'660978_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONFIDENTIAL: {option}"

class ConsumerAcceptance(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONSUMER ACCEPTANCE:: {option}"

class ConsumerAcceptanceExcellent(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONSUMER ACCEPTANCE:_EXCELLENT: {option}"

class ConsumerAcceptanceFair(FormUserAttr):
    values = {'92094746_processed': 'x', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONSUMER ACCEPTANCE:_FAIR: {option}"

class ConsumerAcceptanceGood(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONSUMER ACCEPTANCE:_GOOD: {option}"

class ConsumerAcceptancePoor(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONSUMER ACCEPTANCE:_POOR: {option}"

class ConsumerOffer(FormUserAttr):
    values = {'91939637_processed': '$3 Off Store Redeemable Carton Coupon'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONSUMER OFFER:: {option}"

class Contingency(FormUserAttr):
    values = {'0060068489_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONTINGENCY: {option}"

class Contract(FormUserAttr):
    values = {'0060207528_processed': 'A- 530- 1059'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONTRACT:: {option}"

class ControlAfvertantsPerPlate005MlSolvent(FormUserAttr):
    values = {'00836244_processed': '4 .67 8 .00 123 .00 135 .33 3 .33.33 16 .00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONTROL AFVERTANTS PER PLATE (0.05 ml SOLVENT): {option}"

class ControlRevertantsPerPlateToonMiSolventi(FormUserAttr):
    values = {'01073843_processed': '9.67 14.00 118.00 127.00 9.00 21.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CONTROL REVERTANTS PER PLATE TOON MI SOLVENTI: {option}"

class CostOrRetailPricing(FormUserAttr):
    values = {'0011973451_processed': 'TBD'}

    @staticmethod
    def nl_desc(option):
        return f"The user's COST OR RETAIL PRICING:: {option}"

class CostSummary(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's COST SUMMARY: {option}"

class CostSummaryEstAnnualProductCostChange(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COST SUMMARY_Est. Annual Product Cost Change: {option}"

class CostSummaryObsoleteMaterialCost(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COST SUMMARY_Obsolete Material Cost: {option}"

class CostSummarySpecialEquipmentMaterialCost(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's COST SUMMARY_Special Equipment/ Material Cost: {option}"

class Cqa(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CQA: {option}"

class Cumulative(FormUserAttr):
    values = {'0011505151_processed': '77.900', '12052385_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CUMULATIVE: {option}"

class CurrentBalAvailable(FormUserAttr):
    values = {'0012602424_processed': '17 195. 66'}

    @staticmethod
    def nl_desc(option):
        return f"The user's CURRENT BAL. AVAILABLE:: {option}"

class CustomerShippingNumber(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's CUSTOMER SHIPPING NUMBER: {option}"

class CapitalBudget(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Capital Budget: {option}"

class CharNo(FormUserAttr):
    values = {'71341634_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Char No: {option}"

class CharacteristicTested(FormUserAttr):
    values = {'0060094595_processed': 'Smoke Analysis urn Test Dynamic -Time in seconds -% Burned Completely'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Characteristic Tested: {option}"

class ChargeCode(FormUserAttr):
    values = {'0060173256_processed': 'CAR- MMT- DSP PRV- MMT- DSP'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Charge Code: {option}"

class ChargeToSection(FormUserAttr):
    values = {'71341634_processed': 'PER ATTACHED'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Charge To Section:: {option}"

class CheckColumnsBelowOnlyIfBillMakesARectAppropriationOrAffectASumSufficientAppropriation(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Check columns below only if bill makes a rect appropriation or affect a sum sufficient appropriation.: {option}"

class ChemAbstr(FormUserAttr):
    values = {'81310636_processed': 'N/ A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Chem Abstr#: {option}"

class Chicago(FormUserAttr):
    values = {'0001476912_processed': '8/8'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Chicago:: {option}"

class Cicarettes(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cicarettes: {option}"

class CicarettesAirDilution(FormUserAttr):
    values = {'81574683_processed': 'NA'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cicarettes_Air Dilution: {option}"

class CicarettesCircumference(FormUserAttr):
    values = {'81574683_processed': '24.8 mm'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cicarettes_Circumference: {option}"

class CicarettesGlueRoller(FormUserAttr):
    values = {'81574683_processed': 'Mk II 85'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cicarettes_Glue Roller: {option}"

class CicarettesLength(FormUserAttr):
    values = {'81574683_processed': '21.0 mm'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cicarettes_Length: {option}"

class CicarettesMaker(FormUserAttr):
    values = {'81574683_processed': 'MK 9'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cicarettes_Maker: {option}"

class CicarettesPaper(FormUserAttr):
    values = {'81574683_processed': 'E- 554'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cicarettes_Paper: {option}"

class CicarettesTipPaper(FormUserAttr):
    values = {'81574683_processed': "['51mm cork- Ecusta', 'TOD 01042-4 lines perf.']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cicarettes_Tip. Paper: {option}"

class CicarettesTipPaperPor(FormUserAttr):
    values = {'81574683_processed': '4260'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cicarettes_Tip. Paper Por.: {option}"

class CicarettesWeight(FormUserAttr):
    values = {'81574683_processed': '96.0 g/100'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cicarettes_Weight: {option}"

class Cigarette(FormUserAttr):
    values = {'0060007216_processed': '84 x 24.9 mm circum- ference.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cigarette: {option}"

class CigaretteDescription(FormUserAttr):
    values = {'0001485288_processed': 'KS 1 mg grooved product using 4. 3/ 37 filter material. Cigarette code 244131'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cigarette Description: {option}"

class CigarettesBrand(FormUserAttr):
    values = {'00283813_processed': 'OLD GOLD STRAIGHT'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cigarettes:_Brand: {option}"

class CigarettesCircumference(FormUserAttr):
    values = {'00283813_processed': '25. 3 mm.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cigarettes:_Circumference: {option}"

class CigarettesDraw(FormUserAttr):
    values = {'00283813_processed': 'OLD GOLD STRAIGHT'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cigarettes:_Draw: {option}"

class CigarettesFilterLength(FormUserAttr):
    values = {'00283813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cigarettes:_Filter Length: {option}"

class CigarettesFirmness(FormUserAttr):
    values = {'00283813_processed': 'OLD GOLD STRAIGHT'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cigarettes:_Firmness: {option}"

class CigarettesLength(FormUserAttr):
    values = {'00283813_processed': '85 mm.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cigarettes:_Length: {option}"

class CigarettesPaper(FormUserAttr):
    values = {'00283813_processed': 'Ecusta 556'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cigarettes:_Paper: {option}"

class CigarettesPrint(FormUserAttr):
    values = {'00283813_processed': 'OLD GOLD STRAIGHT'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cigarettes:_Print: {option}"

class CigarettesTippingPaper(FormUserAttr):
    values = {'00283813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cigarettes:_Tipping Paper: {option}"

class CigarettesWeight(FormUserAttr):
    values = {'00283813_processed': 'OLD GOLD STRAIGHT'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cigarettes:_Weight: {option}"

class CigarettesMaker(FormUserAttr):
    values = {'00093726_processed': 'AMF'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cigarettes_Maker: {option}"

class CircOfRod(FormUserAttr):
    values = {'01122115_processed': '24'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Circ of Rod: {option}"

class CirculationQuantity(FormUserAttr):
    values = {'0011974919_processed': '300'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Circulation Quantity:: {option}"

class Circunference(FormUserAttr):
    values = {'81574683_processed': '24.7mm'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Circunference: {option}"

class CityTown(FormUserAttr):
    values = {'0011976929_processed': 'Dundee'}

    @staticmethod
    def nl_desc(option):
        return f"The user's City/ Town:: {option}"

class ClientContact(FormUserAttr):
    values = {'71601299_processed': 'Alberto Marcheggiano Kyu Yeon Hwang'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Client Contact: {option}"

class ClientGroup(FormUserAttr):
    values = {'71601299_processed': 'BAT Korea'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Client Group: {option}"

class ClientName(FormUserAttr):
    values = {'89386032_processed': 'Borriston Laboratories, Inc.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Client Name: {option}"

class ClientStudyNo(FormUserAttr):
    values = {'89386032_processed': '1419A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Client Study No.: {option}"

class Color(FormUserAttr):
    values = {'01122115_processed': 'White'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Color: {option}"

class ColumnInches(FormUserAttr):
    values = {'91581919_processed': 'Insert'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Column Inches: {option}"

class CombWrap(FormUserAttr):
    values = {'81574683_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Comb. Wrap: {option}"

class CombWrapPor(FormUserAttr):
    values = {'81574683_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Comb. Wrap Por.: {option}"

class Commercial(FormUserAttr):
    values = {'0001476912_processed': 'LAKE- NEW PACK: 40 (with BELAIR Badmin- ton: 20)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Commercial:: {option}"

class CommittedToDate(FormUserAttr):
    values = {'0012529284_processed': '1, 652, 955. 53', '12603270_processed': '3,357,545'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Committed To Date:: {option}"

class CommittedToDateCurrentYear(FormUserAttr):
    values = {'0012529295_processed': '1, 233, 308. 08', '11508234_processed': '146,925'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Committed to Date: (Current Year): {option}"

class CommitteeMeeting(FormUserAttr):
    values = {'0060036622_processed': '8/ 26'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Committee meeting : {option}"

class CompensationReceivedLobbying(FormUserAttr):
    values = {'0001477983_processed': '$'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Compensation received lobbying:: {option}"

class Competitive(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Competitive: {option}"

class CompetitiveProposalsObtained(FormUserAttr):
    values = {'11508234_processed': 'Only two bidders because third supplier has not yet signed B & W contract.', '71202511_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Competitive Proposals Obtained:: {option}"

class CompetitiveProposalsObtainedCost(FormUserAttr):
    values = {'0001463282_processed': "['$ 33,675 + 10% Est.', '$ 35,000 + 10 % Est.']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Competitive Proposals Obtained:_Cost: {option}"

class CompetitiveProposalsObtainedCostPerInterview(FormUserAttr):
    values = {'0001463282_processed': "['$ 84.2', '$ 87.5']", '0012529295_processed': "['$47 .22', '$74 .67']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Competitive Proposals Obtained:_Cost Per Interview: {option}"

class CompetitiveProposalsObtainedEst(FormUserAttr):
    values = {'0001463282_processed': "['$ 2000', '$ 2000']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Competitive Proposals Obtained:_Est.: {option}"

class CompetitiveProposalsObtainedEstTravel(FormUserAttr):
    values = {'0012529295_processed': "['-0-', '-O-']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Competitive Proposals Obtained:_Est. Travel: {option}"

class CompetitiveProposalsObtainedSupplier(FormUserAttr):
    values = {'0001463282_processed': "['Kapuler', 'Market Facts']", '0012529295_processed': "['Kapuler Market Research', 'Market Facts, Inc.']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Competitive Proposals Obtained:_Supplier: {option}"

class CompetitiveProposalsObtainedTotalCost(FormUserAttr):
    values = {'0001463282_processed': "['$ 35,675', '$ 37000']", '0012529295_processed': "['$70 ,825 + - 10%', '$112 000 +/ - 10%']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Competitive Proposals Obtained:_Total Cost: {option}"

class Competitive25PgWSorbitol647627(FormUserAttr):
    values = {'0001239897_processed': "['-4', '+7*', '+26*']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Competitive_25% PG w/ SORBITOL (#647/ 627): {option}"

class CompetitiveCurrentViceroy84647647(FormUserAttr):
    values = {'0001239897_processed': "['-13', '-7', '+14']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Competitive_Current VICEROY 84 (#647/ 647: {option}"

class CompetitorsBrandsMild7LightsSmokers(FormUserAttr):
    values = {'71601299_processed': '150 Males, 25 ~ 39 years old, ABC+ who live'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Competitors Brands - Mild7 Lights Smokers: {option}"

class CompleteWeight(FormUserAttr):
    values = {'01122115_processed': '99 .2 gms.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Complete Weight: {option}"

class CompletionDate(FormUserAttr):
    values = {'0001485288_processed': '6/ 25/ 81'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Completion Date: {option}"

class Con(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Con: {option}"

class Confirmation(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Confirmation:: {option}"

class ConfirmationName(FormUserAttr):
    values = {'0001129658_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Confirmation:_Name:: {option}"

class ConfirmationNo(FormUserAttr):
    values = {'0001129658_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Confirmation:_No:: {option}"

class ConfirmationYes(FormUserAttr):
    values = {'0001129658_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Confirmation:_Yes: {option}"

class ConsiderationDeferredUntil(FormUserAttr):
    values = {'0060036622_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Consideration deferred until: {option}"

class ConsumerSegmentS(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Consumer Segment(s):: {option}"

class ConsumerSegmentSBySel(FormUserAttr):
    values = {'71563825_processed': 'AB1 (100%)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Consumer Segment(s):_BY SEL:: {option}"

class ConsumerSegmentSByAge(FormUserAttr):
    values = {'71563825_processed': '18 -29 (100%)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Consumer Segment(s):_By age:: {option}"

class ConsumerSegmentSFemale(FormUserAttr):
    values = {'71563825_processed': '40%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Consumer Segment(s):_Female:: {option}"

class ConsumerSegmentSMale(FormUserAttr):
    values = {'71563825_processed': '60%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Consumer Segment(s):_Male:: {option}"

class ContactNameTelephone(FormUserAttr):
    values = {'0011976929_processed': 'Ms. Joy Weathers (Sales) 312/ 426 - 8000'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Contact (Name/ Telephone):: {option}"

class Contact(FormUserAttr):
    values = {'0011859695_processed': 'Larry Odum', '0060255888_processed': 'Mr. Mary Goldsmith'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Contact:: {option}"

class ContractNo(FormUserAttr):
    values = {'0060029036_processed': '4011 00 00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Contract No.: {option}"

class ContractSubject(FormUserAttr):
    values = {'0060029036_processed': "Joe's Place Exhibits"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Contract Subject:: {option}"

class ContractualOrAgreedFee(FormUserAttr):
    values = {'0001477983_processed': '$'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Contractual or agreed fee:: {option}"

class Contribution(FormUserAttr):
    values = {'0060036622_processed': '☑'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Contribution: {option}"

class Copies(FormUserAttr):
    values = {'0011899960_processed': 'T. HUMBER, M. BATEMAN'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Copies: {option}"

class CopiesToTheFollowing(FormUserAttr):
    values = {'00040534_processed': 'Dr. H. J. Minnemeyer Ms. L. B. Gray', '00836244_processed': 'Dr. H. J. Minnemeyer Ms. L. B. Gray', '01073843_processed': 'H. J. Minnemeyer L. B. Gray', '87672097_processed': 'H. J. Minnemeyer L. B. Gray'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Copies to the Following:: {option}"

class CopiesTo(FormUserAttr):
    values = {'0001485288_processed': 'Factory Cost Dept. Writer Development Center Sue Livesay', '01122115_processed': 'Dr. C. O. Jensen Mr. R. A. Wagner Mr. J. Berner Dr. A. W. Spears', '716552_processed': 'J. F. Banks C. Lamb C. L. Domeck Webb L. C. Lanham Branch QC Branch Supply'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Copies to:: {option}"

class Cost(FormUserAttr):
    values = {'11508234_processed': '27,000 29,216', '71202511_processed': '$ 55,500'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cost ($): {option}"

class CostEstimate(FormUserAttr):
    values = {'89867723_processed': '$ 6.816'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cost Estimate: {option}"

class CostPerInterview(FormUserAttr):
    values = {'11508234_processed': '', '71202511_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Cost per Interview: {option}"

class Country(FormUserAttr):
    values = {'87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Country: {option}"

class CountyOf(FormUserAttr):
    values = {'91581919_processed': 'Floyd )'}

    @staticmethod
    def nl_desc(option):
        return f"The user's County of: {option}"

class CouponExpirationDate(FormUserAttr):
    values = {'87533049_processed': '6 / 30 / 91', '91391286_processed': '11/30/93', '91391310_processed': '6/30/94', '91974562_processed': '12/ 17/ 95', '93351929_93351931_processed': 'December 31, 1992'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Coupon Expiration Date: {option}"

class CouponIssueDate(FormUserAttr):
    values = {'87533049_processed': '10 / 90', '91391286_processed': '5/19/93', '91391310_processed': '10/11/93', '91974562_processed': '10/ 13/ 95', '93351929_93351931_processed': 'September 1, 1992'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Coupon Issue Date: {option}"

class CouponValue(FormUserAttr):
    values = {'87533049_processed': '$2.00', '91391286_processed': '$ .75 OFF 1 PACK', '91391310_processed': '$.50', '91974562_processed': '$2 off 3 Pcks or Crtn', '93351929_93351931_processed': 'Free Pack'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Coupon Value: {option}"

class Court(FormUserAttr):
    values = {'0012947358_processed': 'Circuit Court, Dade County, Florida. No. 69 -1351'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Court:: {option}"

class CurrentBalanceAvailable(FormUserAttr):
    values = {'11508234_processed': '382,575', '12603270_processed': '252,955'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Current Balance Available: {option}"

class CurrentBudget(FormUserAttr):
    values = {'0060173256_processed': '$ 7,569,000.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Current Budget: {option}"

class CurrentYearCost(FormUserAttr):
    values = {'0060029036_processed': '1994-1995'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Current Year Cost: {option}"

class Customer(FormUserAttr):
    values = {'0012199830_processed': 'B&W'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Customer: {option}"

class D(FormUserAttr):
    values = {'0012602424_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's D.: {option}"

class DM(FormUserAttr):
    values = {'80728670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's D. M.: {option}"

class DEC(FormUserAttr):
    values = {'0060207528_processed': '534.1'}

    @staticmethod
    def nl_desc(option):
        return f"The user's D.E.C: {option}"

class DailyEffectiveCirculation(FormUserAttr):
    values = {'12825369_processed': ' '}

    @staticmethod
    def nl_desc(option):
        return f"The user's DAILY EFFECTIVE CIRCULATION: {option}"

class DateComplete(FormUserAttr):
    values = {'71190280_processed': '', '71366499_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE COMPLETE: {option}"

class DateForwardedPromotionServices(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE FORWARDED PROMOTION SERVICES:: {option}"

class DateIssued(FormUserAttr):
    values = {'00860012_00860014_processed': 'December 13, 1983', '00866042_processed': 'Oct. 11, 1983'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE ISSUED: {option}"

class DateOfReport(FormUserAttr):
    values = {'660978_processed': '2/ 17/ 82'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE OF REPORT:: {option}"

class DateOfRequisition(FormUserAttr):
    values = {'0060077689_processed': 'January 3, 1995'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE OF REQUISITION: {option}"

class DatePostersReceivedFromLithographer(FormUserAttr):
    values = {'0060207528_processed': '6/ 27/ 89'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE POSTERS RECEIVED FROM LITHOGRAPHER:: {option}"

class DatePostingCompleted(FormUserAttr):
    values = {'0060207528_processed': '7/ 21/ 89'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE POSTING COMPLETED:: {option}"

class DateReceived(FormUserAttr):
    values = {'00040534_processed': 'Unk.', '0060000813_processed': '1 /25 /91', '0060214859_processed': '11- 6- 86', '00836244_processed': '9 /3 /80', '01073843_processed': 'unknown', '87672097_processed': '3/5/81'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE RECEIVED: {option}"

class DateRequested(FormUserAttr):
    values = {'11875011_processed': '1-23-95'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE REQUESTED:: {option}"

class DateShipped(FormUserAttr):
    values = {'01197604_processed': 'November 2, 1965'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE SHIPPED:: {option}"

class DateSubmittedAndDeptManager(FormUserAttr):
    values = {'91104867_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE SUBMITTED AND DEPT. MANAGER: {option}"

class DateToCorp(FormUserAttr):
    values = {'82254638_processed': '7/11/97'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE TO CORP:: {option}"

class DateToNyo(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE TO NYO:: {option}"

class DateWanted(FormUserAttr):
    values = {'00920222_processed': 'As required', '00922237_processed': 'As required'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATE WANTED: {option}"

class Dates(FormUserAttr):
    values = {'00851772_1780_processed': '', '80728670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DATES: {option}"

class Ddress(FormUserAttr):
    values = {'0060262650_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DDRESS: {option}"

class DeFullfillmentVendor(FormUserAttr):
    values = {'0011974919_processed': 'APAC'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DE Fullfillment Vendor: {option}"

class DeadlineForBidReceipt(FormUserAttr):
    values = {'11875011_processed': '1-26-95 9:00 AM EST'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DEADLINE FOR BID RECEIPT:: {option}"

class Dec1987Accrual(FormUserAttr):
    values = {'0011505151_processed': '9,442'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DEC 1987 ACCRUAL: {option}"

class DeliveryDate(FormUserAttr):
    values = {'716552_processed': '10/ 16/ 81', '88057519_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DELIVERY DATE: {option}"

class DepartmentCharged(FormUserAttr):
    values = {'0060077689_processed': 'Brand Operations'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DEPARTMENT CHARGED: {option}"

class Department(FormUserAttr):
    values = {'0001123541_processed': 'R&D Library', '71108371_processed': 'BD & SS'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DEPARTMENT:: {option}"

class DeptNo(FormUserAttr):
    values = {'00922237_processed': '9590'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DEPT NO.: {option}"

class Description(FormUserAttr):
    values = {'0060068489_processed': '30 sheet Posters (White Background)', '0060077689_processed': 'CARLTON "Free" Carton" Direct Mail Piece This Purchase order is to cover all costs incurred to- date listed below. 42,000 lbs. of 80 lb Sterling C/ 2/ S - 36- 1/ 2" roll 31,000 lbs. of 80 lb. Sterling C/ 2/ S - 26- 1/ 2" roll Prep. (line negatives, paper prints, camera/ stripping) Federal Express charges ALL MATERIALS HAVE BEEN CANCELLED.', '0060080406_processed': 'COLLATERAL MERCHANDISING MATERIALS', '0060173256_processed': 'Displays', '00920222_processed': 'This is your authorization to perform the "Acute Oral Toxicity Study in the Rat" tests on materials D13 and D23 supplied by Lorillard. The fixed price for each test is $2050 for each material, for a total price of $4100. Studies are to be conducted in accordance with the October 17, 1980 formal agreement between Borriston and Lorillard. All work is to be coordinated with our Dr. Connie Stone (919) 373- 6663.', '00922237_processed': 'This is your authorization to provide the "1601.013: The Effect of Inhalation of Reference and Test (D3 and D4) Cigarette Smoke on Two Cytogenetic Endpoints in Mice: Chromosome Aberrations and Sister Chromatid Exchange" test for a fixed price of $19,750 Tests will be performed in accordance with the December 21, 1981 formal agreement between Microbiological Associates and Lorillard. All work is to be coordinated with our Dr. Harry Minnemeyer (919) 373-6603', '71190280_processed': 'Passport Winter Program Ad- EMRO', '71341634_processed': '', '71366499_processed': 'CMS Amerada Hess Dispenser Sign', '716552_processed': "VICEROY Rich Lights 100' s 20' s Label"}

    @staticmethod
    def nl_desc(option):
        return f"The user's DESCRIPTION: {option}"

class DescriptionOfReactivity(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's DESCRIPTION OF REACTIVITY: {option}"

class DescriptionOfReactivityWithHeating80c(FormUserAttr):
    values = {'00837285_processed': "['UNCHANGED', 'UNCHANGED', 'UNCHANGED', 'UNCHANGED', 'UNCHANGED', 'UNCHANGED', 'DECOMPOSITION', 'DECOMPOSITION', 'DECOMPOSITION', 'DECOMPOSITION', 'DECOMPOSITION', 'DECOMPOSITION']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's DESCRIPTION OF REACTIVITY_WITH HEATING (80C): {option}"

class DescriptionOfReactivityWithoutHeating(FormUserAttr):
    values = {'00837285_processed': "['UNCHANGED', 'UNCHANGED', 'UNCHANGED', 'UNCHANCED', 'UNCHANGED', 'UNCHANGED', 'DECOMPOSITION', 'DECOMPOSITION', 'DECOMPOSITION', 'DECOMPOSITION', 'DECOMPOSITION', 'DECOMPOSITION']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's DESCRIPTION OF REACTIVITY_WITHOUT HEATING: {option}"

class Design(FormUserAttr):
    values = {'716552_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DESIGN: {option}"

class DesignNo(FormUserAttr):
    values = {'716552_processed': '15'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DESIGN NO.: {option}"

class DesignOnDisplay(FormUserAttr):
    values = {'12825369_processed': '(Condition And Rendition of Copy)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DESIGN ON DISPLAY: {option}"

class Dessicator(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DESSICATOR: {option}"

class DirOfLifeSciencesHealthServicesCompoundPrepToxScientificResTox(FormUserAttr):
    values = {'00866042_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DIR. OF LIFE SCIENCES HEALTH SERVICES COMPOUND PREP (TOX) SCIENTIFIC RES TOX: {option}"

class DirectAccountAndChainVoidsUseXToIndicateAVoid(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's DIRECT ACCOUNT AND CHAIN VOIDS (USE X TO INDICATE A VOID).: {option}"

class DirectAccountAndChainVoidsUseXToIndicateAVoid100S(FormUserAttr):
    values = {'91315069_91315070_processed': '', '92657311_7313_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DIRECT ACCOUNT AND CHAIN VOIDS (USE X TO INDICATE A VOID)._100'S: {option}"

class DirectAccountAndChainVoidsUseXToIndicateAVoidAccount(FormUserAttr):
    values = {'91315069_91315070_processed': '', '92657311_7313_processed': 'NONE'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DIRECT ACCOUNT AND CHAIN VOIDS (USE X TO INDICATE A VOID)._ACCOUNT: {option}"

class DirectAccountAndChainVoidsUseXToIndicateAVoidLts100S(FormUserAttr):
    values = {'92657311_7313_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DIRECT ACCOUNT AND CHAIN VOIDS (USE X TO INDICATE A VOID)._LTS. 100'S: {option}"

class DirectAccountAndChainVoidsUseXToIndicateAVoidNoStores(FormUserAttr):
    values = {'91315069_91315070_processed': '', '92657311_7313_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DIRECT ACCOUNT AND CHAIN VOIDS (USE X TO INDICATE A VOID)._NO. STORES: {option}"

class DirectorOfRaQa(FormUserAttr):
    values = {'89368010_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DIRECTOR OF RA/QA: {option}"

class DirectorOfResearch(FormUserAttr):
    values = {'89368010_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DIRECTOR OF RESEARCH: {option}"

class DisplayAgreement(FormUserAttr):
    values = {'91939637_processed': 'Lorillard Representative will supply all display materials and assemble display. Display containing deals will be placed on a self- service basis for a two- week period.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DISPLAY AGREEMENT:: {option}"

class DisplayBrands(FormUserAttr):
    values = {'91939637_processed': 'TRUE'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DISPLAY BRANDS:: {option}"

class DisplayMaterial(FormUserAttr):
    values = {'0060068489_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DISPLAY MATERIAL: {option}"

class Distribution(FormUserAttr):
    values = {'81619486_9488_processed': '', '89817999_8002_processed': 'EFFECTIVENESS OF PRE- SELL (REPORT ON FEB. 17 ONLY).'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DISTRIBUTION: {option}"

class DivNameNo(FormUserAttr):
    values = {'82254638_processed': 'ST. LOUIS, MO', '91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DIV. NAME/ NO:: {option}"

class Division(FormUserAttr):
    values = {'0060302201_processed': 'Analytical- Radiochemistry', '91104867_processed': 'Sales', '92091873_processed': 'San Jose/ 933', '93213298_processed': 'Detroit - MCA'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DIVISION: {option}"

class DivisionName(FormUserAttr):
    values = {'81619486_9488_processed': '', '81619511_9513_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DIVISION NAME:: {option}"

class DivisionFull(FormUserAttr):
    values = {'81619511_9513_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DIVISION:_FULL: {option}"

class DivisionPartial(FormUserAttr):
    values = {'81619511_9513_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DIVISION:_PARTIAL: {option}"

class DoesWorkMeritPublication(FormUserAttr):
    values = {'0060302201_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's DOES WORK MERIT PUBLICATION?: {option}"

class Doral(FormUserAttr):
    values = {'81749056_9057_processed': '30 3.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DORAL: {option}"

class DosageMgKgBodyWeight(FormUserAttr):
    values = {'00040534_processed': '1800 2160 2592 3732 4479'}

    @staticmethod
    def nl_desc(option):
        return f"The user's DOSAGE (mg/ kg BODY WEIGHT): {option}"

class DatasetName(FormUserAttr):
    values = {'00920294_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Dataset Name: {option}"

class Date(FormUserAttr):
    values = {'0001123541_processed': '', '0001463282_processed': '5/ 3/ 90', '00070353_processed': 'March 18, 1968', '0011838621_processed': '4/ 22/ 90', '0011856542_processed': '1/4/90', '0012178355_processed': '', '0012529284_processed': '12 -4 -87', '0012529295_processed': '', '0012602424_processed': '12 -11', '0013255595_processed': '', '0060007216_processed': 'April 30, 1985', '0060029036_processed': '', '0060068489_processed': '3/17/82', '0060077689_processed': 'January 3, 1995', '0060080406_processed': '', '0060136394_processed': 'APRIL 1,1957', '0060173256_processed': '', '0060207528_processed': '2/ 25/ 89', '0060214859_processed': '10- NOV- 1986', '0060308251_processed': '7/ 24/ 90', '0071032807_processed': 'November 15, 1968', '00836816_processed': '8/ 10/ 82', '00837285_processed': '11/1381', '00838511_00838525_processed': '12- 4- 80', '00851772_1780_processed': 'May 27, 1982', '00851879_processed': '5-13-81', '00865872_processed': '8/22/83', '00920222_processed': 'March 27, 1984', '00922237_processed': '', '01122115_processed': '11 /2 /61', '01408099_01408101_processed': 'March 1, 1978', '12603270_processed': '', '13149651_processed': '2-2-83', '71190280_processed': '10/22/98', '71341634_processed': 'Check#', '71366499_processed': '12/ 15/ 97', '71601299_processed': '15. 03. 2000', '89368010_processed': '16/3/82', '89867723_processed': 'April 27, 1981', '91372360_processed': '11/4/93', '91581919_processed': '1/31/88', '91939637_processed': '', '92091873_processed': '6/ 12/ 95', '92094746_processed': '9 /8 /95', '92094751_processed': '9/ 8 /95'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Date: {option}"

class DateS(FormUserAttr):
    values = {'92091873_processed': 'September 10, 1995', '93213298_processed': 'June 11, 1995'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Date (s): {option}"

class DateInitiated(FormUserAttr):
    values = {'87533049_processed': 'May 3, 1990', '91391286_processed': '2/3/93', '91391310_processed': '8/06/93', '91974562_processed': '6/ 8/ 95', '93351929_93351931_processed': 'May 14, 1992'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Date Initiated: {option}"

class DateMade(FormUserAttr):
    values = {'01122115_processed': '11 /3 /61'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Date Made: {option}"

class DateRecD(FormUserAttr):
    values = {'0001123541_processed': '6/ 21/ 93', '92091873_processed': '9/ 6/ 95', '93213298_processed': '05/ 01/ 95'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Date Rec'd: {option}"

class DateRequired(FormUserAttr):
    values = {'71108371_processed': '4/20/98'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Date Required:: {option}"

class DateRouted(FormUserAttr):
    values = {'0060029036_processed': 'January 11, 1994'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Date Routed:: {option}"

class DateSent(FormUserAttr):
    values = {'0001209043_processed': '4/19/74'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Date Sent: {option}"

class DateSubmitted(FormUserAttr):
    values = {'0011906503_processed': '', '92091873_processed': 'September 26 1995 (submit by 30 days after event)', '93213298_processed': 'July 6, 1995'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Date Submitted: {option}"

class DateAndHourOfService(FormUserAttr):
    values = {'0012947358_processed': 'January 27, 1969 9: 00 a. m.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Date and Hour of Service: {option}"

class DateOfFinalReportReviewCompletedDate(FormUserAttr):
    values = {'89368010_processed': '27 April 1982'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Date of Final Report (Review Completed Date): {option}"

class DateOfRequest(FormUserAttr):
    values = {'0001485288_processed': '6/ 25/ 81'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Date of Request: {option}"

class DatesOfContact(FormUserAttr):
    values = {'80728670_processed': 'Tuesday 3 /13 and Wednesday, 3 /14'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Dates of contact: {option}"

class DeadlineForResponse(FormUserAttr):
    values = {'0011899960_processed': 'Already handled'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Deadline for response: {option}"

class Dec(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Dec: {option}"

class DecisionOfCommitteeOnPresentRequest(FormUserAttr):
    values = {'0060036622_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Decision of Committee on Present Request -: {option}"

class DeclinedSendLetter(FormUserAttr):
    values = {'0060036622_processed': 'YES NO'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Declined - Send letter: {option}"

class Decrease(FormUserAttr):
    values = {'0011838621_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Decrease: {option}"

class DeliveryRollerOverTape(FormUserAttr):
    values = {'01122115_processed': '.844'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Delivery Roller over Tape: {option}"

class DeptCodeNo(FormUserAttr):
    values = {'91104867_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Dept. Code No.: {option}"

class DescribePossibleSolutionsAndBenefits(FormUserAttr):
    values = {'0001123541_processed': '1. Drop the category specifications altogether. 2. Use moregeneral categories. hote: I have passed this to Scott Appleton for the task force to use in streamlining the records management program.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Describe Possible Solutions And Benefits: {option}"

class DescriptionOfChangeOrder(FormUserAttr):
    values = {'00851879_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Description of change order:: {option}"

class DescriptionCapriExpansion(FormUserAttr):
    values = {'0012529295_processed': 'California- A&U Wave II'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Description: CAPRI Expansion:: {option}"

class Dimension(FormUserAttr):
    values = {'0000989556_processed': 'mm x mm'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Dimension: {option}"

class DirectAccount(FormUserAttr):
    values = {'88057519_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Direct Account: {option}"

class DirectionalDifference(FormUserAttr):
    values = {'0000999294_processed': '66 79% confidence Level'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Directional Difference:: {option}"

class Director(FormUserAttr):
    values = {'80310840a_processed': '', '89867723_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Director: {option}"

class DistAsgmtCF(FormUserAttr):
    values = {'71341634_processed': '39A00A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Dist/Asgmt C.F. #: {option}"

class DistanceFromYourHomeToAirport(FormUserAttr):
    values = {'0060091229_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Distance from your home to airport:: {option}"

class DistributionDropDate(FormUserAttr):
    values = {'0011974919_processed': '10/ 03/ 96'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Distribution Drop Date:: {option}"

class DistributorNo(FormUserAttr):
    values = {'71341634_processed': '20182'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Distributor No: {option}"

class DivisionSToBeContacted(FormUserAttr):
    values = {'80728670_processed': 'Boston'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Division (s) to be contacted: {option}"

class DivisionMgr(FormUserAttr):
    values = {'92091873_processed': 'T. L. Roberts', '93213298_processed': 'R. L. Lavoie'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Division Mgr: {option}"

class DoYouPreferAirlineSeatsInSmokingOrNonSmokingSection(FormUserAttr):
    values = {'0060091229_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Do you prefer airline seats in smoking or non- smoking section:: {option}"

class DocumentS(FormUserAttr):
    values = {'0012947358_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Document(s): {option}"

class Domestic(FormUserAttr):
    values = {'0012178355_processed': 'X', '716552_processed': '☑'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Domestic: {option}"

class Draw(FormUserAttr):
    values = {'0060094595_processed': '0. .34 0 .37 0 .34 0\uf703 .37', '01122115_processed': '.922 1 .059 .54 .20 20 .2 7 .6 62 .4 1 .07 .41 61 .7'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Draw: {option}"

class DryWeight(FormUserAttr):
    values = {'01122115_processed': '86 .9 gms'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Dry Weight: {option}"

class DryWtWithAdhesive(FormUserAttr):
    values = {'01122115_processed': '93 .3 gms.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Dry Wt. With Adhesive: {option}"

class DueThe1StMondayOfTheMonthDuringTheLegislativeSessionToReportThePreviousMonthsActivity(FormUserAttr):
    values = {'0001477983_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Due the 1st Monday of the month during the legislative session to report the previous months' activity.: {option}"

class DuringThisReportingPeriodHaveYouMadeAnyExpenditureOrIncurredAnyObligationOf2500OrMorePerOccurenceToPromoteOrOpposeAnyLegislationIncludingButNotLimitedMailingsMealsPrintOrBroadcastAdvertisementsOrGiftsYesOrNo(FormUserAttr):
    values = {'0001477983_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's During this reporting period, have you made any expenditure or incurred any obligation of $ 25.00 or more per occurence to promote or oppose any legislation, including but not limited mailings, meals, print or broadcast advertisements, or gifts (yes or no): {option}"

class E(FormUserAttr):
    values = {'0012602424_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's E.: {option}"

class EaseOfDraw17Easier(FormUserAttr):
    values = {'0000999294_processed': '4.00 3.96 4.02 3.95 3.99 3.96 4.07** 3.92 3.94 3.99'}

    @staticmethod
    def nl_desc(option):
        return f"The user's EASE OF DRAW 17 Easier: {option}"

class EffectivenessOfAdvertising(FormUserAttr):
    values = {'89817999_8002_processed': 'OUTDOOR AND PRINT ADS HAVE BEEN EFFECTIVE IN CREATING CONSUMER AWARENESS IN THOSE ARE EYE CATCHING AND CONSUMERS ARE MORE AWARE OF THE PRODUCT IN THOSE MARKETS WITH ADVERTISING.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's EFFECTIVENESS OF ADVERTISING:: {option}"

class EffectivenessOf(FormUserAttr):
    values = {'92039708_9710_processed': 'Pre- Sell Booklet /Coupon Maverick /Harley B1 G1 F'}

    @staticmethod
    def nl_desc(option):
        return f"The user's EFFECTIVENESS OF:: {option}"

class EfficiencyRating(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's EFFICIENCY RATING:: {option}"

class EfficiencyRatingExcellent(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's EFFICIENCY RATING:_EXCELLENT: {option}"

class EfficiencyRatingFair(FormUserAttr):
    values = {'92094746_processed': 'x', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's EFFICIENCY RATING:_FAIR: {option}"

class EfficiencyRatingGood(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's EFFICIENCY RATING:_GOOD: {option}"

class EfficiencyRatingPoor(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's EFFICIENCY RATING:_POOR: {option}"

class Elt(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ELT: {option}"

class Endorsements(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ENDORSEMENTS: {option}"

class Epb(FormUserAttr):
    values = {'0071032790_processed': 'ODL'}

    @staticmethod
    def nl_desc(option):
        return f"The user's EPB:: {option}"

class EstimateOfTimeNeededToCompleteWork(FormUserAttr):
    values = {'0060302201_processed': 'approximately one month'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ESTIMATE OF TIME NEEDED TO COMPLETE WORK:: {option}"

class EstimateOfTimeNeededToPrepareManuscriptForPresentation(FormUserAttr):
    values = {'0060302201_processed': 'several weeks after completion'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ESTIMATE OF TIME NEEDED TO PREPARE MANUSCRIPT FOR PRESENTATION:: {option}"

class EstimateOfTimeNeededToPrepareManuscriptForPublication(FormUserAttr):
    values = {'0060302201_processed': 'several weeks after completion of work'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ESTIMATE OF TIME NEEDED TO PREPARE MANUSCRIPT FOR PUBLICATION:: {option}"

class EstimatedPaybackPeriod(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ESTIMATED PAYBACK PERIOD: {option}"

class EstimatedTargetDateOriginalComments(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ESTIMATED TARGET DATE- ORIGINAL COMMENTS: {option}"

class EstimatedToxicityClass(FormUserAttr):
    values = {'00838511_00838525_processed': 'II'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ESTIMATED TOXICITY CLASS: {option}"

class Expense(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's EXPENSE: {option}"

class ExperimentalProcedures(FormUserAttr):
    values = {'00860012_00860014_processed': 'This project sheet is issued to correct Project Sheet which was issued on December 6, 1983 to Project Sheet No 3 instead of 2. Material Safety Data Sheet is attached to Project Sheet 1.', '00866042_processed': 'to performed in Acure/Dermal Toxicology, building 18.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's EXPERIMENTAL PROCEDURES: {option}"

class Explosive(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's EXPLOSIVE: {option}"

class ExtraCopiesTo(FormUserAttr):
    values = {'0060077689_processed': 'D. Barcia'}

    @staticmethod
    def nl_desc(option):
        return f"The user's EXTRA COPIES TO:: {option}"

class EnclosedAreCopiesOfLegalProcesServedUponTheStatutoryAgentOfTheAboveCompanyAsFollows(FormUserAttr):
    values = {'0012947358_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Enclosed are copies of legal proces served upon the statutory agent of the above company as follows:: {option}"

class EstMonthlyOngoing(FormUserAttr):
    values = {'0011973451_processed': 'TBD'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Est. Monthly Ongoing:: {option}"

class EstTravel(FormUserAttr):
    values = {'11508234_processed': '2,500 2,500', '71202511_processed': '3,000'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Est. Travel: {option}"

class EstimateCost(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Estimate Cost: {option}"

class EstimateCostCapital(FormUserAttr):
    values = {'0011906503_processed': '80'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Estimate Cost_CAPITAL: {option}"

class EstimateCostExpense(FormUserAttr):
    values = {'0011906503_processed': '0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Estimate Cost_EXPENSE: {option}"

class EstimateCostTotal(FormUserAttr):
    values = {'0011906503_processed': '80'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Estimate Cost_TOTAL: {option}"

class EstimateNo(FormUserAttr):
    values = {'88547278_88547279_processed': '4854- 5'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Estimate No:: {option}"

class EstimatedAttendance(FormUserAttr):
    values = {'0011976929_processed': '700'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Estimated Attendance: {option}"

class EstimatedFreightCharges(FormUserAttr):
    values = {'0060068489_processed': '2.000.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Estimated Freight Charges: {option}"

class EstimatedManHoursForCompletion(FormUserAttr):
    values = {'0071032807_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Estimated Man Hours for Completion: {option}"

class EstimatedResponders(FormUserAttr):
    values = {'0011974919_processed': '300'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Estimated Responders:: {option}"

class EstimatedResponse(FormUserAttr):
    values = {'0011974919_processed': '100.00 %'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Estimated Response:: {option}"

class EstimatedCostOfTheStudyWillBe(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Estimated cost of the study will be:: {option}"

class Excellent(FormUserAttr):
    values = {'93213298_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Excellent: {option}"

class ExclusiveAdvertisingFor(FormUserAttr):
    values = {'91581919_processed': 'Harley Davidson Cigarettes'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Exclusive advertising for: {option}"

class ExpirationDate(FormUserAttr):
    values = {'0011974919_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Expiration Date:: {option}"

class Export(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Export: {option}"

class ExtAuthoDate(FormUserAttr):
    values = {'0011505151_processed': '11- 16- 87'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Ext. Autho. Date: {option}"

class ExtentOfDistribution(FormUserAttr):
    values = {'81186212_processed': '', '93329540_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Extent of distribution:: {option}"

class ExtraBanquetTickets4000(FormUserAttr):
    values = {'87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Extra banquet tickets @ $ 40.00: {option}"

class FPMDeliveryRoller(FormUserAttr):
    values = {'01122115_processed': '337 .5'}

    @staticmethod
    def nl_desc(option):
        return f"The user's F. P. M. Delivery Roller: {option}"

class FPMNo1Roller(FormUserAttr):
    values = {'01122115_processed': '477 .5'}

    @staticmethod
    def nl_desc(option):
        return f"The user's F. P. M. No. 1 Roller: {option}"

class FPMNo2Roller(FormUserAttr):
    values = {'01122115_processed': '362 .5'}

    @staticmethod
    def nl_desc(option):
        return f"The user's F. P. M. No. 2 Roller: {option}"

class Fax(FormUserAttr):
    values = {'0011845203_processed': '1- 502- 568- 8092', '11875011_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FAX: {option}"

class FaxMumber(FormUserAttr):
    values = {'0011845203_processed': '1- 502- 568 8092'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FAX MUMBER:: {option}"

class FaxNumbers(FormUserAttr):
    values = {'11875011_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FAX NUMBERS:: {option}"

class FdcRepresentatives(FormUserAttr):
    values = {'80718412_8413_processed': 'Tony Anari'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FDC REPRESENTATIVES:: {option}"

class FileFileType(FormUserAttr):
    values = {'01191071_1072_processed': '083 MEMORY TX'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FILE FILE TYPE: {option}"

class FinalFlavor(FormUserAttr):
    values = {'00093726_processed': 'OGS', '00283813_processed': '', '81574683_processed': 'attached'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FINAL FLAVOR: {option}"

class FirmName(FormUserAttr):
    values = {'0030031163_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FIRM NAME: {option}"

class FiscalEstimateAdMba23Rev1180(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FISCAL ESTIMATE AD MBA 23 (Rev 11/80: {option}"

class FixedDistribution(FormUserAttr):
    values = {'00866042_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FIXED DISTRIBUTION:: {option}"

class Flammable(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FLAMMABLE: {option}"

class Fo(FormUserAttr):
    values = {'0060077689_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FO: {option}"

class FoaControlUseOnly(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's FOA CONTROL USE ONLY:: {option}"

class FoaControlUseOnlyCodeAssigned(FormUserAttr):
    values = {'93380187_processed': '57288'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FOA CONTROL USE ONLY:_CODE ASSIGNED:: {option}"

class FoaControlUseOnlyEstRedemption(FormUserAttr):
    values = {'93380187_processed': '80 %'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FOA CONTROL USE ONLY:_EST. REDEMPTION:: {option}"

class FoaControlUseOnlyJoeNumber(FormUserAttr):
    values = {'93380187_processed': '1143'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FOA CONTROL USE ONLY:_JOE NUMBER:: {option}"

class FollowDepartmentAndCompanySafetyManuals(FormUserAttr):
    values = {'00860012_00860014_processed': '', '00866042_processed': '☑'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FOLLOW DEPARTMENT AND COMPANY SAFETY MANUALS: {option}"

class FollowUpDate(FormUserAttr):
    values = {'00920222_processed': '', '00922237_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FOLLOW UP DATE: {option}"

class For(FormUserAttr):
    values = {'0012947358_processed': 'THE AMERICAN TOBACCO COMPANY'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FOR: {option}"

class ForControlUseOnly(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's FOR CONTROL USE ONLY :: {option}"

class ForControlUseOnlyCodeAssigned(FormUserAttr):
    values = {'87533049_processed': '530430'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FOR CONTROL USE ONLY :_Code Assigned: {option}"

class ForControlUseOnlyJobNumber(FormUserAttr):
    values = {'87533049_processed': '1112'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FOR CONTROL USE ONLY :_Job Number: {option}"

class ForPurchasingDepartmentUseOnly(FormUserAttr):
    values = {'00920222_processed': 'Borriston Laboratories, INC. , 5050 Beech Place Temple Hills, MD 20748'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FOR PURCHASING DEPARTMENT USE ONLY: {option}"

class Freezer(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FREEZER: {option}"

class From(FormUserAttr):
    values = {'0001129658_processed': 'Kevin Narko', '0011974919_processed': 'Joyce Bagby', '0012947358_processed': 'C T Corporation System', '0060036622_processed': 'E. E. Curtin', '0060165115_processed': 'Dr. Wolf Reininghaus', '00920294_processed': 'Drew Huyett', '01150773_01150774_processed': 'David H. Remes', '80728670_processed': 'Mary Anne Kayiatos', '81619486_9488_processed': 'R. W. Richardson', '81619511_9513_processed': 'C.J. Leiker', '81749056_9057_processed': 'S. P. McBride', '82254638_processed': 'W. R. KNIGHT - MCA', '87533049_processed': 'J. La Valle', '89817999_8002_processed': 'J. J. BUXTON', '91315069_91315070_processed': '', '91391286_processed': 'THOM SMITH', '91391310_processed': 'M. BORSINI', '91903177_processed': '', '91939637_processed': '', '91974562_processed': 'THOM SMITH', '92039708_9710_processed': '', '92327794_processed': 'Becky Hayden', '92657311_7313_processed': 'S. J. Farnham', '93351929_93351931_processed': 'JESSICA ARATO', '93380187_processed': 'MICHELLE LEPRE'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FROM:: {option}"

class FrontCigarettes(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's FRONT CIGARETTES: {option}"

class FrontCigarettesComments(FormUserAttr):
    values = {'0060000813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FRONT CIGARETTES_Comments:: {option}"

class FrontCigarettesCratering(FormUserAttr):
    values = {'0060000813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FRONT CIGARETTES_Cratering:: {option}"

class FrontCigarettesHoleDepth(FormUserAttr):
    values = {'0060000813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FRONT CIGARETTES_Hole Depth:: {option}"

class FrontCigarettesScorching(FormUserAttr):
    values = {'0060000813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FRONT CIGARETTES_Scorching:: {option}"

class FsMarketing(FormUserAttr):
    values = {'0060029036_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FS - Marketing: {option}"

class Full(FormUserAttr):
    values = {'81619486_9488_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FULL: {option}"

class FullInspection(FormUserAttr):
    values = {'12825369_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's FULL INSPECTION: {option}"

class Funding(FormUserAttr):
    values = {'71206427_processed': '1990 Customized Merchandising Services ESPNS'}

    @staticmethod
    def nl_desc(option):
        return f"The user's FUNDING:: {option}"

class Facility(FormUserAttr):
    values = {'0060024314_processed': 'The American Tobacco Company', '89867723_processed': '1. 500. 00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Facility:: {option}"

class Fair(FormUserAttr):
    values = {'93213298_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Fair: {option}"

class FaxNumber(FormUserAttr):
    values = {'0001129658_processed': '305 400- 6107'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Fax Number:: {option}"

class FaxNo(FormUserAttr):
    values = {'0060165115_processed': '0041- 32- 888 5776'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Fax no:: {option}"

class Feb(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Feb: {option}"

class Female(FormUserAttr):
    values = {'00040534_processed': '', '87672097_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Female: {option}"

class Female106(FormUserAttr):
    values = {'0000999294_processed': '46 43 11 100'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Female (106): {option}"

class FemaleBright(FormUserAttr):
    values = {'0000999294_processed': "['4.71', '3.41', '5.02', '3.06', '2.78', '3.26', '3.96']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Female_Bright: {option}"

class FemaleKl(FormUserAttr):
    values = {'0000999294_processed': "['4.51', '3.47', '3.70***', '3.33**', '2.97*', '3.44', '3.99']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Female_KL: {option}"

class FieldComplete(FormUserAttr):
    values = {'0011505151_processed': '12- -7 -87', '11508234_processed': '', '12603270_processed': '', '71202511_processed': 'w /o 3/ 23 /98'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Field Complete: {option}"

class FieldStart(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Field Start: {option}"

class FieldworkSchedule(FormUserAttr):
    values = {'80310840a_processed': 'Start Field w/o 11 /13 /95'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Fieldwork Schedule:: {option}"

class FilmCleared(FormUserAttr):
    values = {'0011859695_processed': 'VIDEO TAPE APPROVAL "Presenter/ Girl Rev" AT-M B-T-64 :60 "Pall Mall Filter Tip" AT-P/ F-T-317 :30 TAPE WILL FOLLOW AS SOON AS I RECEIVE IT FROM THE TAPE LIBRARY.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Film Cleared:: {option}"

class FilmSEnclosed(FormUserAttr):
    values = {'0011859695_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Film(s) enclosed.: {option}"

class Filter(FormUserAttr):
    values = {'81574683_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Filter: {option}"

class Filters(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Filters: {option}"

class FiltersCircumference(FormUserAttr):
    values = {'00093726_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Filters_Circumference: {option}"

class FiltersKind(FormUserAttr):
    values = {'00093726_processed': '20 mm True plastic rod'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Filters_Kind: {option}"

class FiltersPlasticizer(FormUserAttr):
    values = {'00093726_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Filters_Plasticizer: {option}"

class FiltersPlugWrap(FormUserAttr):
    values = {'00093726_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Filters_Plug Wrap: {option}"

class FiltersPressureDrop(FormUserAttr):
    values = {'00093726_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Filters_Pressure Drop: {option}"

class FiltersProcess(FormUserAttr):
    values = {'00093726_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Filters_Process: {option}"

class FiltersRodLength(FormUserAttr):
    values = {'00093726_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Filters_Rod Length: {option}"

class FiltersWeight(FormUserAttr):
    values = {'00093726_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Filters_Weight: {option}"

class FinalReportDue(FormUserAttr):
    values = {'12603270_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Final Report Due: {option}"

class FinalReportDueSupplierRpt(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Final Report Due (Supplier Rpt.): {option}"

class FinalRptDue(FormUserAttr):
    values = {'0011505151_processed': '1- 11- 88'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Final Rpt. Due: {option}"

class FinalSupplierReportDue(FormUserAttr):
    values = {'71202511_processed': 'w/ o 4/ 6/ 98'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Final Supplier Report Due: {option}"

class FinalApprovalIsOfCourseDependentUponTimeAndPlacementOfTheCommercialS(FormUserAttr):
    values = {'0011859695_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Final approval is, of course, dependent upon time and placement of the commercial(s).: {option}"

class FinalistName(FormUserAttr):
    values = {'0060091229_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Finalist Name:: {option}"

class FirmnessOfRod(FormUserAttr):
    values = {'01122115_processed': 'Good'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Firmness of Rod: {option}"

class First(FormUserAttr):
    values = {'87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's First: {option}"

class FiscalEffect(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Fiscal Effect: {option}"

class FollowingPhysicalVisualPropertiesOutOfSpecifications(FormUserAttr):
    values = {'0060214859_processed': 'WEIGHT OUT OF SPECIFICATIONS ON ROLLS 34 & 35. WT. AV. ROLL 34 (183. 04) ; WT. AV. ROLL 35 (183. 44) : SPECS. 190 -210 GMS/ SQM. LOI OUT DE SPEC. ON ROLL 34 (AV 2. 49%) SPECIFICATIONS (2.6 6- 3. 1% .'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Following physical/ visual properties out of specifications:: {option}"

class ForAmericanBrandsInc(FormUserAttr):
    values = {'0060036622_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's For American Brands, Inc.: {option}"

class FormulaNo(FormUserAttr):
    values = {'0012199830_processed': 'SKGC-4518 '}

    @staticmethod
    def nl_desc(option):
        return f"The user's Formula No.: {option}"

class FromNewspaper(FormUserAttr):
    values = {'91581919_processed': 'New Albany Tribune'}

    @staticmethod
    def nl_desc(option):
        return f"The user's From Newspaper: {option}"

class FromNicotineMgCigt(FormUserAttr):
    values = {'0060308251_processed': '0 .3'}

    @staticmethod
    def nl_desc(option):
        return f"The user's From_Nicotine (Mg /Cigt): {option}"

class FromTarMgCigt(FormUserAttr):
    values = {'0060308251_processed': '3'}

    @staticmethod
    def nl_desc(option):
        return f"The user's From_Tar (Mg /Cigt): {option}"

class FullfillmentDataEntryAt(FormUserAttr):
    values = {'0011974919_processed': 'APAC'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Fullfillment Data Entry at: {option}"

class FundSourceAffected(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Fund Source Affected: {option}"

class FurtherInformationPleaseAttachAnyRelevantMaterialsPosAdvertisingBrochuresEtc(FormUserAttr):
    values = {'81186212_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Further information (please attach any relevant materials; POS, advertising, brochures, etc.):: {option}"

class GPC(FormUserAttr):
    values = {'81749056_9057_processed': '30 $ 3.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's G.P.C: {option}"

class GLCode(FormUserAttr):
    values = {'0060029036_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's G/ L Code:: {option}"

class GeneralInformation(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's GENERAL INFORMATION:: {option}"

class GeneralInformationEventDates(FormUserAttr):
    values = {'91856041_6049_processed': 'June 3, 1995', '92586242_processed': 'June 4, 1995'}

    @staticmethod
    def nl_desc(option):
        return f"The user's GENERAL INFORMATION:_EVENT DATES:: {option}"

class GeneralInformationEventLocation(FormUserAttr):
    values = {'91856041_6049_processed': '42nd- 57th Street, New York NY', '92586242_processed': '68th -86th Street New York, NY'}

    @staticmethod
    def nl_desc(option):
        return f"The user's GENERAL INFORMATION:_EVENT LOCATION:: {option}"

class GeneralInformationEventName(FormUserAttr):
    values = {'91856041_6049_processed': 'The USO Spring Festival', '92586242_processed': 'Upper Madisor Avenue Festival'}

    @staticmethod
    def nl_desc(option):
        return f"The user's GENERAL INFORMATION:_EVENT NAME:: {option}"

class GeneralProjectDescription(FormUserAttr):
    values = {'01408099_01408101_processed': "True 100's, Regular and Menthol tar characteristics as current True 100's product and, 2) Taste characterist- reduction to the range of 8- 10mg tar. Variations to be: 1) Same taste ics similar to True King Size, 5mg. tar product."}

    @staticmethod
    def nl_desc(option):
        return f"The user's GENERAL PROJECT DESCRIPTION: {option}"

class GeneralExport(FormUserAttr):
    values = {'716552_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's GENERAL ☐ EXPORT: {option}"

class GeogfiaphicalAreaS(FormUserAttr):
    values = {'93351929_93351931_processed': 'Tier '}

    @staticmethod
    def nl_desc(option):
        return f"The user's GEOGFIAPHICAL AREA(S): {option}"

class Geography(FormUserAttr):
    values = {'81619486_9488_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's GEOGRAPHY: {option}"

class GolfTournament(FormUserAttr):
    values = {'0030031163_processed': '(Ladies & Men) . . . Friday, August 16, Tee off at 8:00 A. M. SHARP (no green fee)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's GOLF TOURNAMENT: {option}"

class GroupNo(FormUserAttr):
    values = {'00040534_processed': '1 2 3 4 5', '87672097_processed': '1 2 3 4 5'}

    @staticmethod
    def nl_desc(option):
        return f"The user's GROUP NO.: {option}"

class GeneralManager(FormUserAttr):
    values = {'0060165115_processed': 'Dr. Wolf Reninghaus'}

    @staticmethod
    def nl_desc(option):
        return f"The user's General Manager: {option}"

class GeneticAssayNo(FormUserAttr):
    values = {'81310636_processed': '6692'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Genetic Assay No.: {option}"

class GeographicalAreaS(FormUserAttr):
    values = {'87533049_processed': 'National', '91391286_processed': 'TOTAL HOUSTON, GALVESTON, MINNEAPOLIS, ST. PAUL, DULUTH', '91391310_processed': 'NATIONAL', '91974562_processed': 'Regions 11, 17, 21'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Geographical Area (s): {option}"

class GluePreeArea(FormUserAttr):
    values = {'0000989556_processed': 'N/A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Glue Pree Area: {option}"

class GroupProduct(FormUserAttr):
    values = {'89867723_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Group Product: {option}"

class Harshness(FormUserAttr):
    values = {'0001239897_processed': '+5 -5'}

    @staticmethod
    def nl_desc(option):
        return f"The user's HARSHNESS: {option}"

class HasWorkBeenReportedInManuscript(FormUserAttr):
    values = {'0060302201_processed': 'yes'}

    @staticmethod
    def nl_desc(option):
        return f"The user's HAS WORK BEEN REPORTED IN MANUSCRIPT : {option}"

class HazardousCompound(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's HAZARDOUS, COMPOUND: {option}"

class HazardousCompoundCarcinogenOsha(FormUserAttr):
    values = {'00866042_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's HAZARDOUS, COMPOUND_CARCINOGEN (OSHA): {option}"

class HazardousCompoundCarcinogenOther(FormUserAttr):
    values = {'00866042_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's HAZARDOUS, COMPOUND_CARCINOGEN (OTHER): {option}"

class HazardousCompoundExplosive(FormUserAttr):
    values = {'00866042_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's HAZARDOUS, COMPOUND_EXPLOSIVE: {option}"

class HazardousCompoundFlammable(FormUserAttr):
    values = {'00866042_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's HAZARDOUS, COMPOUND_FLAMMABLE: {option}"

class HazardousCompoundRadioactive(FormUserAttr):
    values = {'00866042_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's HAZARDOUS, COMPOUND_RADIOACTIVE: {option}"

class Headline(FormUserAttr):
    values = {'80707440_7443_processed': 'Pick The Winners And Win Up $ 5 ,000'}

    @staticmethod
    def nl_desc(option):
        return f"The user's HEADLINE:: {option}"

class HkTrial(FormUserAttr):
    values = {'0001456787_processed': '99 mm 72 mm 27 mm 62 mm 58.5 mm 24.8 mm mm 32 mm 35 mm 13% mg 858 mg 243.6 mg/ cc'}

    @staticmethod
    def nl_desc(option):
        return f"The user's HK Trial: {option}"

class Hours(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's HOURS:: {option}"

class HoursMondayFriday(FormUserAttr):
    values = {'91856041_6049_processed': '', '92586242_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's HOURS:_MONDAY- FRIDAY: {option}"

class HoursSaturdaySunday(FormUserAttr):
    values = {'91856041_6049_processed': 'llam- 6pm', '92586242_processed': '11 am - 6 pm'}

    @staticmethod
    def nl_desc(option):
        return f"The user's HOURS:_SATURDAY- SUNDAY: {option}"

class HowWidespread(FormUserAttr):
    values = {'91355841_processed': '', '93455715_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's HOW WIDESPREAD?: {option}"

class HaveYouContactedYourManagerSupervisor(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Have you contacted your Manager/ Supervisor?: {option}"

class HaveYouContactedYourManagerSupervisorNo(FormUserAttr):
    values = {'0000971160_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Have you contacted your Manager/ Supervisor?_No: {option}"

class HaveYouContactedYourManagerSupervisorYes(FormUserAttr):
    values = {'0000971160_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Have you contacted your Manager/ Supervisor?_Yes: {option}"

class HaveYouPaidAnyTypeOfCompensationOrIncurredAnyObligationForPaymentToTheAboveNamed(FormUserAttr):
    values = {'0001477983_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Have you paid any type of compensation or incurred any obligation for payment to the above named: {option}"

class HomeAddress(FormUserAttr):
    values = {'0060091229_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Home Address:: {option}"

class HomeTelephone(FormUserAttr):
    values = {'0060091229_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Home Telephone:: {option}"

class HotelMotelReservationsNeeded(FormUserAttr):
    values = {'80728670_processed': 'XX'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Hotel /Motel reservations needed: {option}"

class HousekeepingCleaning(FormUserAttr):
    values = {'0060024314_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Housekeeping Cleaning: {option}"

class IWillParticipateInTheGolfTournament(FormUserAttr):
    values = {'0030031163_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's I will participate in the Golf Tournament: {option}"

class IWillParticipateInTheTennisTournamentIWouldClassifyMyselfAsPleaseCheckAppropriateBox(FormUserAttr):
    values = {'0030031163_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's I will participate in the Tennis Tournament I would classify myself as (please check appropriate box): {option}"

class Id(FormUserAttr):
    values = {'71341634_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ID#: {option}"

class IfNoExplain(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': 'This model/ type of sunglass was not received well at consumer/ retail level.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's IF NO, EXPLAIN:: {option}"

class IfSoGiveDateAndTitle(FormUserAttr):
    values = {'0060302201_processed': 'MBTH- reagent for analysis of aliphatic aldehydes 7 / 5 / 67'}

    @staticmethod
    def nl_desc(option):
        return f"The user's IF SO, GIVE DATE AND TITLE:: {option}"

class IfYesCanItBeImproved(FormUserAttr):
    values = {'92094746_processed': 'The Promotion can be improved by upgrading the quality of the sunglasses', '92094751_processed': 'Velcro on strap did not hold. Two right sides of velcro on same glass did not adhere.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's IF YES, CAN IT BE IMPROVED?: {option}"

class IfYouDoNotReceiveAnyOfThePagesPleaseCall(FormUserAttr):
    values = {'92327794_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's IF YOU DO NOT RECEIVE ANY OF THE PAGES, PLEASE CALL: {option}"

class IfYouHaveAnyQuestionsPleaseContactTheFollowingPerson(FormUserAttr):
    values = {'0011845203_processed': 'Mary D. Davis', '11875011_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's IF YOU HAVE ANY QUESTIONS, PLEASE CONTACT THE FOLLOWING PERSON:: {option}"

class Ii(FormUserAttr):
    values = {'00851772_1780_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's II.: {option}"

class IiiSupplementalLiteratureSearchChemicalAbstractsVol23Vol65ArctanderSPerfumeAndFlavorMaterialsOfNaturalOrigin1960GuentherSMonographsOnFragranceRawMaterials1979TobaccoAbstractsUSDispensatory23RdEdition1943(FormUserAttr):
    values = {'00851772_1780_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's III. SUPPLEMENTAL LITERATURE SEARCH Chemical Abstracts Vol. 23 - Vol. 65 Arctander' s Perfume and Flavor Materials of Natural Origin (1960) Guenther' s Monographs on Fragrance Raw Materials (1979) Tobacco Abstracts U. S. Dispensatory 23rd edition (1943): {option}"

class Illustration(FormUserAttr):
    values = {'80707440_7443_processed': 'Line Drawings of Football Scenes'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ILLUSTRATION:: {option}"

class In(FormUserAttr):
    values = {'0012947358_processed': 'FLORIDA'}

    @staticmethod
    def nl_desc(option):
        return f"The user's IN: {option}"

class InTestimonyWhereofIHaveSetMyHandAndSealTheDayAndYearAforesaid(FormUserAttr):
    values = {'91581919_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's IN TESTIMONY WHEREOF I have set my hand and seal the day and year aforesaid.: {option}"

class InalTitleOfSymposium(FormUserAttr):
    values = {'0060262650_processed': 'THE HUMAN CHROMOSOME'}

    @staticmethod
    def nl_desc(option):
        return f"The user's INAL TITLE OF SYMPOSIUM: {option}"

class InbifoInstitutFRBiologischeForschungGmbh(FormUserAttr):
    values = {'0060165115_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's INBIFO Institut für biologische Forschung GmbH: {option}"

class IndLorVolume(FormUserAttr):
    values = {'81619511_9513_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's IND LOR VOLUME: {option}"

class IndVolume(FormUserAttr):
    values = {'81619511_9513_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's IND VOLUME: {option}"

class IndependentAcceptance(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's INDEPENDENT ACCEPTANCE:: {option}"

class IndependentAcceptanceExcellent(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's INDEPENDENT ACCEPTANCE:_EXCELLENT: {option}"

class IndependentAcceptanceFair(FormUserAttr):
    values = {'92094746_processed': 'x', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's INDEPENDENT ACCEPTANCE:_FAIR: {option}"

class IndependentAcceptanceGood(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's INDEPENDENT ACCEPTANCE:_GOOD: {option}"

class IndependentAcceptancePoor(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's INDEPENDENT ACCEPTANCE:_POOR: {option}"

class InitialMaterialsRequired(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's INITIAL MATERIALS REQUIRED:: {option}"

class InitialMaterialsRequiredCartons(FormUserAttr):
    values = {'0011973451_processed': 'On Hand'}

    @staticmethod
    def nl_desc(option):
        return f"The user's INITIAL MATERIALS REQUIRED:_Cartons:: {option}"

class InitialMaterialsRequiredCases(FormUserAttr):
    values = {'0011973451_processed': '500'}

    @staticmethod
    def nl_desc(option):
        return f"The user's INITIAL MATERIALS REQUIRED:_Cases:: {option}"

class InitialMaterialsRequiredDollarCost(FormUserAttr):
    values = {'0011973451_processed': '$250'}

    @staticmethod
    def nl_desc(option):
        return f"The user's INITIAL MATERIALS REQUIRED:_Dollar Cost: {option}"

class InitialMaterialsRequiredPackFlatsLabels(FormUserAttr):
    values = {'0011973451_processed': 'On Hand'}

    @staticmethod
    def nl_desc(option):
        return f"The user's INITIAL MATERIALS REQUIRED:_Pack Flats Labels:: {option}"

class InitialMaterialsRequiredQtyInUnits(FormUserAttr):
    values = {'0011973451_processed': "['On Hand', 'On Hand', '500']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's INITIAL MATERIALS REQUIRED:_Qty In Units: {option}"

class Initiated(FormUserAttr):
    values = {'0000990274_processed': 'P. H. HARPER PHH'}

    @staticmethod
    def nl_desc(option):
        return f"The user's INITIATED: {option}"

class InspectionBy(FormUserAttr):
    values = {'12825369_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's INSPECTION BY: {option}"

class Instructions(FormUserAttr):
    values = {'11875011_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's INSTRUCTIONS:: {option}"

class InventoryDepletionDate(FormUserAttr):
    values = {'716552_processed': '10/ 30/ 81'}

    @staticmethod
    def nl_desc(option):
        return f"The user's INVENTORY DEPLETION DATE: {option}"

class InvestigatorS(FormUserAttr):
    values = {'00040534_processed': "H. S. Tong & M. S. Forte'", '00836244_processed': 'H. S. Tong & A. A. Poole', '01073843_processed': 'H. S. Tong & A. A. Poole', '87672097_processed': 'H. S. Tong & A. A. Poole'}

    @staticmethod
    def nl_desc(option):
        return f"The user's INVESTIGATOR(S): {option}"

class IssueFrequencyYear(FormUserAttr):
    values = {'91391286_processed': '1', '91391310_processed': 'OCR-DEC', '91974562_processed': '1', '93351929_93351931_processed': 'September'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ISSUE FREQUENCY/ YEAR: {option}"

class Issue(FormUserAttr):
    values = {'80707440_7443_processed': 'August 19, 1969'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ISSUE:: {option}"

class IssuedBy(FormUserAttr):
    values = {'00920222_processed': '', '00922237_processed': '00922237'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ISSUED BY: {option}"

class Item(FormUserAttr):
    values = {'91104867_processed': 'Consumer Consumer Consumer Special'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ITEM: {option}"

class ItemBrand(FormUserAttr):
    values = {'92094751_processed': 'Newport Sunglasses'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ITEM/ BRAND: {option}"

class Items(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's ITEMS: {option}"

class ItemsAnyOtherItemsAvailable(FormUserAttr):
    values = {'82254638_processed': '400'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ITEMS_Any Other Items Available: {option}"

class ItemsBannerS4X8(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ITEMS_BANNER(S) (4 x 8): {option}"

class ItemsBaseballCap(FormUserAttr):
    values = {'82254638_processed': '400'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ITEMS_BASEBALL CAP: {option}"

class ItemsGeneralMarket(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ITEMS_GENERAL MARKET: {option}"

class ItemsSpanishLanguage(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ITEMS_SPANISH LANGUAGE: {option}"

class ItemsUrban(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ITEMS_URBAN: {option}"

class ItemsWaterBottles(FormUserAttr):
    values = {'82254638_processed': "['29-980-7', '29-980-7', '400', '400']", '91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ITEMS_WATER BOTTLES: {option}"

class IfAMaterialOrDimensionalChangeAlsoInvolved(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's If a material or dimensional change also involved?: {option}"

class IfAnyAddressesOrTelephoneNumbersHaveChangedSinceTheLastReportingPeriodPleaseCheckHereAndNoteTheChangeInTheSpaceProvidedAtTheEndOfThisForm(FormUserAttr):
    values = {'0001477983_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's If any addresses or telephone numbers have changed since the last reporting period please check here and note the change in the space provided at the end of this form.: {option}"

class IfThereIsATransmissionProblemPleaseCall(FormUserAttr):
    values = {'01150773_01150774_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's If there is a transmission problem, please call:: {option}"

class IfYesSupplyDetails(FormUserAttr):
    values = {'716552_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's If yes supply details: {option}"

class IfYesPleaseCompleteTheFollowing(FormUserAttr):
    values = {'0001477983_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's If yes, please complete the following.: {option}"

class Implement(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Implement:: {option}"

class ImplementNo(FormUserAttr):
    values = {'0001123541_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Implement:_☐ No: {option}"

class ImplementPending(FormUserAttr):
    values = {'0001123541_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Implement:_☐ Pending: {option}"

class ImplementYes(FormUserAttr):
    values = {'0001123541_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Implement:_☐ Yes: {option}"

class Incidence(FormUserAttr):
    values = {'89867723_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Incidence: {option}"

class IncreaseCostsMayBePossibleToAbsorb(FormUserAttr):
    values = {'13149651_processed': '☑'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Increase Costs - May Be Possible to Absorb: {option}"

class InformationAndHearsayFromOutsideContacts(FormUserAttr):
    values = {'81186212_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Information and hearsay from outside contacts:: {option}"

class InitiationDate(FormUserAttr):
    values = {'89368010_processed': '25 March 1982'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Initiation Date: {option}"

class Inorganic(FormUserAttr):
    values = {'0060024314_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Inorganic: {option}"

class Institution(FormUserAttr):
    values = {'87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Institution:: {option}"

class Insurance(FormUserAttr):
    values = {'0060029036_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Insurance: {option}"

class IntInitDate(FormUserAttr):
    values = {'0011505151_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Int. Init. Date: {option}"

class InternalInitDate(FormUserAttr):
    values = {'11508234_processed': '3/ 1/ 95'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Internal Init Date: {option}"

class InterviewLength(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Interview Length:: {option}"

class InterviewsDividedAmong3Gorups(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Interviews divided among 3 gorups:: {option}"

class Invitations(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Invitations:: {option}"

class InvitationsRequested(FormUserAttr):
    values = {'92091873_processed': '50', '93213298_processed': '10'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Invitations:_#Requested: {option}"

class InvitationsDateNotified(FormUserAttr):
    values = {'92091873_processed': '9/ 5/ 95', '93213298_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Invitations:_Date Notified: {option}"

class InvitationsDateOrdered(FormUserAttr):
    values = {'92091873_processed': 'Unknown', '93213298_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Invitations:_Date Ordered: {option}"

class InviteesComments(FormUserAttr):
    values = {'93213298_processed': 'Invitees stated the Newport hospitality tent was very difficult to locate. Also, the Indy Lights Paddock area was not clearly identified Most Invitees were looking for the hospitality tent in a separate identified area away from the Paddock Brea and the Newport car transporter.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Invitees Comments:: {option}"

class IsThisACorporation(FormUserAttr):
    values = {'71341634_processed': 'Yes X No'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Is this a corporation: {option}"

class Jan(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's JAN.: {option}"

class JobNo(FormUserAttr):
    values = {'0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's JOB NO: {option}"

class Job(FormUserAttr):
    values = {'89867723_processed': '5546/ 1481'}

    @staticmethod
    def nl_desc(option):
        return f"The user's JOB#: {option}"

class Jul(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's JUL.: {option}"

class JimmyHBellBScScientist(FormUserAttr):
    values = {'00851772_1780_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Jimmy H. Bell B. Sc. Scientist: {option}"

class Jun(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Jun: {option}"

class KS(FormUserAttr):
    values = {'81749056_9057_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's K. S.: {option}"

class Kool(FormUserAttr):
    values = {'12052385_processed': '0595- 529- 1510 -0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's KOOL: {option}"

class KoolLights(FormUserAttr):
    values = {'0000999294_processed': '53+++ 60+++ 46 56+++ 50'}

    @staticmethod
    def nl_desc(option):
        return f"The user's KOOL Lights: {option}"

class KoolLightsKsWhiteTipPingMasked(FormUserAttr):
    values = {'0000999294_processed': '9.1 .88 14.0 .4 4'}

    @staticmethod
    def nl_desc(option):
        return f"The user's KOOL Lights KS- white tip- ping masked: {option}"

class KeyCriteriaForAnalysis(FormUserAttr):
    values = {'89867723_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Key Criteria For Analysis: {option}"

class Keywords1993(FormUserAttr):
    values = {'0001123541_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Keywords (1993): {option}"

class Kind(FormUserAttr):
    values = {'81574683_processed': '3.3 35,000y'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Kind: {option}"

class LAngeles(FormUserAttr):
    values = {'0001476912_processed': '8/5 and 6'}

    @staticmethod
    def nl_desc(option):
        return f"The user's L. Angeles: {option}"

class LRGravely(FormUserAttr):
    values = {'0012602424_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's L. R. GRAVELY: {option}"

class LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCratering(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's LASER PERFORATED TIPPING APPEARANCE CHECK HOLE DEPTH, SCORCHING, CRATERING: {option}"

class LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringBrand(FormUserAttr):
    values = {'0060000813_processed': '["CARLTON Filter 100\'s - 4 Mg Laser", \'Mfg. for Taiwan\']'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LASER PERFORATED TIPPING APPEARANCE CHECK HOLE DEPTH, SCORCHING, CRATERING_Brand:: {option}"

class LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringModules(FormUserAttr):
    values = {'0060000813_processed': '412'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LASER PERFORATED TIPPING APPEARANCE CHECK HOLE DEPTH, SCORCHING, CRATERING_Modules:: {option}"

class LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringPower(FormUserAttr):
    values = {'0060000813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LASER PERFORATED TIPPING APPEARANCE CHECK HOLE DEPTH, SCORCHING, CRATERING_Power:: {option}"

class LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringPulse(FormUserAttr):
    values = {'0060000813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LASER PERFORATED TIPPING APPEARANCE CHECK HOLE DEPTH, SCORCHING, CRATERING_Pulse:: {option}"

class LaserPerforatedTippingAppearanceCheckHoleDepthScorchingCrateringShiftDate(FormUserAttr):
    values = {'0060000813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LASER PERFORATED TIPPING APPEARANCE CHECK HOLE DEPTH, SCORCHING, CRATERING_Shift & Date:: {option}"

class Ld5095ConfidenceLimits(FormUserAttr):
    values = {'00040534_processed': '3.5 (3.1 to 3.9 g /kg'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LD50 (95% CONFIDENCE LIMITS): {option}"

class Ld5095Confidence(FormUserAttr):
    values = {'87672097_processed': 'LD0 = 10, 368 mg /kg'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LD50 95% CONFIDENCE : {option}"

class LeadIn(FormUserAttr):
    values = {'80707440_7443_processed': 'New York Football Fans'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LEAD- IN:: {option}"

class LhNumberS(FormUserAttr):
    values = {'00860012_00860014_processed': '21 017'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LH NUMBER (s): {option}"

class ListPrice(FormUserAttr):
    values = {'93329540_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LIST PRICE:: {option}"

class ListTheInformationBelowAsItPertainsToTheUrbanCenterPortionOfYourAssignmentOnly(FormUserAttr):
    values = {'92081358_1359_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LIST THE INFORMATION BELOW AS IT PERTAINS TO THE URBAN CENTER PORTION OF YOUR ASSIGNMENT ONLY:: {option}"

class LiteratureSurveyed(FormUserAttr):
    values = {'00851772_1780_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LITERATURE SURVEYED: {option}"

class LocalApproval(FormUserAttr):
    values = {'0060077689_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LOCAL APPROVAL: {option}"

class LocalPOreleaseNo(FormUserAttr):
    values = {'0060077689_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LOCAL P/ORELEASE NO.: {option}"

class Lorillard(FormUserAttr):
    values = {'00836244_processed': 'OR61 -2'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LORILLARD: {option}"

class LorillardCompoundCode(FormUserAttr):
    values = {'00851772_1780_processed': 'B73'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LORILLARD COMPOUND CODE: {option}"

class LorillardCompoundCodeNumber(FormUserAttr):
    values = {'00838511_00838525_processed': 'A41'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LORILLARD COMPOUND CODE NUMBER: {option}"

class LorillardNo(FormUserAttr):
    values = {'00040534_processed': 'OR39- 23', '87672097_processed': 'B75'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LORILLARD NO: {option}"

class LorillardResearchCenter(FormUserAttr):
    values = {'00837285_processed': 'Acute Cardiovascular- Mix 2 mg A32 with 0.2 ml 80% propylene glycol and grind lightly. Add 0.8 ml saline solution. A32 is a suspension in this mixture at room temperature. Reference OR 72- 152.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LORILLARD RESEARCH CENTER: {option}"

class Lot(FormUserAttr):
    values = {'00836244_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LOT: {option}"

class LotNo(FormUserAttr):
    values = {'87672097_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LOT NO: {option}"

class LotNoS(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LOT NO (s): {option}"

class LotNumber(FormUserAttr):
    values = {'00836816_processed': '', '00865872_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LOT NUMBER: {option}"

class Louisville(FormUserAttr):
    values = {'716552_processed': '10/ 30/ 81'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LOUISVILLE: {option}"

class LrbOrBillNoHanAuNo(FormUserAttr):
    values = {'13149651_processed': 'LRB 1946'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LRB Or Bill No. han Au No: {option}"

class LrcCompoundCode(FormUserAttr):
    values = {'00837285_processed': 'A32'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LRC COMPOUND CODE: {option}"

class LrcFileNumber(FormUserAttr):
    values = {'00836816_processed': 'A30', '00865872_processed': 'B164'}

    @staticmethod
    def nl_desc(option):
        return f"The user's LRC FILE NUMBER: {option}"

class Lt100S(FormUserAttr):
    values = {'81749056_9057_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LT. 100's: {option}"

class LtBox80S(FormUserAttr):
    values = {'81749056_9057_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LT. BOX 80's: {option}"

class LtKS(FormUserAttr):
    values = {'81749056_9057_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's LT. K. S.: {option}"

class LaboratoryAnalysis(FormUserAttr):
    values = {'00093726_processed': 'Smoke Analysis PMO Analysis'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Laboratory Analysis: {option}"

class Last(FormUserAttr):
    values = {'87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Last: {option}"

class LateRegistrationFeeAfterAugust(FormUserAttr):
    values = {'87682908_processed': '$ $185.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Late Registration Fee: (after August: {option}"

class Law(FormUserAttr):
    values = {'0060029036_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Law: {option}"

class LegalApproval(FormUserAttr):
    values = {'71190280_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Legal Approval: {option}"

class LegalApprovalRecommendedRequired(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Legal Approval Recommended/ Required:: {option}"

class LegalApprovalRecommendedRequiredNo(FormUserAttr):
    values = {'0013255595_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Legal Approval Recommended/ Required:_NO: {option}"

class LegalApprovalRecommendedRequiredYes(FormUserAttr):
    values = {'0013255595_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Legal Approval Recommended/ Required:_YES: {option}"

class Length(FormUserAttr):
    values = {'81574683_processed': '126 mm'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Length: {option}"

class LengthInt(FormUserAttr):
    values = {'89867723_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Length Int.: {option}"

class LengthOfCigarettes(FormUserAttr):
    values = {'01122115_processed': '85'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Length of Cigarettes: {option}"

class LengthOfRod(FormUserAttr):
    values = {'01122115_processed': '120 mm.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Length of Rod: {option}"

class LicenseeRefNo(FormUserAttr):
    values = {'0000989556_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Licensee Ref. NO.:: {option}"

class LobbyistName(FormUserAttr):
    values = {'0001477983_processed': 'Peter J. McGinn'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Lobbyist Name:: {option}"

class LocalPurchasing(FormUserAttr):
    values = {'0060025670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Local Purchasing: {option}"

class Local(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Local:: {option}"

class LocalDecreasCorts(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Local:_Decreas Corts: {option}"

class LocalMandatory(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Local:_Mandatory: {option}"

class LocalPermane(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Local:_Permane: {option}"

class LocalIncreaseCosts(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Local:_☐ Increase Costs: {option}"

class LocalNoOcaGOvernmentCost(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Local:_☐ No oca government cost: {option}"

class LocalPermissive(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Local:_☐ Permissive: {option}"

class Location(FormUserAttr):
    values = {'0001209043_processed': 'CHICAGO, DALLAS/ FORT WORTH, INDIANAPOLIS, LOS ANGELES MEMPHIS, PHILADELPHIA, PITTSBURGH', '0060077689_processed': 'STAMFORD, CT', '12825369_processed': 'See attached list', '92091873_processed': 'Leguna Seca, Monterey, Ca', '93213298_processed': 'DETROIT GRAND PRIX'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Location: {option}"

class LongRangeFiscalImplications(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Long Range Fiscal Implications: {option}"

class LotOrSample(FormUserAttr):
    values = {'0060214859_processed': 'ROLL 34 & 35'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Lot or Sample#: {option}"

class MBDavis(FormUserAttr):
    values = {'0011838621_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's M. b. Davis: {option}"

class Macon(FormUserAttr):
    values = {'716552_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's MACON: {option}"

class Madison25MmButt(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's MADISON 25 mm. Butt: {option}"

class Madison25MmButtMeanOfLast12Samples(FormUserAttr):
    values = {'0060094595_processed': "['1 .132', '0\\uf703 .37', '31 .0', '2 2.99', 'Basic', '23', '0', '1', '0']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's MADISON 25 mm. Butt_Mean of Last 12 Samples: {option}"

class Madison25MmButtPresentSample(FormUserAttr):
    values = {'0060094595_processed': "['1 .111', '0 .34', '37 .8', '3 .45', 'Basic', '11', '5', '4', '4']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's MADISON 25 mm. Butt_Present Sample: {option}"

class MajorMktAndMktResearchSteps(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's MAJOR MKT. AND MKT. RESEARCH STEPS: {option}"

class MajorMktAndMktResearchStepsInHomePlacement(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's MAJOR MKT. AND MKT. RESEARCH STEPS_In- home placement: {option}"

class Manufacturer(FormUserAttr):
    values = {'91355841_processed': 'BROWN & WILLIAMSON', '93329540_processed': 'AMERICAN TOBACCO COMPANY'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MANUFACTURER:: {option}"

class Manufacturers(FormUserAttr):
    values = {'93455715_processed': 'R. J. REYNOLDS AND PHILIP MORRIS'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MANUFACTURERS:: {option}"

class Market(FormUserAttr):
    values = {'01408099_01408101_processed': '', '12825369_processed': 'Lakeland Metro Market'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MARKET: {option}"

class MarketS(FormUserAttr):
    values = {'0011973451_processed': 'World- wide Duty Free', '71563825_processed': 'Bogotá, Medellin and Barranquilla'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MARKET (S):: {option}"

class MaterialNo(FormUserAttr):
    values = {'716552_processed': '50- 034'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MATERIAL NO: {option}"

class MaverickHarleyB1G1F(FormUserAttr):
    values = {'92039708_9710_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's MAVERICK/ HARLEY B1 G1 F: {option}"

class MechanicalProduction(FormUserAttr):
    values = {'0060068489_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's MECHANICAL PRODUCTION: {option}"

class Media(FormUserAttr):
    values = {'91391286_processed': 'MAGAZINE- HOT ROD', '91391310_processed': 'COUPON', '91974562_processed': 'DIRECT MAIL'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MEDIA: {option}"

class MediaMagazines(FormUserAttr):
    values = {'93351929_93351931_processed': "['People, Rolling Stone, Cosmopolitan,', 'Mademoiselle, New York Magazine']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's MEDIA_Magazines:: {option}"

class MediaNewspaper(FormUserAttr):
    values = {'93351929_93351931_processed': 'Village Voice'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MEDIA_Newspaper:: {option}"

class Medium(FormUserAttr):
    values = {'0060068489_processed': 'Outdoor', '0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's MEDIUM: {option}"

class Ment(FormUserAttr):
    values = {'0000999294_processed': '.4 4 .841'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MENT: {option}"

class Menthol(FormUserAttr):
    values = {'81574683_processed': '8098'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MENTHOL: {option}"

class MentholFlavor(FormUserAttr):
    values = {'00283813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's MENTHOL FLAVOR: {option}"

class MentholTaste7Better(FormUserAttr):
    values = {'0000999294_processed': '3.39*** 3.04 3.46*** 3.02 3.33** 3.06 3.45*** 2.99 2.34** 2.08'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MENTHOL TASTE (7= Better: {option}"

class Merchandise(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's MERCHANDISE:: {option}"

class MerchandiseOrderThroughYourSupplier(FormUserAttr):
    values = {'91939637_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's MERCHANDISE:_ORDER THROUGH YOUR SUPPLIER.: {option}"

class MerchandiseWillBeArbitrarilyShippedToStore(FormUserAttr):
    values = {'91939637_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's MERCHANDISE:_WILL BE ARBITRARILY SHIPPED TO STORE.: {option}"

class MethodOfPreparation(FormUserAttr):
    values = {'01197604_processed': 'Water removed by co- distillation with acetone under vacum at 45 C.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's METHOD OF PREPARATION:: {option}"

class MilitaryExport(FormUserAttr):
    values = {'716552_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's MILITARY ☐ EXPORT: {option}"

class Moist(FormUserAttr):
    values = {'0000999294_processed': '14.0 13. 5'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MOIST: {option}"

class MolecularWeight(FormUserAttr):
    values = {'00837285_processed': '200. 29'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MOLECULAR WEIGHT: {option}"

class MrPersonnel(FormUserAttr):
    values = {'0011505151_processed': 'B. R. Pellett', '12052385_processed': 'C. B. Pugh'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MR PERSONNEL:: {option}"

class Mrd(FormUserAttr):
    values = {'91161344_91161347_processed': '5546/478'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MRD #: {option}"

class MyCommissionExpires(FormUserAttr):
    values = {'91581919_processed': '2-9-90 Betty J. murphy (Notary Public)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's MY COMMISSION EXPIRES:: {option}"

class Macket(FormUserAttr):
    values = {'0000989556_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Macket:: {option}"

class Magazine(FormUserAttr):
    values = {'0001209043_processed': 'TIME'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Magazine: {option}"

class MaiCheckTo(FormUserAttr):
    values = {'71341634_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Mai Check To:: {option}"

class MailTo(FormUserAttr):
    values = {'87682908_processed': 'Ms. Susan Mathison Canadian Tobacco Manufacturers Council 701- 99 Bank Street Ottawa, Ontario, Canada K1P 6B9 (613) 238- 2799'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Mail to:: {option}"

class Maildate(FormUserAttr):
    values = {'00920294_processed': '3/ 17/ 97'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Maildate:: {option}"

class MailfileCells(FormUserAttr):
    values = {'00920294_processed': 'HD home delivery SP sneak preview'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Mailfile Cells: {option}"

class MailfileDescription(FormUserAttr):
    values = {'00920294_processed': 'Mail Order- Indy Responders'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Mailfile Description: {option}"

class MailfileId(FormUserAttr):
    values = {'00920294_processed': '3,'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Mailfile ID:: {option}"

class MajorAirportNearestYourHome(FormUserAttr):
    values = {'0060091229_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Major Airport Nearest your home:: {option}"

class MakerNo(FormUserAttr):
    values = {'01122115_processed': 'Research Division'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Maker No.: {option}"

class Male(FormUserAttr):
    values = {'0000999294_processed': 'KL', '00040534_processed': 'X', '87672097_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Male: {option}"

class Male99(FormUserAttr):
    values = {'0000999294_processed': '60+++ 34 6 100'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Male (99): {option}"

class Manager(FormUserAttr):
    values = {'0060025670_processed': '', '0060029036_processed': 'John Powell B J. Powell 1-11-94', '89867723_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Manager: {option}"

class ManagerComments(FormUserAttr):
    values = {'0000971160_processed': 'Manager, please contact suggester and forward comments to the Quality Council.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Manager Comments:: {option}"

class ManufacturerBrand(FormUserAttr):
    values = {'81186212_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Manufacturer & Brand:: {option}"

class Mar(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Mar: {option}"

class MarginalDifference(FormUserAttr):
    values = {'0000999294_processed': '80- 94% confidence Level'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Marginal Difference:: {option}"

class MarketSZoneS(FormUserAttr):
    values = {'71601299_processed': 'South Korea'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Market (s) / Zone (s): {option}"

class Marketing(FormUserAttr):
    values = {'0012178355_processed': '', '01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Marketing: {option}"

class MarketingResearch(FormUserAttr):
    values = {'89867723_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Marketing Research: {option}"

class MarketingAndOrResearchObjectives(FormUserAttr):
    values = {'80310840a_processed': 'Determine the level of interest and conversion opportunities among pompotitive smokers. receiving a Direct Mail offer for Newport Lights. Provide insight into the reasons for offer acceptance or rejection of offer and examine consumer perceptions about Newport Lights.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Marketing and or Research Objectives: {option}"

class MaterialTested(FormUserAttr):
    values = {'0060214859_processed': 'P- 830 GLASS FIBER'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Material Tested: {option}"

class May(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's May: {option}"

class MeanDrawOfRod(FormUserAttr):
    values = {'01122115_processed': '0 .12 (new scale)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Mean Draw of Rod: {option}"

class MediaName(FormUserAttr):
    values = {'87533049_processed': 'N/A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Media Name: {option}"

class MediaType(FormUserAttr):
    values = {'87533049_processed': 'ON - Carton Instant Redeemable'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Media Type: {option}"

class Message(FormUserAttr):
    values = {'0060036622_processed': 'Letter 8/ 1/ 76'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Message: {option}"

class Method(FormUserAttr):
    values = {'00851879_processed': 'Verbal Phone (Means of communication)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Method: {option}"

class MethodOfShipment(FormUserAttr):
    values = {'0001485288_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Method of Shipment: {option}"

class MethodOfTravel(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Method of travel:: {option}"

class MethodOfTravelAir(FormUserAttr):
    values = {'80728670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Method of travel:_Air: {option}"

class MethodOfTravelAuto(FormUserAttr):
    values = {'80728670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Method of travel:_Auto: {option}"

class MethodOfTravelOther(FormUserAttr):
    values = {'80728670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Method of travel:_Other: {option}"

class MethodOfTravelTrain(FormUserAttr):
    values = {'80728670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Method of travel:_Train: {option}"

class Mgr(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Mgr.: {option}"

class Middle(FormUserAttr):
    values = {'87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Middle: {option}"

class Military(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Military: {option}"

class Mo(FormUserAttr):
    values = {'0011906503_processed': '7'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Mo.: {option}"

class ModeratorsFee(FormUserAttr):
    values = {'89867723_processed': '$ 4. 500. 00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Moderators fee:: {option}"

class MondayYN(FormUserAttr):
    values = {'87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Monday (Y/ N): {option}"

class MyHandicapIs(FormUserAttr):
    values = {'0030031163_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's My handicap is:: {option}"

class NWKremer(FormUserAttr):
    values = {'0011838621_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's N. W. Kremer: {option}"

class Name(FormUserAttr):
    values = {'0030031163_processed': '', '0060029036_processed': 'Michael Wright John Powell', '00838511_00838525_processed': 'Paul Schickedantz, Jack Reid', '00851772_1780_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NAME: {option}"

class NameOrInitials(FormUserAttr):
    values = {'0013255595_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NAME OR INITIALS: {option}"

class NamesOfOtherPersonsCollaboratingInWork(FormUserAttr):
    values = {'0060302201_processed': 'L. W. McDowell'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NAMES OF OTHER PERSONS COLLABORATING IN WORK:: {option}"

class NatureOfWork(FormUserAttr):
    values = {'0000990274_processed': 'Advise if locally obtained Yucatan Honey (sample enclosed) is an acceptable substitute for HALWAY.', '0060302201_processed': 'Total aldehyde analysis in cigarette mainstream '}

    @staticmethod
    def nl_desc(option):
        return f"The user's NATURE OF WORK:: {option}"

class NewCompetitiveProducts(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW COMPETITIVE PRODUCTS: {option}"

class NewCompetitiveProductsBrandName(FormUserAttr):
    values = {'91361993_processed': 'CARDINAL CIGARETTES (11 PACKINGS)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW COMPETITIVE PRODUCTS_BRAND NAME:: {option}"

class NewCompetitiveProductsDate(FormUserAttr):
    values = {'91361993_processed': '10 /5 /92'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW COMPETITIVE PRODUCTS_DATE:: {option}"

class NewCompetitiveProductsExtentOfDistribution(FormUserAttr):
    values = {'91361993_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW COMPETITIVE PRODUCTS_EXTENT OF DISTRIBUTION:: {option}"

class NewCompetitiveProductsListPrice(FormUserAttr):
    values = {'91361993_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW COMPETITIVE PRODUCTS_LIST PRICE:: {option}"

class NewCompetitiveProductsManufacturer(FormUserAttr):
    values = {'91361993_processed': 'R. J. REYNOLDS'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW COMPETITIVE PRODUCTS_MANUFACTURER:: {option}"

class NewCompetitiveProductsOtherInformation(FormUserAttr):
    values = {'91361993_processed': 'SEE ATTACHMENT'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW COMPETITIVE PRODUCTS_OTHER INFORMATION:: {option}"

class NewCompetitiveProductsReportedBy(FormUserAttr):
    values = {'91361993_processed': 'C. M. WIECHMANN, D. M. , LUBBOCK, TX'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW COMPETITIVE PRODUCTS_REPORTED BY: {option}"

class NewCompetitiveProductsSizeOrSizes(FormUserAttr):
    values = {'91361993_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW COMPETITIVE PRODUCTS_SIZE OR SIZES:: {option}"

class NewCompetitiveProductsTime(FormUserAttr):
    values = {'91361993_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW COMPETITIVE PRODUCTS_TIME:: {option}"

class NewCompetitiveProductsTypeOfProduct(FormUserAttr):
    values = {'91361993_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW COMPETITIVE PRODUCTS_TYPE OF PRODUCT:: {option}"

class NewCompetitiveProductsCc(FormUserAttr):
    values = {'91361993_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW COMPETITIVE PRODUCTS_cc:: {option}"

class NewItem(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW ITEM: {option}"

class NewItemBrandS(FormUserAttr):
    values = {'716552_processed': 'VICEROY Rich Lights'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW ITEM_BRAND (S): {option}"

class NewItemDescription(FormUserAttr):
    values = {'716552_processed': "VICEROY Rich Lights 100' s 20' s Label"}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW ITEM_DESCRIPTION: {option}"

class NewItemMaterialNo(FormUserAttr):
    values = {'716552_processed': '50 -034A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW ITEM_MATERIAL NO.: {option}"

class NewItemNo(FormUserAttr):
    values = {'716552_processed': 'B1 -257'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW ITEM_NO: {option}"

class NewItemUpcNo(FormUserAttr):
    values = {'716552_processed': '272972'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NEW ITEM_UPC NO: {option}"

class NgDocumentsWereFoundWithinTheOriginal(FormUserAttr):
    values = {'0001463448_processed': 'FILE FOLDER REDROPE EXPANDABLE FILE HANGING FILE ENVELOPE OTHER (SPECIFY)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NG DOCUMENTS WERE FOUND WITHIN THE ORIGINAL:: {option}"

class Nic(FormUserAttr):
    values = {'0000999294_processed': '.88 .55'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NIC: {option}"

class Nicotine(FormUserAttr):
    values = {'0060308461_processed': "0.8 mg (Jan. '85 Report)"}

    @staticmethod
    def nl_desc(option):
        return f"The user's NICOTINE:: {option}"

class NoOfRotaries(FormUserAttr):
    values = {'12825369_processed': '8 RB'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NO OF ROTARIES: {option}"

class NoCartons(FormUserAttr):
    values = {'91939637_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NO. CARTONS: {option}"

class NoOfStores(FormUserAttr):
    values = {'81619511_9513_processed': '25'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NO. OF STORES: {option}"

class NotApproved(FormUserAttr):
    values = {'0060025670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NOT APPROVED: {option}"

class Note(FormUserAttr):
    values = {'0060308251_processed': 'Use Separate Form For Each Change', '71563825_processed': 'In order to establish a quantitative basis for determining the winning product, results will be'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NOTE:: {option}"

class NotebookPage(FormUserAttr):
    values = {'00040534_processed': 'B1014- 23', '00836244_processed': 'BIO7 -24', '01073843_processed': 'BC19-25'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NOTEBOOK PAGE: {option}"

class Notes(FormUserAttr):
    values = {'0000990274_processed': 'a) Nature of work should be specified in exact terms. b) R & D should advise if completion date cannot be met. c) Two copies of this form to be sent to R & D by initiator and R & D is to return to T. O. one completed copy.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NOTES:: {option}"

class NumberOfCartons(FormUserAttr):
    values = {'91939637_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NUMBER OF CARTONS: {option}"

class NumberOfCigarettesSmoked(FormUserAttr):
    values = {'01197604_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NUMBER OF CIGARETTES SMOKED:: {option}"

class NumberOfFollowingPages(FormUserAttr):
    values = {'0060165115_processed': '21 '}

    @staticmethod
    def nl_desc(option):
        return f"The user's NUMBER OF FOLLOWING PAGES: {option}"

class NumberOfPagesIncludingCoverSheet(FormUserAttr):
    values = {'92327794_processed': '8'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NUMBER OF PAGES (INCLUDING COVER SHEET):: {option}"

class NumberOfPanels(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's NUMBER OF PANELS: {option}"

class NumberOfPanelsIlluminated(FormUserAttr):
    values = {'0060207528_processed': '45'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NUMBER OF PANELS_ILLUMINATED: {option}"

class NumberOfPanelsRegular(FormUserAttr):
    values = {'0060207528_processed': '9'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NUMBER OF PANELS_REGULAR: {option}"

class NumberOfPanelsTotal(FormUserAttr):
    values = {'0060207528_processed': '54'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NUMBER OF PANELS_TOTAL: {option}"

class NumberOfSamplingPersonnel(FormUserAttr):
    values = {'80718412_8413_processed': '24 per day'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NUMBER OF SAMPLING PERSONNEL:: {option}"

class NumberOfSupervisors(FormUserAttr):
    values = {'80718412_8413_processed': '3'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NUMBER OF SUPERVISORS:: {option}"

class NumberViewed(FormUserAttr):
    values = {'12825369_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NUMBER VIEWED: {option}"

class Number(FormUserAttr):
    values = {'0011845203_processed': '1- 502- 568- 8092'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NUMBER:: {option}"

class Numbers(FormUserAttr):
    values = {'11875011_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NUMBERS:: {option}"

class NyoOnly(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's NYO ONLY:: {option}"

class NyoOnlyDateForwardedToPromotionServices(FormUserAttr):
    values = {'82254638_processed': '7/11/97'}

    @staticmethod
    def nl_desc(option):
        return f"The user's NYO ONLY:_DATE FORWARDED TO PROMOTION SERVICES:: {option}"

class NysawmdInc211East43rdStreetNewYorkNy100174707(FormUserAttr):
    values = {'0030031163_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's NYSAWMD, INC. 211 EAST 43RD STREET, NEW YORK, NY 10017-4707: {option}"

class NamePhoneExt(FormUserAttr):
    values = {'0000971160_processed': 'M. Hamann P. Harper, P. Martinez'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Name / Phone Ext. :: {option}"

class NameOfAccount(FormUserAttr):
    values = {'81619486_9488_processed': '', '81619511_9513_processed': '_7-Eleven ', '81749056_9057_processed': 'None'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Name of Account: {option}"

class NameOfEvent(FormUserAttr):
    values = {'0011976929_processed': 'Mrs. Illinois Beauty Pageant', '82254638_processed': 'Lorillard Metro Golf Outing 1997'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Name of Event:: {option}"

class NameOfGuests(FormUserAttr):
    values = {'0060091229_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Name of Guests: {option}"

class NameOfSpouseParticipatingInTheGuestPrograms(FormUserAttr):
    values = {'87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Name of spouse participating in the guest programs: {option}"

class NatureOfAction(FormUserAttr):
    values = {'0012947358_processed': 'Strike" cigarettes manufactured by defendant, wherein plaintiff alleges breach of was- anties, seeks damages in excess of $5, 000 and demands trial by jury.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Nature of Action:: {option}"

class NewBalance(FormUserAttr):
    values = {'0012529295_processed': '(452 ,408, 08)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's New Balance: {option}"

class NewspaperDate(FormUserAttr):
    values = {'0001438955_processed': 'Pittsburgh Pittsburgh PUTSBURGH PRESS (4 /23 /72 San Diego SAN DIEGO UNION (4 /23 /72 Dayton DAYTON NEWS (4 /23 /72) Birmingham BIRMINGHAM NEWS (4 /23 /72)\uf702'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Newspaper (Date): {option}"

class No(FormUserAttr):
    values = {'0060024314_processed': '', '0060214859_processed': '436', '00836244_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's No: {option}"

class NoPreference(FormUserAttr):
    values = {'0000999294_processed': '8 6 11 9 8'}

    @staticmethod
    def nl_desc(option):
        return f"The user's No Preference: {option}"

class No1RollerOverTape(FormUserAttr):
    values = {'01122115_processed': '1 .194'}

    @staticmethod
    def nl_desc(option):
        return f"The user's No. 1 Roller over Tape: {option}"

class NoOfCartons(FormUserAttr):
    values = {'88057519_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's No. OF CARTONS: {option}"

class Nov(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Nov: {option}"

class NumberOfStores(FormUserAttr):
    values = {'81619486_9488_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Number of Stores: {option}"

class OOrganizerIfApplicable(FormUserAttr):
    values = {'0060262650_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's O ORGANIZER (if applicable):: {option}"

class Objective(FormUserAttr):
    values = {'0011973451_processed': 'Generate incremental volume for B& W by providing a low price brand to various international duty- free markets.', '0071032790_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's OBJECTIVE:: {option}"

class Oct(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's OCT.: {option}"

class Of(FormUserAttr):
    values = {'01408099_01408101_processed': '', '71206427_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's OF: {option}"

class Operator(FormUserAttr):
    values = {'12825369_processed': 'The Lamar Corp.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's OPERATOR: {option}"

class Option(FormUserAttr):
    values = {'01191071_1072_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's OPTION: {option}"

class Or(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's OR: {option}"

class Oral(FormUserAttr):
    values = {'00836816_processed': 'Reference OR 100- 32 . 5g A30 soluble in .5 mL corn oil at room temperature.', '00865872_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ORAL: {option}"

class OrderNo(FormUserAttr):
    values = {'00920222_processed': '', '00922237_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ORDER NO.: {option}"

class OrientationMeeting(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's ORIENTATION MEETING:: {option}"

class OrientationMeetingDate(FormUserAttr):
    values = {'80718412_8413_processed': 'October 3rd'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ORIENTATION MEETING:_Date:: {option}"

class OrientationMeetingPlace(FormUserAttr):
    values = {'80718412_8413_processed': 'Boston Park Plaza Room 412 64 Arlington Street Boston, Mass 02117 617/ 426- 2000'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ORIENTATION MEETING:_Place:: {option}"

class OrientationMeetingTime(FormUserAttr):
    values = {'80718412_8413_processed': '9: 30 a. m.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ORIENTATION MEETING:_Time:: {option}"

class OriginalCompletionDate(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's ORIGINAL COMPLETION DATE: {option}"

class OriginalCompletionDate1St(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ORIGINAL COMPLETION DATE_1st: {option}"

class OriginalCompletionDate79(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ORIGINAL COMPLETION DATE_79: {option}"

class OriginalCompletionDateQtr(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ORIGINAL COMPLETION DATE_Qtr.: {option}"

class OriginalSignedProjectSheetsToPso(FormUserAttr):
    values = {'00866042_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ORIGINAL SIGNED PROJECT SHEETS TO PSO: {option}"

class OtherComments(FormUserAttr):
    values = {'91355841_processed': '', '93455715_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's OTHER COMMENTS:: {option}"

class OtherInformation(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's OTHER INFORMATION: {option}"

class OtherInformationDateRequested(FormUserAttr):
    values = {'0011845203_processed': '2/ 22 by courier'}

    @staticmethod
    def nl_desc(option):
        return f"The user's OTHER INFORMATION_DATE REQUESTED:: {option}"

class OtherInformationDeadlineForBidReceipt(FormUserAttr):
    values = {'0011845203_processed': '3/1/91'}

    @staticmethod
    def nl_desc(option):
        return f"The user's OTHER INFORMATION_DEADLINE FOR BID RECEIPT:: {option}"

class OtherPersonnelAssigned(FormUserAttr):
    values = {'0011856542_processed': '', '0060007216_processed': 'E. P. Barbee', '0071032807_processed': 'Analytical Section is doing most of the work on vapor phase. PDL and John Brooks preparing charocal impregnated RC.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's OTHER PERSONNEL ASSIGNED: {option}"

class OttApprovals(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's OTT APPROVALS: {option}"

class OttApprovalsDate(FormUserAttr):
    values = {'71190280_processed': '10/22/98 10/22/98', '71366499_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's OTT APPROVALS_Date: {option}"

class OttApprovalsDepartment(FormUserAttr):
    values = {'71190280_processed': 'production AE', '71366499_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's OTT APPROVALS_Department: {option}"

class OttApprovalsSignature(FormUserAttr):
    values = {'71190280_processed': 'LKelly ', '71366499_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's OTT APPROVALS_Signature: {option}"

class OurFaxNumberIs(FormUserAttr):
    values = {'92327794_processed': '(919) 373- 6917'}

    @staticmethod
    def nl_desc(option):
        return f"The user's OUR FAX NUMBER IS:: {option}"

class Overall(FormUserAttr):
    values = {'0001209043_processed': '1.0 (.97) 31 (167)', '0001476912_processed': '1.7'}

    @staticmethod
    def nl_desc(option):
        return f"The user's OVERALL: {option}"

class OfferDescription(FormUserAttr):
    values = {'0060173256_processed': 'Displays'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Offer Description: {option}"

class OnWhomProcessWasServed(FormUserAttr):
    values = {'0012947358_processed': 'Phyllis G. Jonnings, Asst. Socy,. The Corporation Company, Jacksonville, Florida'}

    @staticmethod
    def nl_desc(option):
        return f"The user's On Whom Process was Served:: {option}"

class OperatorInitials(FormUserAttr):
    values = {'0001129658_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Operator Initials:: {option}"

class OrganizationEmployerName(FormUserAttr):
    values = {'0001477983_processed': 'R. J. Reynolds Tobacco'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Organization/ Employer Name:: {option}"

class Original(FormUserAttr):
    values = {'0012529295_processed': 'Project File', '0012602424_processed': '- PROJECT FILE', '12603270_processed': 'Project File S. Willinger ', '13149651_processed': '☑'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Original: {option}"

class OriginalBudgetedAmount(FormUserAttr):
    values = {'0001463282_processed': '23.3'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Original Budgeted Amount: {option}"

class OriginalRequestMadeBy(FormUserAttr):
    values = {'00093726_processed': 'Dr. A. W. Spears', '00283813_processed': 'Mr. C. L. Tucker, Jr.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Original Request Made By: {option}"

class Originator(FormUserAttr):
    values = {'0060029036_processed': 'Michael Wright', '0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Originator: {option}"

class Other(FormUserAttr):
    values = {'0001477983_processed': '', '0060024314_processed': '', '0060077689_processed': '', '00860012_00860014_processed': '', '81574683_processed': '1100 pks.', '92314414_processed': '$20.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Other: {option}"

class OtherSpecifications(FormUserAttr):
    values = {'88547278_88547279_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Other Specifications:: {option}"

class OwnBrandDunhillSmokers(FormUserAttr):
    values = {'71601299_processed': '150 Males, 25 ~ 39 years old, ABC+ who live Seoul/ Pusan'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Own Brand - Dunhill Smokers:: {option}"

class POBox(FormUserAttr):
    values = {'87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's P. O. Box #: {option}"

class PS(FormUserAttr):
    values = {'0060000813_processed': '73 -91'}

    @staticmethod
    def nl_desc(option):
        return f"The user's P. S.: {option}"

class PackAndOrCartocarton(FormUserAttr):
    values = {'91391286_processed': 'PACK'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PACK AND OR/ CARTOCARTON: {option}"

class PackAndOrCarton(FormUserAttr):
    values = {'91391310_processed': 'PACK', '91974562_processed': 'PACK OR CARTON', '93351929_93351931_processed': 'Pack'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PACK AND OR/CARTON: {option}"

class Packing(FormUserAttr):
    values = {'81749056_9057_processed': "BOX 80's LT. BOX 80's 100's LT. 100's K. S. LT. K. S."}

    @staticmethod
    def nl_desc(option):
        return f"The user's PACKING: {option}"

class PackingBox80SWhereAvailable(FormUserAttr):
    values = {'91939637_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PACKING_BOX 80's WHERE AVAILABLE: {option}"

class PackingFilter100S(FormUserAttr):
    values = {'91939637_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PACKING_FILTER 100's: {option}"

class PackingFilterKS(FormUserAttr):
    values = {'91939637_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PACKING_FILTER K.S.: {option}"

class Packs(FormUserAttr):
    values = {'81749056_9057_processed': '30 20 30'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PACKS: {option}"

class Page(FormUserAttr):
    values = {'01191071_1072_processed': '03'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PAGE: {option}"

class PageNumberSWereMissingInTheOriginal(FormUserAttr):
    values = {'0001463448_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PAGE NUMBER(S) WERE MISSING IN THE ORIGINAL.: {option}"

class PageS(FormUserAttr):
    values = {'0060029036_processed': 'SME'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PAGE(S): {option}"

class Paid1987(FormUserAttr):
    values = {'0011505151_processed': '47,218'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PAID 1987: {option}"

class PaidOutOf1987Budget(FormUserAttr):
    values = {'12052385_processed': 'JAN'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PAID OUT OF 1987 BUDGET: {option}"

class PaidOutOf1989Budget(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's PAID OUT OF 1989 BUDGET: {option}"

class PaidOutOf1989BudgetDec(FormUserAttr):
    values = {'0011505151_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PAID OUT OF 1989 BUDGET_DEC: {option}"

class PaidOutOf1989BudgetFeb(FormUserAttr):
    values = {'0011505151_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PAID OUT OF 1989 BUDGET_FEB: {option}"

class Partial(FormUserAttr):
    values = {'81619486_9488_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PARTIAL: {option}"

class Payroll(FormUserAttr):
    values = {'92314414_processed': '700'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PAYROLL:: {option}"

class Pdc(FormUserAttr):
    values = {'0000999294_processed': 'C273- 82- 7'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PDC #: {option}"

class PerformingDepartments(FormUserAttr):
    values = {'00860012_00860014_processed': 'Acute/ Dermal Toxicology', '00866042_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PERFORMING DEPARTMENTS: {option}"

class PeriodFrom(FormUserAttr):
    values = {'0060068489_processed': 'April THRU July'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PERIOD. FROM: {option}"

class Permanent(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's PERMANENT: {option}"

class Petersburg(FormUserAttr):
    values = {'716552_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PETERSBURG: {option}"

class PhCalculated50(FormUserAttr):
    values = {'81310636_processed': '5. 26'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PH (CALCULATED 50%): {option}"

class Ph(FormUserAttr):
    values = {'660978_processed': 'mg'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PH:: {option}"

class PhysicalAppearance(FormUserAttr):
    values = {'81310636_processed': 'Yellow liquid'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PHYSICAL APPEARANCE: {option}"

class PhysicalDescription(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's PHYSICAL DESCRIPTION:: {option}"

class PhysicalDescriptionColor(FormUserAttr):
    values = {'00860012_00860014_processed': 'Brown'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PHYSICAL DESCRIPTION:_COLOR: {option}"

class PhysicalDescriptionLiquid(FormUserAttr):
    values = {'00860012_00860014_processed': '', '00866042_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PHYSICAL DESCRIPTION:_LIQUID: {option}"

class PhysicalDescriptionPressurized(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PHYSICAL DESCRIPTION:_PRESSURIZED: {option}"

class PhysicalDescriptionSolid(FormUserAttr):
    values = {'00860012_00860014_processed': 'X', '00866042_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PHYSICAL DESCRIPTION:_SOLID: {option}"

class PhysicalState(FormUserAttr):
    values = {'00836816_processed': 'Clear Colorless liquid', '00865872_processed': 'Brownish- gray powder'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PHYSICAL STATE: {option}"

class Place(FormUserAttr):
    values = {'660978_processed': 'Telephone'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PLACE:: {option}"

class PlantAverage(FormUserAttr):
    values = {'0060207528_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PLANT AVERAGE: {option}"

class PlantOperator(FormUserAttr):
    values = {'0060207528_processed': 'Patrick Media Group, Inc'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PLANT OPERATOR:: {option}"

class PleaseDeliverTransmissionTo(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's PLEASE DELIVER TRANSMISSION TO:: {option}"

class PleaseDeliverTransmissionToFaxPhoneNumber(FormUserAttr):
    values = {'91914407_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PLEASE DELIVER TRANSMISSION TO:_FAX PHONE NUMBER:: {option}"

class PleaseDeliverTransmissionToName(FormUserAttr):
    values = {'91914407_processed': 'Mr. Al Giacoio'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PLEASE DELIVER TRANSMISSION TO:_NAME:: {option}"

class PleaseDeliverTransmissionToOffice(FormUserAttr):
    values = {'91914407_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PLEASE DELIVER TRANSMISSION TO:_OFFICE:: {option}"

class PleaseNotifyThisDepartmentOfAnyChangesInTheCodeNumberS(FormUserAttr):
    values = {'0011859695_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PLEASE NOTIFY THIS DEPARTMENT OF ANY CHANGES IN THE CODE NUMBER(S).: {option}"

class PleaseTransmitThisDocumentTo(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's PLEASE TRANSMIT THIS DOCUMENT TO:: {option}"

class PleaseTransmitThisDocumentToFaxPhoneNumber(FormUserAttr):
    values = {'91372360_processed': '212 545- 3299', '92657391_processed': '(212) 545- 3299'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PLEASE TRANSMIT THIS DOCUMENT TO:_FAX PHONE NUMBER:: {option}"

class PleaseTransmitThisDocumentToName(FormUserAttr):
    values = {'91372360_processed': 'Mr. A. J. Giacoio', '92657391_processed': 'R. H. Orcutt'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PLEASE TRANSMIT THIS DOCUMENT TO:_NAME:: {option}"

class PleaseTransmitThisDocumentToOffice(FormUserAttr):
    values = {'91372360_processed': 'New York- Sales Planning', '92657391_processed': 'Lorillard- New York'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PLEASE TRANSMIT THIS DOCUMENT TO:_OFFICE:: {option}"

class Pm6(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's PM6: {option}"

class Pm6Base(FormUserAttr):
    values = {'0001476912_processed': '(234)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PM6 Base:: {option}"

class Pm6Scores(FormUserAttr):
    values = {'0001476912_processed': '0.0 3.3 0.0 3.3 0.0 0.0 0.0 9.3 0.0 5.0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PM6 SCORES: {option}"

class Pm6Score(FormUserAttr):
    values = {'0001209043_processed': "['1.0', '2.0', '0.0', '2.4', '0.0']", '0001438955_processed': "['3.4%', '1.9', '5.0', '3.2', '3.0', '4.4', '4.0', '3.1', '4.2']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's PM6_SCORE: {option}"

class Population(FormUserAttr):
    values = {'12825369_processed': '400.400 '}

    @staticmethod
    def nl_desc(option):
        return f"The user's POPULATION: {option}"

class PopulationComposition(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's POPULATION COMPOSITION:: {option}"

class PopulationCompositionBlack(FormUserAttr):
    values = {'92081358_1359_processed': '80%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's POPULATION COMPOSITION:_% BLACK =: {option}"

class PopulationCompositionHispanic(FormUserAttr):
    values = {'92081358_1359_processed': '5%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's POPULATION COMPOSITION:_% HISPANIC =: {option}"

class PopulationCompositionOther(FormUserAttr):
    values = {'92081358_1359_processed': '5%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's POPULATION COMPOSITION:_% OTHER : {option}"

class PopulationCompositionTotal(FormUserAttr):
    values = {'92081358_1359_processed': '100%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's POPULATION COMPOSITION:_% TOTAL =: {option}"

class PopulationCompositionWhite(FormUserAttr):
    values = {'92081358_1359_processed': '10%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's POPULATION COMPOSITION:_% WHITE =: {option}"

class PosterDesign(FormUserAttr):
    values = {'0060207528_processed': 'THE TASTE BREAKS THROUGH'}

    @staticmethod
    def nl_desc(option):
        return f"The user's POSTER DESIGN:: {option}"

class PostiveControlUgPlate(FormUserAttr):
    values = {'00836244_processed': '', '01073843_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's POSTIVE CONTROL (ug plate): {option}"

class PpsProgram(FormUserAttr):
    values = {'0011974919_processed': '602399'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PPS Program #: {option}"

class PreSell(FormUserAttr):
    values = {'92039708_9710_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRE- SELL: {option}"

class PredominantBuydownValueOfTargetedBrandsDoralGPCBasic(FormUserAttr):
    values = {'81749056_9057_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PREDOMINANT BUYDOWN VALUE OF TARGETED BRANDS (DORAL G. P. C/ BASIC): {option}"

class Preference(FormUserAttr):
    values = {'0000999294_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PREFERENCE:: {option}"

class PresentForm(FormUserAttr):
    values = {'00070353_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRESENT FORM:: {option}"

class PresentStatusOfWorkCiteProgressReportsWhereAppropriate(FormUserAttr):
    values = {'0060302201_processed': 'Techniques worked out and reported for pure aldehyde samples; must be adapted for cigarette mainstream smoke by further laboratory work'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRESENT STATUS OF WORK (Cite progress reports where appropriate): {option}"

class Present(FormUserAttr):
    values = {'660978_processed': '(For the client) T. Parrack'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRESENT:: {option}"

class PressQuery(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRESS QUERY: {option}"

class PressQueryDate(FormUserAttr):
    values = {'0011899960_processed': '7/ 9/ 84'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRESS QUERY_Date: {option}"

class PressQueryDescribeTheStorylineListTheQuestionsAndProposedAnswersAndSummarizeHandlingIncludingClearances(FormUserAttr):
    values = {'0011899960_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRESS QUERY_Describe the storyline, list the questions and proposed answers, and summarize handling, including clearances.: {option}"

class PressQueryPublication(FormUserAttr):
    values = {'0011899960_processed': 'ADWEEK - Midwest'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRESS QUERY_Publication: {option}"

class PressQueryReceivedBy(FormUserAttr):
    values = {'0011899960_processed': 'Mark Ahearn'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRESS QUERY_Received by: {option}"

class PressQueryReporterEditor(FormUserAttr):
    values = {'0011899960_processed': 'Fran Brock (312) 467- 6500'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRESS QUERY_Reporter/ Editor: {option}"

class PressQueryTime(FormUserAttr):
    values = {'0011899960_processed': '1: 45 P. M.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRESS QUERY_Time: {option}"

class Pressurized(FormUserAttr):
    values = {'00866042_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRESSURIZED: {option}"

class Previous(FormUserAttr):
    values = {'0012602424_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PREVIOUS: {option}"

class Price(FormUserAttr):
    values = {'0060077689_processed': '$20, 580. 00 $15, 190. 00 $431 .25 $48 .75', '00920222_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRICE: {option}"

class PrimaryClassOfTrade(FormUserAttr):
    values = {'92081358_1359_processed': 'Convenience/ Grocery'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRIMARY CLASS OF TRADE:: {option}"

class PrimaryDistributionChannelEGJobberSubJobberMembership(FormUserAttr):
    values = {'92081358_1359_processed': '*Jobber/ Membership'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRIMARY DISTRIBUTION CHANNEL (E. G. JOBBER, SUB- JOBBER MEMBERSHIP: {option}"

class Priority(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRIORITY: {option}"

class PriorityDefer(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRIORITY_Defer: {option}"

class PriorityHigh(FormUserAttr):
    values = {'71108371_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRIORITY_High: {option}"

class PriorityImmediate(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRIORITY_Immediate: {option}"

class PriorityLow(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRIORITY_Low: {option}"

class PriorityMedium(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRIORITY_Medium: {option}"

class ProblemDefinition(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROBLEM DEFINITION: {option}"

class ProblemDefinitionDescriptionOfRequest(FormUserAttr):
    values = {'71108371_processed': 'Please run job FRMRXUM2 for GPC, Misty, and Kool against file b:\\common\\khutchi\\r892unm.lst. Please place output in the same directory.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROBLEM DEFINITION_Description of Request:: {option}"

class ProblemDefinitionReasonForRequest(FormUserAttr):
    values = {'71108371_processed': 'Calculation of 1997 STR volumes for these brands for allocation of Period 2A budgets.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROBLEM DEFINITION_Reason for Request:: {option}"

class ProblemDefinitionRequestAuthorizedBy(FormUserAttr):
    values = {'71108371_processed': 'Karl Hutchison'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROBLEM DEFINITION_Request Authorized By:: {option}"

class Product(FormUserAttr):
    values = {'0000990274_processed': 'LUCKY STRIKE Filter and VICEROY', '0011859695_processed': 'Pall Mail Filter tip', '660978_processed': 'Viceroy', '80707440_7443_processed': 'Kent, Newport, True and Old Gold', '80718412_8413_processed': 'Old Gold Lights'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRODUCT:: {option}"

class ProductCade639(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRODUCT_Cade # 639: {option}"

class ProductCode519(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRODUCT_Code # #519: {option}"

class ProductCode327(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRODUCT_Code # 327: {option}"

class ProductCode462(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRODUCT_Code # 462: {option}"

class ProductCode741(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRODUCT_Code # 741: {option}"

class ProductCode753(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRODUCT_Code # 753: {option}"

class ProductCode934(FormUserAttr):
    values = {'91161344_91161347_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PRODUCT_Code # 934: {option}"

class ProfitImprovement(FormUserAttr):
    values = {'0001123541_processed': '(If Applicable)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROFIT IMPROVEMENT:: {option}"

class Program(FormUserAttr):
    values = {'0060136394_processed': '1/2 HOUR PROGRAMES'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROGRAM: {option}"

class Projeci(FormUserAttr):
    values = {'0012602424_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECI:: {option}"

class Project(FormUserAttr):
    values = {'0001239897_processed': '# 19 4- 26A', '0071032790_processed': 'To develop cigarette Cigarette to utilize a filter tip with longitudinal grooves from the mouth end to the tobacco end in con- junction with perforated tipping paper.', '71601299_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECT: {option}"

class ProjectCode(FormUserAttr):
    values = {'0011856542_processed': 'BD-FF', '0060007216_processed': 'PMRM', '0071032807_processed': 'CST- N- 68'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECT CODE: {option}"

class ProjectCoordinator(FormUserAttr):
    values = {'00860012_00860014_processed': '', '00866042_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECT COORDINATOR: {option}"

class ProjectDescription(FormUserAttr):
    values = {'0011906503_processed': 'The Cigarette Test Station (CTS400) combines many of the stand- alone instruments that R&D currently uses to measure cigarette weight, pressure drop, ventilation, and hardness into one compact module. The CTS400 has the additional measurement of cigarette hardness in comparison with the CTS300. With this added, measurement R&D will be able to replace the Firmness Integrator that measures cigarette firmness in addition to other measurements that are mentioned above. The Firmness Integrator is no longer manufactured and parts are becoming difficult to obtain. Lastly, purchase of this instrument would provide similar capability as the Macon Plant and help facilitate comparisions between laboratories.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECT DESCRIPTION: {option}"

class ProjectLeader(FormUserAttr):
    values = {'0011856542_processed': 'J. F. Anders/ J. E. Mann', '0060007216_processed': 'J. F. Anders', '0071032807_processed': 'Mann', '01408099_01408101_processed': 'Williams/ Giordano'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECT LEADER: {option}"

class ProjectName(FormUserAttr):
    values = {'0011856542_processed': 'BULL DURHAM Full Flavor King Size Cigarettes', '0060007216_processed': 'PALL MALL Regular Menthol', '0071032807_processed': 'Charcoal Smoking Tobacco', '01408099_01408101_processed': "True 100's (R&M)"}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECT NAME: {option}"

class ProjectNumber(FormUserAttr):
    values = {'0011845203_processed': '1991- 18', '11875011_processed': '1995- 13D', '71108371_processed': '(assigned by MIS)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECT NUMBER:: {option}"

class ProjectObjective(FormUserAttr):
    values = {'0011856542_processed': 'Develop 14- mg "tar" delivery king size cigarette for generic pricing directed toward young male smokers. Cigarette dimensions- 85 mm x 24.9 mm circumference- 20 mm filter- 24 mm tipping. Offshore tobacco blend with unique flavor formulation. Cork tipping.', '0060007216_processed': 'To develop a nonfilter menthol cigarette delivering 21- 24 mg "tar" as a menthol companion to PALL MALL Famous Cigarettes.', '0071032807_processed': 'A pipe tobacco containing activated charcoal - must show vapor phase reduction.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECT OBJECTIVE: {option}"

class ProjectOriginatedBy(FormUserAttr):
    values = {'91161344_91161347_processed': 'William Doyle'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECT ORIGINATED BY: {option}"

class ProjectSheetNo(FormUserAttr):
    values = {'00860012_00860014_processed': '4'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECT SHEET NO: {option}"

class ProjectTitle(FormUserAttr):
    values = {'89867723_processed': 'No Side Stream Smoke Focus Groups'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECT TITLE: {option}"

class ProjectedCurrentYearExpenses19(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECTED CURRENT YEAR EXPENSES 19: {option}"

class ProjectedCurrentYearExpenses19Actual8Months(FormUserAttr):
    values = {'91104867_processed': "['17,000', '8.000', '16.000', '19.000', '60,000']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECTED CURRENT YEAR EXPENSES 19_ACTUAL 8 MONTHS: {option}"

class ProjectedCurrentYearExpenses19Projected4Months(FormUserAttr):
    values = {'91104867_processed': "['8,500', '10,000', '4,000', '10.000', '32,500']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECTED CURRENT YEAR EXPENSES 19_PROJECTED 4 MONTHS: {option}"

class ProjectedCurrentYearExpenses19TotalYear(FormUserAttr):
    values = {'91104867_processed': "['25,500', '18,000', '20,000', '29,000', '92,500']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECTED CURRENT YEAR EXPENSES 19_TOTAL YEAR: {option}"

class Projected(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECTED:: {option}"

class ProjectedExtAuthDate(FormUserAttr):
    values = {'0012529284_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECTED:_Ext. Auth. Date: {option}"

class ProjectedExtAuthDateWaveS(FormUserAttr):
    values = {'0001463282_processed': '12/ 90', '0011838621_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECTED:_Ext. Auth. Date Wave (s): {option}"

class ProjectedFieldComplete(FormUserAttr):
    values = {'0012529284_processed': '', '0012529295_processed': '10/ 11/ 87', '0012602424_processed': 'Dec. 1984'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECTED:_Field Complete: {option}"

class ProjectedFieldCompleteWaveS(FormUserAttr):
    values = {'0001463282_processed': '6/ 10/ 90', '0011838621_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECTED:_Field Complete Wave (s): {option}"

class ProjectedFinalReportDueSupplierRpt(FormUserAttr):
    values = {'0012529284_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECTED:_Final Report Due (Supplier Rpt.): {option}"

class ProjectedFinalReportDueSupplierRptWaveS(FormUserAttr):
    values = {'0001463282_processed': '7/ 9/ 90', '0011838621_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECTED:_Final Report Due (Supplier Rpt.) Wave (s): {option}"

class ProjectedInternalInitDate(FormUserAttr):
    values = {'0001463282_processed': '4/ ', '0011838621_processed': '', '0012529284_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROJECTED:_Internal Init. Date: {option}"

class Promo(FormUserAttr):
    values = {'92094746_processed': '28', '92094751_processed': '28'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROMO #: {option}"

class PromotionalImpact(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROMOTIONAL IMPACT:: {option}"

class PromotionalImpact50OffPack(FormUserAttr):
    values = {'92657311_7313_processed': 'Excellent movement when couponed. Without coupons, movement slows dramatically!'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROMOTIONAL IMPACT:_$ 50 OFF PACK:: {option}"

class PromotionalImpact500OffCarton(FormUserAttr):
    values = {'91315069_91315070_processed': '', '92657311_7313_processed': 'Excellent. Continues to drive all carton business'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROMOTIONAL IMPACT:_$5.00 OFF CARTON:: {option}"

class PromotionalImpact20CentsOffPackCouponSticker(FormUserAttr):
    values = {'89817999_8002_processed': 'HAS PROVEN TO BE AN EXCELLENT TOOL IN GENERATING PACK TRIAL IN BOTH HIGH AND LOW DEVELOPMENT PRICE VALUE MARKETS. MANY DISPLAYS SELLING OUT BEFORE RECONTACT.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROMOTIONAL IMPACT:_20 CENTS OFF PACK COUPON/STICKER:: {option}"

class PromotionalImpactSalesForce20S(FormUserAttr):
    values = {'89817999_8002_processed': 'ADDITIONAL SUPPLY WOULD BE HELPFUL. INITIAL QUANTITIES WERE QUICKLY DEPLETED', '92657311_7313_processed': 'Excellent but quickly depleted.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROMOTIONAL IMPACT:_SALES FORCE 20'S: {option}"

class PromotionalPeriod(FormUserAttr):
    values = {'91939637_processed': 'May- June 1992', '92094746_processed': 'June/ July', '92094751_processed': 'June /July 1995'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROMOTIONAL PERIOD:: {option}"

class ProtectivePrecautionsRequired(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROTECTIVE PRECAUTIONS REQUIRED: {option}"

class ProvedRecall(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROVED RECALL: {option}"

class ProvedRecallBase(FormUserAttr):
    values = {'0001209043_processed': "['(167)', '(83)', '(84)', '(81)', '(86)', '(42)', '(125)']", '0001438955_processed': "['(222)', '(101)', '(121)', '(117)', '(105)', '(17)', '(205)']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROVED RECALL_BASE: {option}"

class ProvedRecallScore(FormUserAttr):
    values = {'0001209043_processed': "['31', '31', '31', '33', '29', '33', '30']", '0001438955_processed': "['7%', '7', '7', '5', '9', '6', '7']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's PROVED RECALL_SCORE: {option}"

class Publication(FormUserAttr):
    values = {'80707440_7443_processed': 'Daily Newspapers'}

    @staticmethod
    def nl_desc(option):
        return f"The user's PUBLICATION: {option}"

class Purchasing(FormUserAttr):
    values = {'00922237_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's PURCHASING: {option}"

class PackingAndDistribution(FormUserAttr):
    values = {'88547278_88547279_processed': 'Bulk in cartons, FOB Oceanside Please allow 14 working days for delivery'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Packing and Distribution:: {option}"

class PaperAndMaterials(FormUserAttr):
    values = {'88547278_88547279_processed': '24 pt. Carolina C/1/S'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Paper and Materials:: {option}"

class PartOfFinalReportToBeAmendedExactLocation(FormUserAttr):
    values = {'89368010_processed': 'The attached is an addition to the I- 1725.001 Final Report'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Part of Final Report to be Amended (Exact location): {option}"

class PartOfSalaryReceivedForLobbying(FormUserAttr):
    values = {'0001477983_processed': '$'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Part of salary received for lobbying:: {option}"

class Pay(FormUserAttr):
    values = {'0060036622_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Pay - $: {option}"

class PayMethod(FormUserAttr):
    values = {'71341634_processed': 'Check'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Pay Method: {option}"

class PayTerms(FormUserAttr):
    values = {'71341634_processed': '00000'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Pay Terms: {option}"

class PayTo(FormUserAttr):
    values = {'71341634_processed': 'COREMARK NTERNATIONAL'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Pay To:: {option}"

class Payment(FormUserAttr):
    values = {'0060036622_processed': '1976 $ 40, 921. 30 by A. B., Inc. 1975 84, 309. 94 A. B., Inc. 1974 92, 131. 29 A. B., Inc. 1973 91, 630. 53 A. B., Inc.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Payment -: {option}"

class Per(FormUserAttr):
    values = {'0012947358_processed': 'V. Colvellm Asst. Secy. 277 Park Avenue'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Per: {option}"

class Permit(FormUserAttr):
    values = {'0060024314_processed': '0001'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Permit#:: {option}"

class PhoneNumber(FormUserAttr):
    values = {'71108371_processed': '7970'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Phone Number:: {option}"

class PhysicalCharacteristics(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics: {option}"

class PhysicalCharacteristicsCigaretteCircumference(FormUserAttr):
    values = {'0000989556_processed': '24.75 mm', '0001456787_processed': "['24.8 mm', '24.8 mm']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics_Cigarette Circumference: {option}"

class PhysicalCharacteristicsFilterPlugLength(FormUserAttr):
    values = {'0000989556_processed': '20 mm', '0001456787_processed': "['27 mm', '27 mm']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics_Filter Plug Length: {option}"

class PhysicalCharacteristicsFilterPlugPressureDropEncap(FormUserAttr):
    values = {'0001456787_processed': "['58.5 mm', '58.5 mm']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics_Filter Plug Pressure Drop (encap.): {option}"

class PhysicalCharacteristicsFilterPlugPressureDropUnencap(FormUserAttr):
    values = {'0000989556_processed': '56 mm', '0001456787_processed': "['mm', '62 mm']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics_Filter Plug Pressure Drop (unencap.): {option}"

class PhysicalCharacteristicsFilterVentilationRate(FormUserAttr):
    values = {'0000989556_processed': 'Nil %', '0001456787_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics_Filter ventilation Rate: {option}"

class PhysicalCharacteristicsMoistureContentPacking(FormUserAttr):
    values = {'0001456787_processed': "['13 %', '13%']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics_Moisture content (Packing): {option}"

class PhysicalCharacteristicsMoistureContentExCatcher(FormUserAttr):
    values = {'0000989556_processed': '13.5 %'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics_Moisture content (ex-catcher): {option}"

class PhysicalCharacteristicsOverallCigaretteLength(FormUserAttr):
    values = {'0000989556_processed': '84 mm', '0001456787_processed': "['99 mm', '99 mm']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics_Overall Cigarette Length: {option}"

class PhysicalCharacteristicsPrintPositionFromFilterEnd(FormUserAttr):
    values = {'0000989556_processed': '27 mm', '0001456787_processed': "['35 mm', '35 mm']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics_Print Position (from filter end): {option}"

class PhysicalCharacteristicsTippingLength(FormUserAttr):
    values = {'0000989556_processed': '25 mm', '0001456787_processed': "['32 mm', '32 mm']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics_Tipping Length: {option}"

class PhysicalCharacteristicsTobaccoRodLength(FormUserAttr):
    values = {'0000989556_processed': '64 mm', '0001456787_processed': "['72 mm', '72 mm']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics_Tobacco Rod Length: {option}"

class PhysicalCharacteristicsTotalPressureDropEncap(FormUserAttr):
    values = {'0000989556_processed': '110 mm', '0001456787_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics_Total Pressure Drop (encap.): {option}"

class PhysicalCharacteristicsTotalPressureDropUnencap(FormUserAttr):
    values = {'0000989556_processed': '90 mm', '0001456787_processed': "['mm', 'mm']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Physical Characteristics_Total Pressure Drop (unencap.): {option}"

class PlaceOfManufacture(FormUserAttr):
    values = {'0000989556_processed': 'NICOSIA'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Place of Manufacture:: {option}"

class PlaintiffSAttorneyS(FormUserAttr):
    values = {'0012947358_processed': 'Max A. Goldfarb 414 Biscayne Building Miami, Florida'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Plaintiff's Attorney(s):: {option}"

class PlantManagerPostingSupt(FormUserAttr):
    values = {'0060207528_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Plant Manager/ Posting Supt: {option}"

class Plast(FormUserAttr):
    values = {'81574683_processed': '7% Kent'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Plast.: {option}"

class PleaseDeliverAsSoonPossibleTo(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Please Deliver as soon Possible To:: {option}"

class PleaseDeliverAsSoonPossibleToCompany(FormUserAttr):
    values = {'0001129658_processed': "['Philip Morris', 'Philip Morris']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Please Deliver as soon Possible To:_COMPANY: {option}"

class PleaseDeliverAsSoonPossibleToFax(FormUserAttr):
    values = {'0001129658_processed': "['917 -663 -5796', '917- 663 5979']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Please Deliver as soon Possible To:_FAX: {option}"

class PleaseDeliverAsSoonPossibleToNo(FormUserAttr):
    values = {'0001129658_processed': "['917 -663 -5796', '917- 663 5979']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Please Deliver as soon Possible To:_No.: {option}"

class PleaseDeliverAsSoonPossibleToPhoneNo(FormUserAttr):
    values = {'0001129658_processed': '917- 663 3056'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Please Deliver as soon Possible To:_PHONE No.: {option}"

class PleaseDeliverAsSoonPossibleToRecipient(FormUserAttr):
    values = {'0001129658_processed': "['John Mulderig', 'Gregory Little']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Please Deliver as soon Possible To:_RECIPIENT: {option}"

class PleaseShipTo(FormUserAttr):
    values = {'88057519_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Please Ship To: {option}"

class PleaseCompleteTheFollowingIfCheckedNoForCorporationAbove(FormUserAttr):
    values = {'71341634_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Please complete the following If checked \"NO\" for corporation above:: {option}"

class PleaseIndicateTheCapacityInWhichYouAreExecutingThisDocument(FormUserAttr):
    values = {'0001477983_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Please indicate the capacity in which you are executing this document:: {option}"

class PleaseMakeTheNecessaryFieldTripArrangementsFor(FormUserAttr):
    values = {'80728670_processed': 'Ted van de kamp'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Please make the necessary Field Trip arrangements for: {option}"

class PleasePlaceTheFollowingOrderForKoolAndOrGpcGolfBagsForMySection(FormUserAttr):
    values = {'0030041455_processed': 'KOOL Golf Bags 5 GPC Golf Bags 0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Please place the following order for KOOL and/ or GPC Golf Bags for my Section:: {option}"

class PlugWrap(FormUserAttr):
    values = {'81574683_processed': '626'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Plug Wrap: {option}"

class PlugWrapPor(FormUserAttr):
    values = {'81574683_processed': '1509C'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Plug Wrap Por.: {option}"

class Position(FormUserAttr):
    values = {'0060262650_processed': 'Cytogeneticist'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Position: {option}"

class Positioning(FormUserAttr):
    values = {'0000989556_processed': 'mm from mouth end'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Positioning: {option}"

class PreparationAndComposition(FormUserAttr):
    values = {'88547278_88547279_processed': 'Final Film Supplied Combined Blue'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Preparation and Composition:: {option}"

class PreparedBy(FormUserAttr):
    values = {'80310840a_processed': 'S. R. Benson '}

    @staticmethod
    def nl_desc(option):
        return f"The user's Prepared by: {option}"

class President(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's President: {option}"

class PressureDrop(FormUserAttr):
    values = {'00093726_processed': 'To be determined', '81574683_processed': '370mm'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Pressure Drop: {option}"

class PressureOnAirJet(FormUserAttr):
    values = {'01122115_processed': '16 psig'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Pressure on Air Jet: {option}"

class PrevOrRecommendedSupplier(FormUserAttr):
    values = {'00922237_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Prev. or Recommended Supplier: {option}"

class PreviousCommitmentsThisProject(FormUserAttr):
    values = {'0012529284_processed': '$ 212, 475 + 10%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Previous $ Commitments This Project: {option}"

class PricesAndSchedule(FormUserAttr):
    values = {'88547278_88547279_processed': '$16, 158'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Prices and Schedule:: {option}"

class ProcessAndColors(FormUserAttr):
    values = {'88547278_88547279_processed': '6/1 1/1'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Process and Colors:: {option}"

class ProducionProcess(FormUserAttr):
    values = {'0060024314_processed': 'label adhesive'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Producion Process: {option}"

class ProductManager(FormUserAttr):
    values = {'89867723_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Product Manager: {option}"

class ProductionSupervisedBy(FormUserAttr):
    values = {'01122115_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Production Supervised by:: {option}"

class Products(FormUserAttr):
    values = {'0060255888_processed': 'Tareyton Cigarettes'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Products:: {option}"

class ProgramBudgetCode(FormUserAttr):
    values = {'0060029036_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Program Budget Code: {option}"

class ProgramGroup(FormUserAttr):
    values = {'00920294_processed': '102- Eclipse'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Program Group: {option}"

class ProiectedExternalAuthorizationDate(FormUserAttr):
    values = {'71202511_processed': '2 /26 /98'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Proiected External Authorization Date: {option}"

class ProjectNameDescription(FormUserAttr):
    values = {'71563825_processed': 'K001 vs. Marlboro Menthol Lights'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Project Name/ Description: {option}"

class ProjectNo(FormUserAttr):
    values = {'0060173256_processed': 'S0002 Supp 2'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Project No: {option}"

class ProjectType(FormUserAttr):
    values = {'0001463282_processed': 'Product Test'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Project Type: {option}"

class ProjectTypeProductTestAUEtc(FormUserAttr):
    values = {'71202511_processed': 'Qualatative'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Project Type (Product Test, A & U, etc.): {option}"

class ProjectedFieldStart(FormUserAttr):
    values = {'12603270_processed': 'CANCELLED'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Projected: Field Start: {option}"

class ProjectedFinalReportDue(FormUserAttr):
    values = {'0012529295_processed': '11/ 16/ 87', '0012602424_processed': 'Jan. 1985'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Projected:_Final Report Due: {option}"

class ProjectedInitiationDate(FormUserAttr):
    values = {'0012529295_processed': '8/ 3/ 87'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Projected:_Initiation Date: {option}"

class PromoDates(FormUserAttr):
    values = {'71341634_processed': 'March 15- 19, 1999'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Promo Dates: {option}"

class PromotionCode(FormUserAttr):
    values = {'71341634_processed': '725 725'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Promotion Code: {option}"

class PromotionName(FormUserAttr):
    values = {'71341634_processed': 'GPC BUYDOWN PROGRAMS SEE ATTACHED Section 18 Narl Chain Walgreens'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Promotion Name: {option}"

class PromotionNumber(FormUserAttr):
    values = {'71341634_processed': '288 296'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Promotion Number: {option}"

class PromotionQuantity(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Promotion Quantity:: {option}"

class PromotionQuantityDisplays8(FormUserAttr):
    values = {'92091873_processed': '40', '93213298_processed': '0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Promotion Quantity:_Displays (8): {option}"

class PromotionQuantityFloor40(FormUserAttr):
    values = {'92091873_processed': '20', '93213298_processed': '0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Promotion Quantity:_Floor (40): {option}"

class PromotionQuantityMugs(FormUserAttr):
    values = {'92091873_processed': '720', '93213298_processed': '0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Promotion Quantity:_Mugs: {option}"

class PromotionQuantityPosters(FormUserAttr):
    values = {'92091873_processed': '100', '93213298_processed': '0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Promotion Quantity:_Posters: {option}"

class ProposalNo(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Proposal No.: {option}"

class PumpPressCardRoller(FormUserAttr):
    values = {'01122115_processed': '120 psig'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Pump Press. Card Roller: {option}"

class Purpose(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Purpose: {option}"

class PurposeOfSample(FormUserAttr):
    values = {'81574683_processed': 'Mkt. Research Newport'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Purpose of Sample: {option}"

class PurposeOfTrip(FormUserAttr):
    values = {'80728670_processed': "To evaluate Satin's overall performance and results of Special Cities."}

    @staticmethod
    def nl_desc(option):
        return f"The user's Purpose of trip: {option}"

class PurposeCompanyImprovementsAdministrativeRequirements(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Purpose_Company Improvements & Administrative Requirements: {option}"

class PurposeComplianceWithOutsideRequirements(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Purpose_Compliance with Outside Requirements: {option}"

class PurposeCostReduction(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Purpose_Cost Reduction: {option}"

class PurposeExpansionOfExistingBusiness(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Purpose_Expansion of Existing Business: {option}"

class PurposeMaintenanceOfExistingBusiness(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Purpose_Maintenance of Existing Business: {option}"

class PurposeNewProducts(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Purpose_New Products: {option}"

class PurposeQualityImprovement(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Purpose_Quality Improvement: {option}"

class QipLog1(FormUserAttr):
    values = {'0001123541_processed': '93- 0301'}

    @staticmethod
    def nl_desc(option):
        return f"The user's QIP Log #1: {option}"

class Qned(FormUserAttr):
    values = {'716552_processed': 'S. T. BEASLEY (MRS )/ jlf'}

    @staticmethod
    def nl_desc(option):
        return f"The user's QNED:: {option}"

class QualityAssuranceAssoc(FormUserAttr):
    values = {'89368010_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's QUALITY ASSURANCE ASSOC.: {option}"

class Quantities(FormUserAttr):
    values = {'80718412_8413_processed': '270, 000'}

    @staticmethod
    def nl_desc(option):
        return f"The user's QUANTITIES:: {option}"

class Quantity(FormUserAttr):
    values = {'0060077689_processed': '', '00920222_processed': '', '00922237_processed': '', '71341634_processed': '50, 759 6. 382'}

    @staticmethod
    def nl_desc(option):
        return f"The user's QUANTITY: {option}"

class QuantityRequired(FormUserAttr):
    values = {'82254638_processed': '400 400 400 400', '91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's QUANTITY REQUIRED: {option}"

class Qty(FormUserAttr):
    values = {'88547278_88547279_processed': '89,725'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Qty:: {option}"

class QualitativeResearchProductTestAUEtc(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Qualitative Research (Product Test, A & U etc.): {option}"

class QualitativeResearchProductTestAUEtcRecommendedSupplier(FormUserAttr):
    values = {'11508234_processed': 'Analytic Insight, Inc.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Qualitative Research (Product Test, A & U etc.)_Recommended Supplier:: {option}"

class QualityControl(FormUserAttr):
    values = {'0060025670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Quality Control: {option}"

class QualityOfBloom(FormUserAttr):
    values = {'01122115_processed': 'Good'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Quality of Bloom: {option}"

class QualityOfHospitalityTent(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Quality of Hospitality Tent:: {option}"

class QualityOfHospitalityTentCleanliness(FormUserAttr):
    values = {'92091873_processed': 'X', '93213298_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Quality of Hospitality Tent:_Cleanliness: {option}"

class QualityOfHospitalityTentFood(FormUserAttr):
    values = {'92091873_processed': 'X', '93213298_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Quality of Hospitality Tent:_Food: {option}"

class QualityOfHospitalityTentService(FormUserAttr):
    values = {'92091873_processed': 'X', '93213298_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Quality of Hospitality Tent:_Service: {option}"

class QuanOfTraysProduced(FormUserAttr):
    values = {'01122115_processed': '3'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Quan of Trays Produced: {option}"

class QuantitiesAndDescription(FormUserAttr):
    values = {'88547278_88547279_processed': 'H/D 8 Pk. Wide Header 4 C/P + 2 Hits Day- Glo + Spot Varnish'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Quantities and Description:: {option}"

class QuantityReceived(FormUserAttr):
    values = {'0060214859_processed': '2 ROLLS'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Quantity Received: {option}"

class QuantityCartonsOf200Each(FormUserAttr):
    values = {'0001485288_processed': '20'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Quantity, Cartons of 200 each: {option}"

class QuotationTo(FormUserAttr):
    values = {'88547278_88547279_processed': 'Lorillard One Park Avenue New York, NY 10016 Attn: Neil Toumey'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Quotation To:: {option}"

class RDComments(FormUserAttr):
    values = {'0000990274_processed': 'Target the P A 29Mar 84'}

    @staticmethod
    def nl_desc(option):
        return f"The user's R & D COMMENTS:: {option}"

class RDGroup(FormUserAttr):
    values = {'0000971160_processed': 'Licensee'}

    @staticmethod
    def nl_desc(option):
        return f"The user's R&D Group:: {option}"

class Radioactive(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's RADIOACTIVE: {option}"

class RdEProcess(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's RD&E - Process: {option}"

class RdEProduct(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's RD&E - Product: {option}"

class Re(FormUserAttr):
    values = {'01122115_processed': '-339'}

    @staticmethod
    def nl_desc(option):
        return f"The user's RE: {option}"

class Reactivity(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's REACTIVITY: {option}"

class Reactivity1WaterOrBrine(FormUserAttr):
    values = {'00837285_processed': "['UNCHANGED', 'DECOMPOSITION', 'UNCHANGED', 'UNCHANGED', 'DECOMPOSITION']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's REACTIVITY_1) WATER or BRINE:: {option}"

class Reactivity25Hcl(FormUserAttr):
    values = {'00837285_processed': "['UNCHANGED', 'DECOMPOSITION', 'UNCHANGED', 'DECOMPOSITION']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's REACTIVITY_2) 5% HCL: {option}"

class Reactivity35Naoh(FormUserAttr):
    values = {'00837285_processed': "['UNCHANGED', 'DECOMPOSITION', 'UNCHANGED', 'DECOMPOSITION']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's REACTIVITY_3) 5% NaOH:: {option}"

class Reactivity4Alcohols(FormUserAttr):
    values = {'00837285_processed': "['UNCHANCED', 'DECOMPOSITION', 'UNCHANGED', 'DECOMPOSITION']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's REACTIVITY_4) ALCOHOLS:: {option}"

class Reactivity5Oxygen(FormUserAttr):
    values = {'00837285_processed': "['UNCHANGED', 'DECOMPOSITION', 'UNCHANGED', 'DECOMPOSITION']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's REACTIVITY_5) OXYGEN:: {option}"

class Reactivity6Light(FormUserAttr):
    values = {'00837285_processed': "['UNCHANGED', 'DECOMPOSITION', 'UNCHANGED', 'DECOMPOSITION']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's REACTIVITY_6) LIGHT:: {option}"

class ReasonCode(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's REASON CODE: {option}"

class ReasonCode1ProductivityImprovement(FormUserAttr):
    values = {'71108371_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REASON CODE_1. Productivity Improvement: {option}"

class ReasonCode2ReturnOnInvestment(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REASON CODE_2. Return On Investment: {option}"

class ReasonCode3CustomerImpact(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REASON CODE_3. Customer Impact: {option}"

class ReasonCode4GovernmentRequirement(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REASON CODE_4. Government Requirement: {option}"

class ReasonCode5BusinessChange(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REASON CODE_5. Business Change: {option}"

class ReasonCode6SystemError(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REASON CODE_6. System Error: {option}"

class ReasonCode7ProceduralError(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REASON CODE_7. Procedural Error: {option}"

class Recasing(FormUserAttr):
    values = {'00093726_processed': 'OGS', '00283813_processed': '', '81574683_processed': '7774'}

    @staticmethod
    def nl_desc(option):
        return f"The user's RECASING: {option}"

class ReceiptDateS(FormUserAttr):
    values = {'00860012_00860014_processed': '11 18 83', '00866042_processed': '9/28/83'}

    @staticmethod
    def nl_desc(option):
        return f"The user's RECEIPT DATE (s): {option}"

class Received(FormUserAttr):
    values = {'0000990274_processed': 'APR 2 1984 P. H. H.', '0011859695_processed': 'SEP 30 ', '0011899960_processed': 'JUL 10 1984 JOHN ALAR', '0012199830_processed': 'DEC 1 1 1989'}

    @staticmethod
    def nl_desc(option):
        return f"The user's RECEIVED: {option}"

class ReceivedAndForwardedOn(FormUserAttr):
    values = {'0012947358_processed': '1 29/29/ 69 (Date)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's RECEIVED AND FORWARDED ON: {option}"

class Recommendation(FormUserAttr):
    values = {'00070353_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's RECOMMENDATION:: {option}"

class ReducedToMaterial(FormUserAttr):
    values = {'0001485288_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REDUCED TO MATERIAL ☐: {option}"

class Reference(FormUserAttr):
    values = {'0001239897_processed': '(#627/ 647 (#647/ 627) Current VICEROY 84 25% PG with SORBITOL'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REFERENCE: {option}"

class ReferenceForCalculation(FormUserAttr):
    values = {'00040534_processed': 'Litchfield, J. T. and Wilcoxin F. , J. of Pharmacol and Exper. Ther. , 90: 99 , 1948.', '87672097_processed': 'Weil, Carrol S., Biometrics, Vol. 8, No. 3., Sept. 1952, p. 249.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REFERENCE FOR CALCULATION: {option}"

class Region(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's REGION:: {option}"

class RegionFull(FormUserAttr):
    values = {'81619486_9488_processed': '', '81619511_9513_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REGION:_FULL: {option}"

class RegionPartial(FormUserAttr):
    values = {'81619486_9488_processed': '', '81619511_9513_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REGION:_PARTIAL: {option}"

class RegistryNumberIfApplicable(FormUserAttr):
    values = {'00851772_1780_processed': 'N/A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REGISTRY NUMBER (IF applicable): {option}"

class RegulatoryAffairs(FormUserAttr):
    values = {'89368010_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REGULATORY AFFAIRS: {option}"

class RegulatoryStatus(FormUserAttr):
    values = {'81310636_processed': 'N/ A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REGULATORY STATUS: {option}"

class Rejected(FormUserAttr):
    values = {'0060214859_processed': 'XX'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REJECTED: {option}"

class ReleasedToAcctg(FormUserAttr):
    values = {'0011505151_processed': '2- 25- 88', '12052385_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's RELEASED TO ACCTG: {option}"

class Remarks(FormUserAttr):
    values = {'0060068489_processed': 'For posting in Cincinnati, Covington and Tampa/St. Petersburg. Posters are captioned for identification, "LUCKY STRIKES AGAIN (printed in red) with the word "New" printed in a snipe effect in the upper left corner. These posters have a white background and will be further identified as such in order to differentiate from a second design which will have a solid red background with white lettering. Posters are printed six colors (four color process and two impressions of red) on white 70# outdoor poster paper.', '01197604_processed': 'Moisture content of tar .48% as determined by near infrared spectroscopy'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REMARKS:: {option}"

class RemarksTheseCostsWillIncludeButAreNotExclusiveToTheTheFollowingMaterials(FormUserAttr):
    values = {'0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REMARKS_These costs will include but are not exclusive to the the following materials:: {option}"

class RemarksToCoverTheCostOfCollateralMerchandisingMaterialsToBeUsedIn1991InConnectionWithTheMerchandisingAndPromotionOfBullDurham(FormUserAttr):
    values = {'0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REMARKS_To cover the cost of collateral merchandising materials to be used in 1991 in connection with the merchandising and promotion of BULL DURHAM.: {option}"

class ReportableExpenditures(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES: {option}"

class ReportableExpendituresInThousands(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands): {option}"

class ReportableExpendituresInThousandsCatExpenses(FormUserAttr):
    values = {'0060270727_processed': '0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_CAT - - EXPENSES:: {option}"

class ReportableExpendituresInThousandsCatCExpenses(FormUserAttr):
    values = {'0060270727_processed': '38'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_CAT - C - EXPENSES:: {option}"

class ReportableExpendituresInThousandsCatDExpenses(FormUserAttr):
    values = {'0060270727_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_CAT - D - EXPENSES:: {option}"

class ReportableExpendituresInThousandsCatFExpenses(FormUserAttr):
    values = {'0060270727_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_CAT - F - EXPENSES:: {option}"

class ReportableExpendituresInThousandsCatGExpenses(FormUserAttr):
    values = {'0060270727_processed': '1'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_CAT - G EXPENSES:: {option}"

class ReportableExpendituresInThousandsCatJExpenses(FormUserAttr):
    values = {'0060270727_processed': '20'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_CAT - J - EXPENSES:: {option}"

class ReportableExpendituresInThousandsCatKExpenses(FormUserAttr):
    values = {'0060270727_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_CAT - K - EXPENSES:: {option}"

class ReportableExpendituresInThousandsCatLExpenses(FormUserAttr):
    values = {'0060270727_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_CAT - L - EXPENSES:: {option}"

class ReportableExpendituresInThousandsCatMExpenses(FormUserAttr):
    values = {'0060270727_processed': '1'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_CAT - M EXPENSES:: {option}"

class ReportableExpendituresInThousandsCatEExpenses(FormUserAttr):
    values = {'0060270727_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_CAT E - EXPENSES:: {option}"

class ReportableExpendituresInThousandsCatHExpenses(FormUserAttr):
    values = {'0060270727_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_CAT H - EXPENSES:: {option}"

class ReportableExpendituresInThousandsCatIExpenses(FormUserAttr):
    values = {'0060270727_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_CAT I - EXPENSES:: {option}"

class ReportableExpendituresInThousandsCatAExpenses(FormUserAttr):
    values = {'0060270727_processed': '34'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_CAT- A - EXPENSES:: {option}"

class ReportableExpendituresInThousandsTotalReportableExpendituresForVarietyi(FormUserAttr):
    values = {'0060270727_processed': '94'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES (In Thousands)_TOTAL REPORTABLE EXPENDITURES FOR VARIETYI:: {option}"

class ReportableExpenditures13CatAExpenses(FormUserAttr):
    values = {'0060308461_processed': '2,303'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(13) CAT- A- EXPENSES:: {option}"

class ReportableExpenditures14CatBExpenses(FormUserAttr):
    values = {'0060308461_processed': '3,890'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(14) CAT- B- EXPENSES:: {option}"

class ReportableExpenditures15CatCExpenses(FormUserAttr):
    values = {'0060308461_processed': '741'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(15) CAT- C- EXPENSES:: {option}"

class ReportableExpenditures16CatDExpenses(FormUserAttr):
    values = {'0060308461_processed': '71,445'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(16) CAT- D- EXPENSES:: {option}"

class ReportableExpenditures17CatEExpenses(FormUserAttr):
    values = {'0060308461_processed': '-'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(17) CAT- E- EXPENSES: {option}"

class ReportableExpenditures18CatFExpenses(FormUserAttr):
    values = {'0060308461_processed': '193'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(18) CAT- F- EXPENSES:: {option}"

class ReportableExpenditures19CatGExpenses(FormUserAttr):
    values = {'0060308461_processed': '12,787'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(19) CAT- G- EXPENSES:: {option}"

class ReportableExpenditures20CatHExpenses(FormUserAttr):
    values = {'0060308461_processed': '95,614'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(20) CAT- H- EXPENSES:: {option}"

class ReportableExpenditures21CatIExpenses(FormUserAttr):
    values = {'0060308461_processed': '291,095'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(21) CAT- I- EXPENSES:: {option}"

class ReportableExpenditures22CatJExpenses(FormUserAttr):
    values = {'0060308461_processed': '155,718'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(22) CAT- J- EXPENSES:: {option}"

class ReportableExpenditures23CatKExpenses(FormUserAttr):
    values = {'0060308461_processed': '476,722'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(23) CAT- K- EXPENSES:: {option}"

class ReportableExpenditures24CatLExpenses(FormUserAttr):
    values = {'0060308461_processed': '85,208'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(24) CAT- L- EXPENSES:: {option}"

class ReportableExpenditures25CatMExpenses(FormUserAttr):
    values = {'0060308461_processed': '26,055'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(25) CAT- M- EXPENSES:: {option}"

class ReportableExpenditures26TotalReportableExpendituresForVariety(FormUserAttr):
    values = {'0060308461_processed': '1,221,771'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTABLE EXPENDITURES_(26) TOTAL REPORTABLE EXPENDITURES FOR VARIETY:: {option}"

class Reported(FormUserAttr):
    values = {'00040534_processed': '5/3/79 10/6/80 , Update', '01073843_processed': '4/14/81', '87672097_processed': '3 /30 /81'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REPORTED: {option}"

class RequestAuthorizedBy(FormUserAttr):
    values = {'71108371_processed': 'MUST BE AUTHORIZED BY THE DEPARTMENT DIRECTOR OR THE DESIGNATED SYSTEM OWNER BEFORE SUBMISSION TO THE MIS CLIENT SYSTEMS MANAGER.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REQUEST AUTHORIZED BY: {option}"

class RequestNo(FormUserAttr):
    values = {'0000990274_processed': '25- 84'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REQUEST NO.:: {option}"

class RequestType(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's REQUEST TYPE: {option}"

class RequestType1Enhancement(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REQUEST TYPE_1. Enhancement: {option}"

class RequestType2Maintenance(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REQUEST TYPE_2. Maintenance: {option}"

class RequestType3SpecialProcessing(FormUserAttr):
    values = {'71108371_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REQUEST TYPE_3. Special Processing: {option}"

class RequestType4AdHoc(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REQUEST TYPE_4. Ad Hoc: {option}"

class RequestType5Emergency(FormUserAttr):
    values = {'71108371_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REQUEST TYPE_5. Emergency: {option}"

class RequestedImplementationDate(FormUserAttr):
    values = {'0012178355_processed': '9 /17 /84'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REQUESTED IMPLEMENTATION DATE: {option}"

class RequirementsMp(FormUserAttr):
    values = {'01197604_processed': '150 gm'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REQUIREMENTS /MP.:: {option}"

class RequisitionNo(FormUserAttr):
    values = {'00920222_processed': '', '00922237_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REQUISITION NO.: {option}"

class Requisitioner(FormUserAttr):
    values = {'0060077689_processed': 'Mr. G. Schumacher'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REQUISITIONER: {option}"

class RespondHere(FormUserAttr):
    values = {'0001123541_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's RESPOND HERE: {option}"

class ResultsNoDeadNoTested(FormUserAttr):
    values = {'87672097_processed': '0 /6 0 /6 0 /6 0 /6 0 /6'}

    @staticmethod
    def nl_desc(option):
        return f"The user's RESULTS (NO DEAD/NO TESTED: {option}"

class ResultsNoTested(FormUserAttr):
    values = {'00040534_processed': '1/ 6 0/ 6 0/ 6 3/ 6 6/ 6'}

    @staticmethod
    def nl_desc(option):
        return f"The user's RESULTS (NO TESTED): {option}"

class RetailCallFrequency(FormUserAttr):
    values = {'92081358_1359_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's RETAIL CALL FREQUENCY:: {option}"

class ReversionRateTestReversantsControlRevertantsPerPlate(FormUserAttr):
    values = {'00836244_processed': '.92 1. 00 .79 .83 .97 .88 .97 .92 .90 .96 .92 .85'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REVERSION RATE (TEST REVERSANTS/CONTROL REVERTANTS PER PLATE: {option}"

class ReversionRateTestRevertantsControlRevertantsPerPlate(FormUserAttr):
    values = {'01073843_processed': '.76 1.10 1.12 1.07 .52 .87 .82 .88 .78 .65 .71 .86'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REVERSION RATE TEST REVERTANTS-CONTROL REVERTANTS PER PLATE): {option}"

class ReviewCompleted(FormUserAttr):
    values = {'00070353_processed': '3/ 29/ 68'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REVIEW COMPLETED: {option}"

class ReviewRouting(FormUserAttr):
    values = {'0060029036_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REVIEW ROUTING: {option}"

class Reviewed(FormUserAttr):
    values = {'00851772_1780_processed': '1974- Jan. 1982 to Dec. 1981 1929-1966 1957- Dec. 1981'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REVIEWED: {option}"

class RevisedContractTotals(FormUserAttr):
    values = {'0060136394_processed': '24 @ $ 150.00 TIME 24 @ $ 125.00 NET TALENT'}

    @staticmethod
    def nl_desc(option):
        return f"The user's REVISED CONTRACT TOTALS.: {option}"

class RevisedTargetDate(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REVISED TARGET DATE: {option}"

class Revision(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REVISION #: {option}"

class Revisions(FormUserAttr):
    values = {'71190280_processed': '', '71366499_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REVISIONS: {option}"

class RevisionsApproved(FormUserAttr):
    values = {'71190280_processed': '', '71366499_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REVISIONS APPROVED: {option}"

class RevisionsToShellOtherThanTermCompensationOrJob(FormUserAttr):
    values = {'0060029036_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's REVISIONS TO SHELL (Other than Term Compensation or Job: {option}"

class RincipalOrganizerWhoWillReceiveCorrespondence(FormUserAttr):
    values = {'0060262650_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's RINCIPAL ORGANIZER (who will receive correspondence):: {option}"

class RoomTemperature(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ROOM TEMPERATURE: {option}"

class RouteOfCompoundAdministration(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's ROUTE OF COMPOUND ADMINISTRATION: {option}"

class RaceDayInfo(FormUserAttr):
    values = {'92091873_processed': 'Event Attendance 100, 000 Hospitality Tent Attendance 35- 40'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Race Day Info:: {option}"

class RaceDayInfoEventAttendance(FormUserAttr):
    values = {'93213298_processed': '10'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Race Day Info:_Event Attendance: {option}"

class RaceDayInfoHospitalityTentAttendance(FormUserAttr):
    values = {'93213298_processed': '10'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Race Day Info:_Hospitality Tent Attendance: {option}"

class ReasonSForRecommendation(FormUserAttr):
    values = {'0001463282_processed': 'Lowest project costs', '0012529295_processed': 'Low bidder.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Reason (s) for Recommendation: {option}"

class ReasonForTheAmendment(FormUserAttr):
    values = {'89368010_processed': "Survival after repeated doses over a 14 day period may not be accurately predicted from survival after a single day's exposure."}

    @staticmethod
    def nl_desc(option):
        return f"The user's Reason for the Amendment: {option}"

class Reason(FormUserAttr):
    values = {'80310840a_processed': 'Lower Incidence'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Reason:: {option}"

class Reasons(FormUserAttr):
    values = {'0011838621_processed': 'Original MRA did not include cost for the first month of the study (see L. Lee memo of September 11, 1989)', '0012529284_processed': 'Adjustment due to timing of projects falling into 1988.', '0012602424_processed': 'REVISED COST DUE TO A QUESTION ADDED TO THE SECOND WAVE AND CHANGES MADE IN WORDING OF OTHER QUESTIONS. THIS COVERS THE COST OF ADDITIONAL TELEPHONE INTERVIEW LENGTH, CODING OF THE OPEN- END, PROGRAMING CHANGES, TABULATION AND ANALYSIS.', '12603270_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Reasons:: {option}"

class RecD(FormUserAttr):
    values = {'92091873_processed': '6/ 12/ 95'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Rec'd: {option}"

class RecearchEngineer(FormUserAttr):
    values = {'01122115_processed': 'Benner'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Recearch Engineer: {option}"

class ReceivedByRegulatoryAffatrs(FormUserAttr):
    values = {'89368010_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Received by REGULATORY AFFATRS: {option}"

class RecentActionsRegardingAboveSolicitor(FormUserAttr):
    values = {'0060036622_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Recent actions regarding above solicitor : {option}"

class RecommemdedSupplier(FormUserAttr):
    values = {'0012529295_processed': 'Kapuler Marketing Research'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Recommemded Supplier:: {option}"

class RecommendedBrandSAndPromotionalActivity(FormUserAttr):
    values = {'0011976929_processed': 'BARCLAY sampling 2 - 12M cases mixed. To be placed on tables by B & W Reps.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Recommended Brand(s) and Promotional Activity:: {option}"

class RecommendedSupplier(FormUserAttr):
    values = {'0001463282_processed': 'Kapuler'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Recommended Supplier: {option}"

class Ref(FormUserAttr):
    values = {'71341634_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Ref: {option}"

class RefPaper(FormUserAttr):
    values = {'01122115_processed': '#450'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Ref. Paper: {option}"

class ReferentBrand(FormUserAttr):
    values = {'71601299_processed': 'Dunhill Lights Kent Super Lights Mild 7 This'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Referent Brand: {option}"

class ReferentBrandS(FormUserAttr):
    values = {'71563825_processed': 'Current Kool Filter King Colombia 1 1 mg tar @ 0. 51% menthol white tipping. Kool Milds KS Japan 9mg tar @ 0. 56% menthol white tipping Kool KS. 9 mg tar, @ 0. 51% menthol white tipping Current Marlboro Lights Menthol King US 9mg tar @ 0. 66% menthol, white tipping.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Referent Brand(s):: {option}"

class RegistrationNo(FormUserAttr):
    values = {'00070353_processed': '533'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Registration No: {option}"

class RegistryOfTheToxicEffectsOfChemicals(FormUserAttr):
    values = {'00851772_1780_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Registry of the Toxic Effects of Chemicals: {option}"

class ReimbursementsForExpensesPleaseItemize(FormUserAttr):
    values = {'0001477983_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Reimbursements for expenses (please itemize):: {option}"

class RelationshipToFinalist(FormUserAttr):
    values = {'0060091229_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Relationship to Finalist:: {option}"

class Replaces(FormUserAttr):
    values = {'0000989556_processed': 'New'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Replaces:: {option}"

class Report(FormUserAttr):
    values = {'0060214859_processed': '517'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Report: {option}"

class ReportedBy(FormUserAttr):
    values = {'81186212_processed': '', '91355841_processed': 'A. L. EVERETT, MANAGER, CHAIN ACCOUNTS - ATLANTA, GA', '93329540_processed': 'A. REID, DIVISION MANAGER, SAN FRANCISCO, CA', '93455715_processed': 'R. E. Klein, Regional Sales Manager, Cleveland, OH'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Reported by:: {option}"

class ReportingPeriod(FormUserAttr):
    values = {'0001477983_processed': 'Month of May'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Reporting Period:: {option}"

class ReportingSchedule(FormUserAttr):
    values = {'80310840a_processed': 'Topline w/o 12 /18 /95 Final Report 12/ 31/ 95'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Reporting Schedule:: {option}"

class Reports(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Reports: {option}"

class ReportsCopiesTo(FormUserAttr):
    values = {'00283813_processed': 'Dr. A. W. Spears'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Reports:_Copies to: {option}"

class ReportsOriginalTo(FormUserAttr):
    values = {'00283813_processed': 'Mr. C. L. Tucker, Jr.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Reports:_Original to: {option}"

class ReportsWrittenBy(FormUserAttr):
    values = {'00283813_processed': 'John H. M. Bohlken'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Reports:_Written by: {option}"

class Requested(FormUserAttr):
    values = {'0060036622_processed': 'Harvard Medical School and Dr. Gary Huber Boston, Massachusetts'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Requested: {option}"

class RequestedBy(FormUserAttr):
    values = {'0001463282_processed': 'W. T. Carpenter', '0011974919_processed': '', '0012529295_processed': 'S. H. Trebilcock', '11508234_processed': 'A. A. Strobel', '71108371_processed': 'Karl Hutchison', '71202511_processed': 'Nick Wilkerson', '71341634_processed': 'Robert '}

    @staticmethod
    def nl_desc(option):
        return f"The user's Requested By:: {option}"

class Requirements(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Requirements: {option}"

class RequirementsLaboratory(FormUserAttr):
    values = {'81574683_processed': '30 ctns.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Requirements Laboratory: {option}"

class RequirementsOthers(FormUserAttr):
    values = {'00283813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Requirements:_Others: {option}"

class RequirementsOther(FormUserAttr):
    values = {'00093726_processed': '20, 000 cigts.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Requirements_Other: {option}"

class Res(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Res: {option}"

class ResearchDesign(FormUserAttr):
    values = {'80310840a_processed': 'Group 1= Best redeeming customers (2+ paid coupons): n= 750 Group 2= Paid redeoming customers 1 paid coupon) n= 750 Group 3= Non- redeeming customers (no redemption) n= 750 The total sample size is 2,250. All smokers 21+ years of age.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Research Design: {option}"

class ResearchDesignNCellsElegibilityDesignKeyBannerBreaksMethodologyCities(FormUserAttr):
    values = {'89867723_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Research Design (N, Cells, Elegibility, Design, Key Banner Breaks, Methodology, Cities): {option}"

class ResearchFirm(FormUserAttr):
    values = {'89867723_processed': 'Ruth Manko Assoc.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Research Firm: {option}"

class ResearchLiaison(FormUserAttr):
    values = {'71601299_processed': 'Subi. Jeong'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Research Liaison: {option}"

class ResearchLimitations(FormUserAttr):
    values = {'89867723_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Research Limitations: {option}"

class ResearchReqAttached(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Research Req Attached:: {option}"

class ResearchReqAttachedNo(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Research Req Attached:_No: {option}"

class ResearchReqAttachedYes(FormUserAttr):
    values = {'11508234_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Research Req Attached:_Yes: {option}"

class ResearchRequestAttached(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Research Request Attached:: {option}"

class ResearchRequestAttachedNo(FormUserAttr):
    values = {'0001463282_processed': '', '0012529295_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Research Request Attached:_No: {option}"

class ResearchRequestAttachedYes(FormUserAttr):
    values = {'0001463282_processed': 'x', '0012529295_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Research Request Attached:_Yes: {option}"

class ReservationsMadeAt(FormUserAttr):
    values = {'80728670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Reservations made at: {option}"

class RespondentIncidence(FormUserAttr):
    values = {'80310840a_processed': '38% revised from 70%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Respondent Incidence:: {option}"

class ResponderDate(FormUserAttr):
    values = {'0001123541_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Responder/ Date: {option}"

class ResponseCodeAssigned(FormUserAttr):
    values = {'0011974919_processed': 'W25'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Response Code Assigned:: {option}"

class Responsibility(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Responsibility: {option}"

class ResponsibilityFilterProduction(FormUserAttr):
    values = {'00283813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Responsibility:_Filter Production: {option}"

class ResponsibilityMakingPacking(FormUserAttr):
    values = {'00283813_processed': 'Product Development, John H. M. Bohlker'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Responsibility:_Making & Packing: {option}"

class ResponsibilityShipping(FormUserAttr):
    values = {'00283813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Responsibility:_Shipping: {option}"

class ResponsibilityTobaccoBlend(FormUserAttr):
    values = {'00283813_processed': 'Manufacturing - A. Kraus'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Responsibility:_Tobacco Blend: {option}"

class ResponsibilitySampleRequisitionForm020206(FormUserAttr):
    values = {'00093726_processed': '"'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Responsibility_Sample Requisition [Form 02: 02: 06]: {option}"

class ResponsibilitySampleRequistion(FormUserAttr):
    values = {'81574683_processed': 'T. Skinner'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Responsibility_Sample Requistion: {option}"

class Retainer(FormUserAttr):
    values = {'0001477983_processed': '$'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Retainer: {option}"

class ReturnTo(FormUserAttr):
    values = {'0060029036_processed': 'MARY SEAGRAVES Ext 1485', '0060091229_processed': 'Harden- Kane, Inc. 666 Fifth Avenue New York, N. Y. 10103'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Return To:: {option}"

class ReturnThisFormTo(FormUserAttr):
    values = {'0060262650_processed': 'AAAS Meetings Office 1101 Vermont Ave., N W. Washington, D. C. 20005'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Return this form to:: {option}"

class RevisedBudget(FormUserAttr):
    values = {'0060173256_processed': '$ 7,569,000.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Revised Budget: {option}"

class RevisedCostsIfAny(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Revised Costs (if any): {option}"

class RevisedFrom(FormUserAttr):
    values = {'80310840a_processed': '$76 600'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Revised From:: {option}"

class RevisionDate(FormUserAttr):
    values = {'0001118259_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Revision Date:: {option}"

class Rod(FormUserAttr):
    values = {'81574683_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Rod: {option}"

class RodsPerMin(FormUserAttr):
    values = {'01122115_processed': '1067'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Rods per Min.: {option}"

class Room(FormUserAttr):
    values = {'01150773_01150774_processed': '803E'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Room:: {option}"

class STyphimurium(FormUserAttr):
    values = {'01073843_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's S TYPHIMURIUM: {option}"

class SPV(FormUserAttr):
    values = {'0060207528_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's S.P.V.: {option}"

class Sales(FormUserAttr):
    values = {'0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SALES: {option}"

class SalesObjective(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SALES OBJECTIVE: {option}"

class SampleWeight(FormUserAttr):
    values = {'01197604_processed': '300 mm. tar, 100 mm acetone'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SAMPLE WEIGHT:: {option}"

class Sample(FormUserAttr):
    values = {'0000999294_processed': '408 Menthol Lights / 105 Menthol Ultra, 111 Non- Menthol Lights / 92 Non- Menthol Ultras)', '0001239897_processed': '250 VICEROY/ 125 Marlboro/ 125 Winston', '0001476912_processed': '336'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SAMPLE:: {option}"

class SamplesItemsRequired(FormUserAttr):
    values = {'82254638_processed': "SAMPLE 10'S (400 PACKS PER CASE)"}

    @staticmethod
    def nl_desc(option):
        return f"The user's SAMPLES/ ITEMS REQUIRED:: {option}"

class SamplingDates(FormUserAttr):
    values = {'80718412_8413_processed': 'October 3 through October 5'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SAMPLING DATES: *: {option}"

class SamplingHours(FormUserAttr):
    values = {'80718412_8413_processed': '9: 30 a. m. - 5: 30 p. m.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SAMPLING HOURS: *: {option}"

class Satisfying7More(FormUserAttr):
    values = {'0000999294_processed': '3.12*** 2.78 3.28*** 2.78 2.97* 2.78 3.17*** 2.74 3.08** 2.82'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SATISFYING (7= More: {option}"

class Schedule(FormUserAttr):
    values = {'12825369_processed': '2/ 20 & 3/ 20'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SCHEDULE: {option}"

class ScheduleDateOrInventoryDepletion(FormUserAttr):
    values = {'716552_processed': '1010/ 30/ 8181'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SCHEDULE: DATE OR INVENTORY DEPLETION: {option}"

class ScheduledPostingDate(FormUserAttr):
    values = {'0060207528_processed': '7/ 16/ 89'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SCHEDULED POSTING DATE:: {option}"

class ScientificJournalOfChoice(FormUserAttr):
    values = {'0060302201_processed': 'Tobacco Science'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SCIENTIFIC JOURNAL OF CHOICE:: {option}"

class ScientificMetingOfChoice(FormUserAttr):
    values = {'0060302201_processed': 'none as yet'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SCIENTIFIC METING OF CHOICE:: {option}"

class Scope(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's SCOPE:: {option}"

class ScopeArea(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SCOPE:_AREA: {option}"

class ScopeDivision(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SCOPE:_DIVISION: {option}"

class ScopeOther(FormUserAttr):
    values = {'92094746_processed': 'x', '92094751_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SCOPE:_OTHER*: {option}"

class ScopeRegion(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SCOPE:_REGION: {option}"

class SecondaryClassOfTrade(FormUserAttr):
    values = {'92081358_1359_processed': 'Liquor'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SECONDARY CLASS OF TRADE:: {option}"

class SectionOne(FormUserAttr):
    values = {'0011845203_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SECTION ONE: {option}"

class SectionTwo(FormUserAttr):
    values = {'0011845203_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SECTION TWO: {option}"

class SectionS(FormUserAttr):
    values = {'0060029036_processed': '13 Plaza'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SECTION(S): {option}"

class SectionsRevised(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SECTIONS REVISED: {option}"

class Sensitive(FormUserAttr):
    values = {'00865872_processed': '[] Air'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SENSITIVE: {option}"

class Sex(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's SEX: {option}"

class SexFemale(FormUserAttr):
    values = {'0001209043_processed': "['0.0', '(46)', '31', '(84)']", '0001438955_processed': "['5.0', '(120)', '7', '(121)']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's SEX:_Female: {option}"

class SexMale(FormUserAttr):
    values = {'0001209043_processed': "['2.0', '(51)', '31', '(83)']", '0001438955_processed': "['1.9', '(104)', '7', '(101)']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's SEX:_Male: {option}"

class ShipTo(FormUserAttr):
    values = {'0060077689_processed': 'NO SHIPPING REQUIRED'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SHIP TO: {option}"

class ShipToDeptBranch(FormUserAttr):
    values = {'00920222_processed': '- Lorillard Research Center'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SHIP TO (DEPT- BRANCH): {option}"

class ShipToCustomerShippingNumber(FormUserAttr):
    values = {'82254638_processed': '198-820-0003'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SHIP TO:_CUSTOMER SHIPPING NUMBER: {option}"

class ShipmentToArriveNotLaterThan(FormUserAttr):
    values = {'0060077689_processed': 'NO SHIPPING REQUIRED.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SHIPMENT TO ARRIVE NOT LATER THAN: {option}"

class Shipment(FormUserAttr):
    values = {'0001485288_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SHIPMENT ☐: {option}"

class ShippedTo(FormUserAttr):
    values = {'01197604_processed': 'Dr. Dietrich Hoffman The Kettering New York, New York'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SHIPPED TO:: {option}"

class ShippedVia(FormUserAttr):
    values = {'01197604_processed': 'Railway Express'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SHIPPED VIA:: {option}"

class ShouldPromotionBeRepeated(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's SHOULD PROMOTION BE REPEATED: {option}"

class ShouldPromotionBeRepeatedNo(FormUserAttr):
    values = {'92094751_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SHOULD PROMOTION BE REPEATED?_NO: {option}"

class ShouldPromotionBeRepeatedYes(FormUserAttr):
    values = {'92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SHOULD PROMOTION BE REPEATED?_YES: {option}"

class Signature(FormUserAttr):
    values = {'0060029036_processed': '', '0060207528_processed': '', '0060308251_processed': '', '00836816_processed': '', '00837285_processed': 'Johnson', '00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SIGNATURE: {option}"

class SignatureS(FormUserAttr):
    values = {'00040534_processed': '', '00836244_processed': '', '87672097_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SIGNATURE(S): {option}"

class Signatures(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's SIGNATURES:: {option}"

class SignaturesGroupProductDirector(FormUserAttr):
    values = {'71206427_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SIGNATURES:_GROUP PRODUCT DIRECTOR: {option}"

class SignaturesMerchandisingManager(FormUserAttr):
    values = {'71206427_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SIGNATURES:_MERCHANDISING MANAGER: {option}"

class SignaturesPurchasingDepartment(FormUserAttr):
    values = {'71206427_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SIGNATURES:_PURCHASING DEPARTMENT: {option}"

class SignaturesRequestingManager(FormUserAttr):
    values = {'71206427_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SIGNATURES:_REQUESTING MANAGER: {option}"

class SignaturesReturnTo(FormUserAttr):
    values = {'71206427_processed': 'REQUESTING MANAGER'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SIGNATURES:_RETURN TO:: {option}"

class SizeOrSizes(FormUserAttr):
    values = {'93329540_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SIZE OR SIZES:: {option}"

class SizeShowing(FormUserAttr):
    values = {'0060207528_processed': 'F 75 GRP'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SIZE SHOWING:: {option}"

class Smoker(FormUserAttr):
    values = {'01197604_processed': '100 unit'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SMOKER:: {option}"

class Smoothness75Moother(FormUserAttr):
    values = {'0000999294_processed': '3.60** 3.42 3.73** 3.43 3.47 3.41 3.61* 3.38 3.58 3.46'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SMOOTHNESS (7= 5moother: {option}"

class Solubility(FormUserAttr):
    values = {'00836816_processed': '(See SOE for Biological Solutions)', '00837285_processed': 'MEASURED WATER OTHER ESTIMATED', '00865872_processed': '(See SOP FOX Biological Solutions) B164 forms a suspension in corn oil at 0.5g/ 1.5 ml Triple dosing is required'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SOLUBILITY: {option}"

class Solvent(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's SOLVENT: {option}"

class Source(FormUserAttr):
    values = {'00040534_processed': 'Camm Research', '01073843_processed': 'Lorillard - Organic Chemistry', '87672097_processed': 'Camm Research'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SOURCE: {option}"

class SourceOfBusiness(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's SOURCE OF BUSINESS:: {option}"

class SourceOfBusinessMajorCompetitiveBrands(FormUserAttr):
    values = {'0011973451_processed': 'TBD'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SOURCE OF BUSINESS:_Major Competitive Brands:: {option}"

class SourceOfBusinessTargetAudience(FormUserAttr):
    values = {'0011973451_processed': 'Value- conscious Smokers'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SOURCE OF BUSINESS:_Target Audience:: {option}"

class SourceOfInformation(FormUserAttr):
    values = {'93455715_processed': 'Best Cigarette Co., Mentor, OH'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SOURCE OF INFORMATION:: {option}"

class Space(FormUserAttr):
    values = {'0060068489_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPACE: {option}"

class SpaceColor(FormUserAttr):
    values = {'91391286_processed': 'FULL PAGE', '91391310_processed': '', '91974562_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPACE/ COLOR: {option}"

class SpaceColorMagazines(FormUserAttr):
    values = {'93351929_93351931_processed': 'P 4/ C;'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPACE/ COLOR_Magazines:: {option}"

class SpaceColorNewspapers(FormUserAttr):
    values = {'93351929_93351931_processed': '1/ 2 B/ W'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPACE/ COLOR_Newspapers:: {option}"

class SpecialEventRequestForm(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPECIAL EVENT REQUEST FORM: {option}"

class SpecialEventRequestFormDateOfEvent(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPECIAL EVENT REQUEST FORM_* DATE OF EVENT:: {option}"

class SpecialEventRequestFormNameOfEvent(FormUserAttr):
    values = {'91903177_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPECIAL EVENT REQUEST FORM_NAME OF EVENT:: {option}"

class SpecialEventRequestFormSamplesItemsRequired(FormUserAttr):
    values = {'91903177_processed': "SAMPLE 10'S (400 PACKS PER CASE)"}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPECIAL EVENT REQUEST FORM_SAMPLES/ ITEMS REQUIRED:: {option}"

class SpecialInstructionsWhileDosing(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPECIAL INSTRUCTIONS WHILE DOSING: {option}"

class SpecialSampleManufacture(FormUserAttr):
    values = {'0001485288_processed': '☑'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPECIAL SAMPLE MANUFACTURE: {option}"

class SpecificationChangeNumber8479(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPECIFICATION CHANGE NUMBER 84- 79: {option}"

class Specifics(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPECIFICS:: {option}"

class SpotCheck(FormUserAttr):
    values = {'12825369_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPOT CHECK: {option}"

class Sprouge(FormUserAttr):
    values = {'0012602424_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SPROUGE: {option}"

class SqInchesFeet(FormUserAttr):
    values = {'71190280_processed': '7.96875 sq inches', '71366499_processed': '261 sq'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SQ. INCHES/FEET: {option}"

class Sqc21(FormUserAttr):
    values = {'01122115_processed': '(Revised 5/ 9/ 61)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SQC -21: {option}"

class Ss(FormUserAttr):
    values = {'91581919_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SS:: {option}"

class StateTaxStatus(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's STATE TAX STATUS: {option}"

class Stationary(FormUserAttr):
    values = {'00922237_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's STATIONARY: {option}"

class Stations(FormUserAttr):
    values = {'0060136394_processed': 'WHAS LOUISVILLE, KENTUCKY'}

    @staticmethod
    def nl_desc(option):
        return f"The user's STATIONS: {option}"

class StorageConditions(FormUserAttr):
    values = {'00860012_00860014_processed': '☑ REFRIGERATOR 8 C'}

    @staticmethod
    def nl_desc(option):
        return f"The user's STORAGE CONDITIONS: {option}"

class StorageRecommendations(FormUserAttr):
    values = {'00836816_processed': 'Refrig erate in amber bottle at no more than 8 C.', '00837285_processed': 'NORMAL STORAGE', '00865872_processed': 'Refrigerate in amber glass bottle at no more than 8°C'}

    @staticmethod
    def nl_desc(option):
        return f"The user's STORAGE RECOMMENDATIONS: {option}"

class StoreInDark(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's STORE IN DARK: {option}"

class StoresParticipating(FormUserAttr):
    values = {'91939637_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's STORES PARTICIPATING:: {option}"

class StrainOfMice(FormUserAttr):
    values = {'00040534_processed': 'Swiss- Webster', '87672097_processed': 'Swiss- Webster'}

    @staticmethod
    def nl_desc(option):
        return f"The user's STRAIN OF MICE: {option}"

class Strength(FormUserAttr):
    values = {'0001239897_processed': '+1 -15*'}

    @staticmethod
    def nl_desc(option):
        return f"The user's STRENGTH: {option}"

class Strength7Stronger(FormUserAttr):
    values = {'0000999294_processed': '4.31*** 4.59 4.09** 4.45 4.51 4.71 4.35** 4.74 4.27 4.45'}

    @staticmethod
    def nl_desc(option):
        return f"The user's STRENGTH (7= Stronger): {option}"

class Structure(FormUserAttr):
    values = {'00838511_00838525_processed': 'OH O'}

    @staticmethod
    def nl_desc(option):
        return f"The user's STRUCTURE: {option}"

class StudyDirector(FormUserAttr):
    values = {'89368010_processed': '', '89386032_processed': 'Dr. William O. Iverson Pathologist Dr. Charley E. Gilmore'}

    @staticmethod
    def nl_desc(option):
        return f"The user's STUDY DIRECTOR: {option}"

class StudyTitleProposalNumber(FormUserAttr):
    values = {'00860012_00860014_processed': '', '00866042_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's STUDY TITLE & PROPOSAL NUMBER: {option}"

class SubjectToTheFollowingSuggestedRevisionsItemizeBelow(FormUserAttr):
    values = {'00070353_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBJECT TO THE FOLLOWING SUGGESTED REVISIONS: (itemize below):: {option}"

class Subject(FormUserAttr):
    values = {'0000999294_processed': 'KOOL Lights KS vs. Bright KS Product Monitor', '0001239897_processed': '25% Replacement of Propylene Glycol With SORBITOL', '0013255595_processed': '', '01191071_1072_processed': 'Fax Received', '81619486_9488_processed': 'MAVERICK SPECIALS EXPANSION MARKETS PROGRESS REPORT', '81619511_9513_processed': 'MAVERICK SPECIALS MENTHOL- PROGRESS REPORT', '81749056_9057_processed': 'MAVERICK SPECIALS NON- MENTHOL- EXPANSION PROGRESS REPORT', '89817999_8002_processed': 'STYLE LIGHTS PROGRESS REPORT', '91315069_91315070_processed': "HARLEY- DAVIDSON 100'S CIGARETTES PROGRESS REPORT", '92039708_9710_processed': 'MAVERICK SPECIALS- PROGRESS REPORT', '92657311_7313_processed': "HARLEY DAVIDSON 100'S CIGARETTES PROGRESS REPORT"}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBJECT:: {option}"

class SubmissionDate(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE: {option}"

class SubmissionDateDec26(FormUserAttr):
    values = {'92657311_7313_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE:_DEC 26: {option}"

class SubmissionDateJan23(FormUserAttr):
    values = {'91315069_91315070_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE:_JAN 23 ☐: {option}"

class SubmissionDateJan231995(FormUserAttr):
    values = {'92657311_7313_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE:_JAN 23, 1995: {option}"

class SubmissionDateOct3(FormUserAttr):
    values = {'92657311_7313_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE:_OCT 3: {option}"

class SubmissionDateOct31(FormUserAttr):
    values = {'92657311_7313_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE:_OCT 31: {option}"

class SubmissionDateAug10(FormUserAttr):
    values = {'81619486_9488_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE_AUG 10: {option}"

class SubmissionDateAug26(FormUserAttr):
    values = {'92039708_9710_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE_AUG 26 ☐: {option}"

class SubmissionDateDec8(FormUserAttr):
    values = {'81749056_9057_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE_DEC 8: {option}"

class SubmissionDateFeb23(FormUserAttr):
    values = {'81749056_9057_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE_FEB 23: {option}"

class SubmissionDateJan19(FormUserAttr):
    values = {'81749056_9057_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE_JAN 19: {option}"

class SubmissionDateJun24(FormUserAttr):
    values = {'92039708_9710_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE_JUN 24 ☐: {option}"

class SubmissionDateJune29(FormUserAttr):
    values = {'81619486_9488_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE_JUNE 29: {option}"

class SubmissionDateMay27(FormUserAttr):
    values = {'92039708_9710_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE_MAY 27 ☐: {option}"

class SubmissionDateNov9(FormUserAttr):
    values = {'81619486_9488_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE_NOV 9: {option}"

class SubmissionDateOct07(FormUserAttr):
    values = {'92039708_9710_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE_OCT 07 ☐: {option}"

class SubmissionDateSept21(FormUserAttr):
    values = {'81619486_9488_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMISSION DATE_SEPT 21: {option}"

class SubmittedBy(FormUserAttr):
    values = {'0001123541_processed': 'Carol S. Lincoln', '0001463282_processed': ' L. E. Gravely', '0011838621_processed': 'MD Davis', '0012529284_processed': 'S. L. Willinger', '0012529295_processed': 'L J L. J. Spurtier', '0012602424_processed': '', '11508234_processed': 'Lumea', '12603270_processed': '', '71202511_processed': 'naid'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMITTED BY:: {option}"

class SubmitterSSs(FormUserAttr):
    values = {'0001123541_processed': '407- 64- 3484'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUBMITTER'S SS#:: {option}"

class SuggestionDescribeCurrentSituationAndIdea(FormUserAttr):
    values = {'0001123541_processed': 'The current system of managing records is too complex. The trend seems to be increasingly specific, when we should be getting more general. Right now, people must work to understand the system. We must spend too much time adninistering the system, labeling and cleaning our files. Complying is a real burden, both for the individual and for the records coordinators.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUGGESTION: (Describe Current Situation and Idea): {option}"

class Summary(FormUserAttr):
    values = {'71206427_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUMMARY: {option}"

class SupervisorInformation(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUPERVISOR INFORMATION:: {option}"

class SupervisorInformationBeeperNumber(FormUserAttr):
    values = {'91856041_6049_processed': '(201) 698- 780', '92586242_processed': '(201) 698 1780'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUPERVISOR INFORMATION:_BEEPER NUMBER:: {option}"

class SupervisorInformationNameOfAllwaysSupervisor(FormUserAttr):
    values = {'92586242_processed': 'Jerome Curry'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUPERVISOR INFORMATION:_NAME OF ALLWAYS SUPERVISOR: {option}"

class SupervisorInformationPhoneNumber(FormUserAttr):
    values = {'91856041_6049_processed': '(201) 923-9208 ', '92586242_processed': '(201) 923 -9208'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUPERVISOR INFORMATION:_PHONE NUMBER: {option}"

class SuppliedUntil(FormUserAttr):
    values = {'01197604_processed': 'February, 136'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUPPLIED UNTIL:: {option}"

class Supplier(FormUserAttr):
    values = {'0060077689_processed': 'WEBCRAFT TECHNOLOGIES INC', '0060214859_processed': 'OWENS CORNING', '01122115_processed': 'T. E.', '11508234_processed': 'Analytic Insight, Inc. Goldfarb Consultants'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUPPLIER: {option}"

class SuppliersBeingConsidered(FormUserAttr):
    values = {'71206427_processed': 'Chicago Show Display Equation Chicago Display Robert Nielson & Associates'}

    @staticmethod
    def nl_desc(option):
        return f"The user's SUPPLIERS BEING CONSIDERED:: {option}"

class SalesAnalysis(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sales Analysis ☐: {option}"

class SalesPersonnelToBeContacted(FormUserAttr):
    values = {'80728670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sales Personnel to be contacted: {option}"

class SalesPersonnelToBeWorkedWith(FormUserAttr):
    values = {'80728670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sales Personnel to be worked with:: {option}"

class SalesRepresentative(FormUserAttr):
    values = {'80728670_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sales Representative: {option}"

class SampleDescription(FormUserAttr):
    values = {'0001209043_processed': 'MALE AND FEMALE MENTHOL SMOKERS'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sample Description: {option}"

class SampleDisposition(FormUserAttr):
    values = {'0001485288_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sample Disposition: {option}"

class SampleNo(FormUserAttr):
    values = {'00093726_processed': '6030', '00283813_processed': '5031'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sample No.: {option}"

class SampleSize(FormUserAttr):
    values = {'0001463282_processed': '400', '0012529295_processed': '1. 500'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sample Size: {option}"

class SampleSpecificationsWrittenBy(FormUserAttr):
    values = {'00093726_processed': 'W. E. Routh', '00283813_processed': 'John H. M. Bohlken', '81574683_processed': 'W. Barnes'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sample Specifications Written By: {option}"

class ScreenerQuestionnaire(FormUserAttr):
    values = {'80310840a_processed': '5 minutes 10 minutes'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Screener Questionnaire: {option}"

class ScriptSAndOrStoryBoardSCleared(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Script(s) (and/ or story board(s)) cleared:: {option}"

class ScriptSAndOrStoryBoardSClearedEcu(FormUserAttr):
    values = {'0060255888_processed': '60'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Script(s) (and/ or story board(s)) cleared:_ECU :: {option}"

class ScriptSAndOrStoryBoardSClearedPhoneBooth(FormUserAttr):
    values = {'0060255888_processed': '60'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Script(s) (and/ or story board(s)) cleared:_Phone Booth :: {option}"

class SectionA(FormUserAttr):
    values = {'81574683_processed': '21mm 3.3 35,000y RE- 2218 126 mm 370mm 24.7mm 81.0 g/100 7% Kent 626 1509C'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Section A: {option}"

class SectionB(FormUserAttr):
    values = {'81574683_processed': 'mm'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Section B: {option}"

class SectionIiiA2NdParagraphTheFirstSentenceIsToBeChangedToReadAsFollows(FormUserAttr):
    values = {'00851879_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Section III A. 2nd paragraph- the first sentence is to be changed to read as follows:: {option}"

class SectionNumber(FormUserAttr):
    values = {'0030041455_processed': '2'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Section Number: {option}"

class SectionSalesManagerSName(FormUserAttr):
    values = {'0030041455_processed': 'Peter Hatch'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Section Sales Manager's Name: {option}"

class Seeds(FormUserAttr):
    values = {'00920294_processed': '25'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Seeds: {option}"

class SeniorVpMarketingTo1000000(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Senior VP Marketing (to $ 1,000,000): {option}"

class Sep(FormUserAttr):
    values = {'80310840a_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sep: {option}"

class SeparatePay(FormUserAttr):
    values = {'71341634_processed': 'Y'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Separate Pay-: {option}"

class Served(FormUserAttr):
    values = {'0012947358_processed': 'Summons and Complaint'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Served:: {option}"

class SignPrintNamesSeeInstructionsOnBack(FormUserAttr):
    values = {'0001123541_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sign & Print Names) (See Instructions On Back): {option}"

class SignatureEmployerOrDesignee(FormUserAttr):
    values = {'0001477983_processed': ' '}

    @staticmethod
    def nl_desc(option):
        return f"The user's Signature Employer or Designee: {option}"

class SignatureOfHetailPurchaser(FormUserAttr):
    values = {'88057519_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Signature of Hetail Purchaser: {option}"

class SignatureOfInitiator(FormUserAttr):
    values = {'87533049_processed': '', '91391286_processed': '', '91391310_processed': 'Marine B', '91974562_processed': '', '93351929_93351931_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Signature of Initiator: {option}"

class Signed(FormUserAttr):
    values = {'0001485288_processed': 'B. D. WINGLER', '0060136394_processed': 'HOPE MARTINEZ', '91581919_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Signed: {option}"

class SignificantDifference(FormUserAttr):
    values = {'0000999294_processed': '95+% confidence Level'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Significant Difference:: {option}"

class Size(FormUserAttr):
    values = {'0001209043_processed': 'FULL PAGE', '01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Size: {option}"

class Sizes(FormUserAttr):
    values = {'88547278_88547279_processed': '19.750 X 11'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sizes:: {option}"

class SmokingResults(FormUserAttr):
    values = {'01122115_processed': '.922 1 .059 .54 .20 20 .2 7 .6 62 .4 1 .07 .41 61 .7'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Smoking Results: {option}"

class SolidsComposit(FormUserAttr):
    values = {'0012199830_processed': 'Lecithin (Food Grade) Epoxidized Soy Bean Oil Cellulose Nitrate Wet w /2 Propanol Pigment, Yellow 34 Pigment, Blue 15: 4 Ester of Modified Tricyclic Carboxylic Acid Jonrez IM824'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Solids Composit: {option}"

class SourceOfBusinessLocalPremiumKsSmokers(FormUserAttr):
    values = {'71601299_processed': '250 Males (100 smokers, 25 ~ 29 years old, 150 smokers, 30 ~ 39 years old ABC+ who are not rejectors of imported cigarette and live in Seoul/ Pusan'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Source of Business - Local Premium KS Smokers: {option}"

class SourceOfBusinessThis(FormUserAttr):
    values = {'71601299_processed': '250 Males, (100 smokers 25 ~ 29 years old, 150 smokers, 30 ~ 39 years old) ABC+ who are not rejectors of imported cigarette and live in Seoul/ Pusan'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Source of Business - This:: {option}"

class SpecialInstructionsComments(FormUserAttr):
    values = {'0001485288_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Special Instructions & Comments: {option}"

class SpecialRequirements(FormUserAttr):
    values = {'00093726_processed': 'Spray 50 lbs. tobacco with solution of 880 g (= 1. 94 lbs.) PMC in 1175 ml of denatured alcohol. This should give 3. 4% PMO add- on (3. 3% PMO contained) assuming 88% spraying efficiency. PMO delivery from 85 mm cigarette smoked to 30 mm butt should be 6. 5 mg/ cig.', '81574683_processed': '1. Cigts. to be packed in white labels printed with "20 Class A. ATF Auth. #47 sample not for sale, all applicable state taxes paid, and code No. 746." 2. Cigts. to be inspected, placed in pk. mailers and shipped Inc., for Mkt. Rsh. Study.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Special Requirements: {option}"

class Species(FormUserAttr):
    values = {'89386032_processed': 'Mice'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Species: {option}"

class SpentPriorTo(FormUserAttr):
    values = {'0011906503_processed': '1989'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Spent Prior to: {option}"

class StandardGradeMark(FormUserAttr):
    values = {'0001118259_processed': 'PCFS Flue cured fines PCBS Burley fines MC- 4 Manufacturing fines MC -6 Stem Meal MC -7 Winnowers RXF Fine flue cured stem RBF Fine Burely stem'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Standard Grade Mark: {option}"

class Start(FormUserAttr):
    values = {'0011906503_processed': '7 88', '0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Start: {option}"

class StartPleteFr(FormUserAttr):
    values = {'0012529284_processed': '87 -113 (70, 825) 9 /23 10 /11 11 /16 87 -114 (70. 825) 10 /13 10 /29 12 /7 87 -115 (70, 825 11 /16 12 /7 1 /11'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Start plete FR: {option}"

class State(FormUserAttr):
    values = {'71341634_processed': '', '87682908_processed': '', '88057519_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's State: {option}"

class StateOf(FormUserAttr):
    values = {'91581919_processed': 'Indiana )'}

    @staticmethod
    def nl_desc(option):
        return f"The user's State of: {option}"

class StateCreateNewAppropriation(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's State:_☐ Create New Appropriation: {option}"

class StateDecreaseExistingAppropriation(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's State:_☐ Decrease Existing Appropriation: {option}"

class StateDecreaseExistingRevenues(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's State:_☐ Decrease Existing Revenues: {option}"

class StateIncreaseExistingAppropriation(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's State:_☐ Increase Existing Appropriation: {option}"

class StateIncreaseExistingRevenues(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's State:_☐ Increase Existing Revenues: {option}"

class StateNoStateFiscalEffect(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's State:_☐ No State Fiscal Effect: {option}"

class StaticCompleteCigar(FormUserAttr):
    values = {'0060094595_processed': '0 23 11 23'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Static -Complete Cigar: {option}"

class Status(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Status: {option}"

class Status1993(FormUserAttr):
    values = {'0001123541_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Status (1993): {option}"

class StatusApproved(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Status_Approved;: {option}"

class StatusProposed(FormUserAttr):
    values = {'0011906503_processed': 'x'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Status_Proposed: {option}"

class Street(FormUserAttr):
    values = {'87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Street: {option}"

class Streptozotocin(FormUserAttr):
    values = {'01073843_processed': '1.0 0.5'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Streptozotocin: {option}"

class Strokes(FormUserAttr):
    values = {'0030031163_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Strokes: {option}"

class StudyName(FormUserAttr):
    values = {'89368010_processed': 'Acute Toxicity of Reference Cigarette Smoke lafter Inhalation in Mice.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Study Name: {option}"

class StudyNumber(FormUserAttr):
    values = {'89368010_processed': 'I- 1725.001'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Study Number: {option}"

class StudyTitle(FormUserAttr):
    values = {'89386032_processed': 'Bioassay of Cigarette Smoke Condensates for potential Tumorigenic Activity on Mouse Skin (Revised Pathology Report)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Study Title: {option}"

class Style(FormUserAttr):
    values = {'0000989556_processed': 'HLB- KS'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Style:: {option}"

class Submission(FormUserAttr):
    values = {'0011906503_processed': '88'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Submission: {option}"

class SuggestedSolutionsS(FormUserAttr):
    values = {'0000971160_processed': 'Delete coal retention from the list of standard analyses performed on licensee submitted product samples. Special requests for coal retention testing could still be submitted on an exception basis.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Suggested Solutions (s) :: {option}"

class Suggestion(FormUserAttr):
    values = {'0000971160_processed': 'Discontinue coal retention analyses on licensee submitted product samples (Note : Coal Retention testing is not performed by most licensees. Other B&W physical measurements as ends stability and inspection for soft spots in ciparettes are thought to be sufficient measures to assure cigarette physical integrity. The proposed action will increase laboratory productivity . )'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Suggestion:: {option}"

class SuggestionsRecommendations(FormUserAttr):
    values = {'92091873_processed': 'Perhaps the tickets could be sent but a little sooner This year the tickets arrived on Thursday and the race was Sunday. This made it difficult to get the tickets to customers on tine.', '93213298_processed': 'In the future, please specify where the Newport hospitality area will be located - at the Newport car trans- porter site or in a separate area . Specific directions will be needed.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Suggestions/ Recommendations:: {option}"

class SumaryOfImrdBudget(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sumary of IMRD Budget: {option}"

class SumaryOfImrdBudgetCommittedToDateCurrentYear(FormUserAttr):
    values = {'0011838621_processed': '1.471.873.85'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sumary of IMRD Budget_Committed to Date: (Current Year): {option}"

class SumaryOfImrdBudgetCurrentBalAvailable(FormUserAttr):
    values = {'0011838621_processed': '1.488.126.23'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sumary of IMRD Budget_Current Bal. Available:: {option}"

class SumaryOfImrdBudgetNewBalance(FormUserAttr):
    values = {'0011838621_processed': '1.488.126.15'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sumary of IMRD Budget_New Balance:: {option}"

class SumaryOfImrdBudgetThisAmountFromNextYearSBudget(FormUserAttr):
    values = {'0011838621_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sumary of IMRD Budget_This Amount (From Next Year's Budget): {option}"

class SumaryOfImrdBudgetThisChangeFromCurrentBudget(FormUserAttr):
    values = {'0011838621_processed': '.08'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sumary of IMRD Budget_This Change: (From Current Budget): {option}"

class SumaryOfImrdBudgetTotalAreaBudget(FormUserAttr):
    values = {'0011838621_processed': '$ 2.960.000.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sumary of IMRD Budget_Total Area Budget:: {option}"

class SummaryOfMrdBudget(FormUserAttr):
    values = {'11508234_processed': '1995'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Summary of MRD Budget: {option}"

class SummaryOfMrdBudgetCommitedToDateCurrentYear(FormUserAttr):
    values = {'0001463282_processed': '205,775.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Summary of MRD Budget_Commited to Date: (Current Year): {option}"

class SummaryOfMrdBudgetCurrentBalAvailable(FormUserAttr):
    values = {'0001463282_processed': '199,900.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Summary of MRD Budget_Current Bal. Available:: {option}"

class SummaryOfMrdBudgetNewBalance(FormUserAttr):
    values = {'0001463282_processed': '164,225.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Summary of MRD Budget_New Balance: {option}"

class SummaryOfMrdBudgetThisAmount(FormUserAttr):
    values = {'0001463282_processed': '-O-'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Summary of MRD Budget_This Amount: {option}"

class SummaryOfMrdBudgetThisChangeFromCurrentBudget(FormUserAttr):
    values = {'0001463282_processed': '-35,675,00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Summary of MRD Budget_This Change: (From Current Budget: {option}"

class SummaryOfMrdBudgetTotalAreaBudget(FormUserAttr):
    values = {'0001463282_processed': '370,000.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Summary of MRD Budget_Total Area Budget:: {option}"

class SummaryOfResearchBudget(FormUserAttr):
    values = {'12603270_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Summary of Research Budget: {option}"

class SummaryOfResearchBudgetCurrentBalAvailable(FormUserAttr):
    values = {'0012529295_processed': '(381, 583. 08)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Summary of Research Budget_Current Bal. Available:: {option}"

class SummaryOfResearchBudgetCurrentBalanceAvailable(FormUserAttr):
    values = {'0012529284_processed': '(886, 220. 53)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Summary of Research Budget_Current Balance Available:: {option}"

class SummaryOfResearchBudgetThisAmount(FormUserAttr):
    values = {'0012529284_processed': '-14, 165. 00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Summary of Research Budget_This Amount: {option}"

class SummaryOfResearchBudgetThisChangeFromCurrentBudget(FormUserAttr):
    values = {'0012529295_processed': '-70, 825. 00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Summary of Research Budget_This Change (From Current Budget): {option}"

class SummaryOfResearchBudgetTotalAreaBudget(FormUserAttr):
    values = {'0012529284_processed': '', '0012529295_processed': '780, 900. 00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Summary of Research Budget_Total Area Budget:: {option}"

class SupervisorManager(FormUserAttr):
    values = {'0000971160_processed': 'J. S. Wigand'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Supervisor / Manager: {option}"

class SupplierRabidResearch(FormUserAttr):
    values = {'71202511_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Supplier_Rabid Research: {option}"

class Suppression(FormUserAttr):
    values = {'00920294_processed': '5'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Suppression: {option}"

class SwornToAndSubscribedBeforeMeThis(FormUserAttr):
    values = {'91581919_processed': '4th'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Sworn to and subscribed before me this: {option}"

class System(FormUserAttr):
    values = {'00920294_processed': 'Corp/ Multibrand'}

    @staticmethod
    def nl_desc(option):
        return f"The user's System: {option}"

class T(FormUserAttr):
    values = {'87672097_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's T: {option}"

class TCodesNa(FormUserAttr):
    values = {'00920294_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's T Codes NA: {option}"

class TN(FormUserAttr):
    values = {'71190280_processed': "8'", '71366499_processed': 'NA'}

    @staticmethod
    def nl_desc(option):
        return f"The user's T&N: {option}"

class Ta100(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's TA100: {option}"

class Ta10059(FormUserAttr):
    values = {'01073843_processed': "['127.00', '4.26', '3.63', '3.11', '1.99']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's TA100_(+) 5-9: {option}"

class Ta1535(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's TA1535: {option}"

class Ta153559(FormUserAttr):
    values = {'01073843_processed': "['14.00', '3.07', '2.86', '31.14', '12.29']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's TA1535_(+) 5-9: {option}"

class Ta15359(FormUserAttr):
    values = {'00836244_processed': '4 .67'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TA1535_(-) 9: {option}"

class Ta98(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's TA98: {option}"

class Ta9859(FormUserAttr):
    values = {'01073843_processed': "['21.00', '20.10', '18.81']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's TA98_(+) 5-9: {option}"

class Tar(FormUserAttr):
    values = {'0000999294_processed': '9.1 5. 5', '0060094595_processed': '39. .7 35 .6 37 .8 31 .0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TAR: {option}"

class Target(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TARGET: {option}"

class TargetDate(FormUserAttr):
    values = {'0000990274_processed': 'April 13, 1984'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TARGET DATE:: {option}"

class TelNo(FormUserAttr):
    values = {'01191071_1072_processed': 'SHB'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TEL NO.: {option}"

class Tel(FormUserAttr):
    values = {'88547278_88547279_processed': '(212) 627 4111'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TEL:: {option}"

class TelecopierTransmittalCoverSheet(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's TELECOPIER TRANSMITTAL COVER SHEET: {option}"

class TelecopierTransmittalCoverSheetDate(FormUserAttr):
    values = {'92298125_processed': 'JAN 19. 1995'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TELECOPIER TRANSMITTAL COVER SHEET_DATE:: {option}"

class TelecopierTransmittalCoverSheetFrom(FormUserAttr):
    values = {'92298125_processed': 'Pam Churchill'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TELECOPIER TRANSMITTAL COVER SHEET_FROM:: {option}"

class TelecopierTransmittalCoverSheetPages(FormUserAttr):
    values = {'92298125_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TELECOPIER TRANSMITTAL COVER SHEET_PAGES:: {option}"

class TelecopierTransmittalCoverSheetRe(FormUserAttr):
    values = {'92298125_processed': 'CIGARETTE QUESTIONNAIRE'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TELECOPIER TRANSMITTAL COVER SHEET_RE:: {option}"

class TelecopierTransmittalCoverSheetTo(FormUserAttr):
    values = {'92298125_processed': 'MARY MAZZA'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TELECOPIER TRANSMITTAL COVER SHEET_TO:: {option}"

class TelefaxMessageNo(FormUserAttr):
    values = {'0060165115_processed': '2463'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TELEFAX MESSAGE No.:: {option}"

class Telex(FormUserAttr):
    values = {'01150773_01150774_processed': '89- 193 COVLING WSH'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TELEX: {option}"

class TennisTournament(FormUserAttr):
    values = {'0030031163_processed': '(Ladies & Men) . . . Friday, August 16, starting time is 3:00 P. M.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TENNIS TOURNAMENT: {option}"

class Terms(FormUserAttr):
    values = {'0060077689_processed': 'NET 30 Days', '00922237_processed': '15 Net F.O.S N/A VIA N/A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TERMS: {option}"

class TermsFOB(FormUserAttr):
    values = {'00920222_processed': 'N /A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TERMS_F. O. B.: {option}"

class TermsNet(FormUserAttr):
    values = {'00920222_processed': '15'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TERMS_NET: {option}"

class TermsVia(FormUserAttr):
    values = {'00920222_processed': 'N /A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TERMS_VIA: {option}"

class TestDates(FormUserAttr):
    values = {'0001476912_processed': '8/5 and 6 8/8'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TEST DATES: {option}"

class TestMaterialS(FormUserAttr):
    values = {'00860012_00860014_processed': '', '00866042_processed': 'B166'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TEST MATERIAL (S): {option}"

class Tested(FormUserAttr):
    values = {'00040534_processed': '12/28/78', '00836244_processed': '9 /10 /80 -10 /10 /80', '01073843_processed': '3/18/81-4/8/81'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TESTED: {option}"

class TextOver500PrizesToBeAwarded(FormUserAttr):
    values = {'80707440_7443_processed': 'Now you can win up $ 5,000 for simply picking the winners of the games listed below. Just check the box next to the team you think will win. Allow for the point spread in your selections. (For example, if a team is quoted as +7 pts. this means they must win the game by at least 7 points.) Prizes will be awarded by random drawings to those who have the greatest official number of winning selections. Full details are in the Rules.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TEXT: Over 500 Prizes To Be Awarded: {option}"

class TheFollowingInformationMustBeFurnished(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's THE FOLLOWING INFORMATION MUST BE FURNISHED:: {option}"

class TheFollowingInformationMustBeFurnishedDate(FormUserAttr):
    values = {'92314414_processed': '1 November 1991'}

    @staticmethod
    def nl_desc(option):
        return f"The user's THE FOLLOWING INFORMATION MUST BE FURNISHED:_(Date): {option}"

class TheFollowingInformationMustBeFurnishedSignature(FormUserAttr):
    values = {'92314414_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's THE FOLLOWING INFORMATION MUST BE FURNISHED:_(Signature): {option}"

class TheFollowingInformationMustBeFurnished1FullName(FormUserAttr):
    values = {'92314414_processed': 'Andrew H. Tisch (Print or type)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's THE FOLLOWING INFORMATION MUST BE FURNISHED:_1. Full Name: {option}"

class TheFollowingInformationMustBeFurnished2ResidenceAddress(FormUserAttr):
    values = {'92314414_processed': '26 East 63rd Street, New York, N. Y. 10021 (Include state and zip code)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's THE FOLLOWING INFORMATION MUST BE FURNISHED:_2. Residence Address: {option}"

class TheFollowingInformationMustBeFurnished3BusinessAddress(FormUserAttr):
    values = {'92314414_processed': 'One Park Avenue, New York, N. Y. 10016'}

    @staticmethod
    def nl_desc(option):
        return f"The user's THE FOLLOWING INFORMATION MUST BE FURNISHED:_3. Business Address: {option}"

class TheFollowingInformationMustBeFurnished4Occupation(FormUserAttr):
    values = {'92314414_processed': 'Chairman/ CEO - Lorillard Tobacco Company (Job title or position)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's THE FOLLOWING INFORMATION MUST BE FURNISHED:_4. Occupation: {option}"

class This(FormUserAttr):
    values = {'0012602424_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's THIS: {option}"

class ThisAmount(FormUserAttr):
    values = {'0012602424_processed': '200. 00', '12603270_processed': '0'}

    @staticmethod
    def nl_desc(option):
        return f"The user's THIS AMOUNT: {option}"

class ThisChangeFromCurrentBudget(FormUserAttr):
    values = {'0012602424_processed': '-800. 00', '12603270_processed': '+58,500'}

    @staticmethod
    def nl_desc(option):
        return f"The user's THIS CHANGE: (From Current Budget): {option}"

class ThisDocumentIsFrom(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's THIS DOCUMENT IS FROM:: {option}"

class ThisDocumentIsFromComments(FormUserAttr):
    values = {'91372360_processed': 'The attached Competitive information was secured in Oklahoma today. If you should have any questions.', '91914407_processed': 'The attached was obtained from Mackoul Dist.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's THIS DOCUMENT IS FROM:_COMMENTS:: {option}"

class ThisDocumentIsFromFaxPhoneNumber(FormUserAttr):
    values = {'91372360_processed': '(400) 840- 0639', '92657391_processed': '(713) 591 0204'}

    @staticmethod
    def nl_desc(option):
        return f"The user's THIS DOCUMENT IS FROM:_FAX PHONE NUMBER:: {option}"

class ThisDocumentIsFromFaxTelephoneNumber(FormUserAttr):
    values = {'91914407_processed': '(904) 464- 0744'}

    @staticmethod
    def nl_desc(option):
        return f"The user's THIS DOCUMENT IS FROM:_FAX TELEPHONE NUMBER:: {option}"

class ThisDocumentIsFromName(FormUserAttr):
    values = {'91372360_processed': 'R F ', '91914407_processed': 'Fred Paternostro', '92657391_processed': 'J. L. McGinnis - Region 9'}

    @staticmethod
    def nl_desc(option):
        return f"The user's THIS DOCUMENT IS FROM:_NAME:: {option}"

class ThisDocumentIsFromOffice(FormUserAttr):
    values = {'91372360_processed': 'Oklahoma City. OK', '92657391_processed': 'Lorillard Tobacco Company Houston N., Texas'}

    @staticmethod
    def nl_desc(option):
        return f"The user's THIS DOCUMENT IS FROM:_OFFICE:: {option}"

class Time(FormUserAttr):
    values = {'91372360_processed': '3:28 CST'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TIME: {option}"

class Timetable(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's TIMETABLE:: {option}"

class TimetableInMarketArrivalDate(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TIMETABLE:_In- Market Arrival Date:: {option}"

class TimetableLaunchDate(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TIMETABLE:_Launch Date:: {option}"

class TimetableManufacturing(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TIMETABLE:_Manufacturing:: {option}"

class TimetableProductSpecsDate(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TIMETABLE:_Product Specs Date:: {option}"

class TimetableShipping(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TIMETABLE:_Shipping:: {option}"

class TimetableStartManufactureDate(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TIMETABLE:_Start Manufacture Date:: {option}"

class To(FormUserAttr):
    values = {'0011845203_processed': 'Mr. Johnny Pedersen - Gallup', '0012947358_processed': 'The Corporation Trust Company', '0060036622_processed': 'Mr. G. J. Schramm Mr. R. H. Stinnette Mr. J. B. McCarthy Mr. W. P. Myhan Mr. F. X. Whelan', '0060165115_processed': 'Dr. Don Leyden, Dept. Scientific Affairs', '0071032790_processed': 'Files', '00920294_processed': 'RJR IR - Suz /Art', '01150773_01150774_processed': 'Mark Berlind', '11875011_processed': 'Goldfarb Consultants', '80728670_processed': 'J. R. Mueller', '81619486_9488_processed': 'S. P. ZOLOT', '81619511_9513_processed': 'S.P. Zolot', '81749056_9057_processed': 'S. P. ZOLOT', '82254638_processed': 'SAM ZOLOT', '87533049_processed': 'S. A. Rapisarldi', '91161344_91161347_processed': 'Mr. Flinn Mr. Goldbrenner Mr. Gaalman Mr. Donahue (Loews) Mr. Duffy (Loews) Mr. Miele (Loews) Mr. Hudson (Greensboro) Dr. Schultz (Greensboro Mr. Tucker (Greensboro) Dr. Jones (Greensboro)', '91315069_91315070_processed': 'R. H. ORCUTT', '91391286_processed': 'VINCE LOSITO', '91391310_processed': 'VINCE LOSITO', '91903177_processed': 'K. A. SPARROW', '91939637_processed': '', '91974562_processed': 'VINCE LOSITO', '92039708_9710_processed': 'R. B. SPELL', '92327794_processed': '(919) 378- 001 Ron Goldbrenner', '92657311_7313_processed': 'R. B. SPELL', '93351929_93351931_processed': 'VINCE LOSITO', '93380187_processed': 'V. M. LOSITO'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TO:: {option}"

class TotalOfIndependentNewport1ClubOutlets(FormUserAttr):
    values = {'81749056_9057_processed': '1,020'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TOTAL # OF INDEPENDENT NEWPORT #1 CLUB OUTLETS:: {option}"

class TotalOfIndependentSpecialEmphasisOutlets(FormUserAttr):
    values = {'81749056_9057_processed': '2.471'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TOTAL # OF INDEPENDENT SPECIAL EMPHASIS OUTLETS:: {option}"

class TotalOfNumberOneClubOutletsWithDistribution(FormUserAttr):
    values = {'81749056_9057_processed': '365 346 371 355'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TOTAL # OF NUMBER ONE CLUB OUTLETS WITH DISTRIBUTION: {option}"

class TotalOfSpEmphasisOutleisWithDistribution(FormUserAttr):
    values = {'81749056_9057_processed': '542 475 479 451'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TOTAL # OF SP EMPHASIS OUTLEIS WITH DISTRIBUTION: {option}"

class TotalAreaBudget(FormUserAttr):
    values = {'0012602424_processed': '1984 (REV) 3, 488, 000. 00', '12603270_processed': '3,669,000'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TOTAL AREA BUDGET:: {option}"

class TotalBudget(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TOTAL BUDGET: {option}"

class TotalPages(FormUserAttr):
    values = {'91914407_processed': '14'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TOTAL PAGES: {option}"

class Total(FormUserAttr):
    values = {'0060136394_processed': '$ 6.600.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TOTAL:: {option}"

class Totals(FormUserAttr):
    values = {'0060080406_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TOTALS $: {option}"

class ToxicitySurvival(FormUserAttr):
    values = {'00836244_processed': '50 80 100'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TOXICITY (% SURVIVAL): {option}"

class ToxicitySurvival100(FormUserAttr):
    values = {'01073843_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TOXICITY (%) (SURVIVAL)_100: {option}"

class ToxicitySurvival50(FormUserAttr):
    values = {'01073843_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TOXICITY (%) (SURVIVAL)_50: {option}"

class ToxicitySurvival80(FormUserAttr):
    values = {'01073843_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TOXICITY (%) (SURVIVAL)_80: {option}"

class Transfer(FormUserAttr):
    values = {'0001485288_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TRANSFER ☐: {option}"

class TrimSize(FormUserAttr):
    values = {'71190280_processed': '33/16"WX21/2"H', '71366499_processed': '14 1/2 X 18"'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TRIM SIZE: {option}"

class FieldTrue(FormUserAttr):
    values = {'91939637_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TRUE: {option}"

class TrueCoreAreas(FormUserAttr):
    values = {'93380187_processed': 'TOTAL NEW YORK TOTAL BOSTON NEW HAVEN HARTFORD TOTAL SAN FRANCISCO SYRACUSE ROCHESTER TOTAL PHILADELPHIA TOTAL CHICAGO BUFFALO ALBANY TOTAL NEW JERSEY PROVIDENCE CAMDEN CONCORD SPRINGFIELD BALTIMORE PORTLAND, ME TOTAL DETROIT TOTAL WASHINGTON WILMINGTON REGION 15 x SAN BERNADINO'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TRUE CORE AREAS: {option}"

class TypeChange(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE CHANGE:: {option}"

class TypeDisplay(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE DISPLAY: {option}"

class TypeDisplayCounter(FormUserAttr):
    values = {'91939637_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE DISPLAY_COUNTER: {option}"

class TypeDisplayFloor(FormUserAttr):
    values = {'91939637_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE DISPLAY_FLOOR: {option}"

class TypeDisplayPoster(FormUserAttr):
    values = {'91939637_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE DISPLAY_POSTER: {option}"

class TypeOfProduct(FormUserAttr):
    values = {'93329540_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF PRODUCT:: {option}"

class TypeOfPromotion(FormUserAttr):
    values = {'91355841_processed': 'SEE ATTACHMENTS', '93455715_processed': 'SEE ATTACHED CORRESPONDENCE REGARDING: - R. J. REYNOLDS SPRING DIRECT ACCOUNT INCENTIVE PROGRAM - Philip Morris- SPECIAL PROMOTIONS ON MAKLBORO AND CAMBRIDGE CIGARETTES'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF PROMOTION:: {option}"

class TypeOfSpecificationChangeCheckAllThatApply(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF SPECIFICATION CHANGE (Check all that apply): {option}"

class TypeOfSpecificationChangeCheckAllThatApplyCigaretteDesignPermanent(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF SPECIFICATION CHANGE (Check all that apply)_Cigarette Design, Permanent: {option}"

class TypeOfSpecificationChangeCheckAllThatApplyCigaretteDesignTrial(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF SPECIFICATION CHANGE (Check all that apply)_Cigarette Design, Trial: {option}"

class TypeOfSpecificationChangeCheckAllThatApplyDiscontinueProduct(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF SPECIFICATION CHANGE (Check all that apply)_Discontinue Product: {option}"

class TypeOfSpecificationChangeCheckAllThatApplyEquivalentAdditive(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF SPECIFICATION CHANGE (Check all that apply)_Equivalent Additive: {option}"

class TypeOfSpecificationChangeCheckAllThatApplyEquivalentFilterPaperTipping(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF SPECIFICATION CHANGE (Check all that apply)_Equivalent Filter/ Paper/ /Tipping: {option}"

class TypeOfSpecificationChangeCheckAllThatApplyEquivalentPackagingMaterial(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF SPECIFICATION CHANGE (Check all that apply)_Equivalent Packaging Material: {option}"

class TypeOfSpecificationChangeCheckAllThatApplyNewProduct(FormUserAttr):
    values = {'0012178355_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF SPECIFICATION CHANGE (Check all that apply)_New Product: {option}"

class TypeOfSpecificationChangeCheckAllThatApplyPackagingPermanent(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF SPECIFICATION CHANGE (Check all that apply)_Packaging, Permanent: {option}"

class TypeOfSpecificationChangeCheckAllThatApplyPackagingTemporary(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF SPECIFICATION CHANGE (Check all that apply)_Packaging, Temporary: {option}"

class TypeOfSpecificationChangeCheckAllThatApplyProcessing(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF SPECIFICATION CHANGE (Check all that apply)_Processing: {option}"

class TypeOfSpecificationChangeCheckAllThatApplyTarAdjustment1Mg(FormUserAttr):
    values = {'0012178355_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE OF SPECIFICATION CHANGE (Check all that apply)_Tar Adjustment < 1 mg: {option}"

class TypeBiological(FormUserAttr):
    values = {'00851772_1780_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE_BIOLOGICAL ☐: {option}"

class TypeChemical(FormUserAttr):
    values = {'00851772_1780_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE_CHEMICAL ☐: {option}"

class TypeCombined(FormUserAttr):
    values = {'00851772_1780_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's TYPE_COMBINED: {option}"

class TapeSpeed(FormUserAttr):
    values = {'01122115_processed': '400 F. P. M.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tape Speed: {option}"

class TarNumber(FormUserAttr):
    values = {'01197604_processed': '195'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tar Number:: {option}"

class Tars(FormUserAttr):
    values = {'01122115_processed': '.922 1 .059 .54 .20 20 .2 7 .6 62 .4 1 .07 .41 61 .7'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tars: {option}"

class TaxStatusPaidOrFree(FormUserAttr):
    values = {'0001485288_processed': 'Free'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tax Status Paid or Free: {option}"

class Technician(FormUserAttr):
    values = {'0012199830_processed': 'DLR 12/ 5/ 89'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Technician: {option}"

class Telefax(FormUserAttr):
    values = {'0060165115_processed': '(0 22 03) 303 -362', '01150773_01150774_processed': '(202) 662-6291'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Telefax: {option}"

class Telephone(FormUserAttr):
    values = {'0060165115_processed': '(0 22 03) 303 -1', '0060262650_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Telephone: {option}"

class TestArticle(FormUserAttr):
    values = {'89386032_processed': 'Multiple'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Test Article: {option}"

class TestPeriod(FormUserAttr):
    values = {'0060025670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Test Period:: {option}"

class Tester(FormUserAttr):
    values = {'0060025670_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tester: {option}"

class TheFollowingDocumentIncludingCoverPageIs(FormUserAttr):
    values = {'92657391_processed': '3'}

    @staticmethod
    def nl_desc(option):
        return f"The user's The following document, including cover page is: {option}"

class ThisAmountFromNextYearSBudget(FormUserAttr):
    values = {'0012529295_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's This Amount (From Next Year's Budget): {option}"

class ThisChange(FormUserAttr):
    values = {'11508234_processed': '29,500'}

    @staticmethod
    def nl_desc(option):
        return f"The user's This Change:: {option}"

class ThisProjectIs(FormUserAttr):
    values = {'0011906503_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's This Project is: {option}"

class ThisFormWasPlacedBeforeBatesId(FormUserAttr):
    values = {'0001463448_processed': '6708105266'}

    @staticmethod
    def nl_desc(option):
        return f"The user's This form was placed before Bates ID: {option}"

class TippingPaper(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tipping Paper:: {option}"

class TippingPaperBobbinWidth(FormUserAttr):
    values = {'0000989556_processed': '50 mm mm', '0001456787_processed': "['64 mm', '64 mm']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tipping Paper:_Bobbin Width: {option}"

class TippingPaperColor(FormUserAttr):
    values = {'0000989556_processed': 'Imitation Cork', '0001456787_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tipping Paper:_Color: {option}"

class TippingPaperDobbinLength(FormUserAttr):
    values = {'0001456787_processed': "['2500 M', '2500 M']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tipping Paper:_Dobbin Length: {option}"

class TippingPaperPerforationTypeNoOfLines(FormUserAttr):
    values = {'0001456787_processed': "['N/A', 'N/A']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tipping Paper:_Perforation Type & No. of lines: {option}"

class TippingPaperPerforationTypeAndNoOfLines(FormUserAttr):
    values = {'0000989556_processed': 'None'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tipping Paper:_Perforation Type and No. of lines: {option}"

class TippingPaperPorosity(FormUserAttr):
    values = {'0000989556_processed': '(coresta)', '0001456787_processed': "['Non Porous', 'Non Porous']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tipping Paper:_Porosity: {option}"

class TippingPaperPrintDescription(FormUserAttr):
    values = {'0000989556_processed': 'Brown on yellow', '0001456787_processed': "['N/A', 'N/A']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tipping Paper:_Print Description: {option}"

class TippingPaperRobbinLength(FormUserAttr):
    values = {'0000989556_processed': '2700 m'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tipping Paper:_Robbin Length: {option}"

class TippingPaperSupplierCodeNoS(FormUserAttr):
    values = {'0000989556_processed': 'E.30639', '0001456787_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tipping Paper:_Supplier Code No(s).: {option}"

class TippingPaperSupplierS(FormUserAttr):
    values = {'0000989556_processed': 'Ecusta', '0001456787_processed': "['ECUSTA/ B&W', 'ECUSTA/ B & W']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tipping Paper:_Supplier(s): {option}"

class TippingPaperSubstance(FormUserAttr):
    values = {'0000989556_processed': '36 gm/ m2', '0001456787_processed': "['36 nm/ M2', '36 nm /47M2']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tipping Paper:_substance: {option}"

class TippingAndTippingApplication(FormUserAttr):
    values = {'0000989556_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tipping and Tipping Application: {option}"

class Title(FormUserAttr):
    values = {'0001209043_processed': '"HEAD IN WATER"', '0001438955_processed': '" KALEIDOSCOPE - - GONE WITH THE WIND " *', '00070353_processed': '"Effect of Nitrates in Tobacco on the Catechol Yield in Cigarette Smoke"', '0011906503_processed': 'CICARETTE TEST STATION (CT5400)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Title: {option}"

class TitleOfAction(FormUserAttr):
    values = {'0012947358_processed': 'Reuben Sunstein, Plaintiff, v. The American Tobacco Company, a New Jorsey corporation, Defendant.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Title of Action:: {option}"

class ToBeDeductedFrom1998Budget(FormUserAttr):
    values = {'71202511_processed': '$ 58,500'}

    @staticmethod
    def nl_desc(option):
        return f"The user's To Be Deducted from 1998 Budget: {option}"

class ToBeDeductedFrom1999Budget(FormUserAttr):
    values = {'71202511_processed': '$'}

    @staticmethod
    def nl_desc(option):
        return f"The user's To Be Deducted from 1999 Budget: {option}"

class ToSampleStock(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's To Sample Stock: {option}"

class ToSampleStockMR(FormUserAttr):
    values = {'0001485288_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's To Sample Stock_M. R.: {option}"

class ToSampleStockRD(FormUserAttr):
    values = {'0001485288_processed': "['20', 'Free']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's To Sample Stock_R & D: {option}"

class ToNicotineMgCigt(FormUserAttr):
    values = {'0060308251_processed': '0 .2'}

    @staticmethod
    def nl_desc(option):
        return f"The user's To_Nicotine (Mg/ /Cigt): {option}"

class ToTarMgCigt(FormUserAttr):
    values = {'0060308251_processed': '2'}

    @staticmethod
    def nl_desc(option):
        return f"The user's To_Tar (Mg /Cigt): {option}"

class TobaccoNumber(FormUserAttr):
    values = {'01197604_processed': 'Sample No. 1166, RD 308'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tobacco Number:: {option}"

class TobaccoUsed(FormUserAttr):
    values = {'01122115_processed': 'SPRING'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tobacco Used: {option}"

class TodaySDate(FormUserAttr):
    values = {'91161344_91161347_processed': '3/20/78'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Today's Date: {option}"

class Topic(FormUserAttr):
    values = {'0060262650_processed': 'The Oncogene, the Fragile Site, and Nonrandom Aberrations'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Topic: {option}"

class Total205(FormUserAttr):
    values = {'0000999294_processed': '53+++ 39 8 200'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Total (205): {option}"

class TotalAreaAuthorized(FormUserAttr):
    values = {'11508234_processed': '500,000'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Total Area Authorized: {option}"

class TotalAuthorizedProjectAmount(FormUserAttr):
    values = {'71202511_processed': '$ 58,500'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Total Authorized Project Amount: {option}"

class TotalContractCost(FormUserAttr):
    values = {'0060029036_processed': '$ 1,340,000.00'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Total Contract Cost: {option}"

class TotalCost(FormUserAttr):
    values = {'0011838621_processed': '$ 43.335.00 $ 4.376.47 $ 47.711.47', '11508234_processed': '29,500 31,716', '71202511_processed': '58,500'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Total Cost: {option}"

class TotalDenierAsMarked(FormUserAttr):
    values = {'01122115_processed': '58 ,000'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Total Denier as Marked: {option}"

class TotalDenierAsTested(FormUserAttr):
    values = {'01122115_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Total Denier as Tested: {option}"

class TotalSample(FormUserAttr):
    values = {'0001209043_processed': '214', '0001438955_processed': '285'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Total Sample: {option}"

class TotalSolids(FormUserAttr):
    values = {'0012199830_processed': 'Solvent Composit to % V. O. C. s Toluene Isopropyl Acetate N- Propyl Acetate'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Total Solids: {option}"

class TotalVOCS(FormUserAttr):
    values = {'0012199830_processed': '100. 00%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Total V. O. C. s: {option}"

class TotalNumberOfPagesIncludingThisPage(FormUserAttr):
    values = {'0001129658_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Total number of pages including this page:: {option}"

class TotalBright(FormUserAttr):
    values = {'0000999294_processed': "['4.59', '3.42', '4.94', '3.04', '2.78', '3.24', '3.96']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Total_Bright: {option}"

class TotalKl(FormUserAttr):
    values = {'0000999294_processed': "['4.31***', '3.60**', '3.64***', '3.39***', '3.12***', '3.56***', '4.00']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Total_KL: {option}"

class Toxline(FormUserAttr):
    values = {'00851772_1780_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Toxline: {option}"

class TradeRegister(FormUserAttr):
    values = {'0060165115_processed': 'Cologne HRB 367'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Trade Register: {option}"

class TuesdayYN(FormUserAttr):
    values = {'87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tuesday (Y/ N): {option}"

class Type(FormUserAttr):
    values = {'0001123541_processed': 'EQPR'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Type: {option}"

class TypeOfAd(FormUserAttr):
    values = {'0001438955_processed': 'PARADE, 1 Page, 4- Color'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Type of Ad: {option}"

class TypeOfCigarette(FormUserAttr):
    values = {'00093726_processed': '85 mm Filter'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Type of Cigarette: {option}"

class TypeOfEvent(FormUserAttr):
    values = {'0011976929_processed': 'Beauty Contest'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Type of Event:: {option}"

class TypeOfMaker(FormUserAttr):
    values = {'01122115_processed': 'AMF'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Type of Maker: {option}"

class TypeOfRod(FormUserAttr):
    values = {'01122115_processed': '"D"'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Type of Rod: {option}"

class TypeOfTipper(FormUserAttr):
    values = {'01122115_processed': 'Hauni'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Type of Tipper: {option}"

class TypeOfProductSizeSListPrice(FormUserAttr):
    values = {'81186212_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Type of product, size(s) & list price:: {option}"

class TPic(FormUserAttr):
    values = {'0060262650_processed': 'Cyrogeneric Epidemiology'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Tοpic: {option}"

class Unit(FormUserAttr):
    values = {'00920222_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's UNIT: {option}"

class UnitPrice(FormUserAttr):
    values = {'00922237_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's UNIT PRICE: {option}"

class Units(FormUserAttr):
    values = {'01408099_01408101_processed': '', '71341634_processed': 'CTNS CTNS'}

    @staticmethod
    def nl_desc(option):
        return f"The user's UNITS: {option}"

class UpcNo(FormUserAttr):
    values = {'716552_processed': '272972'}

    @staticmethod
    def nl_desc(option):
        return f"The user's UPC NO.: {option}"

class Use(FormUserAttr):
    values = {'716552_processed': 'CUSTOMER SPEC. (GRAVURE)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's USE:: {option}"

class Under35(FormUserAttr):
    values = {'0001209043_processed': '2.4 (42) 33 (81)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Under 35: {option}"

class Under3535Over(FormUserAttr):
    values = {'0001438955_processed': '3.1 (129) 4.2 (95) 5 9 (117) (105)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Under 35 35 & Over: {option}"

class Up(FormUserAttr):
    values = {'0011973451_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Up:: {option}"

class Vendor(FormUserAttr):
    values = {'00920222_processed': 'Borriston Laboratories, INC. , 5050 Beech Place Temple Hills, MD 20748', '00922237_processed': 'Microbiological Associates 5221 River Rd., Bethesda MD 20816'}

    @staticmethod
    def nl_desc(option):
        return f"The user's VENDOR: {option}"

class Via(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's VIA:: {option}"

class ViaCertifiedMail(FormUserAttr):
    values = {'0012947358_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's VIA:_() Certified Mail: {option}"

class ViaCertifiedAirMail(FormUserAttr):
    values = {'0012947358_processed': '(X)'}

    @staticmethod
    def nl_desc(option):
        return f"The user's VIA:_Certified Air Mail: {option}"

class Viceroy(FormUserAttr):
    values = {'0001239897_processed': '47% 53%'}

    @staticmethod
    def nl_desc(option):
        return f"The user's VICEROY: {option}"

class Volume(FormUserAttr):
    values = {'0011973451_processed': 'TBD'}

    @staticmethod
    def nl_desc(option):
        return f"The user's VOLUME:: {option}"

class VsCurrentYearIncrDecr(FormUserAttr):
    values = {'91104867_processed': '4,500) (10,000) (13,000) 27,500'}

    @staticmethod
    def nl_desc(option):
        return f"The user's VS. CURRENT YEAR (INCR.) DECR.: {option}"

class Verification(FormUserAttr):
    values = {'71341634_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Verification: {option}"

class VickiClark(FormUserAttr):
    values = {'11508234_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Vicki Clark: {option}"

class VoucherApproval(FormUserAttr):
    values = {'71341634_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Voucher Approval:: {option}"

class Warning(FormUserAttr):
    values = {'71190280_processed': 'Exhibt 1(a) Statement A', '71366499_processed': '3A 14 1/2" X 8" - 116 sq."'}

    @staticmethod
    def nl_desc(option):
        return f"The user's WARNING: {option}"

class WereQuantitiesAppropriate(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's WERE QUANTITIES APPROPRIATE?: {option}"

class WereQuantitiesAppropriateNo(FormUserAttr):
    values = {'92094746_processed': '', '92094751_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's WERE QUANTITIES APPROPRIATE?_NO*: {option}"

class WereQuantitiesAppropriateYes(FormUserAttr):
    values = {'92094746_processed': 'x', '92094751_processed': 'X'}

    @staticmethod
    def nl_desc(option):
        return f"The user's WERE QUANTITIES APPROPRIATE?_YES: {option}"

class WinstonSalem(FormUserAttr):
    values = {'716552_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's WINSTON SALEM: {option}"

class WorkRequestedBy(FormUserAttr):
    values = {'0011856542_processed': 'Marketing', '0060007216_processed': 'R. S. Sprinkle, III', '0071032807_processed': 'Marketing'}

    @staticmethod
    def nl_desc(option):
        return f"The user's WORK REQUESTED BY: {option}"

class Writer(FormUserAttr):
    values = {'0013255595_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's WRITER:: {option}"

class WaterTreatment(FormUserAttr):
    values = {'0060024314_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Water Treatment:: {option}"

class Wave(FormUserAttr):
    values = {'71202511_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wave: {option}"

class WaveS(FormUserAttr):
    values = {'11508234_processed': '3/ 31/ 95', '71202511_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wave(s): {option}"

class WavesS(FormUserAttr):
    values = {'11508234_processed': '3/ 25/ 95'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Waves(s): {option}"

class WeHerebyCertifyChargesShownAboveOnDatesPerAttachedBillAreTrueAndCorrectAsBilledToTheAccountInUpperRightHandCornerOfTheAffidavitAndAreExclusive(FormUserAttr):
    values = {'91581919_processed': 'New Albany'}

    @staticmethod
    def nl_desc(option):
        return f"The user's We hereby certify charges shown above on dates per attached bill are true and correct as billed to the account in upper right hand corner of the affidavit and are exclusive: {option}"

class WeekOf(FormUserAttr):
    values = {'0060000813_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Week of:: {option}"

class Weight(FormUserAttr):
    values = {'0060094595_processed': '1 .089 1 .106 1 .111 1 .132', '01122115_processed': '.922 1 .059 .54 .20 20 .2 7 .6 62 .4 1 .07 .41 61 .7', '81574683_processed': '81.0 g/100'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Weight: {option}"

class Weights(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Weights: {option}"

class WeightsNetNetTobacco(FormUserAttr):
    values = {'0000989556_processed': '749 mg', '0001456787_processed': "['858 mg', '858 mg']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Weights_Net Net Tobacco: {option}"

class WeightsNetTobRodDensity(FormUserAttr):
    values = {'0000989556_processed': '245 mg/cc'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Weights_Net Tob. Rod Density: {option}"

class WeightsTobaccoRodDensity(FormUserAttr):
    values = {'0001456787_processed': "['243.6 mg/ ', '243.6 mg/ cc']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Weights_Tobacco Rod Density: {option}"

class WeightsTotalCigaretteWeight(FormUserAttr):
    values = {'0001456787_processed': "['mg', 'mg']"}

    @staticmethod
    def nl_desc(option):
        return f"The user's Weights_Total Cigarette Weight: {option}"

class WeightsTotalCigtWt(FormUserAttr):
    values = {'0000989556_processed': '974 mg'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Weights_Total Cigt. Wt.: {option}"

class WetWeight(FormUserAttr):
    values = {'01122115_processed': '99 .2 gms.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wet Weight: {option}"

class WidthOfBand(FormUserAttr):
    values = {'01122115_processed': 'Good'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Width of Band: {option}"

class WithinAgencySBudget(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Within Agency's Budget: {option}"

class Wrapping(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wrapping: {option}"

class WrappingCartons(FormUserAttr):
    values = {'81574683_processed': 'white'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wrapping_Cartons: {option}"

class WrappingClosures(FormUserAttr):
    values = {'81574683_processed': 'blue'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wrapping_Closures: {option}"

class WrappingLabels(FormUserAttr):
    values = {'81574683_processed': 'white'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wrapping_Labels: {option}"

class WrappingMarkings(FormUserAttr):
    values = {'81574683_processed': 'code #1746'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wrapping_Markings: {option}"

class WrappingTearTape(FormUserAttr):
    values = {'81574683_processed': 'white'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wrapping_Tear Tape: {option}"

class Wrappings(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wrappings:: {option}"

class WrappingsCartons(FormUserAttr):
    values = {'00283813_processed': 'OLD GOLD STRAIGHT'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wrappings:_Cartons: {option}"

class WrappingsClosures(FormUserAttr):
    values = {'00283813_processed': 'Standard Blue'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wrappings:_Closures: {option}"

class WrappingsLabels(FormUserAttr):
    values = {'00283813_processed': 'OLD GOLD STRAIGHT'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wrappings:_Labels: {option}"

class WrappingsMarkings(FormUserAttr):
    values = {'00283813_processed': 'Sample number on each pack and carton'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wrappings:_Markings: {option}"

class WrappingsTearTape(FormUserAttr):
    values = {'00283813_processed': 'Gold'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wrappings:_Tear Tape: {option}"

class WrittenBy(FormUserAttr):
    values = {'660978_processed': 'P. Hendricks'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Written by:: {option}"

class WtOfCigarettes4Oz(FormUserAttr):
    values = {'01122115_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Wt. of Cigarettes /4 oz.: {option}"

class Yea(FormUserAttr):
    values = {'0011505151_processed': '9.442'}

    @staticmethod
    def nl_desc(option):
        return f"The user's YEA -: {option}"

class Year(FormUserAttr):
    values = {'0011906503_processed': '1990 1991 1992 1993 Beyond 1993', '01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's YEAR: {option}"

class YearFive(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's YEAR FIVE: {option}"

class YearFour(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's YEAR FOUR: {option}"

class YearOne(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's YEAR ONE: {option}"

class YearThree(FormUserAttr):
    values = {'01408099_01408101_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's YEAR THREE: {option}"

class Yr(FormUserAttr):
    values = {'0011906503_processed': '88'}

    @staticmethod
    def nl_desc(option):
        return f"The user's Yr.: {option}"

class Zip(FormUserAttr):
    values = {'88057519_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Zip: {option}"

class ZipCode(FormUserAttr):
    values = {'71341634_processed': '', '87682908_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's Zip Code: {option}"

class Advertisements(FormUserAttr):
    values = {'91581919_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's advertisements.: {option}"

class apping(FormUserAttr):
    values = {}

    @staticmethod
    def nl_desc(option):
        return f"The user's apping: {option}"

class AppingCartons(FormUserAttr):
    values = {'00093726_processed': '"'}

    @staticmethod
    def nl_desc(option):
        return f"The user's apping_Cartons: {option}"

class AppingClosures(FormUserAttr):
    values = {'00093726_processed': 'Blue'}

    @staticmethod
    def nl_desc(option):
        return f"The user's apping_Closures: {option}"

class AppingLabels(FormUserAttr):
    values = {'00093726_processed': 'White'}

    @staticmethod
    def nl_desc(option):
        return f"The user's apping_Labels: {option}"

class AppingMarkings(FormUserAttr):
    values = {'00093726_processed': 'Sample No. on overwrap'}

    @staticmethod
    def nl_desc(option):
        return f"The user's apping_Markings: {option}"

class AppingTearRape(FormUserAttr):
    values = {'00093726_processed': 'White'}

    @staticmethod
    def nl_desc(option):
        return f"The user's apping_Tear rape: {option}"

class AsFollows(FormUserAttr):
    values = {'91581919_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's as follows:: {option}"

class BpMp(FormUserAttr):
    values = {'81310636_processed': 'N/ A'}

    @staticmethod
    def nl_desc(option):
        return f"The user's bp/mp : {option}"

class by(FormUserAttr):
    values = {'0060036622_processed': '', '0060077689_processed': '', '0060214859_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's by: {option}"

class Cc(FormUserAttr):
    values = {'0001463282_processed': 'S. Willinger (3) K. A. Hutchison S. A. Howard', '0011838621_processed': 'MRA File N. W. Kremer MRA File N. W. Kremer', '0011856542_processed': 'RSS RDC PHL PRC DRB Records Project Leader Other Personnel Assigned', '0012529284_processed': 'S. Willinger (3) G. D. Raphael V. Hansberry (If Int.)', '0012529295_processed': 'S. Willinger (3) G. D. Raphael V. Hansberry (If Int.)', '0012602424_processed': 'S. WILLINGER (3) ☑ RESEARCH GROUP MANAGER', '0060007216_processed': 'RSS RDC PHL PRC BMC Records Project Leader Other Personnel Assigned', '0071032790_processed': 'BMC/RMI/EPB JEM/DEC PRC/DRB', '11508234_processed': 'H. Williams', '12603270_processed': 'Research Group Manager Bonnie Fuller V. Hansberry (If International)', '660978_processed': 'R. Schoenfein S. Dammers P. Hendricks', '71202511_processed': 'MaDonna Sliker', '87533049_processed': 'R. G. Ryan ', '91355841_processed': 'A. H. TISCH R. H. ORCUTT M. A. PETERSON M. L. ORLOWSKY L. GORDON J. P. MASTANDREA G. R. TELFORD R. G. RYAN N. P. RUFFALO T. L. ACHEY P. J. McCANN A. J. GIACOIO J. J. TATULLI L. H. KERSH J. R. SLATER S. T. JONES R. S. GOLDBRENNER N. SIMEONIDIS S. F. SMITH', '91372360_processed': 'Mr. R. B. Spell Mr. S. L. Enloe', '91391286_processed': 'T. BAYLIES, L GIORDANO, V. LINDSLEY, M. MCGLYNN, S RAPISARLDI,', '91391310_processed': 'T. BAYLIES, L. GIORDANO V. LINDSLEY, J. SCHNEFF, S. RAPISARLDI, N, DISCENZA E LUNDBERG', '91914407_processed': 'R. E. KLEIN', '91974562_processed': 'D. WEST, L. GIORDANO, V. LINDSLEY, A. SADOVNICK S. RAPISARLDI B. DAVIN. A. Pasheluk', '92091873_processed': 'R. P. Bonomo', '92657391_processed': 'R. B. Spell A. J. Giacoio P. J. McCann S. L. Enloe T. L. Achey', '93329540_processed': 'A. H. Tisch R. H. Orcutt M. A. Peterson M. L. Orlowsky L. Gordon G. Telford V. Norman A. W. Spears A. J. Giacoio N. P. Ruffalo T. L. Achey R. B. Spell P. J. McCann J. J. Tatulli L. H. Kersh J. R. Slater A. Pasheluk R. S. Goldbrenner N. Simeonidis S. F. Smith K. P. Augustyn V. D. Lindsley R. C. Bondy R. D. Hammer', '93351929_93351931_processed': 'K. AUGUSTYN. L. GIORDANO, M. McGLYNN, S. RAPISARLDI', '93380187_processed': 'S. A. RAPISARLDI J BAYLIES K. P. AUGUSTYN M. McGLYNN', '93455715_processed': 'Mr. J. R. Ave Mr. R. H. Orcutt Mr. M. A. Peterson Mr. T. H. Mau Ms. S. Ridgway Mr. J. P. Mastandrea Mr. L. Gordon Mr. G. R. Telford Dr. S. T. Jones Mr. C. Toti Mr. N. P. Ruffalo Mr. T. L. Achey P. J. McCann Mr. A. J. Giacoio Mr. L. H. Kersh Mr. R. G. Ryan Mr. P. A. Lawless Mr. J. E. Daghlian Mr. R. S. Goldbrenner Ms. E. R. Harrow Ms. S. F. Smith'}

    @staticmethod
    def nl_desc(option):
        return f"The user's cc:: {option}"

class CheckApplicableBoxEs(FormUserAttr):
    values = {'92586242_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's check applicable box(es): {option}"

class CtionToLitmus(FormUserAttr):
    values = {'0060094595_processed': 'Basic Basic Basic Basic'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ction to Litmus: {option}"

class DayOf(FormUserAttr):
    values = {'91581919_processed': 'March ,1988'}

    @staticmethod
    def nl_desc(option):
        return f"The user's day of: {option}"

class Dimensions(FormUserAttr):
    values = {'0060007216_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's dimensions:: {option}"

class Explain(FormUserAttr):
    values = {'0001477983_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's explain):: {option}"

class GinalRequestMadeBy(FormUserAttr):
    values = {'81574683_processed': 'T. Jessup on 2/13/84'}

    @staticmethod
    def nl_desc(option):
        return f"The user's ginal Request Made By: {option}"

class LobbyistForLobbyingYesOrNo(FormUserAttr):
    values = {'0001477983_processed': 'No.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's lobbyist for lobbying? (yes or no): {option}"

class MmHg(FormUserAttr):
    values = {'81310636_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's mm Hg: {option}"

class OfTheAbovementionedNewspaperAndThatDisplayAdsForTheAboveAccountWereMadeThroughTheAforesaidNewspaperDuring(FormUserAttr):
    values = {'91581919_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's of the abovementioned newspaper and that display ads for the above account were made through the aforesaid newspaper during: {option}"

class on(FormUserAttr):
    values = {'00093726_processed': 'September 21, 1976', '00283813_processed': '7/ 10/ 68'}

    @staticmethod
    def nl_desc(option):
        return f"The user's on: {option}"

class pH(FormUserAttr):
    values = {'00836816_processed': 'The pH of a 50 % concentration of A30 in (52.6% dioxane/ water was calculated to be 8.13 at 24 C according to the extrapolation procedures by Dr. P. D. Schickedantz, Lorillard Research Center Accession Number 1662, Reference OR 83- 81.', '00865872_processed': 'The pH of a 50% concentration of B164 in water was calculated to be 4.82 at 25°C according to the extrapolation procedures by Dr. P. D. Schickedantz, Lorillard Research Center Accession Number 1662.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's pH: {option}"

class PagesLong(FormUserAttr):
    values = {'92657391_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's pages long.: {option}"

class resider(FormUserAttr):
    values = {'0060262650_processed': 'Dr. William J. Schull'}

    @staticmethod
    def nl_desc(option):
        return f"The user's resider: {option}"

class TheMonthOf(FormUserAttr):
    values = {'91581919_processed': 'January ,1988'}

    @staticmethod
    def nl_desc(option):
        return f"The user's the month of: {option}"

class ToBePerformedInAcuteDermalToxicologyBuilding18(FormUserAttr):
    values = {'00860012_00860014_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's to be performed in Acute /Dermal Toxicology, building 18.: {option}"

class WeightedAsFollows(FormUserAttr):
    values = {'71563825_processed': 'Alternate 60%, Regular 40%.'}

    @staticmethod
    def nl_desc(option):
        return f"The user's weighted as follows:: {option}"

class WhoBeingDulySwornSaysThatHeSheIs(FormUserAttr):
    values = {'91581919_processed': 'Bookkeeper'}

    @staticmethod
    def nl_desc(option):
        return f"The user's who being duly sworn, says that (he) (she) is: {option}"

class YesPleaseDetailIncludingTheNamesOfThePersonsReceivingAndInWhoseBehalfSuchExpendituresHaveBeenMadeTheAmountDatePlaceAndReasonForTheExpenditure(FormUserAttr):
    values = {'0001477983_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's yes, please detail. including the names of the persons receiving and in whose behalf such expenditures have been made, the amount, date, place, and reason for the expenditure.: {option}"

class FieldCorrected(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ☐ CORRECTED: {option}"

class FieldDecreaseRevenues(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ☐ Decrease Revenues: {option}"

class FieldIncreaseRevenues(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ☐ Increase Revenues: {option}"

class FieldMandatory(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ☐ Mandatory: {option}"

class FieldMembership(FormUserAttr):
    values = {'0060036622_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ☐ Membership: {option}"

class FieldPurchasing(FormUserAttr):
    values = {'00920222_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ☐ PURCHASING: {option}"

class FieldPermissive(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ☐ Permissive: {option}"

class FieldStationary(FormUserAttr):
    values = {'00920222_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ☐ STATIONARY: {option}"

class FieldSupplemental(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ☐ SUPPLEMENTAL: {option}"

class FieldUpdated(FormUserAttr):
    values = {'13149651_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ☐ UPDATED: {option}"

class FieldCombined(FormUserAttr):
    values = {'00851772_1780_processed': ''}

    @staticmethod
    def nl_desc(option):
        return f"The user's ☑_COMBINED: {option}"

