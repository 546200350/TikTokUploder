import requests
import datetime
import hashlib
import hmac
import random
import zlib
import string


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def getCreationId():
    length = 21
    characters = string.ascii_letters + string.digits
    creationid = ''.join(random.choice(characters) for i in range(length))
    return creationid


def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


def AWSsignature(access_key, secret_key, request_parameters, headers, method="GET", payload='', region="ap-singapore-1", service="vod"):
    # https://docs.aws.amazon.com/fr_fr/general/latest/gr/sigv4-signed-request-examples.html
    canonical_uri = '/'
    canonical_querystring = request_parameters
    canonical_headers = '\n'.join(
        [f"{h[0]}:{h[1]}" for h in headers.items()]) + '\n'
    signed_headers = ';'.join(headers.keys())
    payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + \
        '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
    amzdate = headers["x-amz-date"]
    datestamp = amzdate.split('T')[0]

    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = datestamp + '/' + region + \
        '/' + service + '/' + 'aws4_request'
    string_to_sign = algorithm + '\n' + amzdate + '\n' + credential_scope + \
        '\n' + hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

    signing_key = getSignatureKey(secret_key, datestamp, region, service)
    signature = hmac.new(signing_key, (string_to_sign).encode(
        'utf-8'), hashlib.sha256).hexdigest()

    return signature


def crc32(content):
    prev = 0
    prev = zlib.crc32(content, prev)
    return ("%X" % (prev & 0xFFFFFFFF)).lower().zfill(8)


def printResponse(r):
    print(f"{r = }")
    print(f"{r.content = }")


def printError(url, r):
    print(f"[-] An error occured while reaching {url}")
    printResponse(r)


def assertSuccess(url, r):
    if r.status_code != 200:
        printError(url, r)
    return r.status_code == 200


def log(name):
    print(f'============{name}===========')
# 获取真实标签


def getTagsExtra(title, tags, users, session, url_prefix):
    text_extra = []
    # 处理tag
    for tag in tags:
        url = "https://www.tiktok.com/api/upload/challenge/sug/"
        params = {"keyword": tag}
        r = session.get(url, params=params)
        if not assertSuccess(url, r):
            return False
        try:
            verified_tag = r.json()["sug_list"][0]["cha_name"]
        except:
            verified_tag = tag
        title += " #"+verified_tag
        text_extra.append({"start": len(title)-len(verified_tag)-1, "end": len(
            title), "user_id": "", "type": 1, "hashtag_name": verified_tag})
    # 处理users
    for user in users:
        url = f"https://{url_prefix}.tiktok.com/api/upload/search/user/"
        params = {"keyword": user}
        r = session.get(url, params=params)
        if not assertSuccess(url, r):
            return False
        try:
            verified_user = r.json()["user_list"][0]["user_info"]["unique_id"]
            verified_user_id = r.json()["user_list"][0]["user_info"]["uid"]
        except:
            verified_user = user
            verified_user_id = ""
        title += " @"+verified_user
        text_extra.append({"start": len(title)-len(verified_user)-1, "end": len(
            title), "user_id": verified_user_id, "type": 0, "hashtag_name": verified_user})
    return title, text_extra

# 上传视频


def uploadToTikTok(video, session):
    # 获取上传前的授权信息
    url = "https://www.tiktok.com/api/v1/video/upload/auth/"
    r = session.get(url)
    access_key = r.json()["video_token_v5"]["access_key_id"]
    secret_key = r.json()["video_token_v5"]["secret_acess_key"]
    session_token = r.json()["video_token_v5"]["session_token"]
    with open(video, "rb") as f:
        video_content = f.read()
    file_size = len(video_content)
    # 进一步处理授权，拿到最终上传数据
    url = "https://vod-ap-singapore-1.bytevcloudapi.com/"
    request_parameters = f'Action=ApplyUploadInner&FileSize={file_size}&FileType=video&IsInner=1&SpaceName=tiktok&Version=2020-11-19&s=zdxefu8qvq8'
    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d')
    headers = {  # Must be in alphabetical order, keys in lower case
        "x-amz-date": amzdate,
        "x-amz-security-token": session_token
    }
    signature = AWSsignature(
        access_key, secret_key, request_parameters, headers)
    authorization = f"AWS4-HMAC-SHA256 Credential={access_key}/{datestamp}/ap-singapore-1/vod/aws4_request, SignedHeaders=x-amz-date;x-amz-security-token, Signature={signature}"
    headers["authorization"] = authorization
    r = session.get(f"{url}?{request_parameters}", headers=headers)
    if not assertSuccess(url, r):
        return False
    upload_node = r.json()["Result"]["InnerUploadAddress"]["UploadNodes"][0]
    video_id = upload_node["Vid"]
    store_uri = upload_node["StoreInfos"][0]["StoreUri"]
    video_auth = upload_node["StoreInfos"][0]["Auth"]
    upload_host = upload_node["UploadHost"]
    session_key = upload_node["SessionKey"]

    # 真正开始上传
    url = f"https://{upload_host}/{store_uri}?uploads"
    rand = ''.join(random.choice(
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']) for _ in range(30))
    headers = {
        "Authorization": video_auth,
        "Content-Type": f"multipart/form-data; boundary=---------------------------{rand}"
    }
    data = f"-----------------------------{rand}--"
    r = session.post(url, headers=headers, data=data)
    if not assertSuccess(url, r):
        return False
    upload_id = r.json()["payload"]["uploadID"]
    # 文件分割成块上传
    # Split file in chunks of 5242880 bytes
    chunk_size = 5242880
    chunks = []
    i = 0
    while i < file_size:
        chunks.append(video_content[i:i+chunk_size])
        i += chunk_size

    # 上传数据块
    crcs = []
    for i in range(len(chunks)):
        chunk = chunks[i]
        crc = crc32(chunk)
        crcs.append(crc)
        url = f"https://{upload_host}/{store_uri}?partNumber={i+1}&uploadID={upload_id}"
        headers = {
            "Authorization": video_auth,
            "Content-Type": "application/octet-stream",
            "Content-Disposition": 'attachment; filename="undefined"',
            "Content-Crc32": crc
        }
        r = session.post(url, headers=headers, data=chunk)
        if not assertSuccess(url, r):
            return False

    url = f"https://{upload_host}/{store_uri}?uploadID={upload_id}"
    headers = {
        "Authorization": video_auth,
        "origin": "https://www.tiktok.com",
        "Content-Type": "text/plain;charset=UTF-8",
    }
    data = ','.join([f"{i+1}:{crcs[i]}" for i in range(len(crcs))])
    r = requests.post(url, headers=headers, data=data, verify=False)
    if not assertSuccess(url, r):
        return False
    url = "https://vod-ap-singapore-1.bytevcloudapi.com/"
    request_parameters = f'Action=CommitUploadInner&SpaceName=tiktok&Version=2020-11-19'
    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d')
    data = '{"SessionKey":"'+session_key+'","Functions":[]}'
    amzcontentsha256 = hashlib.sha256(data.encode('utf-8')).hexdigest()
    headers = {  # Must be in alphabetical order, keys in lower case
        "x-amz-content-sha256": amzcontentsha256,
        "x-amz-date": amzdate,
        "x-amz-security-token": session_token
    }
    signature = AWSsignature(
        access_key, secret_key, request_parameters, headers, method="POST", payload=data)
    authorization = f"AWS4-HMAC-SHA256 Credential={access_key}/{datestamp}/ap-singapore-1/vod/aws4_request, SignedHeaders=x-amz-content-sha256;x-amz-date;x-amz-security-token, Signature={signature}"
    headers["authorization"] = authorization
    headers["Content-Type"] = "text/plain;charset=UTF-8"
    r = session.post(f"{url}?{request_parameters}", headers=headers, data=data)
    if not assertSuccess(url, r):
        return False
    return video_id
