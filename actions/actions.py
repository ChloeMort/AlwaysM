# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")


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
    """Greets the user with/without privacy policy."""

    def name(self) -> Text:
        return "action_greet_user"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        intent = tracker.latest_message["intent"].get("name")
        shown_privacy = tracker.get_slot("shown_privacy")
        name_entity = next(tracker.get_latest_entity_values("name"), None)
        if intent == "greet" or (intent == "enter_data" and name_entity):
            if shown_privacy and name_entity and name_entity.lower() != "sara":
                dispatcher.utter_message(response="utter_greet_name", name=name_entity)
                return []
            elif shown_privacy:
                dispatcher.utter_message(response="utter_greet_noname")
                return []
            else:
                dispatcher.utter_message(response="utter_greet")
        return []

class ActionRestartWithButton(Action):
    def name(self) -> Text:
        return "action_restart_with_button"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> None:

        dispatcher.utter_message(template="utter_restart_with_button")




class ActionQueryUser(Action):
    def name(self) -> Text:
        return "action_query_user"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> None:

        if session.query(User).filter(User.id_num == tracker.getslot('user_id')).first():
            dispatcher.utter_message(response="utter_exist_user")
        else:
            dispatcher.utter_message(response="utter_no_user")

class ActionQueryShop(Action):
    def name(self) -> Text:
        return "action_query_shop"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> None:

        if session.query(Shop).filter(Shop.location == tracker.getslot('user_location')).all():
            dispatcher.utter_message(response="utter_exist_shop")
            for row in session.query(Shop).filter(Shop.location == tracker.getslot('user_location')).all():
                text = row.name + "in" + row.location + "is available from " + row.open_time + " to " + row.close_time + '.'
                dispatcher.utter_message(text=text)
        else:
            dispatcher.utter_message(response="utter_no_shop")

class ActionQueryPlan(Action):
    def name(self) -> Text:
        return "action_query_plan"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> None:
        if tracker.getslot('generation') == 'all' and tracker.getslot('pay_method') == 'both':
            res = session.query(Plan).all()
            for row in res:
                text = row.name + "\t" + row.generation + "\t" + row.pay_method + "\t" + str(row.price) + '\n' + row.description
                dispatcher.utter_message(text='The available plans are:\n' + text)
        elif tracker.getslot('generation') == 'all':
            res = session.query(Plan).filter(Plan.pay_method == tracker.getslot('pay_method')).all()
            for row in res:
                text = row.name + "\t" + row.generation + "\t" + row.pay_method + "\t" + str(row.price) + '\n' + row.description
                dispatcher.utter_message(text='The available plans are:\n' + text)
        elif session.query(Plan).filter(Plan.pay_method == tracker.getslot('pay_method') and Plan.generation == tracker.getslot('generation')).all():
                dispatcher.utter_message(response="utter_no_plan")
        else:
            res = session.query(Plan).filter(Plan.pay_method == tracker.getslot('pay_method') and Plan.generation == tracker.getslot('generation')).all()
            for row in res:
                text = row.name + "\t" + row.generation + "\t" + row.pay_method + "\t" + str(row.price) + '\n' + row.description
                dispatcher.utter_message(text=f"The available plans are:\n" + text)


class ValidateSimForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_sim_form"

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

        if session.query(SIM).filter(SIM.phone_num == tracker.getslot('phone_num') and SIM.user_id == tracker.getslot('user_id')).first():
            for row in session.query(SIM).filter(SIM.phone_num == tracker.getslot('phone_num') and SIM.user_id == tracker.getslot('user_id')).first():
                boo = row.status
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
            session.query(SIM).filter(SIM.phone_num == tracker.getslot('phone_num') and SIM.user_id == tracker.getslot('user_id')).update({'status':0})
            dispatcher.utter_message(text =f"Your SIM card is now frozen.")
        except:
            dispatcher.utter_message(text="There is something wrong with you phone number or ID.")