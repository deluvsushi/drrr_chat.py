import requests
from datetime import datetime

class DrrrChat:
	def __init__(self) -> None:
		self.api = "https://drrr.chat"
		self.headers = {
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
		self.token = None
		self.user_id = None
		self.get_cookies()
		
	def get_cookies(self) -> None:
		response = requests.get(self.api, headers=self.headers)
		self.flarum_session = response.cookies["flarum_session"]
		self.csrf_token = response.headers["X-CSRF-Token"]
		self.headers["cookie"] = f"flarum_session={self.flarum_session}"
		self.headers["x-csrf-token"] = self.csrf_token
		
	def login(
			self,
			email: str,
			password: str,
			remember: bool = True) -> dict:
		data = {
			"identification": email,
			"password": password,
			"remember": remember
		}
		response = requests.post(
			f"{self.api}/login",
			data=data,
			headers=self.headers)
		json = response.json()
		cookies = response.cookies
		if "token" in json:
			self.token = json["token"]
			self.user_id = json["userId"]
			self.flarum_session = cookies["flarum_session"]
			self.flarum_remember = cookies["flarum_remember"]
			self.headers["x-csrf-token"] = self.csrf_token
			self.headers["cookie"] = f"flarum_remember={self.flarum_remember}; flarum_session={self.flarum_session}"
		return json

	def register(
			self,
			email: str,
			password: str,
			username: str) -> dict:
		data = {
			"email": email,
			"password": password,
			"username": username
		}
		return requests.post(
			f"{self.api}/register",
			data=data,
			headers=self.headers).json()

	def send_confirmation_code(self, user_id: int) -> dict:
		return requests.post(
			f"{self.api}/api/users/{user_id}/send-confirmation",
			headers=self.headers).json()

	def forgot_password(self, email: str) -> dict:
		data = {
			"email": email
		}
		return requests.post(
			f"{self.api}/api/forgot",
			data=data,
			headers=self.headers).json()

	def change_email(
			self,
			email: str,
			password: str) -> dict:
		data = {
			"data": {
				"type": "users",
				"id": self.user_id,
				"attributes": {"email": email}
			},
			"meta": {"password": password}
		}
		return requests.post(
			f"{self.api}/api/users/{self.user_id}",
			data=data,
			headers=self.headers).json()

	def get_discussions(
			self,
			offset: int = 0,
			include: str = "user,lastPostedUser,tags,tags.parent,firstPost") -> dict:
		return requests.get(
			f"{self.api}/api/discussions?include={include}&sort&page[offset]={offset}", 
			headers=self.headers).json()

	def get_announcements(
			self,
			offset: int = 0,
			include: str = "user,lastPostedUser,tags,tags.parent,firstPost",
			tag: str = "announcement") -> dict:
		return requests.get(
			f"{self.api}/api/discussions?include={include}&filter[tag]={tag}&sort&page[offset]={offset}",
			headers=self.headers).json()

	def get_following(
			self,
			offset: int = 0,
			include: str = "user,lastPostedUser,tags,tags.parent,firstPost") -> dict:
		return requests.get(
			f"{self.api}/api/discussions?include={include}&filter[subscription]=following&sort&page[offset]={offset}",
			headers=self.headers).json()

	def create_discussion(
			self,
			title: str, 
			content: str, 
			tag_id: int = 20) -> dict:
		data = {
			"data": {
				"type": "discussions", 
				"attributes": {
					"title": title,
					"content": content
				},
				"relationships": {
					"tags": {
						"data": [
							{
								"type": "tags", 
								"id": tag_id
							}
						]
					}
				}
			}
		}
		return requests.post(
			f"{self.api}/api/discussions",
			data=data,
			headers=self.headers).json()
	
	def get_notifications(self) -> dict:
		return requests.get(
			f"{self.api}/api/notifications",
			headers=self.headers).json()

	def get_discussion(
			self,
			discussion_id: int,
			last_read_post_number: int = 1) -> dict:
		data = {
			"data": {
				"type": "discussions",
				"attributes": {
					"lastReadPostNumber": last_read_post_number
				},
				"id": discussion_id
			}
		}
		return requests.post(
			f"{self.api}/api/discussions/{discussion_id}",
			data=data,
			headers=self.headers).json()

	def follow_discussion(self, discussion_id: int) -> dict:
		data = {
			"data": {
				"type": "discussions",
				"attributes": {
					"subscription": "follow"
				},
				"id": discussion_id
			}
		}
		return requests.post(
			f"{self.api}/api/discussions/{discussion_id}",
			data=data,
			headers=self.headers).json()

	def unfollow_discussion(self, discussion_id: int) -> dict:
		data = {
			"data": {
				"type": "discussions",
				"attributes": {
					"subscription": None
				},
				"id": discussion_id
			}
		}
		return requests.post(
			f"{self.api}/api/discussions/{discussion_id}",
			data=data,
			headers=self.headers).json()

	def ignore_discussion(self, discussion_id: int) -> dict:
		data = {
			"data": {
				"type": "discussions",
				"attributes": {
					"subscription": "ignore"
				},
				"id": discussion_id
			}
		}
		return requests.post(
			f"{self.api}/api/discussions/{discussion_id}",
			data=data,
			headers=self.headers).json()

	def get_user_posts(
			self,
			username: str,
			type: str = "comment",
			offset: int = 20,
			limit: int = 20,
			sort: str = "-createdAt") -> dict:
		return requests.get(
			f"{self.api}/api/posts?filter[author]={username}&filter[type]={type}&page[offset]={offset}&page[limit]={limit}&sort={sort}",
			headers=self.headers).json()

	def get_user_discussions(
			self,
			username: str,
			include: str = "user,lastPostedUser,tags,tags.parent",
			sort: str = "-createdAt",
			offset: int = 0) -> dict:
		return requests.get(
			f"{self.api}/api/discussions?include={include}&filter[author]={username}&sort={sort}&page[offset]={offset}",
			headers=self.headers).json()

	def get_user_mentions(
			self,
			user_id: int,
			type: str = "comment",
			offset: int = 20,
			limit: int = 20,
			sort: str = "-createdAt") -> dict:
		return requests.get(
			f"{self.api}/api/posts?filter[type]={type}&filter[mentioned]={user_id}&page[offset]={offset}&page[limit]={limit}&sort={sort}",
			headers=self.headers).json()

	def get_user_info(self, user_id: int) -> dict:
		return requests.get(
			f"{self.api}/api/users/{user_id}",
			headers=self.headers).json()

	def comment_discussion(
			self,
			discussion_id: int,
			content: str) -> dict:
		data = {
			"data": {
				"type": "posts",
				"attributes": {
					"content": content
				},
				"relationships": {
					"discussion": {
						"data": {
							"type": "discussions",
							"id": discussion_id
						}
					}
				}
			}
		}
		return requests.post(
			f"{self.api}/api/posts",
			data=data,
			headers=self.headers).json()

	def search_user(self, query: str, limit: int = 5) -> dict:
		return requests.get(
			f"{self.api}/api/users?filter[q]={query}&page[limit]={limit}",
			headers=self.headers).json()

	def search_discussion(
			self,
			query: str,
			limit: int = 5,
			include: str = "mostRelevantPost") -> dict:
		return requests.get(
			f"{self.api}/api/discussions?filter[q]={query}&page[limit]={limit}&include={include}",
			headers=self.headers).json()

	def mark_all_discussions_read(self) -> dict:
		data = {
			"data": {
				"type": "users",
				"attributes": {
					"markedAllAsReadAt": f"{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"
				},
				"id": self.user_id
			}
		}
		return requests.post(
			f"{self.api}/api/users/{user_id}",
			data=data,
			headers=self.headers).json()

