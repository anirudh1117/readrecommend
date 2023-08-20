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
        "image": "readrecommend.com" + celebrity.image.url if celebrity.image else "/static/img/read-recommend-logo-2.png",
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
        "image": "readrecommend.com" + celebrity.image.url if celebrity.image else "/static/img/read-recommend-logo-2.png",
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
        "image": "readrecommend.com" + (author.image.url if author.image else "/static/img/read-recommend-logo-2.png"),
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
        # "amazon": book.amazonlink,
        "author": create_json_for_book_author(book.author_name),
        "datePublished": book.dateOfPublish
    }

    return json


def create_json_for_category(category, index):
    json = {
        "@type": "ListItem",
        "position": index + 1,
        "name": category.get('name'),
        "item": {
            "@id": "readrecommend.com" + str(reverse('books')) + "?categories=" + category.get('name_slug'),
            "url": "readrecommend.com" + str(reverse('books')) + "?categories=" + category.get('name_slug'),
            "name": category.get('name'),
            "image": "https://www.readrecommend.com/static/img/read-recommend-logo-2.png"
        }
    }
    return json


def create_breadcumb_for_celebrity(people, index, url):
    json = {
        "@type": "ListItem",
        "position": index + 1,
        "name": people.name,
        "item": {
            "@id": "readrecommend.com" + str(reverse(url + '-detail', args=[people.name_slug])),
            "url": "readrecommend.com" + str(reverse(url + '-detail', args=[people.name_slug])),
            "name": people.name,
            "image": "https://www.readrecommend.com" + people.image.url if people.image else '/static/img/read-recommend-logo-2.png'
        }
    }
    return json

def create_breadcumb_for_book(book, index):
    json = {
        "@type": "ListItem",
        "position": index + 1,
        "name": book.name,
        "item": {
            "@id": "readrecommend.com" + str(reverse('book-detail', args=[book.name_slug])),
            "url": "readrecommend.com" + str(reverse('book-detail', args=[book.name_slug])),
            "name": book.name,
            "image": "readrecommend.com" + ''.join(bookimage.image.url for bookimage in book.bookimages_set.all()),
        }
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
    breadcumb_list = []
    i = 0
    for people, platform in peoples:
        people_list.append(create_json_for_celebrity(people, platform))
        breadcumb_list.append(
            create_breadcumb_for_celebrity(people, i, 'people'))
        i = i + 1

    website_json = create_json_for_readrecommed()

    json_breadcumb = {
        "@type": "BreadcrumbList",
        "name": "People",
        "url": "readrecommend.com" + str(reverse('people')),
        "itemListElement": breadcumb_list
    }

    json = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "url": "readrecommend.com" + str(reverse('people')),
        "breadcrumb": "Home > People",
        "@graph": [people_list, website_json, json_breadcumb],
        "name":  "Renowned Personalities and Their Recommended Reads: A Curated List",
        "description": "Explore a curated compilation of celebrated individuals and their literary recommendations on our platform. Discover a treasure trove of insightful books endorsed by notable personalities across various domains. ",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "readrecommend.com" + str(reverse('people')) + "?keyword={search_term}",
            "query-input": "name=search_term"
        }
    }
    return json


def create_json_for_list_author(peoples):
    people_list = []
    breadcumb_list = []
    i = 0
    for people, platform in peoples:
        people_list.append(create_json_for_author(people, platform))
        breadcumb_list.append(
            create_breadcumb_for_celebrity(people, i, 'author'))
        i = i + 1

    website_json = create_json_for_readrecommed()
    json_breadcumb = {
        "@type": "BreadcrumbList",
        "name": "Author",
        "url": "readrecommend.com" + str(reverse('author')),
        "itemListElement": breadcumb_list
    }

    json = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "url": "readrecommend.com" + str(reverse('author')),
        "breadcrumb": "Home > Author",
        "@graph": [people_list, website_json, json_breadcumb],
        "name":  "Discover Amazing Authors: A Curated List",
        "description": "Explore a curated list of authors and their contributions in various fields.",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "readrecommend.com" + str(reverse('author')) + "?keyword={search_term}",
            "query-input": "name=search_term"
        }
    }

    return json


def create_json_for_list_book(books):
    book_list = []
    breadcumb_list = []
    i = 0
    for book in books:
        book_list.append(create_json_for_book(book))
        breadcumb_list.append(create_breadcumb_for_book(book, i))
        i = i + 1

    website_json = create_json_for_readrecommed()
    json_breadcumb = {
        "@type": "BreadcrumbList",
        "name": "Books",
        "url": "readrecommend.com" + str(reverse('books')),
        "itemListElement": breadcumb_list
    }

    json = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "url": "readrecommend.com" + str(reverse('books')),
        "breadcrumb": "Home > Books",
        "@graph": [book_list, website_json, json_breadcumb],
        "name":  "Discover Your Next Read: A Curated List",
        "description": "Explore a diverse collection of books from various genres and authors. Discover new stories and expand your reading list.",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "readrecommend.com" + str(reverse('books')) + "?keyword={search_term}",
            "query-input": "name=search_term"
        }
    }

    return json


def create_json_for_celebrity_Detail(people, platform, books):
    json_celebrity = create_json_for_celebrity(people, platform)
    website_json = create_json_for_readrecommed()
    book_list = []
    for book in books:
        book_list.append(create_json_for_book(book))
    json_books = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "breadcrumb": "Home > People > " + people.name,
        "url": "readrecommend.com" + str(reverse('people-detail', args=[people.name_slug])),
        "@graph": [book_list, json_celebrity, website_json],
        "name":  people.name + "'s Must-Reads: Books Recommended by " + people.name,
        "description": "Delve into a curated selection of " + people.name_slug + "-recommended books that span across diverse fields and subjects. y immersing yourself in these pages, you're tapping into the wisdom and expertise that have resonated deeply with the experts themselves. Embark on a journey of enlightenment, exploration, and empowerment as you absorb the lessons, perspectives, and discoveries that have stood the test of rigorous scrutiny."
    }

    return json_books


def create_json_for_author_Detail(people, platform, books):
    json_celebrity = create_json_for_author(people, platform)
    website_json = create_json_for_readrecommed()
    book_list = []
    for book in books:
        book_list.append(create_json_for_book(book))
    json_books = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "breadcrumb": "Home > Author > " + people.name,
        "url": "readrecommend.com" + str(reverse('author-detail', args=[people.name_slug])),
        "@graph": [book_list, json_celebrity, website_json],
        "name":  "Mastery Unveiled: Books Authored by " + people.name,
        "description": "Step into the world of unparalleled expertise with this captivating collection of books authored by " + people.name + ". Gain a deep understanding of the intricacies of their fields and cultivate your own journey towards mastery through the guidance of the " + people.name
    }

    return json_books


def create_json_for_book_Detail(book, peoples):
    json_book = create_json_for_book(book)
    people_list = create_json_for_list_celebrity(peoples)
    website_json = create_json_for_readrecommed()

    json = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "breadcrumb": "Home > Books > " + book.name,
        "url": "readrecommend.com" + str(reverse('book-detail', args=[book.name_slug])),
        "@graph": [json_book, people_list, website_json],
        "name":  "Mastery Unveiled: Embark on a Journey with Reading " + book.name,
        "description": "Dive into a world of imagination, knowledge, and inspiration with the enchanting selection of  " + book.name + ". With each turn of the page, you're invited to discover the countless treasures woven into the fabric of literature. Embrace the joy of reading, embrace the world of possibilities that these pages hold, and let your imagination soar to new heights."
    }

    return json


def create_json_for_categories(categories):
    website_json = create_json_for_readrecommed()
    breadcumb_list = []
    for i in range(0, len(categories)):
        print(categories[i])
        breadcumb_list.append(create_json_for_category(categories[i], i))
    json_breadcumb = {
        "@type": "BreadcrumbList",
        "name": "Categories",
        "url": "readrecommend.com" + str(reverse('categories')),
        "itemListElement": breadcumb_list
    }

    json = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "breadcrumb": "Home > Categories",
        "url": "readrecommend.com" + str(reverse('categories')),
        "@graph": [json_breadcumb, website_json],
        "name":  "Literary Universe Unveiled: A Kaleidoscope of Book Categories",
        "description": "Whether you're a fervent fiction enthusiast, a devoted non-fiction reader, or an eclectic explorer of literary landscapes, these categories are your compass to navigate the boundless expanse of literature. Embark on a voyage of discovery, as you delve into worlds both familiar and uncharted, guided by the threads of human creativity and storytelling brilliance."
    }

    return json


def create_json_for_readrecommed():
    json = {
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


def get_breadcum_json():
    json = {
        "@type": "BreadcrumbList",
        "itemListElement": [{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": {
                "@id": "readrecommend.com" + str(reverse('home')),
                "name": "Home",
                "image": "https://www.readrecommend.com/static/img/read-recommend-logo-2.png"
            }
        }, {
            "@type": "ListItem",
            "position": 2,
            "name": "People",
            "item": {
                "@id": "readrecommend.com" + str(reverse('people')),
                "name": "People",
                "image": "https://www.readrecommend.com/static/img/read-recommend-logo-2.png"
            }
        }, {
            "@type": "ListItem",
            "position": 3,
            "name": "Author",
            "item": {
                "@id": "readrecommend.com" + str(reverse('author')),
                "name": "Author",
                "image": "https://www.readrecommend.com/static/img/read-recommend-logo-2.png"
            }
        }, {
            "@type": "ListItem",
            "position": 3,
            "name": "Books",
            "item": {
                "@id": "readrecommend.com" + str(reverse('books')),
                "name": "Books",
                "image": "https://www.readrecommend.com/static/img/read-recommend-logo-2.png"
            }
        }, {
            "@type": "ListItem",
            "position": 3,
            "name": "Categories",
            "item": {
                "@id": "readrecommend.com" + str(reverse('categories')),
                "name": "Categories",
                "image": "https://www.readrecommend.com/static/img/read-recommend-logo-2.png"
            }
        }]
    }
    return json


def get_json_for_home():
    website_json = create_json_for_readrecommed()
    breadcumb_json = get_breadcum_json()
    json = {
        "@context": "https://schema.org/",
        "@type": "WebPage",
        "breadcrumb": "Home",
        "url": "readrecommend.com" + str(reverse('home')),
        "@graph": [website_json, breadcumb_json],
        "name":  "Read Recommend (Literary Nexus): Where Books, Authors, and Influencers Converge",
        "description": "Discover a digital haven where the worlds of literature, authorship, and celebrity influence intersect in harmonious synergy. Read Recommend is your gateway to a meticulously curated compilation of books spanning diverse genres, an illustrious assembly of renowned authors, and a revered roster of celebrity influencers who have bestowed their endorsements upon these literary gems.",
         "potentialAction": {
            "@type": "SearchAction",
            "target": "readrecommend.com/search/" + "{search_term}",
            "query-input": "name=search_term"
        }
    }
    return json


def get_category(str1):
    str2 = "best-books"
    category = ''

    str1_length = len(str1)
    str2_length = len(str2)
    j = 0
    i = 0

    while i < str1_length and j < str2_length:
        if str1[i] != str2[j]:
            category = category + str1[i]
        else:
            j = j + 1
        i = i + 1

    return category[:-1]


def get_categories_list(categories):
    categories = categories.split(',')
    category_list = []
    for category in categories:
        category_list.append(get_category(category))
    return category_list
