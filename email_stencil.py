from email.message import EmailMessage
from io import StringIO

import stencil


class MessageBuilder:
    list_fields = [
        'to', 'bcc', 'cc', 'reply_to',
    ]

    def __init__(self, template_loader, list_fields=None):
        self.loader = template_loader
        if list_fields is not None:
            self.list_fields = list_fields

    def render(self, template_names, context, **defaults):
        if not isinstance(template_names, (list, tuple)):
            template_names = [template_names]

        for name in template_names:
            try:
                template = self.template_loader[name]
                break
            except LookupError:
                pass
        else:
            raise LookupError(template_names)

        blocks = {
            node.block_name: node
            for node in template.nodes_by_type(stencil.BlockTag)
        }

        data = defaults.copy()

        context = stencil.Context(context)

        msg = EmailMessage()

        for field, block in blocks.items():
            value = StringIO()
            block.render(context, value)
            value = value.getvalue()
            if field in self.list_fields:
                value = [
                    line.strip()
                    for line in value.splitlines()
                    if line.strip()
                ]
            data[field] = value

        for field, value in data.items():
            if field == 'body':
                msg.set_content(value)
            elif field == 'html':
                msg.add_alternative(value, subtype='html')
            else:
                msg[field] = value

        return msg
