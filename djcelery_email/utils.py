from django.core.mail import EmailMultiAlternatives, EmailMessage


def chunked(iterator, chunksize):
    """
    Yields items from 'iterator' in chunks of size 'chunksize'.

    >>> list(chunked([1, 2, 3, 4, 5], chunksize=2))
    [(1, 2), (3, 4), (5,)]
    """
    chunk = []
    for idx, item in enumerate(iterator, 1):
        chunk.append(item)
        if idx % chunksize == 0:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def email_to_dict(message):
    if isinstance(message, dict):
        return message

    message_dict = {'subject': message.subject,
                    'body': message.body,
                    'from_email': message.from_email,
                    'to': message.to,
                    'bcc': message.bcc,
                    # ignore connection
                    'attachments': message.attachments,
                    'headers': message.extra_headers,
                    'cc': message.cc}

    # Django 1.8 support
    # https://docs.djangoproject.com/en/1.8/topics/email/#django.core.mail.EmailMessage
    if hasattr(message, 'reply_to'):
        message_dict['reply_to'] = message.reply_to

    if hasattr(message, 'alternatives'):
        message_dict['alternatives'] = message.alternatives
    if message.content_subtype != EmailMessage.content_subtype:
        message_dict["content_subtype"] = message.content_subtype

    return message_dict


def dict_to_email(messagedict):
    if isinstance(messagedict, dict) and "content_subtype" in messagedict:
        content_subtype = messagedict["content_subtype"]
        del messagedict["content_subtype"]
    else:
        content_subtype = None
    if hasattr(messagedict, 'from_email'):
        ret = messagedict
    elif 'alternatives' in messagedict:
        ret = EmailMultiAlternatives(**messagedict)
    else:
        ret = EmailMessage(**messagedict)
    if content_subtype:
        ret.content_subtype = content_subtype
        messagedict["content_subtype"] = content_subtype  # bring back content subtype for 'retry'
    return ret
