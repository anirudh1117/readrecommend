from django.shortcuts import reverse
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
    clean_description = clean_description.translate(
        str.maketrans('', '', string.punctuation))

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


def create_json_for_celebrity(celebrity, social_media):
    json = {
        "@type": "Person",
        "name": celebrity.name,
        # "slug": celebrity.name_slug,
        "description": celebrity.description,
        "jobTitle": ', '.join(profession.name for profession in celebrity.professions.all()),
        "image": "readrecommend.com" + celebrity.image.url if celebrity.image else "",
        "url": "readrecommend.com" + str(reverse('people-detail', args=[celebrity.name_slug])),
        "sameAs": social_media
    }

    return json


def create_json_for_author(celebrity, social_media):
    json = {
        "@type": "Person",
        "name": celebrity.name,
        # "slug": celebrity.name_slug,
        "description": celebrity.description,
        "jobTitle": ', '.join(profession.name for profession in celebrity.professions.all()),
        "image": "readrecommend.com" + celebrity.image.url,
        "url": "readrecommend.com" + str(reverse('author-detail', args=[celebrity.name_slug])),
        "sameAs": social_media
    }

    return json


def create_json_for_book_author(author):
    json = {
        "@type": "Person",
        "name": author.name,
        # "slug": author.name_slug,
        "description": author.description,
        "jobTitle": ', '.join(profession.name for profession in author.professions.all()),
        "image": "readrecommend.com" + (author.image.url if author.image else ""),
        "url": "readrecommend.com" + str(reverse('author-detail', args=[author.name_slug])),
    }

    return json


def create_json_for_book(book):
    json = {
        "@type": "Book",
        "name": book.name,
        # "slug": book.name_slug,
        "@id": "readrecommend.com" + str(reverse('book-detail', args=[book.name_slug])),
        "url": str(reverse('book-detail', args=[book.name_slug])),
        "description": book.description,
        "about": ', '.join(category.name for category in book.categories.all()),
        "image": "readrecommend.com" + ''.join(bookimage.image.url for bookimage in book.bookimages_set.all()),
        "url": "readrecommend.com" + str(reverse('book-detail', args=[book.name_slug])),
        #"amazon": book.amazonlink,
        "author": create_json_for_book_author(book.author_name),
        "datePublished": book.dateOfPublish
    }

    return json


def create_json_for_list_books(books):
    books_list = []
    for book in books:
        books_list.append(create_json_for_book(book))
    json = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "hasPart": books_list,
    }

    return json


def create_json_for_list_celebrity(peoples):
    people_list = []
    for people, platform in peoples:
        people_list.append(create_json_for_celebrity(people, platform))

    json = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "@graph": people_list,
    }
    return json


def create_json_for_list_author(peoples):
    people_list = []
    for people, platform in peoples:
        people_list.append(create_json_for_author(people, platform))

    json = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "@graph": people_list,
    }

    return json

def create_json_for_list_book(books):
    book_list = []
    for book in books:
        book_list.append(create_json_for_book(book))

    json = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "@graph": book_list,
    }

    return json


def create_json_for_celebrity_Detail(people, platform, books):
    json_celebrity = create_json_for_celebrity(people, platform)
    json_celebrity["context"] = "https://schema.org/"
    book_list = []
    for book in books:
        book_list.append(create_json_for_book(book))
    json_books = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "hasPart": book_list
    }
    json = {
        "books": json_books,
        "celebrity": json_celebrity
    }

    return json

def create_json_for_author_Detail(people, platform, books):
    json_celebrity = create_json_for_author(people, platform)
    json_celebrity["context"] = "https://schema.org/"
    book_list = []
    for book in books:
        book_list.append(create_json_for_book(book))
    json_books = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "hasPart": book_list
    }
    json = {
        "books": json_books,
        "celebrity": json_celebrity
    }

    return json

def create_json_for_book_Detail(book, peoples):
    json_book = create_json_for_book(book)
    people_list = create_json_for_list_celebrity(peoples)
    json = {
        "book": json_book,
        "celebrity": people_list
    }

    return json


def create_json_for_readrecommed():
    json = {
        "@context": "http://schema.org",
        "@type": "Organization",
        "name": "readrecommend",
        "url": "https://www.readrecommend.com/",
        "logo": "https://www.readrecommend.com/static/img/read-recommend-logo-2.png",
        "description": "Unlock Literary Treasures: Celebrity-Backed Reads and Renowned Authors Await. Experience the magic of literature through the eyes of your favorite celebrities.",
        "sameAs": [
            "https://www.instagram.com/readrecommend_book/?igshid=MzRlODBiNWFlZA%3D%3D"
        ]
    }

    return json
