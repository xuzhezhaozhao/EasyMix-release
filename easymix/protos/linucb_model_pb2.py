# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: linucb_model.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='linucb_model.proto',
  package='aimaker.predictor.linucb',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x12linucb_model.proto\x12\x18\x61imaker.predictor.linucb\"\xbc\x01\n\x0bLinucbModel\x12\x39\n\x0btrain_stage\x18\x01 \x01(\x0e\x32$.aimaker.predictor.linucb.TrainStage\x12\x37\n\nmodel_info\x18\x02 \x01(\x0b\x32#.aimaker.predictor.linucb.ModelInfo\x12\x39\n\x0b\x63onfig_info\x18\x03 \x01(\x0b\x32$.aimaker.predictor.linucb.ConfigInfo\"\xd7\x01\n\tModelInfo\x12\x19\n\x11\x66\x65\x61ture_dimension\x18\x01 \x01(\x05\x12\x0b\n\x03\x61rm\x18\x02 \x03(\x02\x12\x32\n\x08matrix_a\x18\x03 \x03(\x0b\x32 .aimaker.predictor.linucb.Matrix\x12:\n\x10inverse_matrix_a\x18\x04 \x03(\x0b\x32 .aimaker.predictor.linucb.Matrix\x12\x32\n\x08vector_b\x18\x05 \x03(\x0b\x32 .aimaker.predictor.linucb.Vector\"<\n\x06Matrix\x12\x0f\n\x07num_row\x18\x01 \x01(\x05\x12\x0f\n\x07num_col\x18\x02 \x01(\x05\x12\x10\n\x08\x65lements\x18\x03 \x03(\x02\"\x1a\n\x06Vector\x12\x10\n\x08\x65lements\x18\x03 \x03(\x02\"E\n\nConfigInfo\x12\r\n\x05\x61lpha\x18\x01 \x01(\x02\x12\x12\n\nscore_type\x18\x02 \x01(\x05\x12\x14\n\x0c\x65xplore_prob\x18\x03 \x01(\x02*6\n\nTrainStage\x12\x0e\n\nCOLD_START\x10\x00\x12\x0b\n\x07HOT_RUN\x10\x01\x12\x0b\n\x07UNKNOWN\x10\x63\x62\x06proto3')
)

_TRAINSTAGE = _descriptor.EnumDescriptor(
  name='TrainStage',
  full_name='aimaker.predictor.linucb.TrainStage',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='COLD_START', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HOT_RUN', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=2, number=99,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=618,
  serialized_end=672,
)
_sym_db.RegisterEnumDescriptor(_TRAINSTAGE)

TrainStage = enum_type_wrapper.EnumTypeWrapper(_TRAINSTAGE)
COLD_START = 0
HOT_RUN = 1
UNKNOWN = 99



_LINUCBMODEL = _descriptor.Descriptor(
  name='LinucbModel',
  full_name='aimaker.predictor.linucb.LinucbModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='train_stage', full_name='aimaker.predictor.linucb.LinucbModel.train_stage', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='model_info', full_name='aimaker.predictor.linucb.LinucbModel.model_info', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='config_info', full_name='aimaker.predictor.linucb.LinucbModel.config_info', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=49,
  serialized_end=237,
)


_MODELINFO = _descriptor.Descriptor(
  name='ModelInfo',
  full_name='aimaker.predictor.linucb.ModelInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_dimension', full_name='aimaker.predictor.linucb.ModelInfo.feature_dimension', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='arm', full_name='aimaker.predictor.linucb.ModelInfo.arm', index=1,
      number=2, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='matrix_a', full_name='aimaker.predictor.linucb.ModelInfo.matrix_a', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='inverse_matrix_a', full_name='aimaker.predictor.linucb.ModelInfo.inverse_matrix_a', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vector_b', full_name='aimaker.predictor.linucb.ModelInfo.vector_b', index=4,
      number=5, type=11, cpp_type=10, label=3,
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
  serialized_start=240,
  serialized_end=455,
)


_MATRIX = _descriptor.Descriptor(
  name='Matrix',
  full_name='aimaker.predictor.linucb.Matrix',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='num_row', full_name='aimaker.predictor.linucb.Matrix.num_row', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='num_col', full_name='aimaker.predictor.linucb.Matrix.num_col', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='elements', full_name='aimaker.predictor.linucb.Matrix.elements', index=2,
      number=3, type=2, cpp_type=6, label=3,
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
  serialized_start=457,
  serialized_end=517,
)


_VECTOR = _descriptor.Descriptor(
  name='Vector',
  full_name='aimaker.predictor.linucb.Vector',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='elements', full_name='aimaker.predictor.linucb.Vector.elements', index=0,
      number=3, type=2, cpp_type=6, label=3,
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
  serialized_start=519,
  serialized_end=545,
)


_CONFIGINFO = _descriptor.Descriptor(
  name='ConfigInfo',
  full_name='aimaker.predictor.linucb.ConfigInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='alpha', full_name='aimaker.predictor.linucb.ConfigInfo.alpha', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='score_type', full_name='aimaker.predictor.linucb.ConfigInfo.score_type', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='explore_prob', full_name='aimaker.predictor.linucb.ConfigInfo.explore_prob', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=547,
  serialized_end=616,
)

_LINUCBMODEL.fields_by_name['train_stage'].enum_type = _TRAINSTAGE
_LINUCBMODEL.fields_by_name['model_info'].message_type = _MODELINFO
_LINUCBMODEL.fields_by_name['config_info'].message_type = _CONFIGINFO
_MODELINFO.fields_by_name['matrix_a'].message_type = _MATRIX
_MODELINFO.fields_by_name['inverse_matrix_a'].message_type = _MATRIX
_MODELINFO.fields_by_name['vector_b'].message_type = _VECTOR
DESCRIPTOR.message_types_by_name['LinucbModel'] = _LINUCBMODEL
DESCRIPTOR.message_types_by_name['ModelInfo'] = _MODELINFO
DESCRIPTOR.message_types_by_name['Matrix'] = _MATRIX
DESCRIPTOR.message_types_by_name['Vector'] = _VECTOR
DESCRIPTOR.message_types_by_name['ConfigInfo'] = _CONFIGINFO
DESCRIPTOR.enum_types_by_name['TrainStage'] = _TRAINSTAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LinucbModel = _reflection.GeneratedProtocolMessageType('LinucbModel', (_message.Message,), dict(
  DESCRIPTOR = _LINUCBMODEL,
  __module__ = 'linucb_model_pb2'
  # @@protoc_insertion_point(class_scope:aimaker.predictor.linucb.LinucbModel)
  ))
_sym_db.RegisterMessage(LinucbModel)

ModelInfo = _reflection.GeneratedProtocolMessageType('ModelInfo', (_message.Message,), dict(
  DESCRIPTOR = _MODELINFO,
  __module__ = 'linucb_model_pb2'
  # @@protoc_insertion_point(class_scope:aimaker.predictor.linucb.ModelInfo)
  ))
_sym_db.RegisterMessage(ModelInfo)

Matrix = _reflection.GeneratedProtocolMessageType('Matrix', (_message.Message,), dict(
  DESCRIPTOR = _MATRIX,
  __module__ = 'linucb_model_pb2'
  # @@protoc_insertion_point(class_scope:aimaker.predictor.linucb.Matrix)
  ))
_sym_db.RegisterMessage(Matrix)

Vector = _reflection.GeneratedProtocolMessageType('Vector', (_message.Message,), dict(
  DESCRIPTOR = _VECTOR,
  __module__ = 'linucb_model_pb2'
  # @@protoc_insertion_point(class_scope:aimaker.predictor.linucb.Vector)
  ))
_sym_db.RegisterMessage(Vector)

ConfigInfo = _reflection.GeneratedProtocolMessageType('ConfigInfo', (_message.Message,), dict(
  DESCRIPTOR = _CONFIGINFO,
  __module__ = 'linucb_model_pb2'
  # @@protoc_insertion_point(class_scope:aimaker.predictor.linucb.ConfigInfo)
  ))
_sym_db.RegisterMessage(ConfigInfo)


# @@protoc_insertion_point(module_scope)