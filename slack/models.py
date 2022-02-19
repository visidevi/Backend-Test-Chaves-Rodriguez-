"""Slack Models Integration"""
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str
    username: str
    name: str
    team_id: str


class Container(BaseModel):
    type: str
    message_ts: str
    channel_id: str
    is_ephemeral: bool


class Team(BaseModel):
    id: str
    domain: str


class Channel(BaseModel):
    id: str
    name: str


class Text(BaseModel):
    type: str
    text: str
    emoji: Optional[bool]
    verbatim: Optional[bool]


class SelectedOption(BaseModel):
    text: Text
    value: str


class Label(BaseModel):
    type: str
    text: str
    emoji: bool


class Option(BaseModel):
    text: Text
    value: str


class Placeholder(BaseModel):
    type: str
    text: str
    emoji: bool


class DispatchActionConfig(BaseModel):
    trigger_actions_on: List[str]


class Element(BaseModel):
    type: str
    action_id: str
    options: Optional[List[Option]] = None
    placeholder: Optional[Placeholder] = None
    dispatch_action_config: Optional[DispatchActionConfig] = None


class Block(BaseModel):
    type: str
    block_id: str
    text: Optional[Text] = None
    label: Optional[Label] = None
    optional: Optional[bool] = None
    dispatch_action: Optional[bool] = None
    element: Optional[Element] = None


class Message(BaseModel):
    bot_id: str
    type: str
    text: str
    user: str
    ts: str
    team: str
    blocks: List[Block]


class RadioButtonsAction(BaseModel):
    type: str
    selected_option: SelectedOption


class Options(BaseModel):
    radio_buttons_action: RadioButtonsAction = Field(
        ..., alias='radio_buttons-action')


class PlainTextInputAction(BaseModel):
    type: str
    value: Any


class Customizations(BaseModel):
    plain_text_input_action: PlainTextInputAction = Field(
        ..., alias='plain_text_input-action'
    )


class Values(BaseModel):
    options: Optional[Options]
    customizations: Optional[Customizations]


class State(BaseModel):
    values: Values


class Action(BaseModel):
    action_id: str
    block_id: str
    selected_option: Optional[SelectedOption]
    type: str
    action_ts: str
    value: Optional[str]


class Payload(BaseModel):
    type: Optional[str] = None
    user: Optional[User] = None
    api_app_id: Optional[str] = None
    token: Optional[str] = None
    container: Optional[Container] = None
    trigger_id: Optional[str] = None
    team: Optional[Team] = None
    enterprise: Optional[Any] = None
    is_enterprise_install: Optional[bool] = None
    channel: Optional[Channel] = None
    message: Optional[Message] = None
    state: Optional[State] = None
    response_url: Optional[str] = None
    actions: Optional[List[Action]] = None
