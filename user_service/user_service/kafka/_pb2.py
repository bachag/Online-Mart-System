# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: .proto
# Protobuf Python Version: 5.28.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    3,
    '',
    '.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x06.proto\x12\x04user\"Z\n\x0eUserRegistered\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x16\n\x0eoperation_type\x18\x04 \x01(\t\"U\n\x0fUserDataCreated\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\x12\x10\n\x08owner_id\x18\x03 \x01(\t\x12\x16\n\x0eoperation_type\x18\x04 \x01(\tb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, '_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_USERREGISTERED']._serialized_start=16
  _globals['_USERREGISTERED']._serialized_end=106
  _globals['_USERDATACREATED']._serialized_start=108
  _globals['_USERDATACREATED']._serialized_end=193
# @@protoc_insertion_point(module_scope)
