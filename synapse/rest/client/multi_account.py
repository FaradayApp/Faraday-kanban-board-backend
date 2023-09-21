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
from synapse.types import JsonDict

from ._base import client_patterns

if TYPE_CHECKING:
    from synapse.server import HomeServer

logger = logging.getLogger(__name__)


class MultiAccountServlet(RestServlet):
    """
    GET /user/multi_account HTTP/1.1
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
        multi_account_id = await self.store.get_multi_account(user_id=user_id)
        if multi_account_id is None:
            raise NotFoundError("Multi account not found")
        return 200, await self.store.get_multi_account_info(multi_account_id)

    async def on_POST(
        self, request: SynapseRequest,
    ) -> Tuple[int, JsonDict]:
        requester = await self.auth.get_user_by_req(request)
        user_id = requester.user.to_string()
        multi_account_id = await self.store.get_multi_account(user_id=user_id)
        if multi_account_id:
            raise StoreError(code=400, msg="Multi account exists")
        multi_account_id = await self.store.create_multi_account(user_id=user_id)
        return 200, await self.store.get_multi_account_info(multi_account_id)


def register_servlets(hs: "HomeServer", http_server: HttpServer) -> None:
    MultiAccountServlet(hs).register(http_server)
