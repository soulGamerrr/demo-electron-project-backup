HTTP_REQUEST_ERROR = {
    "400": "Bad Request! 请求参数错误,请检查参数是否出现错误。",
    "401": "Unauthorized! 当前请求的用户需要验证，请检查是否包含响应相同的身份验证，如果已经包含，则服务器已经拒绝了这些证书。",
    "403": "Forbidden! 服务器拒绝请求",
    "404": "Not Found! 请求失败，页面不可用，资源找不到！",
    "405": "Method Not Allowed! 方法不允许，请检查使用请求方法!",
}


HTTP_REQUEST_SUCC = {
    "200": "OK!{}方法已经正确的在消息中传输。",
    "201": "Created! POST方法请求成功并创建一新的资源。 "
}