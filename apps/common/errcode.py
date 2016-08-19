# -*- coding: utf-8 -*-

#//-----------------//
#// 全局错误码定义//
#//-----------------//

#error code
#|第一段系统代码（0000开始，16进制）|第二段为子系统（0000开始，16进制）
#0x|0000|0000

#//-----------------//
#// 通用错误码定义//
#//-----------------//

#/** 格式错误. */
FORMAT_ILLEGAL = "FORMAT_ILLEGAL"
FORMAT_ILLEGAL_CODE = 0x00000001

#token错误，一般用于数据库中找不到对应的账户
TOKEN_ILLEGAL = "TOKEN_ILLEGAL"
TOKEN_ILLEGAL_CODE = 0x00000002

#token已过期，需要重新登陆
TOKEN_EXPIRE = "TOKEN_EXPIRE"
TOKEN_EXPIRE_CODE = 0x00000003

#code错误，激活失败
CODE_ILLEGAL = "CODE_ILLEGAL"
CODE_ILLEGAL_CODE = 0x00000004




#//-----------------//
#// 账户系统错误码定义//
#//-----------------//
#/** 邮箱已被注册. */
EMAIL_REPEAT = "EMAIL_REPEAT"
EMAIL_REPEAT_CODE = 0x00010001

#账户错误，一般用于数据库中找不到相应账户
ACCOUNT_INVALID = "ACCOUNT_INVALID"
ACCOUNT_INVALID_CODE = 0x00010002

#密码错误.
PASSWORD_INVALID = "PASSWORD_INVALID"
PASSWORD_INVALID_CODE = 0x00010003

#账户未激活.
ACCOUNT_NOTACTIVATED = "ACCOUNT_NOTACTIVATED"
ACCOUNT_NOTACTIVATED_CODE = 0x00010004

#账户已激活过.
ACCOUNT_ACTIVATED = "ACCOUNT_ACTIVATED"
ACCOUNT_ACTIVATED_CODE = 0x00010005
