# pylint: disable=too-many-lines
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from enum import Enum
from ._generated.models import LanguageInput, MultiLanguageInput


class EntityAssociation(str, Enum):
    """Describes if the entity is the subject of the text or if it describes someone else."""

    SUBJECT = "subject"
    OTHER = "other"


class EntityCertainty(str, Enum):
    """Describes the entities certainty and polarity."""

    POSITIVE = "positive"
    POSITIVE_POSSIBLE = "positivePossible"
    NEUTRAL_POSSIBLE = "neutralPossible"
    NEGATIVE_POSSIBLE = "negativePossible"
    NEGATIVE = "negative"


class EntityConditionality(str, Enum):
    """Describes any conditionality on the entity."""

    HYPOTHETICAL = "hypothetical"
    CONDITIONAL = "conditional"


class HealthcareEntityRelation(str, Enum):
    """Type of relation. Examples include: 'DosageOfMedication' or 'FrequencyOfMedication', etc."""

    ABBREVIATION = "Abbreviation"
    DIRECTION_OF_BODY_STRUCTURE = "DirectionOfBodyStructure"
    DIRECTION_OF_CONDITION = "DirectionOfCondition"
    DIRECTION_OF_EXAMINATION = "DirectionOfExamination"
    DIRECTION_OF_TREATMENT = "DirectionOfTreatment"
    DOSAGE_OF_MEDICATION = "DosageOfMedication"
    FORM_OF_MEDICATION = "FormOfMedication"
    FREQUENCY_OF_MEDICATION = "FrequencyOfMedication"
    FREQUENCY_OF_TREATMENT = "FrequencyOfTreatment"
    QUALIFIER_OF_CONDITION = "QualifierOfCondition"
    RELATION_OF_EXAMINATION = "RelationOfExamination"
    ROUTE_OF_MEDICATION = "RouteOfMedication"
    TIME_OF_CONDITION = "TimeOfCondition"
    TIME_OF_EVENT = "TimeOfEvent"
    TIME_OF_EXAMINATION = "TimeOfExamination"
    TIME_OF_MEDICATION = "TimeOfMedication"
    TIME_OF_TREATMENT = "TimeOfTreatment"
    UNIT_OF_CONDITION = "UnitOfCondition"
    UNIT_OF_EXAMINATION = "UnitOfExamination"
    VALUE_OF_CONDITION = "ValueOfCondition"
    VALUE_OF_EXAMINATION = "ValueOfExamination"


class PiiEntityCategory(str, Enum):
    """Categories of Personally Identifiable Information (PII)."""

    ABA_ROUTING_NUMBER = "ABARoutingNumber"
    AR_NATIONAL_IDENTITY_NUMBER = "ARNationalIdentityNumber"
    AU_BANK_ACCOUNT_NUMBER = "AUBankAccountNumber"
    AU_DRIVERS_LICENSE_NUMBER = "AUDriversLicenseNumber"
    AU_MEDICAL_ACCOUNT_NUMBER = "AUMedicalAccountNumber"
    AU_PASSPORT_NUMBER = "AUPassportNumber"
    AU_TAX_FILE_NUMBER = "AUTaxFileNumber"
    AU_BUSINESS_NUMBER = "AUBusinessNumber"
    AU_COMPANY_NUMBER = "AUCompanyNumber"
    AT_IDENTITY_CARD = "ATIdentityCard"
    AT_TAX_IDENTIFICATION_NUMBER = "ATTaxIdentificationNumber"
    AT_VALUE_ADDED_TAX_NUMBER = "ATValueAddedTaxNumber"
    AZURE_DOCUMENT_DB_AUTH_KEY = "AzureDocumentDBAuthKey"
    AZURE_IAAS_DATABASE_CONNECTION_AND_SQL_STRING = (
        "AzureIAASDatabaseConnectionAndSQLString"
    )
    AZURE_IO_T_CONNECTION_STRING = "AzureIoTConnectionString"
    AZURE_PUBLISH_SETTING_PASSWORD = "AzurePublishSettingPassword"
    AZURE_REDIS_CACHE_STRING = "AzureRedisCacheString"
    AZURE_SAS = "AzureSAS"
    AZURE_SERVICE_BUS_STRING = "AzureServiceBusString"
    AZURE_STORAGE_ACCOUNT_KEY = "AzureStorageAccountKey"
    AZURE_STORAGE_ACCOUNT_GENERIC = "AzureStorageAccountGeneric"
    BE_NATIONAL_NUMBER = "BENationalNumber"
    BE_NATIONAL_NUMBER_V2 = "BENationalNumberV2"
    BE_VALUE_ADDED_TAX_NUMBER = "BEValueAddedTaxNumber"
    BRCPF_NUMBER = "BRCPFNumber"
    BR_LEGAL_ENTITY_NUMBER = "BRLegalEntityNumber"
    BR_NATIONAL_IDRG = "BRNationalIDRG"
    BG_UNIFORM_CIVIL_NUMBER = "BGUniformCivilNumber"
    CA_BANK_ACCOUNT_NUMBER = "CABankAccountNumber"
    CA_DRIVERS_LICENSE_NUMBER = "CADriversLicenseNumber"
    CA_HEALTH_SERVICE_NUMBER = "CAHealthServiceNumber"
    CA_PASSPORT_NUMBER = "CAPassportNumber"
    CA_PERSONAL_HEALTH_IDENTIFICATION = "CAPersonalHealthIdentification"
    CA_SOCIAL_INSURANCE_NUMBER = "CASocialInsuranceNumber"
    CL_IDENTITY_CARD_NUMBER = "CLIdentityCardNumber"
    CN_RESIDENT_IDENTITY_CARD_NUMBER = "CNResidentIdentityCardNumber"
    CREDIT_CARD_NUMBER = "CreditCardNumber"
    HR_IDENTITY_CARD_NUMBER = "HRIdentityCardNumber"
    HR_NATIONAL_ID_NUMBER = "HRNationalIDNumber"
    HR_PERSONAL_IDENTIFICATION_NUMBER = "HRPersonalIdentificationNumber"
    HR_PERSONAL_IDENTIFICATION_OIB_NUMBER_V2 = "HRPersonalIdentificationOIBNumberV2"
    CY_IDENTITY_CARD = "CYIdentityCard"
    CY_TAX_IDENTIFICATION_NUMBER = "CYTaxIdentificationNumber"
    CZ_PERSONAL_IDENTITY_NUMBER = "CZPersonalIdentityNumber"
    CZ_PERSONAL_IDENTITY_V2 = "CZPersonalIdentityV2"
    DK_PERSONAL_IDENTIFICATION_NUMBER = "DKPersonalIdentificationNumber"
    DK_PERSONAL_IDENTIFICATION_V2 = "DKPersonalIdentificationV2"
    DRUG_ENFORCEMENT_AGENCY_NUMBER = "DrugEnforcementAgencyNumber"
    EE_PERSONAL_IDENTIFICATION_CODE = "EEPersonalIdentificationCode"
    EU_DEBIT_CARD_NUMBER = "EUDebitCardNumber"
    EU_DRIVERS_LICENSE_NUMBER = "EUDriversLicenseNumber"
    EUGPS_COORDINATES = "EUGPSCoordinates"
    EU_NATIONAL_IDENTIFICATION_NUMBER = "EUNationalIdentificationNumber"
    EU_PASSPORT_NUMBER = "EUPassportNumber"
    EU_SOCIAL_SECURITY_NUMBER = "EUSocialSecurityNumber"
    EU_TAX_IDENTIFICATION_NUMBER = "EUTaxIdentificationNumber"
    FI_EUROPEAN_HEALTH_NUMBER = "FIEuropeanHealthNumber"
    FI_NATIONAL_ID = "FINationalID"
    FI_NATIONAL_IDV2 = "FINationalIDV2"
    FI_PASSPORT_NUMBER = "FIPassportNumber"
    FR_DRIVERS_LICENSE_NUMBER = "FRDriversLicenseNumber"
    FR_HEALTH_INSURANCE_NUMBER = "FRHealthInsuranceNumber"
    FR_NATIONAL_ID = "FRNationalID"
    FR_PASSPORT_NUMBER = "FRPassportNumber"
    FR_SOCIAL_SECURITY_NUMBER = "FRSocialSecurityNumber"
    FR_TAX_IDENTIFICATION_NUMBER = "FRTaxIdentificationNumber"
    FR_VALUE_ADDED_TAX_NUMBER = "FRValueAddedTaxNumber"
    DE_DRIVERS_LICENSE_NUMBER = "DEDriversLicenseNumber"
    DE_PASSPORT_NUMBER = "DEPassportNumber"
    DE_IDENTITY_CARD_NUMBER = "DEIdentityCardNumber"
    DE_TAX_IDENTIFICATION_NUMBER = "DETaxIdentificationNumber"
    DE_VALUE_ADDED_NUMBER = "DEValueAddedNumber"
    GR_NATIONAL_ID_CARD = "GRNationalIDCard"
    GR_NATIONAL_IDV2 = "GRNationalIDV2"
    GR_TAX_IDENTIFICATION_NUMBER = "GRTaxIdentificationNumber"
    HK_IDENTITY_CARD_NUMBER = "HKIdentityCardNumber"
    HU_VALUE_ADDED_NUMBER = "HUValueAddedNumber"
    HU_PERSONAL_IDENTIFICATION_NUMBER = "HUPersonalIdentificationNumber"
    HU_TAX_IDENTIFICATION_NUMBER = "HUTaxIdentificationNumber"
    IN_PERMANENT_ACCOUNT = "INPermanentAccount"
    IN_UNIQUE_IDENTIFICATION_NUMBER = "INUniqueIdentificationNumber"
    ID_IDENTITY_CARD_NUMBER = "IDIdentityCardNumber"
    INTERNATIONAL_BANKING_ACCOUNT_NUMBER = "InternationalBankingAccountNumber"
    IE_PERSONAL_PUBLIC_SERVICE_NUMBER = "IEPersonalPublicServiceNumber"
    IE_PERSONAL_PUBLIC_SERVICE_NUMBER_V2 = "IEPersonalPublicServiceNumberV2"
    IL_BANK_ACCOUNT_NUMBER = "ILBankAccountNumber"
    IL_NATIONAL_ID = "ILNationalID"
    IT_DRIVERS_LICENSE_NUMBER = "ITDriversLicenseNumber"
    IT_FISCAL_CODE = "ITFiscalCode"
    IT_VALUE_ADDED_TAX_NUMBER = "ITValueAddedTaxNumber"
    JP_BANK_ACCOUNT_NUMBER = "JPBankAccountNumber"
    JP_DRIVERS_LICENSE_NUMBER = "JPDriversLicenseNumber"
    JP_PASSPORT_NUMBER = "JPPassportNumber"
    JP_RESIDENT_REGISTRATION_NUMBER = "JPResidentRegistrationNumber"
    JP_SOCIAL_INSURANCE_NUMBER = "JPSocialInsuranceNumber"
    JP_MY_NUMBER_CORPORATE = "JPMyNumberCorporate"
    JP_MY_NUMBER_PERSONAL = "JPMyNumberPersonal"
    JP_RESIDENCE_CARD_NUMBER = "JPResidenceCardNumber"
    LV_PERSONAL_CODE = "LVPersonalCode"
    LT_PERSONAL_CODE = "LTPersonalCode"
    LU_NATIONAL_IDENTIFICATION_NUMBER_NATURAL = "LUNationalIdentificationNumberNatural"
    LU_NATIONAL_IDENTIFICATION_NUMBER_NON_NATURAL = (
        "LUNationalIdentificationNumberNonNatural"
    )
    MY_IDENTITY_CARD_NUMBER = "MYIdentityCardNumber"
    MT_IDENTITY_CARD_NUMBER = "MTIdentityCardNumber"
    MT_TAX_ID_NUMBER = "MTTaxIDNumber"
    NL_CITIZENS_SERVICE_NUMBER = "NLCitizensServiceNumber"
    NL_CITIZENS_SERVICE_NUMBER_V2 = "NLCitizensServiceNumberV2"
    NL_TAX_IDENTIFICATION_NUMBER = "NLTaxIdentificationNumber"
    NL_VALUE_ADDED_TAX_NUMBER = "NLValueAddedTaxNumber"
    NZ_BANK_ACCOUNT_NUMBER = "NZBankAccountNumber"
    NZ_DRIVERS_LICENSE_NUMBER = "NZDriversLicenseNumber"
    NZ_INLAND_REVENUE_NUMBER = "NZInlandRevenueNumber"
    NZ_MINISTRY_OF_HEALTH_NUMBER = "NZMinistryOfHealthNumber"
    NZ_SOCIAL_WELFARE_NUMBER = "NZSocialWelfareNumber"
    NO_IDENTITY_NUMBER = "NOIdentityNumber"
    PH_UNIFIED_MULTI_PURPOSE_ID_NUMBER = "PHUnifiedMultiPurposeIDNumber"
    PL_IDENTITY_CARD = "PLIdentityCard"
    PL_NATIONAL_ID = "PLNationalID"
    PL_NATIONAL_IDV2 = "PLNationalIDV2"
    PL_PASSPORT_NUMBER = "PLPassportNumber"
    PL_TAX_IDENTIFICATION_NUMBER = "PLTaxIdentificationNumber"
    PLREGON_NUMBER = "PLREGONNumber"
    PT_CITIZEN_CARD_NUMBER = "PTCitizenCardNumber"
    PT_CITIZEN_CARD_NUMBER_V2 = "PTCitizenCardNumberV2"
    PT_TAX_IDENTIFICATION_NUMBER = "PTTaxIdentificationNumber"
    RO_PERSONAL_NUMERICAL_CODE = "ROPersonalNumericalCode"
    RU_PASSPORT_NUMBER_DOMESTIC = "RUPassportNumberDomestic"
    RU_PASSPORT_NUMBER_INTERNATIONAL = "RUPassportNumberInternational"
    SA_NATIONAL_ID = "SANationalID"
    SG_NATIONAL_REGISTRATION_IDENTITY_CARD_NUMBER = (
        "SGNationalRegistrationIdentityCardNumber"
    )
    SK_PERSONAL_NUMBER = "SKPersonalNumber"
    SI_TAX_IDENTIFICATION_NUMBER = "SITaxIdentificationNumber"
    SI_UNIQUE_MASTER_CITIZEN_NUMBER = "SIUniqueMasterCitizenNumber"
    ZA_IDENTIFICATION_NUMBER = "ZAIdentificationNumber"
    KR_RESIDENT_REGISTRATION_NUMBER = "KRResidentRegistrationNumber"
    ESDNI = "ESDNI"
    ES_SOCIAL_SECURITY_NUMBER = "ESSocialSecurityNumber"
    ES_TAX_IDENTIFICATION_NUMBER = "ESTaxIdentificationNumber"
    SQL_SERVER_CONNECTION_STRING = "SQLServerConnectionString"
    SE_NATIONAL_ID = "SENationalID"
    SE_NATIONAL_IDV2 = "SENationalIDV2"
    SE_PASSPORT_NUMBER = "SEPassportNumber"
    SE_TAX_IDENTIFICATION_NUMBER = "SETaxIdentificationNumber"
    SWIFT_CODE = "SWIFTCode"
    CH_SOCIAL_SECURITY_NUMBER = "CHSocialSecurityNumber"
    TW_NATIONAL_ID = "TWNationalID"
    TW_PASSPORT_NUMBER = "TWPassportNumber"
    TW_RESIDENT_CERTIFICATE = "TWResidentCertificate"
    TH_POPULATION_IDENTIFICATION_CODE = "THPopulationIdentificationCode"
    TR_NATIONAL_IDENTIFICATION_NUMBER = "TRNationalIdentificationNumber"
    UK_DRIVERS_LICENSE_NUMBER = "UKDriversLicenseNumber"
    UK_ELECTORAL_ROLL_NUMBER = "UKElectoralRollNumber"
    UK_NATIONAL_HEALTH_NUMBER = "UKNationalHealthNumber"
    UK_NATIONAL_INSURANCE_NUMBER = "UKNationalInsuranceNumber"
    UK_UNIQUE_TAXPAYER_NUMBER = "UKUniqueTaxpayerNumber"
    USUK_PASSPORT_NUMBER = "USUKPassportNumber"
    US_BANK_ACCOUNT_NUMBER = "USBankAccountNumber"
    US_DRIVERS_LICENSE_NUMBER = "USDriversLicenseNumber"
    US_INDIVIDUAL_TAXPAYER_IDENTIFICATION = "USIndividualTaxpayerIdentification"
    US_SOCIAL_SECURITY_NUMBER = "USSocialSecurityNumber"
    UA_PASSPORT_NUMBER_DOMESTIC = "UAPassportNumberDomestic"
    UA_PASSPORT_NUMBER_INTERNATIONAL = "UAPassportNumberInternational"
    ORGANIZATION = "Organization"
    EMAIL = "Email"
    URL = "URL"
    AGE = "Age"
    PHONE_NUMBER = "PhoneNumber"
    IP_ADDRESS = "IPAddress"
    DATE = "Date"
    PERSON = "Person"
    ADDRESS = "Address"
    ALL = "All"
    DEFAULT = "Default"


class HealthcareEntityCategory(str, Enum):
    """Healthcare Entity Category."""

    BODY_STRUCTURE = "BodyStructure"
    AGE = "Age"
    GENDER = "Gender"
    EXAMINATION_NAME = "ExaminationName"
    DATE = "Date"
    DIRECTION = "Direction"
    FREQUENCY = "Frequency"
    MEASUREMENT_VALUE = "MeasurementValue"
    MEASUREMENT_UNIT = "MeasurementUnit"
    RELATIONAL_OPERATOR = "RelationalOperator"
    TIME = "Time"
    GENE_OR_PROTEIN = "GeneOrProtein"
    VARIANT = "Variant"
    ADMINISTRATIVE_EVENT = "AdministrativeEvent"
    CARE_ENVIRONMENT = "CareEnvironment"
    HEALTHCARE_PROFESSION = "HealthcareProfession"
    DIAGNOSIS = "Diagnosis"
    SYMPTOM_OR_SIGN = "SymptomOrSign"
    CONDITION_QUALIFIER = "ConditionQualifier"
    MEDICATION_CLASS = "MedicationClass"
    MEDICATION_NAME = "MedicationName"
    DOSAGE = "Dosage"
    MEDICATION_FORM = "MedicationForm"
    MEDICATION_ROUTE = "MedicationRoute"
    FAMILY_RELATION = "FamilyRelation"
    TREATMENT_NAME = "TreatmentName"


class PiiEntityDomain(str, Enum):
    """The different domains of PII entities that users can filter by"""

    PROTECTED_HEALTH_INFORMATION = (
        "phi"  # See https://aka.ms/tanerpii for more information.
    )


class DetectedLanguage:
    """DetectedLanguage contains the predicted language found in text,
    its confidence score, and its ISO 639-1 representation.

    :ivar name: Long name of a detected language (e.g. English,
        French).
    :vartype name: str
    :ivar iso6391_name: A two letter representation of the detected
        language according to the ISO 639-1 standard (e.g. en, fr).
    :vartype iso6391_name: str
    :ivar confidence_score: A confidence score between 0 and 1. Scores close
        to 1 indicate 100% certainty that the identified language is true.
    :vartype confidence_score: float
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.iso6391_name = kwargs.get("iso6391_name", None)
        self.confidence_score = kwargs.get("confidence_score", None)


class RecognizeEntitiesResult:
    """RecognizeEntitiesResult is a result object which contains
    the recognized entities from a particular document.

    :ivar id: Unique, non-empty document identifier that matches the
        document id that was passed in with the request. If not specified
        in the request, an id is assigned for the document.
    :vartype id: str
    :ivar entities: Recognized entities in the document.
    :vartype entities:
        list[~azure.ai.textanalytics.CategorizedEntity]
    :ivar warnings: Warnings encountered while processing document. Results will still be returned
        if there are warnings, but they may not be fully accurate.
    :vartype warnings: list[~azure.ai.textanalytics.TextAnalyticsWarning]
    :ivar statistics: If `show_stats=True` was specified in the request this
        field will contain information about the document payload.
    :vartype statistics:
        ~azure.ai.textanalytics.TextDocumentStatistics
    :ivar str detected_language: If 'language' is set to 'auto' for the document in the request this
         field will contain a 2 letter ISO 639-1 representation of the language detected for this
         document.
    :ivar bool is_error: Boolean check for error item when iterating over list of
        results. Always False for an instance of a RecognizeEntitiesResult.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.entities = kwargs.get("entities", None)
        self.warnings = kwargs.get("warnings", [])
        self.statistics = kwargs.get("statistics", None)
        self.detected_language = kwargs.get("detected_language", None)
        self.is_error = False


class RecognizePiiEntitiesResult:
    """RecognizePiiEntitiesResult is a result object which contains
    the recognized Personally Identifiable Information (PII) entities
    from a particular document.

    :ivar str id: Unique, non-empty document identifier that matches the
        document id that was passed in with the request. If not specified
        in the request, an id is assigned for the document.
    :ivar entities: Recognized PII entities in the document.
    :vartype entities:
        list[~azure.ai.textanalytics.PiiEntity]
    :ivar str redacted_text: Returns the text of the input document with all of the PII information
        redacted out.
    :ivar warnings: Warnings encountered while processing document. Results will still be returned
        if there are warnings, but they may not be fully accurate.
    :vartype warnings: list[~azure.ai.textanalytics.TextAnalyticsWarning]
    :ivar statistics: If `show_stats=True` was specified in the request this
        field will contain information about the document payload.
    :vartype statistics:
        ~azure.ai.textanalytics.TextDocumentStatistics
    :ivar str detected_language: If 'language' is set to 'auto' for the document in the request this
         field will contain a 2 letter ISO 639-1 representation of the language detected for this
         document.
    :ivar bool is_error: Boolean check for error item when iterating over list of
        results. Always False for an instance of a RecognizePiiEntitiesResult.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.entities = kwargs.get("entities", None)
        self.redacted_text = kwargs.get("redacted_text", None)
        self.warnings = kwargs.get("warnings", [])
        self.statistics = kwargs.get("statistics", None)
        self.detected_language = kwargs.get("detected_language", None)
        self.is_error = False


class AnalyzeHealthcareEntitiesResult:
    """
    AnalyzeHealthcareEntitiesResult contains the Healthcare entities from a
    particular document.

    :ivar str id: Unique, non-empty document identifier that matches the
        document id that was passed in with the request. If not specified
        in the request, an id is assigned for the document.
    :ivar entities: Identified Healthcare entities in the document, i.e. in
        the document "The subject took ibuprofen", "ibuprofen" is an identified entity
        from the document.
    :vartype entities:
        list[~azure.ai.textanalytics.HealthcareEntity]
    :ivar entity_relations: Identified Healthcare relations between entities. For example, in the
        document "The subject took 100mg of ibuprofen", we would identify the relationship
        between the dosage of 100mg and the medication ibuprofen.
    :vartype entity_relations: list[~azure.ai.textanalytics.HealthcareRelation]
    :ivar warnings: Warnings encountered while processing document. Results will still be returned
        if there are warnings, but they may not be fully accurate.
    :vartype warnings: list[~azure.ai.textanalytics.TextAnalyticsWarning]
    :ivar statistics: If show_stats=true was specified in the request this
        field will contain information about the document payload.
    :vartype statistics:
        ~azure.ai.textanalytics.TextDocumentStatistics
    :ivar str detected_language: If 'language' is set to 'auto' for the document in the request this
         field will contain a 2 letter ISO 639-1 representation of the language detected for this
         document.
    :ivar bool is_error: Boolean check for error item when iterating over list of
        results. Always False for an instance of a AnalyzeHealthcareEntitiesResult.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.entities = kwargs.get("entities", None)
        self.entity_relations = kwargs.get("entity_relations", None)
        self.warnings = kwargs.get("warnings", [])
        self.statistics = kwargs.get("statistics", None)
        self.detected_language = kwargs.get("detected_language", None)
        self.is_error = False


class HealthcareRelation:
    """HealthcareRelation is a result object which represents a relation detected in a document.

    Every HealthcareRelation is an entity graph of a certain relation type,
    where all entities are connected and have specific roles within the relation context.

    :ivar relation_type: The type of relation, i.e. the relationship between "100mg" and
        "ibuprofen" in the document "The subject took 100 mg of ibuprofen" is "DosageOfMedication".
        Possible values found in :class:`~azure.ai.textanalytics.HealthcareEntityRelation`
    :vartype relation_type: str
    :ivar roles: The roles present in this relation. I.e., in the document
        "The subject took 100 mg of ibuprofen", the present roles are "Dosage" and "Medication".
    :vartype roles: list[~azure.ai.textanalytics.HealthcareRelationRole]
    """

    def __init__(self, **kwargs):
        self.relation_type = kwargs.get("relation_type")
        self.roles = kwargs.get("roles")


class HealthcareRelationRole:
    """A model representing a role in a relation.

    For example, in "The subject took 100 mg of ibuprofen",
    "100 mg" is a dosage entity fulfilling the role "Dosage"
    in the extracted relation "DosageofMedication".

    :ivar name: The role of the entity in the relationship. I.e., in the relation
        "The subject took 100 mg of ibuprofen", the dosage entity "100 mg" has role
        "Dosage".
    :vartype name: str
    :ivar entity: The entity that is present in the relationship. For example, in
        "The subject took 100 mg of ibuprofen", this property holds the dosage entity
        of "100 mg".
    :vartype entity: ~azure.ai.textanalytics.HealthcareEntity
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.entity = kwargs.get("entity")


class DetectLanguageResult:
    """DetectLanguageResult is a result object which contains
    the detected language of a particular document.

    :ivar id: Unique, non-empty document identifier that matches the
        document id that was passed in with the request. If not specified
        in the request, an id is assigned for the document.
    :vartype id: str
    :ivar primary_language: The primary language detected in the document.
    :vartype primary_language: ~azure.ai.textanalytics.DetectedLanguage
    :ivar warnings: Warnings encountered while processing document. Results will still be returned
        if there are warnings, but they may not be fully accurate.
    :vartype warnings: list[~azure.ai.textanalytics.TextAnalyticsWarning]
    :ivar statistics: If `show_stats=True` was specified in the request this
        field will contain information about the document payload.
    :vartype statistics:
        ~azure.ai.textanalytics.TextDocumentStatistics
    :ivar bool is_error: Boolean check for error item when iterating over list of
        results. Always False for an instance of a DetectLanguageResult.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.primary_language = kwargs.get("primary_language", None)
        self.warnings = kwargs.get("warnings", [])
        self.statistics = kwargs.get("statistics", None)
        self.is_error = False


class CategorizedEntity:
    """CategorizedEntity contains information about a particular
    entity found in text.

    :ivar text: Entity text as appears in the request.
    :vartype text: str
    :ivar category: Entity category, such as Person/Location/Org/SSN etc
    :vartype category: str
    :ivar subcategory: Entity subcategory, such as Age/Year/TimeRange etc
    :vartype subcategory: str
    :ivar int length: The entity text length.  This value depends on the value of the
        `string_index_type` parameter set in the original request, which is UnicodeCodePoints
        by default.
    :ivar int offset: The entity text offset from the start of the document.
        The value depends on the value of the `string_index_type` parameter
        set in the original request, which is UnicodeCodePoints by default.
    :ivar confidence_score: Confidence score between 0 and 1 of the extracted
        entity.
    :vartype confidence_score: float

    .. versionadded:: v3.1
        The *offset* and *length* properties.
    """

    def __init__(self, **kwargs):
        self.text = kwargs.get("text", None)
        self.category = kwargs.get("category", None)
        self.subcategory = kwargs.get("subcategory", None)
        self.length = kwargs.get("length", None)
        self.offset = kwargs.get("offset", None)
        self.confidence_score = kwargs.get("confidence_score", None)


class PiiEntity:
    """PiiEntity contains information about a Personally Identifiable
    Information (PII) entity found in text.

    :ivar str text: Entity text as appears in the request.
    :ivar str category: Entity category, such as Financial Account
        Identification/Social Security Number/Phone Number, etc.
    :ivar str subcategory: Entity subcategory, such as Credit Card/EU
        Phone number/ABA Routing Numbers, etc.
    :ivar int length: The PII entity text length.  This value depends on the value
        of the `string_index_type` parameter specified in the original request, which
        is UnicodeCodePoints by default.
    :ivar int offset: The PII entity text offset from the start of the document.
        This value depends on the value of the `string_index_type` parameter specified
        in the original request, which is UnicodeCodePoints by default.
    :ivar float confidence_score: Confidence score between 0 and 1 of the extracted
        entity.
    """

    def __init__(self, **kwargs):
        self.text = kwargs.get("text", None)
        self.category = kwargs.get("category", None)
        self.subcategory = kwargs.get("subcategory", None)
        self.length = kwargs.get("length", None)
        self.offset = kwargs.get("offset", None)
        self.confidence_score = kwargs.get("confidence_score", None)


class HealthcareEntity:
    """HealthcareEntity contains information about a Healthcare entity found in text.

    :ivar str text: Entity text as appears in the document.
    :ivar str normalized_text: Optional. Normalized version of the raw `text` we extract
        from the document. Not all `text` will have a normalized version.
    :ivar str category: Entity category, see the :class:`~azure.ai.textanalytics.HealthcareEntityCategory`
        type for possible healthcare entity categories.
    :ivar str subcategory: Entity subcategory.
    :ivar assertion: Contains various assertions about this entity. For example, if
        an entity is a diagnosis, is this diagnosis 'conditional' on a symptom?
        Are the doctors 'certain' about this diagnosis? Is this diagnosis 'associated'
        with another diagnosis?
    :vartype assertion: ~azure.ai.textanalytics.HealthcareEntityAssertion
    :ivar int length: The entity text length.  This value depends on the value
        of the `string_index_type` parameter specified in the original request, which is
        UnicodeCodePoints by default.
    :ivar int offset: The entity text offset from the start of the document.
        This value depends on the value of the `string_index_type` parameter specified
        in the original request, which is UnicodeCodePoints by default.
    :ivar float confidence_score: Confidence score between 0 and 1 of the extracted
        entity.
    :ivar data_sources: A collection of entity references in known data sources.
    :vartype data_sources: list[~azure.ai.textanalytics.HealthcareEntityDataSource]
    """

    def __init__(self, **kwargs):
        self.text = kwargs.get("text", None)
        self.normalized_text = kwargs.get("normalized_text", None)
        self.category = kwargs.get("category", None)
        self.subcategory = kwargs.get("subcategory", None)
        self.assertion = kwargs.get("assertion", None)
        self.length = kwargs.get("length", None)
        self.offset = kwargs.get("offset", None)
        self.confidence_score = kwargs.get("confidence_score", None)
        self.data_sources = kwargs.get("data_sources", [])


class HealthcareEntityAssertion:
    """Contains various assertions about a `HealthcareEntity`.

    For example, if an entity is a diagnosis, is this diagnosis 'conditional' on a symptom?
    Are the doctors 'certain' about this diagnosis? Is this diagnosis 'associated'
    with another diagnosis?

    :ivar str conditionality: Describes whether the healthcare entity it's on is conditional on another entity.
        For example, "If the patient has a fever, he has pneumonia", the diagnosis of pneumonia
        is 'conditional' on whether the patient has a fever. Possible values are "hypothetical" and
        "conditional".
    :ivar str certainty: Describes how certain the healthcare entity it's on is. For example,
        in "The patient may have a fever", the fever entity is not 100% certain, but is instead
        "positivePossible". Possible values are "positive", "positivePossible", "neutralPossible",
        "negativePossible", and "negative".
    :ivar str association: Describes whether the healthcare entity it's on is the subject of the document, or
        if this entity describes someone else in the document. For example, in "The subject's mother has
        a fever", the "fever" entity is not associated with the subject themselves, but with the subject's
        mother. Possible values are "subject" and "other".
    """

    def __init__(self, **kwargs):
        self.conditionality = kwargs.get("conditionality", None)
        self.certainty = kwargs.get("certainty", None)
        self.association = kwargs.get("association", None)


class HealthcareEntityDataSource:
    """
    HealthcareEntityDataSource contains information representing an entity reference in a known data source.

    :ivar str entity_id: ID of the entity in the given source catalog.
    :ivar str name: The name of the entity catalog from where the entity was identified, such as UMLS, CHV, MSH, etc.
    """

    def __init__(self, **kwargs):
        self.entity_id = kwargs.get("entity_id", None)
        self.name = kwargs.get("name", None)


class TextAnalyticsError:
    """TextAnalyticsError contains the error code, message, and
    other details that explain why the batch or individual document
    failed to be processed by the service.

    :ivar code: Error code. Possible values include:
     'invalidRequest', 'invalidArgument', 'internalServerError',
     'serviceUnavailable', 'invalidParameterValue', 'invalidRequestBodyFormat',
     'emptyRequest', 'missingInputRecords', 'invalidDocument', 'modelVersionIncorrect',
     'invalidDocumentBatch', 'unsupportedLanguageCode', 'invalidCountryHint'
    :vartype code: str
    :ivar message: Error message.
    :vartype message: str
    :ivar target: Error target.
    :vartype target: str
    """

    def __init__(self, **kwargs):
        self.code = kwargs.get("code", None)
        self.message = kwargs.get("message", None)
        self.target = kwargs.get("target", None)


class TextAnalyticsWarning:
    """TextAnalyticsWarning contains the warning code and message that explains why
    the response has a warning.

    :ivar code: Warning code. Possible values include: 'LongWordsInDocument',
     'DocumentTruncated'.
    :vartype code: str
    :ivar message: Warning message.
    :vartype message: str
    """

    def __init__(self, **kwargs):
        self.code = kwargs.get("code", None)
        self.message = kwargs.get("message", None)


class ExtractKeyPhrasesResult:
    """ExtractKeyPhrasesResult is a result object which contains
    the key phrases found in a particular document.

    :ivar id: Unique, non-empty document identifier that matches the
        document id that was passed in with the request. If not specified
        in the request, an id is assigned for the document.
    :vartype id: str
    :ivar key_phrases: A list of representative words or phrases.
        The number of key phrases returned is proportional to the number of words
        in the input document.
    :vartype key_phrases: list[str]
    :ivar warnings: Warnings encountered while processing document. Results will still be returned
        if there are warnings, but they may not be fully accurate.
    :vartype warnings: list[~azure.ai.textanalytics.TextAnalyticsWarning]
    :ivar statistics: If `show_stats=True` was specified in the request this
        field will contain information about the document payload.
    :vartype statistics:
        ~azure.ai.textanalytics.TextDocumentStatistics
    :ivar str detected_language: If 'language' is set to 'auto' for the document in the request this
         field will contain a 2 letter ISO 639-1 representation of the language detected for this
         document.
    :ivar bool is_error: Boolean check for error item when iterating over list of
        results. Always False for an instance of a ExtractKeyPhrasesResult.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.key_phrases = kwargs.get("key_phrases", None)
        self.warnings = kwargs.get("warnings", [])
        self.statistics = kwargs.get("statistics", None)
        self.detected_language = kwargs.get("detected_language", None)
        self.is_error = False


class RecognizeLinkedEntitiesResult:
    """RecognizeLinkedEntitiesResult is a result object which contains
    links to a well-known knowledge base, like for example, Wikipedia or Bing.

    :ivar id: Unique, non-empty document identifier that matches the
        document id that was passed in with the request. If not specified
        in the request, an id is assigned for the document.
    :vartype id: str
    :ivar entities: Recognized well-known entities in the document.
    :vartype entities:
        list[~azure.ai.textanalytics.LinkedEntity]
    :ivar warnings: Warnings encountered while processing document. Results will still be returned
        if there are warnings, but they may not be fully accurate.
    :vartype warnings: list[~azure.ai.textanalytics.TextAnalyticsWarning]
    :ivar statistics: If `show_stats=True` was specified in the request this
        field will contain information about the document payload.
    :vartype statistics:
        ~azure.ai.textanalytics.TextDocumentStatistics
    :ivar str detected_language: If 'language' is set to 'auto' for the document in the request this
         field will contain a 2 letter ISO 639-1 representation of the language detected for this
         documents.
    :ivar bool is_error: Boolean check for error item when iterating over list of
        results. Always False for an instance of a RecognizeLinkedEntitiesResult.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.entities = kwargs.get("entities", None)
        self.warnings = kwargs.get("warnings", [])
        self.statistics = kwargs.get("statistics", None)
        self.detected_language = kwargs.get("detected_language", None)
        self.is_error = False


class AnalyzeSentimentResult:
    """AnalyzeSentimentResult is a result object which contains
    the overall predicted sentiment and confidence scores for your document
    and a per-sentence sentiment prediction with scores.

    :ivar id: Unique, non-empty document identifier that matches the
        document id that was passed in with the request. If not specified
        in the request, an id is assigned for the document.
    :vartype id: str
    :ivar sentiment: Predicted sentiment for document (Negative,
        Neutral, Positive, or Mixed). Possible values include: 'positive',
        'neutral', 'negative', 'mixed'
    :vartype sentiment: str
    :ivar warnings: Warnings encountered while processing document. Results will still be returned
        if there are warnings, but they may not be fully accurate.
    :vartype warnings: list[~azure.ai.textanalytics.TextAnalyticsWarning]
    :ivar statistics: If `show_stats=True` was specified in the request this
        field will contain information about the document payload.
    :vartype statistics:
        ~azure.ai.textanalytics.TextDocumentStatistics
    :ivar confidence_scores: Document level sentiment confidence
        scores between 0 and 1 for each sentiment label.
    :vartype confidence_scores:
        ~azure.ai.textanalytics.SentimentConfidenceScores
    :ivar sentences: Sentence level sentiment analysis.
    :vartype sentences:
        list[~azure.ai.textanalytics.SentenceSentiment]
    :ivar str detected_language: If 'language' is set to 'auto' for the document in the request this
         field will contain a 2 letter ISO 639-1 representation of the language detected for this
         documents.
    :ivar bool is_error: Boolean check for error item when iterating over list of
        results. Always False for an instance of a AnalyzeSentimentResult.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.sentiment = kwargs.get("sentiment", None)
        self.warnings = kwargs.get("warnings", [])
        self.statistics = kwargs.get("statistics", None)
        self.confidence_scores = kwargs.get("confidence_scores", None)
        self.sentences = kwargs.get("sentences", None)
        self.detected_language = kwargs.get("detected_language", None)
        self.is_error = False


class TextDocumentStatistics:
    """TextDocumentStatistics contains information about
    the document payload.

    :ivar character_count: Number of text elements recognized in
        the document.
    :vartype character_count: int
    :ivar transaction_count: Number of transactions for the document.
    :vartype transaction_count: int
    """

    def __init__(self, **kwargs):
        self.character_count = kwargs.get("character_count", None)
        self.transaction_count = kwargs.get("transaction_count", None)

    @classmethod
    def _from_generated(cls, stats):
        if stats is None:
            return None
        return cls(
            character_count=stats.characters_count,
            transaction_count=stats.transactions_count,
        )

    def __repr__(self):
        return (
            "TextDocumentStatistics(character_count={}, transaction_count={})".format(
                self.character_count, self.transaction_count
            )[:1024]
        )


class DocumentError:
    """DocumentError is an error object which represents an error on
    the individual document.

    :ivar id: Unique, non-empty document identifier that matches the
        document id that was passed in with the request. If not specified
        in the request, an id is assigned for the document.
    :vartype id: str
    :ivar error: The document error.
    :vartype error: ~azure.ai.textanalytics.TextAnalyticsError
    :ivar bool is_error: Boolean check for error item when iterating over list of
        results. Always True for an instance of a DocumentError.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.error = kwargs.get("error", None)
        self.is_error = True

    def __getattr__(self, attr):
        result_set = set()
        result_set.update(
            RecognizeEntitiesResult().keys()
            + RecognizePiiEntitiesResult().keys()
            + DetectLanguageResult().keys()
            + RecognizeLinkedEntitiesResult().keys()
            + AnalyzeSentimentResult().keys()
            + ExtractKeyPhrasesResult().keys()
        )
        result_attrs = result_set.difference(DocumentError().keys())
        if attr in result_attrs:
            raise AttributeError(
                "'DocumentError' object has no attribute '{}'. The service was unable to process this document:\n"
                "Document Id: {}\nError: {} - {}\n".format(
                    attr, self.id, self.error.code, self.error.message
                )
            )
        raise AttributeError(
            f"'DocumentError' object has no attribute '{attr}'"
        )


class DetectLanguageInput(LanguageInput):
    """The input document to be analyzed for detecting language.

    :keyword str id: Unique, non-empty document identifier.
    :keyword str text: The input text to process.
    :keyword str country_hint: A country hint to help better detect
     the language of the text. Accepts two letter country codes
     specified by ISO 3166-1 alpha-2. Defaults to "US". Pass
     in the string "none" to not use a country_hint.
    :ivar id: Required. Unique, non-empty document identifier.
    :vartype id: str
    :ivar text: Required. The input text to process.
    :vartype text: str
    :ivar country_hint: A country hint to help better detect
     the language of the text. Accepts two letter country codes
     specified by ISO 3166-1 alpha-2. Defaults to "US". Pass
     in the string "none" to not use a country_hint.
    :vartype country_hint: str
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id", None)
        self.text = kwargs.get("text", None)
        self.country_hint = kwargs.get("country_hint", None)


class LinkedEntity:
    """LinkedEntity contains a link to the well-known recognized
    entity in text. The link comes from a data source like Wikipedia
    or Bing. It additionally includes all of the matches of this
    entity found in the document.

    :ivar name: Entity Linking formal name.
    :vartype name: str
    :ivar matches: List of instances this entity appears in the text.
    :vartype matches:
        list[~azure.ai.textanalytics.LinkedEntityMatch]
    :ivar language: Language used in the data source.
    :vartype language: str
    :ivar data_source_entity_id: Unique identifier of the recognized entity from the data
        source.
    :vartype data_source_entity_id: str
    :ivar url: URL to the entity's page from the data source.
    :vartype url: str
    :ivar data_source: Data source used to extract entity linking,
        such as Wiki/Bing etc.
    :vartype data_source: str
    :ivar str bing_entity_search_api_id: Bing Entity Search unique identifier of the recognized entity.
        Use in conjunction with the Bing Entity Search SDK to fetch additional relevant information.

    .. versionadded:: v3.1
        The *bing_entity_search_api_id* property.
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.matches = kwargs.get("matches", None)
        self.language = kwargs.get("language", None)
        self.data_source_entity_id = kwargs.get("data_source_entity_id", None)
        self.url = kwargs.get("url", None)
        self.data_source = kwargs.get("data_source", None)
        self.bing_entity_search_api_id = kwargs.get("bing_entity_search_api_id", None)


class LinkedEntityMatch:
    """A match for the linked entity found in text. Provides
    the confidence score of the prediction and where the entity
    was found in the text.

    :ivar confidence_score: If a well-known item is recognized, a
        decimal number denoting the confidence level between 0 and 1 will be
        returned.
    :vartype confidence_score: float
    :ivar text: Entity text as appears in the request.
    :ivar int length: The linked entity match text length.  This value depends on the value of the
        `string_index_type` parameter set in the original request, which is UnicodeCodePoints by default.
    :ivar int offset: The linked entity match text offset from the start of the document.
        The value depends on the value of the `string_index_type` parameter
        set in the original request, which is UnicodeCodePoints by default.
    :vartype text: str

    .. versionadded:: v3.1
        The *offset* and *length* properties.
    """

    def __init__(self, **kwargs):
        self.confidence_score = kwargs.get("confidence_score", None)
        self.text = kwargs.get("text", None)
        self.length = kwargs.get("length", None)
        self.offset = kwargs.get("offset", None)


class TextDocumentInput(MultiLanguageInput):
    """The input document to be analyzed by the service.

    :keyword str id: Unique, non-empty document identifier.
    :keyword str text: The input text to process.
    :keyword str language: This is the 2 letter ISO 639-1 representation
     of a language. For example, use "en" for English; "es" for Spanish etc. If
     not set, uses "en" for English as default.
    :ivar id: Required. Unique, non-empty document identifier.
    :vartype id: str
    :ivar text: Required. The input text to process.
    :vartype text: str
    :ivar language: This is the 2 letter ISO 639-1 representation
     of a language. For example, use "en" for English; "es" for Spanish etc. If
     not set, uses "en" for English as default.
    :vartype language: str
    :ivar default_language: (Optional) A 2 letter ISO 639-1 representation of a language to be used
     as a default value when the "language" property is set to "auto". The default value will be
     used as a fallback if a language cannot be automatically detected.
    :vartype default_language: str
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id", None)
        self.text = kwargs.get("text", None)
        self.language = kwargs.get("language", None)
        self.default_language = kwargs.get('default_language', None)


class SentenceSentiment:
    """SentenceSentiment contains the predicted sentiment and
    confidence scores for each individual sentence in the document.

    :ivar text: The sentence text.
    :vartype text: str
    :ivar sentiment: The predicted Sentiment for the sentence.
        Possible values include: 'positive', 'neutral', 'negative'
    :vartype sentiment: str
    :ivar confidence_scores: The sentiment confidence score between 0
        and 1 for the sentence for all labels.
    :vartype confidence_scores:
        ~azure.ai.textanalytics.SentimentConfidenceScores
    :ivar int length: The sentence text length.  This value depends on the value of the
        `string_index_type` parameter set in the original request, which is UnicodeCodePoints
        by default.
    :ivar int offset: The sentence text offset from the start of the document.
        The value depends on the value of the `string_index_type` parameter
        set in the original request, which is UnicodeCodePoints by default.
    :ivar mined_opinions: The list of opinions mined from this sentence.
        For example in the sentence "The food is good, but the service is bad", we would
        mine the two opinions "food is good" and "service is bad". Only returned
        if `show_opinion_mining` is set to True in the call to `analyze_sentiment` and
        api version is v3.1 and up.
    :vartype mined_opinions:
        list[~azure.ai.textanalytics.MinedOpinion]

    .. versionadded:: v3.1
        The *offset*, *length*, and *mined_opinions* properties.
    """

    def __init__(self, **kwargs):
        self.text = kwargs.get("text", None)
        self.sentiment = kwargs.get("sentiment", None)
        self.confidence_scores = kwargs.get("confidence_scores", None)
        self.length = kwargs.get("length", None)
        self.offset = kwargs.get("offset", None)
        self.mined_opinions = kwargs.get("mined_opinions", None)


class MinedOpinion:
    """A mined opinion object represents an opinion we've extracted from a sentence.
    It consists of both a target that these opinions are about, and the assessments
    representing the opinion.

    :ivar target: The target of an opinion about a product/service.
    :vartype target: ~azure.ai.textanalytics.TargetSentiment
    :ivar assessments: The assessments representing the opinion of the target.
    :vartype assessments: list[~azure.ai.textanalytics.AssessmentSentiment]
    """

    def __init__(self, **kwargs):
        self.target = kwargs.get("target", None)
        self.assessments = kwargs.get("assessments", None)


class TargetSentiment:
    """TargetSentiment contains the predicted sentiment,
    confidence scores and other information about a key component of a product/service.
    For example in "The food at Hotel Foo is good", "food" is an key component of
    "Hotel Foo".

    :ivar str text: The text value of the target.
    :ivar str sentiment: The predicted Sentiment for the target. Possible values
        include 'positive', 'mixed', and 'negative'.
    :ivar confidence_scores: The sentiment confidence score between 0
        and 1 for the target for 'positive' and 'negative' labels. It's score
        for 'neutral' will always be 0
    :vartype confidence_scores:
        ~azure.ai.textanalytics.SentimentConfidenceScores
    :ivar int length: The target text length.  This value depends on the value of the
        `string_index_type` parameter set in the original request, which is UnicodeCodePoints
        by default.
    :ivar int offset: The target text offset from the start of the document.
        The value depends on the value of the `string_index_type` parameter
        set in the original request, which is UnicodeCodePoints by default.
    """

    def __init__(self, **kwargs):
        self.text = kwargs.get("text", None)
        self.sentiment = kwargs.get("sentiment", None)
        self.confidence_scores = kwargs.get("confidence_scores", None)
        self.length = kwargs.get("length", None)
        self.offset = kwargs.get("offset", None)


class AssessmentSentiment:
    """AssessmentSentiment contains the predicted sentiment,
    confidence scores and other information about an assessment given about
    a particular target.  For example, in the sentence "The food is good", the assessment
    of the target 'food' is 'good'.

    :ivar str text: The assessment text.
    :ivar str sentiment: The predicted Sentiment for the assessment. Possible values
        include 'positive', 'mixed', and 'negative'.
    :ivar confidence_scores: The sentiment confidence score between 0
        and 1 for the assessment for 'positive' and 'negative' labels. It's score
        for 'neutral' will always be 0
    :vartype confidence_scores:
        ~azure.ai.textanalytics.SentimentConfidenceScores
    :ivar int length: The assessment text length.  This value depends on the value of the
        `string_index_type` parameter set in the original request, which is UnicodeCodePoints
        by default.
    :ivar int offset: The assessment text offset from the start of the document.
        The value depends on the value of the `string_index_type` parameter
        set in the original request, which is UnicodeCodePoints by default.
    :ivar bool is_negated: Whether the value of the assessment is negated. For example, in
        "The food is not good", the assessment "good" is negated.
    """

    def __init__(self, **kwargs):
        self.text = kwargs.get("text", None)
        self.sentiment = kwargs.get("sentiment", None)
        self.confidence_scores = kwargs.get("confidence_scores", None)
        self.length = kwargs.get("length", None)
        self.offset = kwargs.get("offset", None)
        self.is_negated = kwargs.get("is_negated", None)


class SentimentConfidenceScores:
    """The confidence scores (Softmax scores) between 0 and 1.
    Higher values indicate higher confidence.

    :ivar positive: Positive score.
    :vartype positive: float
    :ivar neutral: Neutral score.
    :vartype neutral: float
    :ivar negative: Negative score.
    :vartype negative: float
    """

    def __init__(self, **kwargs):
        self.positive = kwargs.get("positive", 0.0)
        self.neutral = kwargs.get("neutral", 0.0)
        self.negative = kwargs.get("negative", 0.0)


class RecognizeEntitiesAction:
    """RecognizeEntitiesAction encapsulates the parameters for starting a long-running Entities Recognition operation.

    If you just want to recognize entities in a list of documents, and not perform multiple
    long running actions on the input of documents, call method `recognize_entities` instead
    of interfacing with this model.

    :keyword str model_version: The model version to use for the analysis.
    :keyword str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str model_version: The model version to use for the analysis.
    :ivar str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :ivar bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str kind: Enumeration of supported Text Analysis tasks. Constant filled by server.
        Possible values include: "SentimentAnalysis", "EntityRecognition", "PiiEntityRecognition",
        "KeyPhraseExtraction", "LanguageDetection", "EntityLinking", "Healthcare",
        "ExtractiveSummarization", "CustomEntityRecognition", "CustomSingleClassification",
        "CustomMultiClassification".
    """

    def __init__(self, **kwargs):
        self.kind = "EntityRecognition"
        self.model_version = kwargs.get("model_version", None)
        self.string_index_type = kwargs.get("string_index_type", "UnicodeCodePoint")
        self.disable_service_logs = kwargs.get("disable_service_logs", None)


class AnalyzeSentimentAction:
    """AnalyzeSentimentAction encapsulates the parameters for starting a long-running
    Sentiment Analysis operation.

    If you just want to analyze sentiment in a list of documents, and not perform multiple
    long running actions on the input of documents, call method `analyze_sentiment` instead
    of interfacing with this model.

    :keyword str model_version: The model version to use for the analysis.
    :keyword bool show_opinion_mining: Whether to mine the opinions of a sentence and conduct more
        granular analysis around the aspects of a product or service (also known as
        aspect-based sentiment analysis). If set to true, the returned
        :class:`~azure.ai.textanalytics.SentenceSentiment` objects
        will have property `mined_opinions` containing the result of this analysis.
    :keyword str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str model_version: The model version to use for the analysis.
    :ivar bool show_opinion_mining: Whether to mine the opinions of a sentence and conduct more
        granular analysis around the aspects of a product or service (also known as
        aspect-based sentiment analysis). If set to true, the returned
        :class:`~azure.ai.textanalytics.SentenceSentiment` objects
        will have property `mined_opinions` containing the result of this analysis.
    :ivar str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :ivar bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str kind: Enumeration of supported Text Analysis tasks. Constant filled by server.
        Possible values include: "SentimentAnalysis", "EntityRecognition", "PiiEntityRecognition",
        "KeyPhraseExtraction", "LanguageDetection", "EntityLinking", "Healthcare",
        "ExtractiveSummarization", "CustomEntityRecognition", "CustomSingleClassification",
        "CustomMultiClassification".
    """

    def __init__(self, **kwargs):
        self.kind = "SentimentAnalysis"
        self.model_version = kwargs.get("model_version", None)
        self.show_opinion_mining = kwargs.get("show_opinion_mining", None)
        self.string_index_type = kwargs.get("string_index_type", "UnicodeCodePoint")
        self.disable_service_logs = kwargs.get("disable_service_logs", None)


class RecognizePiiEntitiesAction:
    """RecognizePiiEntitiesAction encapsulates the parameters for starting a long-running PII
    Entities Recognition operation.

    If you just want to recognize pii entities in a list of documents, and not perform multiple
    long running actions on the input of documents, call method `recognize_pii_entities` instead
    of interfacing with this model.

    :keyword str model_version: The model version to use for the analysis.
    :keyword str domain_filter: An optional string to set the PII domain to include only a
        subset of the PII entity categories. Possible values include 'phi' or None.
    :keyword categories_filter: Instead of filtering over all PII entity categories, you can pass in a list of
        the specific PII entity categories you want to filter out. For example, if you only want to filter out
        U.S. social security numbers in a document, you can pass in
        `[PiiEntityCategory.US_SOCIAL_SECURITY_NUMBER]` for this kwarg.
    :paramtype categories_filter: list[~azure.ai.textanalytics.PiiEntityCategory]
    :keyword str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :keyword bool disable_service_logs: Defaults to true, meaning that Text Analytics will not log your
        input text on the service side for troubleshooting. If set to False, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str model_version: The model version to use for the analysis.
    :ivar str domain_filter: An optional string to set the PII domain to include only a
        subset of the PII entity categories. Possible values include 'phi' or None.
    :ivar categories_filter: Instead of filtering over all PII entity categories, you can pass in a list of
        the specific PII entity categories you want to filter out. For example, if you only want to filter out
        U.S. social security numbers in a document, you can pass in
        `[PiiEntityCategory.US_SOCIAL_SECURITY_NUMBER]` for this kwarg.
    :vartype categories_filter: list[~azure.ai.textanalytics.PiiEntityCategory]
    :ivar str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :ivar bool disable_service_logs: Defaults to true, meaning that Text Analytics will not log your
        input text on the service side for troubleshooting. If set to False, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str kind: Enumeration of supported Text Analysis tasks. Constant filled by server.
        Possible values include: "SentimentAnalysis", "EntityRecognition", "PiiEntityRecognition",
        "KeyPhraseExtraction", "LanguageDetection", "EntityLinking", "Healthcare",
        "ExtractiveSummarization", "CustomEntityRecognition", "CustomSingleClassification",
        "CustomMultiClassification".
    """

    def __init__(self, **kwargs):
        self.kind = "PiiEntityRecognition"
        self.model_version = kwargs.get("model_version", None)
        self.domain_filter = kwargs.get("domain_filter", None)
        self.categories_filter = kwargs.get("categories_filter", None)
        self.string_index_type = kwargs.get("string_index_type", "UnicodeCodePoint")
        self.disable_service_logs = kwargs.get("disable_service_logs", None)


class ExtractKeyPhrasesAction:
    """ExtractKeyPhrasesAction encapsulates the parameters for starting a long-running key phrase
    extraction operation

    If you just want to extract key phrases from a list of documents, and not perform multiple
    long running actions on the input of documents, call method `extract_key_phrases` instead
    of interfacing with this model.

    :keyword str model_version: The model version to use for the analysis.
    :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str model_version: The model version to use for the analysis.
    :ivar bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str kind: Enumeration of supported Text Analysis tasks. Constant filled by server.
        Possible values include: "SentimentAnalysis", "EntityRecognition", "PiiEntityRecognition",
        "KeyPhraseExtraction", "LanguageDetection", "EntityLinking", "Healthcare",
        "ExtractiveSummarization", "CustomEntityRecognition", "CustomSingleClassification",
        "CustomMultiClassification".
    """

    def __init__(self, **kwargs):
        self.kind = "KeyPhraseExtraction"
        self.model_version = kwargs.get("model_version", None)
        self.disable_service_logs = kwargs.get("disable_service_logs", None)


class RecognizeLinkedEntitiesAction:
    """RecognizeLinkedEntitiesAction encapsulates the parameters for starting a long-running Linked Entities
    Recognition operation.

    If you just want to recognize linked entities in a list of documents, and not perform multiple
    long running actions on the input of documents, call method `recognize_linked_entities` instead
    of interfacing with this model.

    :keyword str model_version: The model version to use for the analysis.
    :keyword str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str model_version: The model version to use for the analysis.
    :ivar str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :ivar bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str kind: Enumeration of supported Text Analysis tasks. Constant filled by server.
        Possible values include: "SentimentAnalysis", "EntityRecognition", "PiiEntityRecognition",
        "KeyPhraseExtraction", "LanguageDetection", "EntityLinking", "Healthcare",
        "ExtractiveSummarization", "CustomEntityRecognition", "CustomSingleClassification",
        "CustomMultiClassification".
    """

    def __init__(self, **kwargs):
        self.kind = "EntityLinking"
        self.model_version = kwargs.get("model_version", None)
        self.string_index_type = kwargs.get("string_index_type", "UnicodeCodePoint")
        self.disable_service_logs = kwargs.get("disable_service_logs", None)


class ExtractSummaryAction:
    """ExtractSummaryAction encapsulates the parameters for starting a long-running Extractive Text
    Summarization operation. For a conceptual discussion of extractive summarization, see the service documentation:
    https://docs.microsoft.com/azure/cognitive-services/text-analytics/how-tos/extractive-summarization

    :keyword str model_version: The model version to use for the analysis.
    :keyword str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :keyword int max_sentence_count: Maximum number of sentences to return. Defaults to 3.
    :keyword str order_by:  Possible values include: "Offset", "Rank". Default value: "Offset".
    :ivar str model_version: The model version to use for the analysis.
    :ivar str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :ivar bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar int max_sentence_count: Number of sentences to return. Defaults to 3.
    :ivar str order_by:  Possible values include: "Offset", "Rank". Default value: "Offset".
    :ivar str kind: Enumeration of supported Text Analysis tasks. Constant filled by server.
        Possible values include: "SentimentAnalysis", "EntityRecognition", "PiiEntityRecognition",
        "KeyPhraseExtraction", "LanguageDetection", "EntityLinking", "Healthcare",
        "ExtractiveSummarization", "CustomEntityRecognition", "CustomSingleClassification",
        "CustomMultiClassification".
    """

    def __init__(self, **kwargs):
        self.kind = "ExtractiveSummarization"
        self.model_version = kwargs.get("model_version", None)
        self.string_index_type = kwargs.get("string_index_type", "UnicodeCodePoint")
        self.disable_service_logs = kwargs.get("disable_service_logs", None)
        self.max_sentence_count = kwargs.get("max_sentence_count", None)
        self.order_by = kwargs.get("order_by", None)


class ExtractSummaryResult:
    """ExtractSummaryResult is a result object which contains
    the extractive text summarization from a particular document.

    :ivar str id: Unique, non-empty document identifier.
    :ivar sentences: A ranked list of sentences representing the extracted summary.
    :vartype sentences: list[~azure.ai.textanalytics.SummarySentence]
    :ivar warnings: Warnings encountered while processing document.
    :vartype warnings: list[~azure.ai.textanalytics.TextAnalyticsWarning]
    :ivar statistics: If `show_stats=True` was specified in the request this
        field will contain information about the document payload.
    :vartype statistics: ~azure.ai.textanalytics.TextDocumentStatistics
    :ivar str detected_language: If 'language' is set to 'auto' for the document in the request this
         field will contain a 2 letter ISO 639-1 representation of the language detected for this
         documents.
    :ivar bool is_error: Boolean check for error item when iterating over list of
        results. Always False for an instance of an ExtractSummaryResult.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.sentences = kwargs.get("sentences", None)
        self.warnings = kwargs.get("warnings", None)
        self.statistics = kwargs.get("statistics", None)
        self.detected_language = kwargs.get("detected_language", None)
        self.is_error = False


class SummarySentence:
    """Represents a single sentence from the extractive text summarization.

    :ivar str text: The extracted sentence text.
    :ivar float rank_score: A float value representing the relevance of the sentence within
        the summary. Higher values indicate higher importance.
    :ivar int offset: The sentence offset from the start of the document.
        The value depends on the value of the `string_index_type` parameter
        set in the original request, which is UnicodeCodePoint by default.
    :ivar int length: The length of the sentence. This value depends on the value of the
        `string_index_type` parameter set in the original request, which is UnicodeCodePoint
        by default.
    """

    def __init__(self, **kwargs):
        self.text = kwargs.get("text", None)
        self.rank_score = kwargs.get("rank_score", None)
        self.offset = kwargs.get("offset", None)
        self.length = kwargs.get("length", None)


class RecognizeCustomEntitiesAction:
    """RecognizeCustomEntitiesAction encapsulates the parameters for starting a long-running custom entity
    recognition operation. For information on regional support of custom features and how to train a model to
    recognize custom entities, see https://aka.ms/azsdk/textanalytics/customentityrecognition

    :param str project_name: Required. This field indicates the project name for the model.
    :param str deployment_name: This field indicates the deployment name for the model.
    :keyword str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str project_name: This field indicates the project name for the model.
    :ivar str deployment_name: This field indicates the deployment name for the model.
    :ivar str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :ivar bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str kind: Enumeration of supported Text Analysis tasks. Constant filled by server.
        Possible values include: "SentimentAnalysis", "EntityRecognition", "PiiEntityRecognition",
        "KeyPhraseExtraction", "LanguageDetection", "EntityLinking", "Healthcare",
        "ExtractiveSummarization", "CustomEntityRecognition", "CustomSingleClassification",
        "CustomMultiClassification".
    """

    def __init__(
        self,
        project_name,
        deployment_name,
        **kwargs
    ):
        self.kind = "CustomEntityRecognition"
        self.project_name = project_name
        self.deployment_name = deployment_name
        self.disable_service_logs = kwargs.get('disable_service_logs', None)
        self.string_index_type = kwargs.get('string_index_type', "UnicodeCodePoint")


class RecognizeCustomEntitiesResult:
    """RecognizeCustomEntitiesResult is a result object which contains
    the custom recognized entities from a particular document.

    :ivar str id: Unique, non-empty document identifier that matches the
        document id that was passed in with the request. If not specified
        in the request, an id is assigned for the document.
    :ivar entities: Recognized custom entities in the document.
    :vartype entities:
        list[~azure.ai.textanalytics.CategorizedEntity]
    :ivar warnings: Warnings encountered while processing document.
    :vartype warnings: list[~azure.ai.textanalytics.TextAnalyticsWarning]
    :ivar statistics: If `show_stats=True` was specified in the request this
        field will contain information about the document payload.
    :vartype statistics: ~azure.ai.textanalytics.TextDocumentStatistics
    :ivar str detected_language: If 'language' is set to 'auto' for the document in the request this
         field will contain a 2 letter ISO 639-1 representation of the language detected for this
         documents.
    :ivar bool is_error: Boolean check for error item when iterating over list of
        results. Always False for an instance of a RecognizeCustomEntitiesResult.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.entities = kwargs.get("entities", None)
        self.warnings = kwargs.get("warnings", [])
        self.statistics = kwargs.get("statistics", None)
        self.detected_language = kwargs.get("detected_language", None)
        self.is_error = False


class MultiCategoryClassifyAction:
    """MultiCategoryClassifyAction encapsulates the parameters for starting a long-running custom multi category
    classification operation. For information on regional support of custom features and how to train a model to
    classify your documents, see https://aka.ms/azsdk/textanalytics/customfunctionalities

    :param str project_name: Required. This field indicates the project name for the model.
    :param str deployment_name: Required. This field indicates the deployment name for the model.
    :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str project_name: This field indicates the project name for the model.
    :ivar str deployment_name: This field indicates the deployment name for the model.
    :ivar bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str kind: Enumeration of supported Text Analysis tasks. Constant filled by server.
        Possible values include: "SentimentAnalysis", "EntityRecognition", "PiiEntityRecognition",
        "KeyPhraseExtraction", "LanguageDetection", "EntityLinking", "Healthcare",
        "ExtractiveSummarization", "CustomEntityRecognition", "CustomSingleClassification",
        "CustomMultiClassification".
    """

    def __init__(
        self,
        project_name,
        deployment_name,
        **kwargs
    ):
        self.kind = "CustomMultiClassification"
        self.project_name = project_name
        self.deployment_name = deployment_name
        self.disable_service_logs = kwargs.get('disable_service_logs', None)


class MultiCategoryClassifyResult:
    """MultiCategoryClassifyResult is a result object which contains
    the classifications for a particular document.

    :ivar str id: Unique, non-empty document identifier.
    :ivar classifications: Recognized classification results in the document.
    :vartype classifications: list[~azure.ai.textanalytics.ClassificationCategory]
    :ivar warnings: Warnings encountered while processing document.
    :vartype warnings: list[~azure.ai.textanalytics.TextAnalyticsWarning]
    :ivar statistics: If `show_stats=True` was specified in the request this
        field will contain information about the document payload.
    :vartype statistics: ~azure.ai.textanalytics.TextDocumentStatistics
    :ivar str detected_language: If 'language' is set to 'auto' for the document in the request this
         field will contain a 2 letter ISO 639-1 representation of the language detected for this
         documents.
    :ivar bool is_error: Boolean check for error item when iterating over list of
        results. Always False for an instance of a MultiCategoryClassifyResult.
    """

    def __init__(
        self,
        **kwargs
    ):
        self.id = kwargs.get('id', None)
        self.classifications = kwargs.get('classifications', None)
        self.warnings = kwargs.get('warnings', [])
        self.statistics = kwargs.get('statistics', None)
        self.detected_language = kwargs.get("detected_language", None)
        self.is_error = False


class SingleCategoryClassifyAction:
    """SingleCategoryClassifyAction encapsulates the parameters for starting a long-running custom single category
    classification operation. For information on regional support of custom features and how to train a model to
    classify your documents, see https://aka.ms/azsdk/textanalytics/customfunctionalities

    :param str project_name: Required. This field indicates the project name for the model.
    :param str deployment_name: Required. This field indicates the deployment name for the model.
    :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str project_name: This field indicates the project name for the model.
    :ivar str deployment_name: This field indicates the deployment name for the model.
    :ivar bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str kind: Enumeration of supported Text Analysis tasks. Constant filled by server.
        Possible values include: "SentimentAnalysis", "EntityRecognition", "PiiEntityRecognition",
        "KeyPhraseExtraction", "LanguageDetection", "EntityLinking", "Healthcare",
        "ExtractiveSummarization", "CustomEntityRecognition", "CustomSingleClassification",
        "CustomMultiClassification".
    """

    def __init__(
        self,
        project_name,
        deployment_name,
        **kwargs
    ):
        self.kind = "CustomSingleClassification"
        self.project_name = project_name
        self.deployment_name = deployment_name
        self.disable_service_logs = kwargs.get('disable_service_logs', None)


class SingleCategoryClassifyResult:
    """SingleCategoryClassifyResult is a result object which contains
    the classification for a particular document.

    :ivar str id: Unique, non-empty document identifier.
    :ivar classification: Recognized classification results in the document.
    :vartype classification: ~azure.ai.textanalytics.ClassificationCategory
    :ivar warnings: Warnings encountered while processing document.
    :vartype warnings: list[~azure.ai.textanalytics.TextAnalyticsWarning]
    :ivar statistics: If `show_stats=True` was specified in the request this
        field will contain information about the document payload.
    :vartype statistics: ~azure.ai.textanalytics.TextDocumentStatistics
    :ivar str detected_language: If 'language' is set to 'auto' for the document in the request this
         field will contain a 2 letter ISO 639-1 representation of the language detected for this
         documents.
    :ivar bool is_error: Boolean check for error item when iterating over list of
        results. Always False for an instance of a SingleCategoryClassifyResult.
    """

    def __init__(
        self,
        **kwargs
    ):
        self.id = kwargs.get('id', None)
        self.classification = kwargs.get('classification', None)
        self.warnings = kwargs.get('warnings', [])
        self.statistics = kwargs.get('statistics', None)
        self.detected_language = kwargs.get("detected_language", None)
        self.is_error = False


class ClassificationCategory:
    """ClassificationCategory represents a classification of the input document.

    :ivar str category: Custom classification category for the document.
    :ivar float confidence_score: Confidence score between 0 and 1 of the recognized classification.
    """

    def __init__(
        self,
        **kwargs
    ):
        self.category = kwargs.get('category', None)
        self.confidence_score = kwargs.get('confidence_score', None)


class AnalyzeHealthcareEntitiesAction:
    """AnalyzeHealthcareEntitiesAction.

    :keyword str model_version: The model version to use for the analysis.
    :keyword str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str model_version: The model version to use for the analysis.
    :ivar str string_index_type: Specifies the method used to interpret string offsets.
        `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
        you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
        see https://aka.ms/text-analytics-offsets
    :ivar bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str kind: Enumeration of supported Text Analysis tasks. Constant filled by server.
        Possible values include: "SentimentAnalysis", "EntityRecognition", "PiiEntityRecognition",
        "KeyPhraseExtraction", "LanguageDetection", "EntityLinking", "Healthcare",
        "ExtractiveSummarization", "CustomEntityRecognition", "CustomSingleClassification",
        "CustomMultiClassification".
    """

    def __init__(self, **kwargs):
        self.kind = "Healthcare"
        self.model_version = kwargs.get("model_version", None)
        self.string_index_type = kwargs.get("string_index_type", "UnicodeCodePoint")
        self.disable_service_logs = kwargs.get("disable_service_logs", None)


class DetectLanguageAction:
    """DetectLanguageAction.

    :keyword str model_version: The model version to use for the analysis.
    :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :keyword str region_hint:
    :ivar str model_version: The model version to use for the analysis.
    :ivar bool disable_service_logs: If set to true, you opt-out of having your text input
        logged on the service side for troubleshooting. By default, Text Analytics logs your
        input text for 48 hours, solely to allow for troubleshooting issues in providing you with
        the Text Analytics natural language processing functions. Setting this parameter to true,
        disables input logging and may limit our ability to remediate issues that occur. Please see
        Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
        additional details, and Microsoft Responsible AI principles at
        https://www.microsoft.com/ai/responsible-ai.
    :ivar str region_hint:
    :ivar str kind: Enumeration of supported Text Analysis tasks. Constant filled by server.
        Possible values include: "SentimentAnalysis", "EntityRecognition", "PiiEntityRecognition",
        "KeyPhraseExtraction", "LanguageDetection", "EntityLinking", "Healthcare",
        "ExtractiveSummarization", "CustomEntityRecognition", "CustomSingleClassification",
        "CustomMultiClassification".
    """

    def __init__(self, **kwargs):
        self.kind = "LanguageDetection"
        self.model_version = kwargs.get("model_version", None)
        self.region_hint = kwargs.get("region_hint", None)
        self.disable_service_logs = kwargs.get("disable_service_logs", None)

