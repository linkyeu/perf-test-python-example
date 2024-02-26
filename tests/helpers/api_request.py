import json
from typing import Dict, Union, Any

import httpx
from requests.models import Response as RequestsResponse

from dataclasses import dataclass


@dataclass
class Response:
    status_code: int
    text: str
    as_dict: object
    headers: Dict[str, str]


class APIClient:
    async def get(self, url: str, **args) -> Response:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, **args)
            return self.__get_responses(response)

    async def post(
        self,
        url: str,
        payload: Union[Dict[str, Any], str],
        headers: Dict[str, str]
    ) -> Response:
        async with httpx.AsyncClient() as client:
            response = await client.post(url=url, json=payload, headers=headers)
            return self.__get_responses(response)

    async def delete(self, url: str, **args) -> Response:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, **args)
            return self.__get_responses(response)

    def __get_responses(self, response: RequestsResponse) -> Response:
        status_code = response.status_code
        text = response.text

        try:
            as_dict = response.json()
        except json.JSONDecodeError:
            as_dict = {"error": "Invalid JSON format"}
        except Exception as e:
            as_dict = {"error": str(e)}

        headers = response.headers

        return Response(
            status_code, text, as_dict, headers
        )
