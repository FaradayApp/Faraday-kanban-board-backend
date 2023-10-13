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
import uuid

from synapse.api.errors import AuthError, NotFoundError, StoreError
from synapse.http.server import HttpServer
from synapse.http.servlet import RestServlet, parse_json_object_from_request
from synapse.http.site import SynapseRequest
from synapse.types import JsonDict, UserID

from ._base import client_patterns

if TYPE_CHECKING:
    from synapse.server import HomeServer

logger = logging.getLogger(__name__)


class NoticeServlet(RestServlet):
    """
    GET /notice HTTP/1.1
    """

    PATTERNS = client_patterns(
        "/notice",
        releases=("v3", "r0"),
        v1=True
    )
    CATEGORY = "Notice requests"

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
        data = await self.store.get_all_notifications(user_id)
        result = []
        for entry in data:
            entry['date'] = entry['date'].strftime('%Y-%m-%d')
            entry_user_id = UserID.from_string(entry["user_id"])
            entry_profileinfo = await self.store.get_profileinfo(entry_user_id)
            entry.pop("user_id")
            entry["user"] = entry_profileinfo.display_name
            result.append(entry)
        return 200, result


class ViewNoticeServlet(RestServlet):
    """
    POST /notice/{notice_id} HTTP/1.1
    """

    PATTERNS = client_patterns(
        "/notice/(?P<notice_id>[^/]*)",
        releases=("v3", "r0"),
        v1=True
    )
    CATEGORY = "Notice requests"

    def __init__(self, hs: "HomeServer"):
        super().__init__()
        self._hs = hs
        self.auth = hs.get_auth()
        self.store = hs.get_datastores().main
        self.handler = hs.get_account_data_handler()
        self._push_rules_handler = hs.get_push_rules_handler()

    async def on_POST(
        self, request: SynapseRequest,
        notice_id: str
    ) -> Tuple[int, JsonDict]:
        requester = await self.auth.get_user_by_req(request)
        user_id = requester.user.to_string()
        await self.store.add_user_to_viewed(user_id=user_id, notification_id=notice_id)
        return 200, {"status": "OK"}


def register_servlets(hs: "HomeServer", http_server: HttpServer) -> None:
    ViewNoticeServlet(hs).register(http_server)
    NoticeServlet(hs).register(http_server)
