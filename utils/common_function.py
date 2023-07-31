import re
import string

def slugify(s):
  s = s.lower().strip()
  s = re.sub(r'[^\w\s-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s


def clean_description(description, max_length=160):
    # Remove HTML tags
    clean_description = re.sub(r'<.*?>', '', description)

    # Remove special characters and punctuation
    clean_description = clean_description.translate(str.maketrans('', '', string.punctuation))

    # Convert to lowercase
    clean_description = clean_description.lower()

    # Remove excessive whitespace
    clean_description = re.sub(r'\s+', ' ', clean_description).strip()

    # Remove repetitive consecutive words
    clean_description = re.sub(r'\b(\w+)( \1\b)+', r'\1', clean_description)

    # Truncate to the maximum length
    clean_description = clean_description[:max_length]

    comma_separated_string = ', '.join(clean_description.split())

    return comma_separated_string
