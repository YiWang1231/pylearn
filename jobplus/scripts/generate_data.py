from jobplus.models import db, Company
import os
import json

def iter_company():
	with open(os.path.join(os.path.dirname(__file__),'data.json')) as f:
		companies = json.load(f)
		for company in companies:
			yield Company(
				name=company['name'],
				logo_url=company['images_url'],
				description=company['description'],
				Slogan=company['Slogan'],
				)


def run():
	for company in iter_company():
		db.session.add(company)

	try:
		db.session.commit()
	except Exception as e:
		print(e)
		db.session.rollback()