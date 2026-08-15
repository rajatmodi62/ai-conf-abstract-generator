
"""
Fetch accepted paper titles, authors, and abstracts from OpenReview for ICML.

Requires: pip install openreview-py --break-system-packages

OpenReview has two API versions. ICML 2024 onward uses API v2 (client2 / openreview.api).
Older venues (e.g. ICML 2023 and before, when they were on OpenReview at all) may need
the v1 client (openreview.Client). This script uses v2, which is what ICML 2026 will use.

Output format (same .txt file):
  1. A block listing just all accepted paper titles.
  2. A separator.
  3. A block with full details per paper: title, authors, abstract.
"""

import os
import openreview
import pyotp
import time


def get_client(username=None, password=None, totp_secret=None):
    if totp_secret:
        totp = pyotp.TOTP(totp_secret)
        otp_code = totp.now()
        client = openreview.api.OpenReviewClient(
            baseurl='https://api2.openreview.net',
            username=username,
            password=password,
        )
        try:
            client.login(username=username, password=password, otp=otp_code)
        except (AttributeError, TypeError):
            pass
        return client
    else:
        return openreview.api.OpenReviewClient(
            baseurl='https://api2.openreview.net',
            username=username,
            password=password,
        )


def fetch_accepted_papers(client, venue_id, txt_name):
    """
    venue_id examples:
      'ICML.cc/2026/Conference'
      'ICML.cc/2025/Conference'
      'ICML.cc/2024/Conference'
    """
    print(f"Fetching venue group: {venue_id}")
    venue_group = client.get_group(venue_id)

    submission_name = venue_group.content.get('submission_name', {}).get('value', 'Submission')
    submissions_invitation = f'{venue_id}/-/{submission_name}'
    print(f"Using submissions invitation: {submissions_invitation}")

    submissions = client.get_all_notes(
        invitation=submissions_invitation,
        details='replies'
    )
    print(f"Total submissions fetched: {len(submissions)}")

    accepted_papers = []

    for i, note in enumerate(submissions):
        content = note.content

        venueid = content.get('venueid', {}).get('value', '')

        is_accepted = (
            venueid == venue_id
            or venueid.startswith(venue_id + '/')
        ) and 'Submission' not in venueid.split('/')[-1]

        if not is_accepted:
            continue

        title = content.get('title', {}).get('value', '').strip()
        abstract = content.get('abstract', {}).get('value', '').strip()
        authors = content.get('authors', {}).get('value', [])
        authors_str = ', '.join(authors) if authors else ''

        accepted_papers.append({
            'title': title,
            'authors': authors_str,
            'abstract': abstract,
        })

        if (i + 1) % 200 == 0:
            print(f"Processed {i+1}/{len(submissions)} submissions...")

    print(f"Accepted papers found: {len(accepted_papers)}")

    with open(txt_name, 'w', encoding='utf-8') as f:
        # --- Section 1: titles only ---
        f.write("=== TITLES ONLY ===\n\n")
        for paper in accepted_papers:
            f.write(paper['title'] + '\n')

        # --- Section 2: full details ---
        f.write("\n\n=== FULL DETAILS (title / authors / abstract) ===\n\n")
        for paper in accepted_papers:
            f.write(paper['title'] + '\n')
            f.write(paper['authors'] + '\n')
            f.write(paper['abstract'] + '\n')
            f.write('*****************************\n')

    print(f"Saved to {txt_name}")
    return accepted_papers


if __name__ == '__main__':
    # Recommended: load credentials from environment variables instead of
    # hardcoding them here.
    #   export OPENREVIEW_USERNAME="you@example.com"
    #   export OPENREVIEW_PASSWORD="your_password"
    client = get_client(
        username='rajatmodi62@gmail.com',#os.environ.get('OPENREVIEW_USERNAME'),
        password='Bash@1995',
    )

    conf = [
        ('ICML.cc/2026/Conference', 'icml26.txt'),
        # ('ICML.cc/2025/Conference', 'icml25.txt'),
        # ('ICML.cc/2024/Conference', 'icml24.txt'),
    ]

    for venue_id, txt_name in conf:
        try:
            fetch_accepted_papers(client, venue_id, txt_name)
        except Exception as e:
            print(f"Failed for {venue_id}: {e}")
        time.sleep(1)
# """
# Fetch accepted paper titles, authors, and abstracts from OpenReview for ICML.

# Requires: pip install openreview-py --break-system-packages

# OpenReview has two API versions. ICML 2024 onward uses API v2 (client2 / openreview.api).
# Older venues (e.g. ICML 2023 and before, when they were on OpenReview at all) may need
# the v1 client (openreview.Client). This script uses v2, which is what ICML 2026 will use.
# """

# import openreview
# import pyotp
# import time


# def get_client(username=None, password=None, totp_secret=None):
#     if totp_secret:
#         totp = pyotp.TOTP(totp_secret)
#         otp_code = totp.now()
#         client = openreview.api.OpenReviewClient(
#             baseurl='https://api2.openreview.net',
#             username=username,
#             password=password,
#         )
#         try:
#             client.login(username=username, password=password, otp=otp_code)
#         except (AttributeError, TypeError):
#             pass
#         return client
#     else:
#         return openreview.api.OpenReviewClient(
#             baseurl='https://api2.openreview.net',
#             username=username,
#             password=password,
#         )


# def fetch_accepted_papers(client, venue_id, txt_name):
#     """
#     venue_id examples:
#       'ICML.cc/2026/Conference'
#       'ICML.cc/2025/Conference'
#       'ICML.cc/2024/Conference'

#     We first read the venue's group to find the "venueid" value that accepted
#     papers carry in their content (this varies slightly by year/venue setup),
#     then filter submissions accordingly.
#     """
#     print(f"Fetching venue group: {venue_id}")
#     venue_group = client.get_group(venue_id)

#     # The group's content usually stores the invitation ids for submissions
#     # and the accepted-venue-id value used to tag accepted papers.
#     submission_name = venue_group.content.get('submission_name', {}).get('value', 'Submission')

#     submissions_invitation = f'{venue_id}/-/{submission_name}'
#     print(f"Using submissions invitation: {submissions_invitation}")

#     # Pull all submissions (this includes rejected/withdrawn/desk-rejected too,
#     # so we filter below).
#     submissions = client.get_all_notes(
#         invitation=submissions_invitation,
#         details='replies'
#     )
#     print(f"Total submissions fetched: {len(submissions)}")

#     accepted_papers = []

#     for i, note in enumerate(submissions):
#         content = note.content

#         # The most reliable signal for "accepted" is the note's own venueid
#         # field once decisions are finalized: rejected/withdrawn papers get
#         # moved to a different venueid (e.g. ".../Rejected_Submission" or
#         # they simply keep the "Submission" venueid and never get accepted).
#         # Accepted papers typically get a venueid like:
#         #   "ICML.cc/2026/Conference" (main track accept)
#         # or with a note like "...Oral", "...Spotlight", "...Poster" appended,
#         # depending on how the venue configured decisions.
#         venueid = content.get('venueid', {}).get('value', '')

#         is_accepted = (
#             venueid == venue_id
#             or venueid.startswith(venue_id + '/')  # covers Oral/Spotlight/Poster suffixes
#         ) and 'Submission' not in venueid.split('/')[-1]  # excludes venueid still == plain submission track

#         if not is_accepted:
#             continue

#         title = content.get('title', {}).get('value', '').strip()
#         abstract = content.get('abstract', {}).get('value', '').strip()
#         authors = content.get('authors', {}).get('value', [])
#         authors_str = ', '.join(authors) if authors else ''

#         accepted_papers.append({
#             'title': title,
#             'authors': authors_str,
#             'abstract': abstract,
#         })

#         if (i + 1) % 200 == 0:
#             print(f"Processed {i+1}/{len(submissions)} submissions...")

#     print(f"Accepted papers found: {len(accepted_papers)}")

#     with open(txt_name, 'w', encoding='utf-8') as f:
#         for paper in accepted_papers:
#             f.write(paper['title'] + '\n')
#             f.write(paper['authors'] + '\n')
#             f.write(paper['abstract'] + '\n')
#             f.write('*****************************\n')

#     print(f"Saved to {txt_name}")
#     return accepted_papers


# if __name__ == '__main__':
#     # client = get_client(
#     #     username='your_email@example.com',
#     #     password='your_password',
#     #     totp_secret='YOUR_TOTP_SECRET_HERE',  # from your authenticator app setup
#     # )


#     client = get_client(
#         username='rajatmodi62@gmail.com',
#         password='Bash@1995',
#     )

#     conf = [
#         ('ICML.cc/2026/Conference', 'icml26.txt'),
#         # ('ICML.cc/2025/Conference', 'icml25.txt'),
#         # ('ICML.cc/2024/Conference', 'icml24.txt'),
#     ]

#     for venue_id, txt_name in conf:
#         try:
#             fetch_accepted_papers(client, venue_id, txt_name)
#         except Exception as e:
#             print(f"Failed for {venue_id}: {e}")
#         time.sleep(1)