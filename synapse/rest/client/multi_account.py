# Copyright 2015, 2016 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from typing import TYPE_CHECKING, Optional, Tuple

from synapse.api.errors import AuthError, NotFoundError, StoreError
from synapse.http.server import HttpServer
from synapse.http.servlet import RestServlet, parse_json_object_from_request
from synapse.http.site import SynapseRequest
from synapse.types import JsonDict, UserID

from ._base import client_patterns

if TYPE_CHECKING:
    from synapse.server import HomeServer

logger = logging.getLogger(__name__)


class MultiAccountServlet(RestServlet):
    """
    GET /user/multi_account HTTP/1.1
    POST /user/multi_account HTTP/1.1
    """

    PATTERNS = client_patterns(
        "/user/multi_account",
        releases=("v3", "r0"),
        v1=True
    )
    CATEGORY = "Multi account requests"

    def __init__(self, hs: "HomeServer"):
        super().__init__()
        self._hs = hs
        self.auth = hs.get_auth()
        self.store = hs.get_datastores().main
        self.handler = hs.get_account_data_handler()
        self._push_rules_handler = hs.get_push_rules_handler()

    async def on_GET(
        self, request: SynapseRequest,
    ) -> Tuple[int, JsonDict]:
        requester = await self.auth.get_user_by_req(request)
        user_id = requester.user.to_string()
        multi_account = await self.store.get_multi_account(user_id=user_id)
        if multi_account is None:
            raise NotFoundError("Multi account not found")
        multi_account_id = multi_account["multi_account_id"]
        multi_account_users = await self.store.get_multi_account_info(multi_account_id)
        result = []
        for user in multi_account_users:
            if user["user_id"] == user_id:
                continue
            entry_user_id = UserID.from_string(user["user_id"])
            entry_profileinfo = await self.store.get_profileinfo(entry_user_id)
            rooms_ids = await self.store.get_rooms_for_user(user["user_id"])
            unread_count = 0
            for room_id in rooms_ids:
                room_counts = await self.store.get_unread_event_push_actions_by_room_for_user(room_id=room_id, user_id=user["user_id"])
                unread_count += room_counts.main_timeline.unread_count
            result.append({
                "display_name": entry_profileinfo.display_name, 
                "avatar_url": entry_profileinfo.avatar_url,
                "unread_count": unread_count
                }
            )
        return 200, result
    
    async def on_POST(
        self, request: SynapseRequest,
    ) -> Tuple[int, JsonDict]:
        # get users for multi-account
        requester = await self.auth.get_user_by_req(request)
        user_id = requester.user.to_string()
        body = parse_json_object_from_request(request)
        new_user_data = await self.store.get_user_by_access_token(body["token"])
        new_user_id = new_user_data.user_id
        
        # check for multi-account exists
        if user_id == new_user_id:
            raise StoreError(code=400, msg="Incorrect user")
        second_user_multi_account = await self.store.get_multi_account(user_id=new_user_id)
        if second_user_multi_account:
            second_user_multi_account_id = second_user_multi_account["multi_account_id"]
            users_in_multi_account = await self.store.get_multi_account_info(second_user_multi_account_id)
            if len(users_in_multi_account) <= 1:
                await self.store.delete_multi_account(second_user_multi_account_id)
            else:
                raise StoreError(code=400, msg="User is in a different multi-account")
        
        # multi-account check
        multi_account = await self.store.get_multi_account(user_id=user_id)
        if multi_account:
            multi_account_id = multi_account["multi_account_id"]
            users_in_multi_account = await self.store.get_multi_account_info(multi_account_id)
            if len(users_in_multi_account) > 4:
                raise StoreError(code=400, msg="Multi-account has a maximum number of users")
        else:
            multi_account_id = await self.store.create_multi_account(user_id=user_id)
        
        # add new user in multi-account
        await self.store.add_user_to_multi_account(id=multi_account_id, user_id=new_user_id)
        return 201, {"status": "OK"}


def register_servlets(hs: "HomeServer", http_server: HttpServer) -> None:
    MultiAccountServlet(hs).register(http_server)
