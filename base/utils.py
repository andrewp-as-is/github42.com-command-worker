
def headers2str(data):
    if data:
        lines = []
        for k,v in data.items():
            lines.append('%s: %s' % (k,v))
        return "\n".join(sorted(lines))
