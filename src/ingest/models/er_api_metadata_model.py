from pydantic import BaseModel, Field, model_validator
from typing import Union, Optional

import deepl
import re
import tomli




# Load the API key from the .toml file
def load_api_key() -> str:
    with open("./models/.secrets.toml", "rb") as f:
        config = tomli.load(f)
    return config["deepl"]["api_key"]


def is_hangul(text):
    # This regex pattern matches the full range of Hangul characters
    hangul_pattern = re.compile(r"[\uac00-\ud7a3]")
    return bool(hangul_pattern.search(text))


def translate_name(name: str, auth_key: str):
    translator = deepl.Translator(auth_key)

    # if is_hangul(name):  # Check if there is any Hangul
    try:
        result = translator.translate_text(
                name,source_lang="KO",  target_lang="EN-US"
                )
        print(f"Translated {name} to {result}")
        return str(result)
    except deepl.exceptions.DeepLException as e:
        print(f"DeepL API error: {e}")
        return name
    return name


class Character(BaseModel):
    code: float
    name: str
    max_hp: float = Field(..., alias="maxHp")
    max_sp: float = Field(..., alias="maxSp")
    str_learn_start_skill: str = Field(..., alias="strLearnStartSkill")
    str_use_point_learn_start_skill: str = Field(
        ..., alias="strUsePointLearnStartSkill"
    )
    init_extra_point: float = Field(..., alias="initExtraPoint")
    max_extra_point: float = Field(..., alias="maxExtraPoint")
    attack_power: float = Field(..., alias="attackPower")
    defense: float
    skill_amp: float = Field(..., alias="skillAmp")
    adaptive_force: float = Field(..., alias="adaptiveForce")
    critical_strike_chance: float = Field(..., alias="criticalStrikeChance")
    hp_regen: float = Field(..., alias="hpRegen")
    sp_regen: float = Field(..., alias="spRegen")
    attack_speed: float = Field(..., alias="attackSpeed")
    attack_speed_ratio: float = Field(..., alias="attackSpeedRatio")
    increase_basic_attack_damage_ratio: float = Field(
        ..., alias="increaseBasicAttackDamageRatio"
    )
    skill_amp_ratio: float = Field(..., alias="skillAmpRatio")
    prevent_basic_attack_damaged_ratio: float = Field(
        ..., alias="preventBasicAttackDamagedRatio"
    )
    prevent_skill_damaged_ratio: float = Field(..., alias="preventSkillDamagedRatio")
    attack_speed_limit: float = Field(..., alias="attackSpeedLimit")
    attack_speed_min: float = Field(..., alias="attackSpeedMin")
    move_speed: float = Field(..., alias="moveSpeed")
    sight_range: float = Field(..., alias="sightRange")
    radius: float
    pathing_radius: float = Field(..., alias="pathingRadius")
    ui_height: float = Field(..., alias="uiHeight")
    init_state_display_index: float = Field(..., alias="initStateDisplayIndex")
    local_scale_in_cutscene: float = Field(..., alias="localScaleInCutscene")
    local_scale_in_victory_scene: str = Field(..., alias="localScaleInVictoryScene")
    resource: str
    lobby_sub_object: str = Field(..., alias="lobbySubObject")

    class Config:
        populate_by_name = True


class Area(BaseModel):
    code: float
    name: str
    mode_type: float = Field(..., alias="modeType")
    mask_code: float = Field(..., alias="maskCode")
    starting_area: float = Field(..., alias="startingArea")
    area_type: float = Field(..., alias="areaType")
    is_provide_collectible_item: bool = Field(..., alias="isProvideCollectibleItem")
    route_calc_bit_code: float = Field(..., alias="routeCalcBitCode")
    has_hyperloop: bool = Field(..., alias="isHyperloopInstalled")

    class Config:
        populate_by_name = True


class Collectible(BaseModel):
    code: float
    cooldown: float
    item_code_1: str = Field(..., alias="itemCode1")
    item_code_2: str = Field(..., alias="itemCode2")
    probability_1: float = Field(..., alias="probability1")
    probability_2: float = Field(..., alias="probability2")
    drop_count: float = Field(..., alias="dropCount")
    casting_action_type: str = Field(..., alias="castingActionType")

    class Config:
        populate_by_name = True


class Armor(BaseModel):
    code: float
    name: str
    en_name: Optional[str] = None
    mode_type: float = Field(alias="modeType")
    item_type: str = Field(alias="itemType")
    armor_type: str = Field(alias="armorType")
    item_grade: str = Field(alias="itemGrade")
    is_completed_item: bool = Field(alias="isCompletedItem")
    alert_in_spectator: bool = Field(alias="alertInSpectator")
    marking_type: str = Field(alias="markingType")
    craft_anim_trigger: str = Field(alias="craftAnimTrigger")
    stackable: float
    initial_count: float = Field(alias="initialCount")
    item_usable_type: str = Field(alias="itemUsableType")
    item_usable_value_list: Union[float, list[float]] = Field(alias="itemUsableValueList")
    exclusive_producer: float = Field(alias="exclusiveProducer")
    is_removed_from_player_corpse_inventory_when_player_killed: bool = Field(
        alias="isRemovedFromPlayerCorpseInventoryWhenPlayerKilled"
    )
    make_material1: float = Field(alias="makeMaterial1")
    make_material2: float = Field(alias="makeMaterial2")
    make_custom_action: str = Field(alias="makeCustomAction")
    not_disarm: bool = Field(alias="notDisarm")
    manufacturable_type: float = Field(alias="manufacturableType")
    attack_power: float = Field(alias="attackPower")
    attack_power_by_lv: float = Field(alias="attackPowerByLv")
    defense: float
    defense_by_lv: float = Field(alias="defenseByLv")
    skill_amp: float = Field(alias="skillAmp")
    skill_amp_by_level: float = Field(alias="skillAmpByLevel")
    skill_amp_ratio: float = Field(alias="skillAmpRatio")
    skill_amp_ratio_by_level: float = Field(alias="skillAmpRatioByLevel")
    adaptive_force: float = Field(alias="adaptiveForce")
    adaptive_force_by_level: float = Field(alias="adaptiveForceByLevel")
    max_hp: float = Field(alias="maxHp")
    max_hp_by_lv: float = Field(alias="maxHpByLv")
    max_sp: float = Field(alias="maxSp")
    hp_regen_ratio: float = Field(alias="hpRegenRatio")
    hp_regen: float = Field(alias="hpRegen")
    sp_regen_ratio: float = Field(alias="spRegenRatio")
    sp_regen: float = Field(alias="spRegen")
    attack_speed_ratio: float = Field(alias="attackSpeedRatio")
    attack_speed_ratio_by_lv: float = Field(alias="attackSpeedRatioByLv")
    critical_strike_chance: float = Field(alias="criticalStrikeChance")
    critical_strike_damage: float = Field(alias="criticalStrikeDamage")
    prevent_critical_strike_damaged: float = Field(alias="preventCriticalStrikeDamaged")
    cooldown_reduction: float = Field(alias="cooldownReduction")
    cooldown_limit: float = Field(alias="cooldownLimit")
    life_steal: float = Field(alias="lifeSteal")
    normal_life_steal: float = Field(alias="normalLifeSteal")
    skill_life_steal: float = Field(alias="skillLifeSteal")
    move_speed: float = Field(alias="moveSpeed")
    move_speed_out_of_combat: float = Field(alias="moveSpeedOutOfCombat")
    sight_range: float = Field(alias="sightRange")
    attack_range: float = Field(alias="attackRange")
    increase_basic_attack_damage: float = Field(alias="increaseBasicAttackDamage")
    increase_basic_attack_damage_by_lv: float = Field(
        alias="increaseBasicAttackDamageByLv"
    )
    prevent_basic_attack_damaged: float = Field(alias="preventBasicAttackDamaged")
    prevent_basic_attack_damaged_by_lv: float = Field(
        alias="preventBasicAttackDamagedByLv"
    )
    prevent_basic_attack_damaged_ratio: float = Field(
        alias="preventBasicAttackDamagedRatio"
    )
    prevent_basic_attack_damaged_ratio_by_lv: float = Field(
        alias="preventBasicAttackDamagedRatioByLv"
    )
    increase_basic_attack_damage_ratio: float = Field(
        alias="increaseBasicAttackDamageRatio"
    )
    increase_basic_attack_damage_ratio_by_lv: float = Field(
        alias="increaseBasicAttackDamageRatioByLv"
    )
    prevent_skill_damaged: float = Field(alias="preventSkillDamaged")
    prevent_skill_damaged_by_lv: float = Field(alias="preventSkillDamagedByLv")
    prevent_skill_damaged_ratio: float = Field(alias="preventSkillDamagedRatio")
    prevent_skill_damaged_ratio_by_lv: float = Field(alias="preventSkillDamagedRatioByLv")
    penetration_defense: float = Field(alias="penetrationDefense")
    penetration_defense_ratio: float = Field(alias="penetrationDefenseRatio")
    trap_damage_reduce: float = Field(alias="trapDamageReduce")
    trap_damage_reduce_ratio: float = Field(alias="trapDamageReduceRatio")
    hp_healed_increase_ratio: float = Field(alias="hpHealedIncreaseRatio")
    healer_give_hp_heal_ratio: float = Field(alias="healerGiveHpHealRatio")
    unique_attack_range: float = Field(alias="uniqueAttackRange")
    unique_hp_healed_increase_ratio: float = Field(alias="uniqueHpHealedIncreaseRatio")
    unique_cooldown_limit: float = Field(alias="uniqueCooldownLimit")
    unique_tenacity: float = Field(alias="uniqueTenacity")
    unique_move_speed: float = Field(alias="uniqueMoveSpeed")
    unique_penetration_defense: float = Field(alias="uniquePenetrationDefense")
    unique_penetration_defense_ratio: float = Field(alias="uniquePenetrationDefenseRatio")
    unique_life_steal: float = Field(alias="uniqueLifeSteal")
    unique_skill_amp_ratio: float = Field(alias="uniqueSkillAmpRatio")
    restore_item_when_resurrected: bool = Field(alias="restoreItemWhenResurrected")
    credit_value_when_converted_to_bounty: float = Field(
        alias="creditValueWhenConvertedToBounty"
    )

    @model_validator(mode="before")
    @classmethod
    def translate_korean_name(cls, v: str, values: dict) -> str:
        name = values.get("name", "")
        if not v and name:  # Only translate if en_name is not provided
            api_key = load_api_key()
            return translate_name(name, api_key)
        return (
            v or name
        )  # If en_name is provided, use it; otherwise, use the original name

    class Config:
        populate_by_name = True

    def model_post_init(self, __context):
        if self.en_name is None:
            self.en_name = self.name  # Fallback to 'name' if translation fails


class Consumables(BaseModel):
    code: float
    name: str
    en_name: Optional[str] = None
    mode_type: float = Field(alias="modeType")
    item_type: str = Field(alias="itemType")
    consumable_type: str = Field(alias="consumableType")
    consumable_tag: str = Field(alias="consumableTag")
    item_grade: str = Field(alias="itemGrade")
    is_completed_item: bool = Field(alias="isCompletedItem")
    alert_in_spectator: bool = Field(alias="alertInSpectator")
    marking_type: str = Field(alias="markingType")
    craft_anim_trigger: str = Field(alias="craftAnimTrigger")
    stackable: float
    initial_count: float = Field(alias="initialCount")
    item_usable_type: str = Field(alias="itemUsableType")
    item_usable_value_list: Union[float, list[float]] = Field(alias="itemUsableValueList")
    exclusive_producer: float = Field(alias="exclusiveProducer")
    is_removed_from_player_corpse_inventory_when_player_killed: bool = Field(
        alias="isRemovedFromPlayerCorpseInventoryWhenPlayerKilled"
    )
    manufacturable_type: float = Field(alias="manufacturableType")
    make_material1: float = Field(alias="makeMaterial1")
    make_material2: float = Field(alias="makeMaterial2")
    heal: float
    hp_recover: float = Field(alias="hpRecover")
    sp_recover: float = Field(alias="spRecover")
    attack_power_by_buff: float = Field(alias="attackPowerByBuff")
    defense_by_buff: float = Field(alias="defenseByBuff")
    skill_amp_by_buff: float = Field(alias="skillAmpByBuff")
    skill_amp_ratio_by_buff: float = Field(alias="skillAmpRatioByBuff")
    add_state_code: float = Field(alias="addStateCode")
    is_vpad_quick_slot_item: bool = Field(alias="isVPadQuickSlotItem")
    restore_item_when_resurrected: bool = Field(alias="restoreItemWhenResurrected")
    credit_value_when_converted_to_bounty: float = Field(
        alias="creditValueWhenConvertedToBounty"
    )
    is_reduce_loot_on_death: bool = Field(alias="isReduceLootOnDeath")

    @model_validator(mode="before")
    @classmethod
    def translate_korean_name(cls, v: str, values: dict) -> str:
        name = values.get("name", "")
        if not v and name:  # Only translate if en_name is not provided
            api_key = load_api_key()
            return translate_name(name, api_key)
        return (
            v or name
        )  # If en_name is provided, use it; otherwise, use the original name

    class Config:
        populate_by_name = True

    def model_post_init(self, __context):
        if self.en_name is None:
            self.en_name = self.name  # Fallback to 'name' if translation fails


class MiscItem(BaseModel):
    code: float
    name: str
    en_name: Optional[str] = None
    mode_type: float = Field(alias="modeType")
    item_type: str = Field(alias="itemType")
    misc_item_type: str = Field(alias="miscItemType")
    item_grade: str = Field(alias="itemGrade")
    grade_bg_override: str = Field(alias="gradeBgOverride")
    is_completed_item: bool = Field(alias="isCompletedItem")
    alert_in_spectator: bool = Field(alias="alertInSpectator")
    marking_type: str = Field(alias="markingType")
    craft_anim_trigger: str = Field(alias="craftAnimTrigger")
    stackable: float
    initial_count: float = Field(alias="initialCount")
    item_usable_type: str = Field(alias="itemUsableType")
    item_usable_value_list: Union[float, list[float]] = Field(alias="itemUsableValueList")
    exclusive_producer: float = Field(alias="exclusiveProducer")
    is_removed_from_player_corpse_inventory_when_player_killed: bool = Field(
        alias="isRemovedFromPlayerCorpseInventoryWhenPlayerKilled"
    )
    manufacturable_type: float = Field(alias="manufacturableType")
    make_material1: float = Field(alias="makeMaterial1")
    make_material2: float = Field(alias="makeMaterial2")
    make_custom_action: str = Field(alias="makeCustomAction")
    restore_item_when_resurrected: bool = Field(alias="restoreItemWhenResurrected")
    credit_value_when_converted_to_bounty: float = Field(
        alias="creditValueWhenConvertedToBounty"
    )

    @model_validator(mode="before")
    @classmethod
    def translate_korean_name(cls, v: str, values: dict) -> str:
        name = values.get("name", "")
        if not v and name:  # Only translate if en_name is not provided
            api_key = load_api_key()
            return translate_name(name, api_key)

    class Config:
        populate_by_name = True

    def model_post_init(self, __context):
        if self.en_name is None:
            self.en_name = self.name  # Fallback to 'name' if translation fails


class SpawnItem(BaseModel):
    code: float
    area_code: float = Field(alias="areaCode")
    area_spawn_group: float = Field(alias="areaSpawnGroup")
    item_code: float = Field(alias="itemCode")
    drop_point: str = Field(alias="dropPoint")
    drop_count: float = Field(alias="dropCount")

    class Config:
        populate_by_name = True


class SpecialItem(BaseModel):
    code: float
    name: str
    en_name: Optional[str] = None
    mode_type: float = Field(alias="modeType")
    item_type: str = Field(alias="itemType")
    special_item_type: str = Field(alias="specialItemType")
    item_grade: str = Field(alias="itemGrade")
    is_completed_item: bool = Field(alias="isCompletedItem")
    alert_in_spectator: bool = Field(alias="alertInSpectator")
    marking_type: str = Field(alias="markingType")
    craft_anim_trigger: str = Field(alias="craftAnimTrigger")
    stackable: float
    initial_count: float = Field(alias="initialCount")
    cooldown_group_code: float = Field(alias="cooldownGroupCode")
    cooldown: float
    item_usable_type: str = Field(alias="itemUsableType")
    item_usable_value_list: Union[float, list[float]] = Field(alias="itemUsableValueList")
    exclusive_producer: float = Field(alias="exclusiveProducer")
    is_removed_from_player_corpse_inventory_when_player_killed: bool = Field(
        alias="isRemovedFromPlayerCorpseInventoryWhenPlayerKilled"
    )
    manufacturable_type: float = Field(alias="manufacturableType")
    make_material1: float = Field(alias="makeMaterial1")
    make_material2: float = Field(alias="makeMaterial2")
    make_custom_action: str = Field(alias="makeCustomAction")
    consume_count: float = Field(alias="consumeCount")
    summon_code: float = Field(alias="summonCode")
    ghost_item_state_group: float = Field(alias="ghostItemStateGroup")
    is_vpad_quick_slot_item: bool = Field(alias="isVPadQuickSlotItem")
    restore_item_when_resurrected: bool = Field(alias="restoreItemWhenResurrected")
    credit_value_when_converted_to_bounty: float = Field(
        alias="creditValueWhenConvertedToBounty"
    )
    is_reduce_loot_on_death: bool = Field(alias="isReduceLootOnDeath")

    @model_validator(mode="before")
    @classmethod
    def translate_korean_name(cls, v: str, values: dict) -> str:
        name = values.get("name", "")
        if not v and name:  # Only translate if en_name is not provided
            api_key = load_api_key()
            return translate_name(name, api_key)
        return v or name

    class Config:
        populate_by_name = True

    def model_post_init(self, __context):
        if self.en_name is None:
            self.en_name = self.name  # Fallback to 'name' if translation fails


class Weapon(BaseModel):
    code: float
    name: str
    en_name: Optional[str] = None
    mode_type: float = Field(alias="modeType")
    item_type: str = Field(alias="itemType")
    weapon_type: str = Field(alias="weaponType")
    item_grade: str = Field(alias="itemGrade")
    grade_bg_override: str = Field(alias="gradeBgOverride")
    is_completed_item: bool = Field(alias="isCompletedItem")
    alert_in_spectator: bool = Field(alias="alertInSpectator")
    marking_type: str = Field(alias="markingType")
    craft_anim_trigger: str = Field(alias="craftAnimTrigger")
    stackable: float
    initial_count: float = Field(alias="initialCount")
    item_usable_type: str = Field(alias="itemUsableType")
    item_usable_value_list: Union[float, list[float]] = Field(alias="itemUsableValueList")
    exclusive_producer: float = Field(alias="exclusiveProducer")
    is_removed_from_player_corpse_inventory_when_player_killed: bool = Field(
        alias="isRemovedFromPlayerCorpseInventoryWhenPlayerKilled"
    )
    make_material1: float = Field(alias="makeMaterial1")
    make_material2: float = Field(alias="makeMaterial2")
    make_custom_action: str = Field(alias="makeCustomAction")
    not_disarm: bool = Field(alias="notDisarm")
    consumable: bool
    manufacturable_type: float = Field(alias="manufacturableType")
    attack_power: float = Field(alias="attackPower")
    attack_power_by_lv: float = Field(alias="attackPowerByLv")
    defense: float
    defense_by_lv: float = Field(alias="defenseByLv")
    skill_amp: float = Field(alias="skillAmp")
    skill_amp_by_level: float = Field(alias="skillAmpByLevel")
    skill_amp_ratio: float = Field(alias="skillAmpRatio")
    skill_amp_ratio_by_level: float = Field(alias="skillAmpRatioByLevel")
    adaptive_force: float = Field(alias="adaptiveForce")
    adaptive_force_by_level: float = Field(alias="adaptiveForceByLevel")
    max_hp: float = Field(alias="maxHp")
    max_hp_by_lv: float = Field(alias="maxHpByLv")
    hp_regen_ratio: float = Field(alias="hpRegenRatio")
    hp_regen: float = Field(alias="hpRegen")
    max_sp: float = Field(alias="maxSP")
    sp_regen_ratio: float = Field(alias="spRegenRatio")
    sp_regen: float = Field(alias="spRegen")
    attack_speed_ratio: float = Field(alias="attackSpeedRatio")
    attack_speed_ratio_by_lv: float = Field(alias="attackSpeedRatioByLv")
    critical_strike_chance: float = Field(alias="criticalStrikeChance")
    critical_strike_damage: float = Field(alias="criticalStrikeDamage")
    cooldown_reduction: float = Field(alias="cooldownReduction")
    prevent_critical_strike_damaged: float = Field(alias="preventCriticalStrikeDamaged")
    cooldown_limit: float = Field(alias="cooldownLimit")
    life_steal: float = Field(alias="lifeSteal")
    normal_life_steal: float = Field(alias="normalLifeSteal")
    skill_life_steal: float = Field(alias="skillLifeSteal")
    move_speed: float = Field(alias="moveSpeed")
    move_speed_out_of_combat: float = Field(alias="moveSpeedOutOfCombat")
    sight_range: float = Field(alias="sightRange")
    attack_range: float = Field(alias="attackRange")
    increase_basic_attack_damage: float = Field(alias="increaseBasicAttackDamage")
    increase_basic_attack_damage_by_lv: float = Field(
        alias="increaseBasicAttackDamageByLv"
    )
    increase_basic_attack_damage_ratio: float = Field(
        alias="increaseBasicAttackDamageRatio"
    )
    increase_basic_attack_damage_ratio_by_lv: float = Field(
        alias="increaseBasicAttackDamageRatioByLv"
    )
    prevent_basic_attack_damaged: float = Field(alias="preventBasicAttackDamaged")
    prevent_basic_attack_damaged_by_lv: float = Field(
        alias="preventBasicAttackDamagedByLv"
    )
    prevent_basic_attack_damaged_ratio: float = Field(
        alias="preventBasicAttackDamagedRatio"
    )
    prevent_basic_attack_damaged_ratio_by_lv: float = Field(
        alias="preventBasicAttackDamagedRatioByLv"
    )
    prevent_skill_damaged: float = Field(alias="preventSkillDamaged")
    prevent_skill_damaged_by_lv: float = Field(alias="preventSkillDamagedByLv")
    prevent_skill_damaged_ratio: float = Field(alias="preventSkillDamagedRatio")
    prevent_skill_damaged_ratio_by_lv: float = Field(alias="preventSkillDamagedRatioByLv")
    penetration_defense: float = Field(alias="penetrationDefense")
    penetration_defense_ratio: float = Field(alias="penetrationDefenseRatio")
    trap_damage_reduce: float = Field(alias="trapDamageReduce")
    trap_damage_reduce_ratio: float = Field(alias="trapDamageReduceRatio")
    hp_healed_increase_ratio: float = Field(alias="hpHealedIncreaseRatio")
    healer_give_hp_heal_ratio: float = Field(alias="healerGiveHpHealRatio")
    unique_attack_range: float = Field(alias="uniqueAttackRange")
    unique_hp_healed_increase_ratio: float = Field(alias="uniqueHpHealedIncreaseRatio")
    unique_cooldown_limit: float = Field(alias="uniqueCooldownLimit")
    unique_tenacity: float = Field(alias="uniqueTenacity")
    unique_move_speed: float = Field(alias="uniqueMoveSpeed")
    unique_penetration_defense: float = Field(alias="uniquePenetrationDefense")
    unique_penetration_defense_ratio: float = Field(
        alias="uniquePenetrationDefenseRatio"
    )
    unique_life_steal: float = Field(alias="uniqueLifeSteal")
    unique_skill_amp_ratio: float = Field(alias="uniqueSkillAmpRatio")
    restore_item_when_resurrected: bool = Field(alias="restoreItemWhenResurrected")
    credit_value_when_converted_to_bounty: float = Field(
        alias="creditValueWhenConvertedToBounty"
    )

    @model_validator(mode="after")
    def translate_korean_name(self) -> None:
        if not self.en_name and self.name:
            api_key = load_api_key()
            self.en_name = translate_name(self.name, api_key)
            print(f"Translated {self.name} to {self.en_name}")

    class Config:
        populate_by_name = True


class Monster(BaseModel):
    code: float = Field(alias="Code")
    monster: str
    en_name: Optional[str] = None
    is_mutant: bool = Field(alias="isMutant")
    grade: str
    mode: float
    create_day: str = Field(alias="createDay")
    create_time: float = Field(alias="createTime")
    regen_time: float = Field(alias="regenTime")
    level_up_period: float = Field(alias="levelUpPeriod")
    level_up_amount: float = Field(alias="levelUpAmount")
    level_up_max: float = Field(alias="levelUpMax")
    max_hp: float = Field(alias="maxHp")
    max_ep: float = Field(alias="maxEp")
    init_extra_point: float = Field(alias="initExtraPoint")
    attack_power: float = Field(alias="attackPower")
    defense: float
    attack_speed: float = Field(alias="attackSpeed")
    move_speed: float = Field(alias="moveSpeed")
    sight_range: float = Field(alias="sightRange")
    chasing_range: float = Field(alias="chasingRange")
    attack_range: float = Field(alias="attackRange")
    first_attack_range: float = Field(alias="firstAttackRange")
    aggressive: str
    detect_invisible: bool = Field(alias="detectInvisible")
    radius: float
    pathing_radius: float = Field(alias="pathingRadius")
    ui_height: float = Field(alias="uiHeight")
    gain_exp: float = Field(alias="gainExp")
    target_on_range: float = Field(alias="targetOnRange")
    random_drop_count: float = Field(alias="randomDropCount")
    resource: str
    corpse_resource: str = Field(alias="corpseResource")
    appear_time: float = Field(alias="appearTime")

    @model_validator(mode="after")
    @classmethod
    def translate_korean_name(cls, v: str, values: dict) -> str:
        name = values.get("monster", "")
        if not v and name:  # Only translate if en_name is not provided
            api_key = load_api_key()
            return translate_name(name, api_key)
        return v or name

    class Config:
        populate_by_name = True

    def model_post_init(self, __context):
        if self.en_name is None:
            self.en_name = self.monster  # Fallback to 'monster' if translation fails


class MonsterDropGroup(BaseModel):
    monster_code: float = Field(alias="monsterCode")
    monster_level: float = Field(alias="monsterLevel")
    drop_group: float = Field(alias="dropGroup")

    class Config:
        populate_by_name = True


class DropGroup(BaseModel):
    group_code: float = Field(alias="groupCode")
    item_code: float = Field(alias="itemCode")
    min: float
    max: float
    probability: float
    drop_type: str = Field(alias="dropType")


class WeaponType(BaseModel):
    weapon_type: str = Field(alias="type")
    attack_speed: float = Field(alias="attackSpeed")
    attack_range: float = Field(alias="attackRange")
    shop_filter: float = Field(alias="shopFilter")
    summon_object_hit_damage: float = Field(alias="summonObjectHitDamage")

    class Config:
        populate_by_name = True
