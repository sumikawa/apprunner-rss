import os, re
import json
import mimetypes
import feedgenerator, datetime
import dropbox
import boto3
import pprint
import hashlib

def getlist():
    ssm = boto3.client('ssm', region_name='ap-northeast-1')
    param = ssm.get_parameter(Name='dropbox', WithDecryption=True)
    dbx = dropbox.Dropbox(param['Parameter']['Value'])

    mimetypes.add_type("video/mp4", ".m4v")
    mimetypes.add_type("audio/aac", ".m4a")

    feed = feedgenerator.Rss201rev2Feed(
        title = u'Videos',
        link = u'https://7pqp7k8u6k.execute-api.ap-northeast-1.amazonaws.com/Prod/rss/',
        description = u'test',
        pubdate = datetime.datetime.utcnow())

    pp = pprint.PrettyPrinter(indent=4)

    result = dbx.files_list_folder('/movies')
    entries = result.entries
    while result.has_more:
        result = dbx.files_list_folder_continue(result.cursor)
        entries.extend(result.entries)

    for entry in entries:
        pattern = re.compile(r".*\.(mp4|m4v|mp3|m4a)$", re.IGNORECASE)
        if not(re.match(pattern, entry.name)):
            continue
        contentname = re.sub(r"\.(mp4|m4v|mp3|m4a)$", '', entry.name)
        # url = dbx.files_get_temporary_link(entry.path_lower).link
        # cfurl = url.replace('content.dropboxapi.com', 'd3fynstehsnhva.cloudfront.net')
        cfurl2 = 'https://d3fynstehsnhva.cloudfront.net' + entry.path_lower
        # print(cfurl2)

        (mtype, mencoding) = mimetypes.guess_type(entry.name)

        enclosure = feedgenerator.Enclosure(cfurl2, str(entry.size), mtype)
        # enclosure = feedgenerator.Enclosure(cfurl, str(entry.size), mtype)
        # enclosure = feedgenerator.Enclosure("http://emacs.don.to/" + entry.name, str(entry.size), mtype)

        md5 = hashlib.md5(entry.path_lower.encode('utf-8')).hexdigest()
        # print(contentname)
        # print(vars(enclosure))
        feed.add_item(
            title = contentname,
            link = cfurl2,
            description = entry.name,
            author_name = u'nobody@example.com',
            unique_id = md5,
            enclosure = enclosure,
            pubdate = entry.client_modified
        )

    return(feed.writeString('utf-8'))

def lambda_handler(event, context):
    # dbx.files_upload(feed.writeString('utf-8').encode(), '/movies/videos.rss', mode = dropbox.files.WriteMode.overwrite)
    result = getlist()

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/rss+xml",
            "Cache-Control": "max-age=14300" # < 4hours
        },
        "body": result
    }

if __name__ == "__main__":
    print(getlist())
