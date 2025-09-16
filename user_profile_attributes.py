from enum import Enum
from typing import Dict, Any, List, Optional

class FormUserAttributeMeta(type):
    """Metaclass for user profile attributes."""
    registry: Dict[str, type] = {}

    def __new__(cls, name: str, bases: tuple, attrs: dict) -> type:
        new_p_attr = super().__new__(cls, name, bases, attrs)
        if name not in ["FormUserAttr"]:
            assert name not in cls.registry, f"User attribute {name} already exists"
            cls.registry[name] = new_p_attr
        return new_p_attr


class FormUserProfile:
    """Class representing a user's profile for form filling."""
    
    def __init__(self, form_name: Optional[str] = None, idx: Optional[int] = None):
        """
        Initialize a user profile.
        
        Args:
            form_name: Name of the form to use
            idx: Index of the form to use if form_name is not provided
        """
        class Features:
            """Container for user profile features."""
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

    def get_nl_profile(self) -> List[str]:
        """
        Get a natural language description of the user profile.
        
        Returns:
            List of natural language descriptions for each attribute
        """
        nl_profile = []
        for name, attr_class in FormUserAttributeMeta.registry.items():
            nl_profile.append(attr_class.nl_desc(getattr(self.features, name)))
        return nl_profile
    
    # Store all form names for reference
    all_form_names: List[str] = ['0000971160_processed', '0000989556_processed', '0000990274_processed', '0000999294_processed', '0001118259_processed', '0001123541_processed', '0001129658_processed', '0001209043_processed', '0001239897_processed', '0001438955_processed', '0001456787_processed', '0001463282_processed', '0001463448_processed', '0001476912_processed', '0001477983_processed', '0001485288_processed', '00040534_processed', '00070353_processed', '00093726_processed', '0011505151_processed', '0011838621_processed', '0011845203_processed', '0011856542_processed', '0011859695_processed', '0011899960_processed', '0011906503_processed', '0011973451_processed', '0011974919_processed', '0011976929_processed', '0012178355_processed', '0012199830_processed', '0012529284_processed', '0012529295_processed', '0012602424_processed', '0012947358_processed', '0013255595_processed', '00283813_processed', '0030031163_processed', '0030041455_processed', '0060000813_processed', '0060007216_processed', '0060024314_processed', '0060025670_processed', '0060029036_processed', '0060036622_processed', '0060068489_processed', '0060077689_processed', '0060080406_processed', '0060091229_processed', '0060094595_processed', '0060136394_processed', '0060165115_processed', '0060173256_processed', '0060207528_processed', '0060214859_processed', '0060255888_processed', '0060262650_processed', '0060270727_processed', '0060302201_processed', '0060308251_processed', '0060308461_processed', '0071032790_processed', '0071032807_processed', '00836244_processed', '00836816_processed', '00837285_processed', '00838511_00838525_processed', '00851772_1780_processed', '00851879_processed', '00860012_00860014_processed', '00865872_processed', '00866042_processed', '00920222_processed', '00920294_processed', '00922237_processed', '01073843_processed', '01122115_processed', '01150773_01150774_processed', '01191071_1072_processed', '01197604_processed', '01408099_01408101_processed', '11508234_processed', '11875011_processed', '12052385_processed', '12603270_processed', '12825369_processed', '13149651_processed', '660978_processed', '71108371_processed', '71190280_processed', '71202511_processed', '71206427_processed', '71341634_processed', '71366499_processed', '71563825_processed', '71601299_processed', '716552_processed', '80310840a_processed', '80707440_7443_processed', '80718412_8413_processed', '80728670_processed', '81186212_processed', '81310636_processed', '81574683_processed', '81619486_9488_processed', '81619511_9513_processed', '81749056_9057_processed', '82254638_processed', '87533049_processed', '87672097_processed', '87682908_processed', '88057519_processed', '88547278_88547279_processed', '89368010_processed', '89386032_processed', '89817999_8002_processed', '89867723_processed', '91104867_processed', '91161344_91161347_processed', '91315069_91315070_processed', '91355841_processed', '91356315_processed', '91361993_processed', '91372360_processed', '91391286_processed', '91391310_processed', '91581919_processed', '91856041_6049_processed', '91903177_processed', '91914407_processed', '91939637_processed', '91974562_processed', '92039708_9710_processed', '92081358_1359_processed', '92091873_processed', '92094746_processed', '92094751_processed', '92298125_processed', '92314414_processed', '92327794_processed', '92433599_92433601_processed', '92586242_processed', '92657311_7313_processed', '92657391_processed', '93213298_processed', '93329540_processed', '93351929_93351931_processed', '93380187_processed', '93455715_processed']


class FormUserAttr(metaclass=FormUserAttributeMeta):
    """Base class for user profile attributes."""
    pass