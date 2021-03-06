import json
import re

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from room.models import Room
from user.models import User, Session
from user.serializers import UserSerializer, SessionSerializer, UserSessionSerializer


class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self, sessions={}):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_id = await self.get_room_id()
		self.session_key = self.scope["cookies"]["sessionid"]
		self.user_nickname = await self.get_user_nickname()
		self.room_group_name = f'chat_{self.room_name}'
		self.color_user_in_list = await self.define_user_color_in_list()
		self.user_data = [self.session_key, 
			self.user_nickname, 
			self.color_user_in_list, 
		]

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()

		try:
			sessions[self.room_name].append(self.user_data)
		except KeyError as ex:
			sessions[self.room_name] = [self.user_data, ]

		number_users = self.number_users_in_room(sessions)

		# send current number users in room
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_visitors',
				'value': number_users,
				'isIncrement': False
			}
		)

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'system_message',
				'message': f"{self.user_nickname} joined the room"
			}
		)

		for session in sessions[self.room_name]:
			await self.channel_layer.group_send(
				self.room_group_name,
				{
					'type': 'update_user_list',
					'userId': session[0],
					'userNickname': session[1],
					'userColor': session[2],
					'isAdd': 1
				}
			)

		# upload saved messages to WebSocket
		if self.receive.__defaults__[0]:
			for message in self.receive.__defaults__[0]:
				if message[0] == self.room_name:
					await self.send(text_data=json.dumps({
						'message': message[1],
						'author': message[2],
						'color': message[3],
					}))

	async def disconnect(self, close_code):
		sessions = self.connect.__defaults__[0][self.room_name]
		sessions.remove(self.user_data)

		# sending a new users counter state
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_visitors',
				'value': -1,
				'isIncrement': True
			}
		)

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'system_message',
				'message': f"{self.user_nickname} left the room"
			}
		)

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'update_user_list',
				'userNickname': self.user_nickname,
				'userId': self.session_key,
				'userColor': self.color_user_in_list,
				'isAdd': 0
			}
		)
		
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def receive(self, text_data, messages=[]):
		''' Receive message from WebSocket '''
		text_data_json = json.loads(text_data)
		message_type = text_data_json["type"]
		message = text_data_json['message']
		author = text_data_json['author']
		color = text_data_json['color']

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': message_type,
				'message': message,
				'author': author,
				'color': color,
			}
		)

		if message_type != "system_message":
			messages.append([self.room_name, message, author, color])

	async def chat_message(self, event):
		''' Receive message from room group '''
		message = event['message']
		author = event['author']
		color = event['color']

		await self.send(text_data=json.dumps({
			'message': message, 
			'author': author,
			'color': color,
		}))

	async def chat_visitors(self, event):
		''' Receive number visitors from room group '''
		value = event['value']
		is_increment = event["isIncrement"]

		await self.send(text_data=json.dumps({
			'type': "visitors",
			'value': value,
			'isIncrement': is_increment
		}))

	async def system_message(self, event):
		''' Receive system messages from room group '''
		message = event['message']

		await self.send(text_data=json.dumps({
			'type': "system_message",
			'message': message
		}))

	async def update_user_list(self, event):
		''' Receive a message about updating the list of users from room group '''
		user_nickname = event['userNickname']
		user_id = event['userId']
		user_color = event['userColor']
		is_add = event["isAdd"]

		await self.send(text_data=json.dumps({
			'type': "update_user_list",
			'userNickname': user_nickname,
			'userId': user_id,
			'userColor': user_color,
			'isAdd': is_add
		}))

	def number_users_in_room(self, sessions):
		number_users = len(sessions[self.room_name])
		return number_users

	@database_sync_to_async
	def get_room_id(self):
		return Room.objects.filter(code=self.room_name)[0].id

	@database_sync_to_async
	def get_user_nickname(self):
		session_id = Session.objects.filter(session_key=self.session_key)[0].id
		user_nickname = User.objects.filter(session=session_id, room=self.room_id)[0].user_nickname
		return user_nickname

	@database_sync_to_async
	def define_user_color_in_list(self):
		session_id = Session.objects.filter(session_key=self.session_key)[0].id
		user_status = User.objects.filter(session=session_id, room=self.room_id)[0].user_status
		
		if user_status == "HO":
			user_color = "#4b0b0b"
		elif user_status == "MO":
			user_color = "#503704"
		else:
			user_color = "#383838"

		return user_color
