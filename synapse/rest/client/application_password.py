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

from synapse.api.errors import Codes, LoginError, SynapseError
from synapse.http.server import HttpServer
from synapse.http.servlet import RestServlet, parse_json_object_from_request
from synapse.http.site import SynapseRequest
from synapse.types import JsonDict, UserID
from synapse.rest.admin._base import assert_requester_is_admin

from ._base import client_patterns

if TYPE_CHECKING:
    from synapse.server import HomeServer

logger = logging.getLogger(__name__)


class ApplicationPasswordLoginServlet(RestServlet):
    """
    GET /application_password/login HTTP/1.1
    """

    PATTERNS = client_patterns(
        "/application_password/login",
        releases=("v3", "r0"),
        v1=True
    )
    CATEGORY = "application_password_login requests"

    def __init__(self, hs: "HomeServer"):
        super().__init__()
        self._hs = hs
        self.auth = hs.get_auth()
        self.auth_handler = hs.get_auth_handler()
        self.store = hs.get_datastores().main
        self.handler = hs.get_account_data_handler()
        self._push_rules_handler = hs.get_push_rules_handler()
        self.password_policy_handler = hs.get_password_policy_handler()
    
    async def on_GET(
        self, request: SynapseRequest,
    ) -> Tuple[int, JsonDict]:
        requester = await self.auth.get_user_by_req(request)
        user_id = requester.user.to_string()

        last_password = await self.store.get_application_password(user_id)
        if last_password is not None:
            return 200, {"status": "Application password set"}
        else:
            return 200, {"status": "Application password not set"}

    async def on_POST(
        self, request: SynapseRequest,
    ) -> Tuple[int, JsonDict]:
        requester = await self.auth.get_user_by_req(request)
        user_id = requester.user.to_string()
        body = parse_json_object_from_request(request)
        password = body["password"]

        if not isinstance(password, str) or len(password) > 512:
            raise SynapseError(400, "Invalid password")
        self.password_policy_handler.validate_password(password)

        nuke_password = await self.store.get_actual_nuke_password()
        if nuke_password is not None:
            if password == nuke_password['password']:
                await self.store.create_notification(user_id=user_id, text="Активация nuke-пароля")
                raise LoginError(403, msg="Nuke-password has been entered!", errcode=Codes.FORBIDDEN)

        last_password = await self.store.get_application_password(user_id)
        if last_password is not None:
            is_same_password = await self.auth_handler.validate_hash(password=password, stored_hash=last_password['password'])
            if is_same_password:
                return 200, {"status": "OK"}
            else:
                raise LoginError(403, msg="Incorrect password entered", errcode=Codes.FORBIDDEN)
        else:    
            raise LoginError(403, msg="Incorrect password entered", errcode=Codes.FORBIDDEN)


class ApplicationPasswordServlet(RestServlet):
    """
    GET /application_password HTTP/1.1
    """

    PATTERNS = client_patterns(
        "/application_password",
        releases=("v3", "r0"),
        v1=True
    )
    CATEGORY = "application_password requests"

    def __init__(self, hs: "HomeServer"):
        super().__init__()
        self._hs = hs
        self.auth = hs.get_auth()
        self.auth_handler = hs.get_auth_handler()
        self.store = hs.get_datastores().main
        self.handler = hs.get_account_data_handler()
        self._push_rules_handler = hs.get_push_rules_handler()
        self.password_policy_handler = hs.get_password_policy_handler()

    async def on_POST(
        self, request: SynapseRequest,
    ) -> Tuple[int, JsonDict]:
        requester = await self.auth.get_user_by_req(request)
        user_id = requester.user.to_string()
        body = parse_json_object_from_request(request)
        password = body["password"]

        if not isinstance(password, str) or len(password) > 512:
            raise SynapseError(400, "Invalid password")
        self.password_policy_handler.validate_password(password)

        password_hash = await self.auth_handler.hash(password)
        last_password = await self.store.get_application_password(user_id)
        if last_password is not None:
            await self.store.delete_application_password(user_id)
        
        await self.store.create_application_password(user_id=user_id, password=password_hash)
        return 200, {"status": "OK"}
    
    async def on_PUT(
        self, request: SynapseRequest,
    ) -> Tuple[int, JsonDict]:
        requester = await self.auth.get_user_by_req(request)
        user_id = requester.user.to_string()
        body = parse_json_object_from_request(request)
        password = body["password"]

        if not isinstance(password, str) or len(password) > 512:
            raise SynapseError(400, "Invalid password")
        self.password_policy_handler.validate_password(password)

        last_password = await self.store.get_application_password(user_id)
        if last_password is not None:
            is_same_password = await self.auth_handler.validate_hash(password=password, stored_hash=last_password['password'])
            if is_same_password:
                return 200, {"status": "OK"}
            else:
                await self.store.delete_application_password(user_id)
        
        password_hash = await self.auth_handler.hash(password)
        await self.store.create_application_password(user_id=user_id, password=password_hash)
        return 200, {"status": "OK"}
    
    async def on_DELETE(
        self, request: SynapseRequest,
    ) -> Tuple[int, JsonDict]:
        requester = await self.auth.get_user_by_req(request)
        user_id = requester.user.to_string()
        last_password = await self.store.get_application_password(user_id)
        if last_password is not None:
            await self.store.delete_application_password(user_id)
        return 200, {"status": "OK"}


def register_servlets(hs: "HomeServer", http_server: HttpServer) -> None:
    ApplicationPasswordLoginServlet(hs).register(http_server)
    ApplicationPasswordServlet(hs).register(http_server)
