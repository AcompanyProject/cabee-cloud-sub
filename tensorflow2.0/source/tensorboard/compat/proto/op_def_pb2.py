# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/compat/proto/op_def.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorboard.compat.proto import attr_value_pb2 as tensorboard_dot_compat_dot_proto_dot_attr__value__pb2
from tensorboard.compat.proto import types_pb2 as tensorboard_dot_compat_dot_proto_dot_types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorboard/compat/proto/op_def.proto',
  package='tensorboard',
  syntax='proto3',
  serialized_options=_b('\n\030org.tensorflow.frameworkB\013OpDefProtosP\001Z=github.com/tensorflow/tensorflow/tensorflow/go/core/framework\370\001\001'),
  serialized_pb=_b('\n%tensorboard/compat/proto/op_def.proto\x12\x0btensorboard\x1a)tensorboard/compat/proto/attr_value.proto\x1a$tensorboard/compat/proto/types.proto\"\xd7\x05\n\x05OpDef\x12\x0c\n\x04name\x18\x01 \x01(\t\x12,\n\tinput_arg\x18\x02 \x03(\x0b\x32\x19.tensorboard.OpDef.ArgDef\x12-\n\noutput_arg\x18\x03 \x03(\x0b\x32\x19.tensorboard.OpDef.ArgDef\x12\x16\n\x0e\x63ontrol_output\x18\x14 \x03(\t\x12(\n\x04\x61ttr\x18\x04 \x03(\x0b\x32\x1a.tensorboard.OpDef.AttrDef\x12/\n\x0b\x64\x65precation\x18\x08 \x01(\x0b\x32\x1a.tensorboard.OpDeprecation\x12\x0f\n\x07summary\x18\x05 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x06 \x01(\t\x12\x16\n\x0eis_commutative\x18\x12 \x01(\x08\x12\x14\n\x0cis_aggregate\x18\x10 \x01(\x08\x12\x13\n\x0bis_stateful\x18\x11 \x01(\x08\x12\"\n\x1a\x61llows_uninitialized_input\x18\x13 \x01(\x08\x1a\xa0\x01\n\x06\x41rgDef\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12#\n\x04type\x18\x03 \x01(\x0e\x32\x15.tensorboard.DataType\x12\x11\n\ttype_attr\x18\x04 \x01(\t\x12\x13\n\x0bnumber_attr\x18\x05 \x01(\t\x12\x16\n\x0etype_list_attr\x18\x06 \x01(\t\x12\x0e\n\x06is_ref\x18\x10 \x01(\x08\x1a\xbf\x01\n\x07\x41ttrDef\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12-\n\rdefault_value\x18\x03 \x01(\x0b\x32\x16.tensorboard.AttrValue\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x13\n\x0bhas_minimum\x18\x05 \x01(\x08\x12\x0f\n\x07minimum\x18\x06 \x01(\x03\x12.\n\x0e\x61llowed_values\x18\x07 \x01(\x0b\x32\x16.tensorboard.AttrValue\"5\n\rOpDeprecation\x12\x0f\n\x07version\x18\x01 \x01(\x05\x12\x13\n\x0b\x65xplanation\x18\x02 \x01(\t\"(\n\x06OpList\x12\x1e\n\x02op\x18\x01 \x03(\x0b\x32\x12.tensorboard.OpDefBk\n\x18org.tensorflow.frameworkB\x0bOpDefProtosP\x01Z=github.com/tensorflow/tensorflow/tensorflow/go/core/framework\xf8\x01\x01\x62\x06proto3')
  ,
  dependencies=[tensorboard_dot_compat_dot_proto_dot_attr__value__pb2.DESCRIPTOR,tensorboard_dot_compat_dot_proto_dot_types__pb2.DESCRIPTOR,])




_OPDEF_ARGDEF = _descriptor.Descriptor(
  name='ArgDef',
  full_name='tensorboard.OpDef.ArgDef',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorboard.OpDef.ArgDef.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='tensorboard.OpDef.ArgDef.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='tensorboard.OpDef.ArgDef.type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type_attr', full_name='tensorboard.OpDef.ArgDef.type_attr', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='number_attr', full_name='tensorboard.OpDef.ArgDef.number_attr', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type_list_attr', full_name='tensorboard.OpDef.ArgDef.type_list_attr', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_ref', full_name='tensorboard.OpDef.ArgDef.is_ref', index=6,
      number=16, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=509,
  serialized_end=669,
)

_OPDEF_ATTRDEF = _descriptor.Descriptor(
  name='AttrDef',
  full_name='tensorboard.OpDef.AttrDef',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorboard.OpDef.AttrDef.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='tensorboard.OpDef.AttrDef.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='default_value', full_name='tensorboard.OpDef.AttrDef.default_value', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='tensorboard.OpDef.AttrDef.description', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='has_minimum', full_name='tensorboard.OpDef.AttrDef.has_minimum', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='minimum', full_name='tensorboard.OpDef.AttrDef.minimum', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='allowed_values', full_name='tensorboard.OpDef.AttrDef.allowed_values', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=672,
  serialized_end=863,
)

_OPDEF = _descriptor.Descriptor(
  name='OpDef',
  full_name='tensorboard.OpDef',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorboard.OpDef.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='input_arg', full_name='tensorboard.OpDef.input_arg', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output_arg', full_name='tensorboard.OpDef.output_arg', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='control_output', full_name='tensorboard.OpDef.control_output', index=3,
      number=20, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='attr', full_name='tensorboard.OpDef.attr', index=4,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='deprecation', full_name='tensorboard.OpDef.deprecation', index=5,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='summary', full_name='tensorboard.OpDef.summary', index=6,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='tensorboard.OpDef.description', index=7,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_commutative', full_name='tensorboard.OpDef.is_commutative', index=8,
      number=18, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_aggregate', full_name='tensorboard.OpDef.is_aggregate', index=9,
      number=16, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_stateful', full_name='tensorboard.OpDef.is_stateful', index=10,
      number=17, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='allows_uninitialized_input', full_name='tensorboard.OpDef.allows_uninitialized_input', index=11,
      number=19, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_OPDEF_ARGDEF, _OPDEF_ATTRDEF, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=136,
  serialized_end=863,
)


_OPDEPRECATION = _descriptor.Descriptor(
  name='OpDeprecation',
  full_name='tensorboard.OpDeprecation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='tensorboard.OpDeprecation.version', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='explanation', full_name='tensorboard.OpDeprecation.explanation', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=865,
  serialized_end=918,
)


_OPLIST = _descriptor.Descriptor(
  name='OpList',
  full_name='tensorboard.OpList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='op', full_name='tensorboard.OpList.op', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=920,
  serialized_end=960,
)

_OPDEF_ARGDEF.fields_by_name['type'].enum_type = tensorboard_dot_compat_dot_proto_dot_types__pb2._DATATYPE
_OPDEF_ARGDEF.containing_type = _OPDEF
_OPDEF_ATTRDEF.fields_by_name['default_value'].message_type = tensorboard_dot_compat_dot_proto_dot_attr__value__pb2._ATTRVALUE
_OPDEF_ATTRDEF.fields_by_name['allowed_values'].message_type = tensorboard_dot_compat_dot_proto_dot_attr__value__pb2._ATTRVALUE
_OPDEF_ATTRDEF.containing_type = _OPDEF
_OPDEF.fields_by_name['input_arg'].message_type = _OPDEF_ARGDEF
_OPDEF.fields_by_name['output_arg'].message_type = _OPDEF_ARGDEF
_OPDEF.fields_by_name['attr'].message_type = _OPDEF_ATTRDEF
_OPDEF.fields_by_name['deprecation'].message_type = _OPDEPRECATION
_OPLIST.fields_by_name['op'].message_type = _OPDEF
DESCRIPTOR.message_types_by_name['OpDef'] = _OPDEF
DESCRIPTOR.message_types_by_name['OpDeprecation'] = _OPDEPRECATION
DESCRIPTOR.message_types_by_name['OpList'] = _OPLIST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OpDef = _reflection.GeneratedProtocolMessageType('OpDef', (_message.Message,), dict(

  ArgDef = _reflection.GeneratedProtocolMessageType('ArgDef', (_message.Message,), dict(
    DESCRIPTOR = _OPDEF_ARGDEF,
    __module__ = 'tensorboard.compat.proto.op_def_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.OpDef.ArgDef)
    ))
  ,

  AttrDef = _reflection.GeneratedProtocolMessageType('AttrDef', (_message.Message,), dict(
    DESCRIPTOR = _OPDEF_ATTRDEF,
    __module__ = 'tensorboard.compat.proto.op_def_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.OpDef.AttrDef)
    ))
  ,
  DESCRIPTOR = _OPDEF,
  __module__ = 'tensorboard.compat.proto.op_def_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.OpDef)
  ))
_sym_db.RegisterMessage(OpDef)
_sym_db.RegisterMessage(OpDef.ArgDef)
_sym_db.RegisterMessage(OpDef.AttrDef)

OpDeprecation = _reflection.GeneratedProtocolMessageType('OpDeprecation', (_message.Message,), dict(
  DESCRIPTOR = _OPDEPRECATION,
  __module__ = 'tensorboard.compat.proto.op_def_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.OpDeprecation)
  ))
_sym_db.RegisterMessage(OpDeprecation)

OpList = _reflection.GeneratedProtocolMessageType('OpList', (_message.Message,), dict(
  DESCRIPTOR = _OPLIST,
  __module__ = 'tensorboard.compat.proto.op_def_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.OpList)
  ))
_sym_db.RegisterMessage(OpList)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
