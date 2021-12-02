from typing import Any, Dict, List, Text, Optional
import sqlalchemy as sa
from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    ConversationPaused,
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
    UserUtteranceReverted,
)
from actions.profile_db import User, Shop, SIM, Plan, Grievance
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import sessionmaker

engine=create_engine('sqlite:///am.db')
Base=declarative_base()
Session=sessionmaker(bind=engine)
session=Session()

class ActionGreetUser(Action):
    def name(self) -> Text:
        return "action_greet_user"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        name_entity = tracker.get_slot("user_name")
        if name_entity:
            dispatcher.utter_message(response="utter_greet_name")
        else:
            dispatcher.utter_message(response="utter_greet_noname")
        return []



class ValidateUserForm(FormValidationAction):
    def name(self) -> Text:
        return "action_validate_user_form"

    def validate_user_id(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `user_id` value."""

        if len(slot_value) == 0:
            dispatcher.utter_message(text=f"You need to enter your ID number")
            return {"user_id": None}
        dispatcher.utter_message(text=f"Your ID number is {slot_value}.")
        return {"user_id": slot_value}

class AskUserID(Action):
    def name(self) -> Text:
        return "action_ask_user_id"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(text="What is your Id Number?")
        return []

class ActionQueryUser(Action):
    def name(self) -> Text:
        return "action_query_user"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> None:
        if tracker.get_slot('user_id'):
            if session.query(User).filter(User.id_num == tracker.get_slot('user_id')).first():
                dispatcher.utter_message(response="utter_exist_user")
            else:
                dispatcher.utter_message(response="utter_no_user")
        else:
            dispatcher.utter_message(response="utter_no_user")


class ValidateShopForm(FormValidationAction):
    def name(self) -> Text:
        return "action_validate_shop_form"

    def validate_shop_city(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `shop_city` value."""

        if len(slot_value) == 0:
            dispatcher.utter_message(text=f"You need to enter city to search shops.")
            return {"shop_city": None}
        dispatcher.utter_message(text=f"Your ID number is {slot_value}.")
        return {"shop_city": slot_value}

class ActionQueryShop(Action):
    def name(self) -> Text:
        return "action_query_shop"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> None:
        res = session.query(Shop).filter(Shop.location == tracker.get_slot('shop_city').lower()).all()
        if res:
            dispatcher.utter_message(response="utter_exist_shop")
            for row in res:
                text = row.name + " in " + row.location + " is available from " + row.open_time + " to " + row.close_time + '.'
                dispatcher.utter_message(text=text)
        else:
            dispatcher.utter_message(response="utter_no_shop")
            # return {"shop_city": None}

class ActionQueryPlan(Action):
    def name(self) -> Text:
        return "action_query_plan"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> None:
        if tracker.get_slot('generation') == 'all' and tracker.get_slot('pay_method') == 'both' and session.query(Plan).all():
            dispatcher.utter_message(text=f"The available plans are:\nName\tGeneration\tpay methods\tPrice")
            res = session.query(Plan).all()
            for row in res:
                text = row.name + "\t" + row.generation + "\t" + row.pay_method + "\t" + str(row.price) + '\nDescription:' + row.description
                dispatcher.utter_message(text = text)
        elif tracker.get_slot('generation') == 'all' and session.query(Plan).filter(Plan.pay_method == tracker.get_slot('pay_method').lower()).all():
            dispatcher.utter_message(text=f"The available plans are:\nName\tGeneration\tpay methods\tPrice")
            res = session.query(Plan).filter(Plan.pay_method == tracker.get_slot('pay_method').lower()).all()
            for row in res:
                text = row.name + "\t" + row.generation + "\t" + row.pay_method + "\t" + str(row.price) + '\nDescription' + row.description
                dispatcher.utter_message(text=text)
        elif session.query(Plan).filter(Plan.pay_method == tracker.get_slot('pay_method').lower() and Plan.generation == tracker.get_slot('generation').lower()).all():
            res = session.query(Plan).filter(Plan.pay_method == tracker.get_slot('pay_method').lower() and Plan.generation == tracker.get_slot('generation').lower()).all()
            for row in res:
                text = row.name + "\t" + row.generation + "\t" + row.pay_method + "\t" + str(row.price) + '\nDescription' + row.description
                dispatcher.utter_message(text=text)
        else:
            dispatcher.utter_message(response="utter_no_plan")



class ValidateSimForm(FormValidationAction):
    def name(self) -> Text:
        return "action_validate_sim_form"

    def validate_phone_num(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `phone_num` value."""

        if len(slot_value) == 0:
            dispatcher.utter_message(text=f"You need to enter a phone number")
            return {"phone_num": None}
        dispatcher.utter_message(text=f"Your phone number is {slot_value}.")
        return {"phone_num": slot_value}

    def validate_user_id(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `user_id` value."""

        if len(slot_value) == 0:
            dispatcher.utter_message(text=f"You need to enter an ID number")
            return {"user_id": None}
        dispatcher.utter_message(text=f"Your ID number is {slot_value}.")
        return {"user_id": slot_value}
    
    
class ActionQuerySim(Action):
    def name(self) -> Text:
        return "action_query_sim"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> None:

        if session.query(SIM).filter(SIM.phone_num == tracker.get_slot('phone_num') and SIM.user_id == tracker.get_slot('user_id')).first():
            boo = session.query(SIM).filter(SIM.phone_num == tracker.get_slot('phone_num') and SIM.user_id == tracker.get_slot('user_id')).first().status
            if boo == 0:
                dispatcher.utter_message(text =f"Your SIM card is frozen now.")
            else:
                dispatcher.utter_message(text =f"Your SIM card is now in use.")
        else:
            dispatcher.utter_message(text="There is something wrong with you phone number or ID.")


class ActionUpdateSim(Action):
    def name(self) -> Text:
        return "action_update_sim"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> None:

        try:
            session.query(SIM).filter(SIM.phone_num == tracker.get_slot('phone_num') and SIM.user_id == tracker.get_slot('user_id')).update({'status':0})
            dispatcher.utter_message(text =f"Your SIM card is now frozen.")
        except:
            dispatcher.utter_message(text="There is something wrong with you phone number or ID.")