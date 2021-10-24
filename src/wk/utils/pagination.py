import math
from typing import Mapping, Optional, Union

from flask import request
from marshmallow import Schema, fields
from peewee import ModelSelect


def get_page(arg_name: str = "page") -> int:
    try:
        return int(request.args.get(arg_name, "1"))
    except ValueError:
        return 1


class PaginationMetaSchema(Schema):
    page = fields.Int(strict=True, dump_only=True)
    page_size = fields.Int(strict=True, dump_only=True, data_key="pageSize")
    obj_count = fields.Int(strict=True, dump_only=True, data_key="count")
    pages = fields.Int(strict=True, dump_only=True, data_key="numPages")
    has_next = fields.Bool(dump_only=True, data_key="hasNext")
    has_prev = fields.Bool(dump_only=True, data_key="hasPrev")
    next_page = fields.Int(strict=True, dump_only=True, data_key="nextPage")
    prev_page = fields.Int(strict=True, dump_only=True, data_key="prevPage")


pagination_meta = PaginationMetaSchema()


class Pagination:
    def __init__(
        self,
        query: ModelSelect,
        count: Optional[int] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ):
        self.query = query
        self.page = page or get_page()
        self.page_size = page_size or 10
        obj_count = count or query.count()
        self.pages = math.ceil(obj_count / self.page_size)
        self.has_next = self.pages > self.page
        self.has_prev = self.page > 1
        self.next_page = self.page + 1
        self.prev_page = self.page - 1

    @property
    def items(self):
        return self.query.paginate(self.page, self.page_size)

    def serialize_meta(self) -> Mapping[str, Union[bool, int]]:
        pagination_meta.dump(self)
