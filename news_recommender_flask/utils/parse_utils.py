import re

def parse_text(text):
    sections = re.split(r'(\[\w.*\]:|\n<\w.*>:)', text)
    result = {}
    current_key = "Category"
    result.setdefault(current_key, "")

    for section in sections:
        section = section.strip()
        if not section:
            continue
        if section.startswith('[') or section.startswith('<'):
            current_key = section[1:-2]
            result[current_key] = ''
        elif current_key:
            result[current_key] += section + '\n'
        else:
            # Handling sections that do not follow the "key: value" format
            if ':' in section:
                key, value = section.split(': ', 1)  # 初始为1
                result[key] = value
            else:
                print("the error section is:\n",section)
                result[current_key] = section.strip()
    return result

import re

def parse_response_news(response_data: str):
    if not isinstance(response_data, str):
        response_data = str(response_data)

    start_marker = r"recommend\s+news\s*:"
    end_marker = r"recommend\s+news\s+end"
    m_start = re.search(start_marker, response_data, flags=re.IGNORECASE)
    m_end = re.search(end_marker, response_data, flags=re.IGNORECASE)
    if m_start and m_end and m_end.start() > m_start.end():
        block = response_data[m_start.end():m_end.start()]
    else:
        block = response_data

    text = block.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("：", ":")
    text = re.sub(r'(?i)(C\s*\d+)\s*,\s*', r'\1\n', text)

    lines = [ln.strip() for ln in text.split("\n")]
    lines = [ln for ln in lines if ln]

    items = []
    noid_items = []

    pat = re.compile(r'^\s*[Cc]\s*(\d+)\s*:\s*(.+)$')

    for ln in lines:
        m = pat.match(ln)
        if m:
            rank = int(m.group(1))
            rest = m.group(2).strip()
            if ":" in rest:
                title, reason = rest.split(":", 1)
            else:
                title, reason = rest, ""
            title = title.strip()
            if title:
                items.append((rank, title, reason.strip()))
        else:
            cleaned = re.sub(r'^[\-\*\d\.\)\s]+', '', ln).strip()
            if cleaned:
                noid_items.append((None, cleaned, ""))

    items.sort(key=lambda x: x[0])
    items.extend(noid_items)

    seen = set()
    titles = []
    for _, title, _ in items:
        if title not in seen:
            seen.add(title)
            titles.append(title)

    return titles

def parse_response_summary(data):
    start_index = data.find('[Summary]:')
    if start_index != -1:
        summary_content = data[start_index + len('[Summary]:'):].strip()
        return summary_content
    else:
        return "find failure!"