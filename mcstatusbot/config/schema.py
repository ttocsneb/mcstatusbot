from marshmallow import post_load, fields, Schema, post_dump


class Config:
    def __init__(self, update: float, ip: str, port: int, prefix: str,
                 token: str = None):
        self.token = token
        self.update = update
        self.ip = ip
        self.port = port
        self.prefix = prefix

    @property
    def address(self):
        address = self.ip
        if self.port != 25565:
            address += ":" + self.port
        return address


class ConfigSchema(Schema):
    token = fields.String(allow_none=True)
    update = fields.Float(missing=60)
    ip = fields.String(missing="127.0.0.1")
    port = fields.Int(missing=25565)
    prefix = fields.String(missing="mc")

    @post_load
    def createConfig(self, data, **kwargs):
        return Config(**data)

    @post_dump
    def put_empty_token(self, data, **kwargs):
        if not data['token']:
            data['token'] = "Put Token Here"
        return data
