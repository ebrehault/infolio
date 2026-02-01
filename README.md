# In-folio

In-folio ("made of pages" in latin) is a fediverse web publication platform.

Mastodon offers a microblogging service, while In-folio aims to provide a genuine web publication service, allowing the fediverse users to create full web pages.

## Main features

- Login with a Mastodon account
- Create web pages, including images or other file assets
- A page can be in draft or published
- A page can have nested pages
- A page is tooted on Mastodon when published

Management tasks:

- The user can export all their pages
- The user can reassign the ownership of their account in case the user moves from one Mastodon instance to another
- The admin can ban a user

## Architecture

The backend provides:

- a REST API offering a CRUD service for pages
- the Mastodon auth flow
- the display of the pages to the visitors

The frontend offers a simple, efficient and accessible web editing experience.
